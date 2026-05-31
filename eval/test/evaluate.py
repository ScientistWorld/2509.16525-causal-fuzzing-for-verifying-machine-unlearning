"""Held-out test-slice scoring for feature-unlearning artifacts.

This evaluator reads the same method-output contract as the train slice, but
scores a stricter mediated-effect consistency view. It does not import method
code or regenerate experiments.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable


DATASETS = ("heart_disease", "performance")
SUBGROUP_EXPERIMENT = "heart_disease_subgroup_unlearning"
GRAPH_ROBUSTNESS_EXPERIMENT = "graph_misspecification_robustness"
MAX_QUERY_RATIO = 10.0


def _load_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Missing artifact: {path}")
    return json.loads(path.read_text())


def _rank_score(rank: int, n_features: int) -> float:
    if n_features <= 1:
        return 1.0
    return float((n_features - rank) / (n_features - 1))


def _query_ratio_score(fuzzing_queries: float, cafe_queries: float) -> float:
    if fuzzing_queries <= 0 or cafe_queries <= 0:
        return 0.0
    return min(fuzzing_queries / cafe_queries, MAX_QUERY_RATIO)


def _artifact_files(outputs_dir: Path) -> Iterable[Path]:
    for path in sorted(outputs_dir.glob("*.json")):
        if path.name != "summary.json":
            yield path
    for child in sorted(outputs_dir.iterdir() if outputs_dir.exists() else []):
        if not child.is_dir():
            continue
        for path in sorted(child.glob("*.json")):
            if path.name != "summary.json":
                yield path


def _dataset_from_artifact(path: Path, artifact: dict) -> str | None:
    dataset = artifact.get("dataset")
    if dataset in DATASETS:
        return str(dataset)
    for candidate in DATASETS:
        if path.name.startswith(f"{candidate}_"):
            return candidate
    return None


def _method_from_artifact(path: Path, dataset: str, artifact: dict) -> str:
    method = artifact.get("method")
    if method:
        return str(method)
    prefix = f"{dataset}_"
    stem = path.stem
    if stem.startswith(prefix):
        return stem[len(prefix) :]
    return path.parent.name


def _discover_artifacts(outputs_dir: Path) -> dict[str, dict[str, dict]]:
    by_dataset: dict[str, dict[str, dict]] = {dataset: {} for dataset in DATASETS}
    for path in _artifact_files(outputs_dir):
        artifact = _load_json(path)
        dataset = _dataset_from_artifact(path, artifact)
        if dataset is None:
            continue
        method = _method_from_artifact(path, dataset, artifact)
        if method in by_dataset[dataset]:
            previous = by_dataset[dataset][method]["_path"]
            raise ValueError(
                f"Duplicate artifact for dataset={dataset!r}, method={method!r}: "
                f"{previous} and {path}"
            )
        artifact["_path"] = str(path)
        by_dataset[dataset][method] = artifact
    return by_dataset


def _train_methods(train_scores: Path) -> dict[str, set[str]] | None:
    if not train_scores.exists():
        return None
    payload = _load_json(train_scores)
    methods_by_experiment: dict[str, set[str]] = {}
    for experiment, body in payload.get("experiments", {}).items():
        methods_by_experiment[experiment] = set(body.get("results", {}).keys())
    return methods_by_experiment


def _fallback_rank(artifact: dict) -> int:
    if "target_total_rank" in artifact:
        return int(artifact["target_total_rank"])
    target = artifact["target_feature"]
    if "ranking" in artifact:
        return list(artifact["ranking"]).index(target) + 1
    return len(artifact["features"])


def _feature_scores(artifact: dict) -> dict[str, float]:
    features = list(artifact["features"])
    n_features = len(features)
    target = artifact["target_feature"]

    if "effects" not in artifact:
        rank = n_features if target in features else _fallback_rank(artifact)
        target_effect = float(artifact.get("target_total_effect", 0.0))
        return {
            "target_rank": float(rank),
            "rank_score": _rank_score(rank, n_features),
            "indirect_detected": 0.0,
            "direct_unlearned": 1.0 if target_effect <= 1e-8 else 0.0,
            "fuzzing_agreement": 0.0,
            "query_ratio_vs_fuzzing": 0.0,
        }

    effects = artifact["effects"]

    def mediated_score(feature: str) -> float:
        effect = effects[feature]
        indirect = float(effect["indirect_effect"])
        direct = abs(float(effect["direct_effect"]))
        return indirect - direct

    ranking = sorted(features, key=mediated_score, reverse=True)
    rank = ranking.index(target) + 1
    total_ranking = sorted(
        features,
        key=lambda feature: float(effects[feature]["total_effect"]),
        reverse=True,
    )
    total_rank = total_ranking.index(target) + 1
    target_effects = effects[target]
    total = float(target_effects["total_effect"])
    direct = abs(float(target_effects["direct_effect"]))
    indirect = float(target_effects["indirect_effect"])
    scale = max(abs(total), 1e-12)
    indirect_fraction = indirect / scale
    direct_fraction = direct / scale

    fuzzing = artifact.get("causal_fuzzing", {})
    fuzz_total = float(fuzzing.get("total_effect", 0.0))
    relative_error = abs(total - fuzz_total) / max(abs(fuzz_total), 1e-12)
    has_fuzzing = "total_effect" in fuzzing

    cafe_queries = float(artifact.get("cafe_model_query_count", 0.0))
    fuzzing_queries = float(artifact.get("fuzzing_model_query_count", 0.0))

    return {
        "target_rank": float(rank),
        "rank_score": 0.75 * _rank_score(total_rank, n_features)
        + 0.25 * _rank_score(rank, n_features),
        "indirect_detected": 1.0
        if mediated_score(target) > 0.05 and indirect_fraction >= 0.55
        else 0.0,
        "direct_unlearned": 1.0 if direct_fraction <= 0.12 else 0.0,
        "fuzzing_agreement": 1.0 if has_fuzzing and relative_error <= 0.75 and indirect > 0 else 0.0,
        "query_ratio_vs_fuzzing": _query_ratio_score(fuzzing_queries, cafe_queries),
    }


def _subgroup_scores(artifact: dict) -> dict[str, float] | None:
    subgroup = artifact.get("subgroup_unlearning")
    if not subgroup:
        return None

    direct_gap = float(subgroup.get("direct_gap_abs", 0.0))
    if "age_gt_50" not in subgroup or "age_le_50" not in subgroup:
        return {
            "direct_gap_abs": direct_gap,
            "direct_gap_small": 1.0 if direct_gap <= 0.15 else 0.0,
            "indirect_gap": 0.0,
            "indirect_gap_detected": 0.0,
            "subgroup_residual_score": 0.0,
            "total_gap": 0.0,
            "total_gap_detected": 0.0,
        }

    gt = subgroup["age_gt_50"]
    le = subgroup["age_le_50"]
    direct_scale = max(
        (abs(float(gt["direct_effect"])) + abs(float(le["direct_effect"]))) / 2.0,
        1e-12,
    )
    indirect_gap = float(subgroup.get("indirect_gap", 0.0))
    total_gap = float(subgroup.get("total_gap", 0.0))
    positive_indirect_gap = max(indirect_gap, 0.0)
    residual_score = positive_indirect_gap / max(
        positive_indirect_gap + 2.0 * direct_gap,
        1e-12,
    )

    return {
        "direct_gap_abs": direct_gap,
        "direct_gap_small": 1.0 if direct_gap / direct_scale <= 0.20 else 0.0,
        "indirect_gap": indirect_gap,
        "indirect_gap_detected": 1.0 if indirect_gap > max(0.05, direct_gap) else 0.0,
        "subgroup_residual_score": residual_score,
        "total_gap": total_gap,
        "total_gap_detected": 1.0 if total_gap > max(0.05, direct_gap) else 0.0,
    }


def _graph_robustness_scores(artifacts: dict[str, dict[str, dict]]) -> dict[str, float] | None:
    changes: list[dict[str, float]] = []
    for dataset in DATASETS:
        artifact = artifacts.get(dataset, {}).get("cafe")
        if not artifact or "graph_robustness" not in artifact:
            continue
        robust = artifact["graph_robustness"]
        changes.append(
            {
                "add_50pct_rank_change_pct": float(
                    robust["add_50pct_edges"]["rank_change_pct"]
                ),
                "remove_25pct_rank_change_pct": float(
                    robust["remove_25pct_edges"]["rank_change_pct"]
                ),
                "remove_50pct_rank_change_pct": float(
                    robust["remove_50pct_edges"]["rank_change_pct"]
                ),
                "fully_connected_rank_change_pct": float(
                    robust["fully_connected_dag"]["rank_change_pct"]
                ),
            }
        )
    if not changes:
        return None

    average = {
        key: sum(row[key] for row in changes) / len(changes)
        for key in changes[0]
    }
    moderate_change = (
        average["add_50pct_rank_change_pct"]
        + average["remove_25pct_rank_change_pct"]
    ) / 2.0
    extreme_change = max(
        average["remove_50pct_rank_change_pct"],
        average["fully_connected_rank_change_pct"],
    )
    average["moderate_robustness_score"] = max(0.0, 1.0 - moderate_change / 20.0)
    average["extreme_shift_present"] = 1.0 if extreme_change > moderate_change else 0.0
    return average


def _methods_for_experiment(
    experiment: str, discovered: dict[str, dict[str, dict]], train_methods: dict[str, set[str]] | None
) -> list[str]:
    dataset = experiment.removesuffix("_feature_unlearning")
    available = set(discovered.get(dataset, {}).keys())
    if experiment == SUBGROUP_EXPERIMENT:
        available = set(discovered.get("heart_disease", {}).keys())
    if experiment == GRAPH_ROBUSTNESS_EXPERIMENT:
        available = {"cafe"} if _graph_robustness_scores(discovered) is not None else set()
    if train_methods is None:
        return sorted(available)
    requested = train_methods.get(experiment, set())
    missing = requested - available
    if missing:
        raise FileNotFoundError(
            f"Test slice is missing artifacts for methods scored on train "
            f"for {experiment}: {sorted(missing)}"
        )
    return sorted(requested)


def evaluate(outputs_dir: Path, train_scores: Path | None = None) -> dict:
    artifacts = _discover_artifacts(outputs_dir)
    train_method_sets = _train_methods(train_scores) if train_scores is not None else None
    scores = {"_slice": "test", "experiments": {}}

    for dataset in DATASETS:
        experiment = f"{dataset}_feature_unlearning"
        scores["experiments"][experiment] = {"results": {}}
        for method in _methods_for_experiment(experiment, artifacts, train_method_sets):
            scores["experiments"][experiment]["results"][method] = _feature_scores(
                artifacts[dataset][method]
            )

    scores["experiments"][SUBGROUP_EXPERIMENT] = {"results": {}}
    for method in _methods_for_experiment(SUBGROUP_EXPERIMENT, artifacts, train_method_sets):
        subgroup = _subgroup_scores(artifacts["heart_disease"][method])
        if subgroup is None and train_method_sets is not None:
            raise FileNotFoundError(
                f"Test slice is missing subgroup artifact fields for train-scored "
                f"method {method!r}"
            )
        if subgroup is not None:
            scores["experiments"][SUBGROUP_EXPERIMENT]["results"][method] = subgroup

    graph_scores = _graph_robustness_scores(artifacts)
    if graph_scores is not None:
        scores["experiments"][GRAPH_ROBUSTNESS_EXPERIMENT] = {
            "results": {"cafe": graph_scores}
        }

    return scores


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outputs-dir", default="outputs")
    parser.add_argument("--scores", default="scoring/scores_test.json")
    parser.add_argument("--train-scores", default="scoring/scores_train.json")
    args = parser.parse_args()

    scores = evaluate(Path(args.outputs_dir), Path(args.train_scores))
    score_path = Path(args.scores)
    score_path.parent.mkdir(parents=True, exist_ok=True)
    score_path.write_text(json.dumps(scores, indent=2, sort_keys=True))
    print(json.dumps(scores, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
