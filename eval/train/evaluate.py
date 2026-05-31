"""Visible train-slice scoring for feature-unlearning artifacts.

This evaluator reads method outputs only. It does not import method code or
regenerate experiments.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable


DATASETS = ("heart_disease", "performance")
SUBGROUP_EXPERIMENT = "heart_disease_subgroup_unlearning"
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


def _total_rank(artifact: dict) -> int:
    if "target_total_rank" in artifact:
        return int(artifact["target_total_rank"])
    target = artifact["target_feature"]
    if "ranking" in artifact:
        return list(artifact["ranking"]).index(target) + 1
    effects = artifact["effects"]
    ranking = sorted(
        artifact["features"],
        key=lambda feature: float(effects[feature]["total_effect"]),
        reverse=True,
    )
    return ranking.index(target) + 1


def _feature_scores(artifact: dict) -> dict[str, float]:
    features = list(artifact["features"])
    n_features = len(features)
    target = artifact["target_feature"]

    if "effects" not in artifact:
        rank = _total_rank(artifact)
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
    ranking = sorted(
        features,
        key=lambda feature: float(effects[feature]["total_effect"]),
        reverse=True,
    )
    rank = ranking.index(target) + 1
    target_effects = effects[target]
    total = float(target_effects["total_effect"])
    direct = float(target_effects["direct_effect"])
    indirect = float(target_effects["indirect_effect"])
    scale = max(abs(total), 1e-12)
    indirect_fraction = indirect / scale

    fuzzing = artifact.get("causal_fuzzing", {})
    fuzz_total = float(fuzzing.get("total_effect", 0.0))
    relative_error = abs(total - fuzz_total) / max(abs(fuzz_total), 1e-12)
    has_fuzzing = "total_effect" in fuzzing

    cafe_queries = float(artifact.get("cafe_model_query_count", 0.0))
    fuzzing_queries = float(artifact.get("fuzzing_model_query_count", 0.0))

    return {
        "target_rank": float(rank),
        "rank_score": _rank_score(rank, n_features),
        "indirect_detected": 1.0 if indirect_fraction >= 0.50 and indirect > 0.05 else 0.0,
        "direct_unlearned": 1.0 if abs(direct) <= 0.15 * scale else 0.0,
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
        positive_indirect_gap + direct_gap,
        1e-12,
    )

    return {
        "direct_gap_abs": direct_gap,
        "direct_gap_small": 1.0 if direct_gap / direct_scale <= 0.20 else 0.0,
        "indirect_gap": indirect_gap,
        "indirect_gap_detected": 1.0 if indirect_gap > 0.05 else 0.0,
        "subgroup_residual_score": residual_score,
        "total_gap": total_gap,
        "total_gap_detected": 1.0 if total_gap > 0.05 else 0.0,
    }


def evaluate(outputs_dir: Path) -> dict:
    artifacts = _discover_artifacts(outputs_dir)
    scores = {"_slice": "train", "experiments": {}}

    for dataset in DATASETS:
        experiment = f"{dataset}_feature_unlearning"
        scores["experiments"][experiment] = {"results": {}}
        for method, artifact in sorted(artifacts[dataset].items()):
            scores["experiments"][experiment]["results"][method] = _feature_scores(artifact)

    scores["experiments"][SUBGROUP_EXPERIMENT] = {"results": {}}
    for method, artifact in sorted(artifacts["heart_disease"].items()):
        subgroup = _subgroup_scores(artifact)
        if subgroup is not None:
            scores["experiments"][SUBGROUP_EXPERIMENT]["results"][method] = subgroup

    return scores


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outputs-dir", default="outputs")
    parser.add_argument("--scores", default="scoring/scores_train.json")
    args = parser.parse_args()

    scores = evaluate(Path(args.outputs_dir))
    score_path = Path(args.scores)
    score_path.parent.mkdir(parents=True, exist_ok=True)
    score_path.write_text(json.dumps(scores, indent=2, sort_keys=True))
    print(json.dumps(scores, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
