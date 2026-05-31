"""CAFÉ causal influence estimator for black-box model predictions."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict, deque
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

from data.synthetic_causal import load_dataset


def _parents(edges: list[tuple[str, str]], node: str) -> list[str]:
    return [src for src, dst in edges if dst == node]


def _descendants(edges: list[tuple[str, str]], node: str) -> set[str]:
    children: dict[str, list[str]] = defaultdict(list)
    for src, dst in edges:
        children[src].append(dst)
    seen: set[str] = set()
    queue: deque[str] = deque(children[node])
    while queue:
        cur = queue.popleft()
        if cur in seen:
            continue
        seen.add(cur)
        queue.extend(children[cur])
    return seen


def _topological_order(nodes: list[str], edges: list[tuple[str, str]]) -> list[str]:
    indegree = {node: 0 for node in nodes}
    children: dict[str, list[str]] = defaultdict(list)
    for src, dst in edges:
        if src in indegree and dst in indegree:
            children[src].append(dst)
            indegree[dst] += 1
    queue = deque([node for node in nodes if indegree[node] == 0])
    order: list[str] = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for child in children[node]:
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    if len(order) != len(nodes):
        raise ValueError("Causal graph must be acyclic")
    return order


def _fit_structural_models(
    frame: pd.DataFrame, features: list[str], edges: list[tuple[str, str]]
) -> dict[str, object]:
    models: dict[str, object] = {}
    for feature in features:
        parents = [p for p in _parents(edges, feature) if p in features]
        if not parents:
            continue
        model = RandomForestRegressor(
            n_estimators=80,
            min_samples_leaf=10,
            random_state=19,
            n_jobs=1,
        )
        model.fit(frame[parents], frame[feature])
        models[feature] = model
    return models


def causal_fuzzing_effect(
    frame: pd.DataFrame,
    model: object,
    model_features: list[str],
    features: list[str],
    edges: list[tuple[str, str]],
    target_feature: str,
    seed: int,
    n_samples: int | None = None,
) -> dict[str, float | int]:
    """Algorithm 1-style intervention propagation with learned H_v models.

    The audited model is still treated as a black box: the oracle only calls
    predict on original and causally propagated counterfactual rows.
    """

    rng = np.random.default_rng(seed)
    sample_size = len(frame) if n_samples is None else min(n_samples, len(frame))
    sample = frame.sample(n=sample_size, random_state=seed).copy()
    structural_models = _fit_structural_models(frame, features, edges)
    descendants = _descendants(edges, target_feature)
    topo = _topological_order(features, edges)
    source_values = frame[target_feature].to_numpy()

    original_pred = model.predict(sample[model_features])
    direct_rows = sample.copy()
    total_rows = sample.copy()
    intervention_values = rng.choice(source_values, size=len(sample), replace=True)
    direct_rows[target_feature] = intervention_values
    total_rows[target_feature] = intervention_values

    changed = {target_feature}
    for node in topo:
        if node == target_feature or node not in descendants or node not in structural_models:
            continue
        parents = [p for p in _parents(edges, node) if p in features]
        if changed.intersection(parents):
            total_rows[node] = structural_models[node].predict(total_rows[parents])
            changed.add(node)

    direct_pred = model.predict(direct_rows[model_features])
    total_pred = model.predict(total_rows[model_features])
    direct = float(np.mean(np.abs(direct_pred - original_pred)))
    total = float(np.mean(np.abs(total_pred - original_pred)))
    return {
        "total_effect": total,
        "direct_effect": direct,
        "indirect_effect": max(total - direct, 0.0),
        "model_query_count": int(3 * len(sample)),
        "structural_model_count": len(structural_models),
        "sample_count": int(len(sample)),
    }


def _intervention_values(values: pd.Series) -> tuple[float, float]:
    """Choose the two treatment values used in Definition 4 contrasts."""

    unique = np.sort(values.dropna().unique())
    if len(unique) <= 1:
        only = float(unique[0]) if len(unique) == 1 else 0.0
        return only, only
    if len(unique) == 2 and set(np.round(unique, 8)).issubset({0.0, 1.0}):
        return float(unique[0]), float(unique[-1])
    return float(values.quantile(0.25)), float(values.quantile(0.75))


def _conditional_prediction_contrast(
    frame: pd.DataFrame,
    prediction_col: str,
    feature: str,
    controls: list[str],
    seed: int,
) -> dict[str, float | int | list[str]]:
    """Finite-sample CAFÉ effect from adjusted expected prediction contrasts.

    The paper's CAFÉ score compares black-box predictions under two values of a
    target feature while adjusting for a valid backdoor set. For direct effects,
    the adjustment set is augmented with mediators. We estimate the conditional
    expectation E[M'(X) | feature, controls] with a lightweight regression model,
    then average the prediction contrast over the empirical control distribution.
    """

    controls = [c for c in controls if c != feature]
    theta_low, theta_high = _intervention_values(frame[feature])
    if abs(theta_high - theta_low) < 1e-12 or frame[prediction_col].std() < 1e-12:
        return {
            "effect": 0.0,
            "theta_low": theta_low,
            "theta_high": theta_high,
            "controls": controls,
            "response_model_rows": int(len(frame)),
        }

    columns = [feature] + controls
    response_model = RandomForestRegressor(
        n_estimators=80,
        min_samples_leaf=12,
        random_state=seed,
        n_jobs=1,
    )
    response_model.fit(frame[columns], frame[prediction_col])

    low_rows = frame[columns].copy()
    high_rows = frame[columns].copy()
    low_rows[feature] = theta_low
    high_rows[feature] = theta_high
    low_mu = response_model.predict(low_rows)
    high_mu = response_model.predict(high_rows)
    effect = float(np.mean(np.abs(high_mu - low_mu)))
    return {
        "effect": effect,
        "theta_low": theta_low,
        "theta_high": theta_high,
        "controls": controls,
        "response_model_rows": int(len(frame)),
    }


def cafe_scores(
    frame: pd.DataFrame,
    features: list[str],
    outcome: str,
    edges: list[tuple[str, str]],
    prediction_col: str = "prediction",
    seed: int = 7,
) -> dict[str, dict[str, float | int]]:
    rows: dict[str, dict[str, float | int]] = {}
    for feature in features:
        backdoor = [p for p in _parents(edges, feature) if p in features]
        mediators = [
            d for d in _descendants(edges, feature) if d in features and d != outcome
        ]
        total_estimate = _conditional_prediction_contrast(
            frame, prediction_col, feature, backdoor, seed=seed
        )
        direct_estimate = _conditional_prediction_contrast(
            frame, prediction_col, feature, backdoor + mediators, seed=seed + 101
        )
        total = float(total_estimate["effect"])
        direct = float(direct_estimate["effect"])
        indirect = max(total - direct, 0.0)
        rows[feature] = {
            "total_effect": total,
            "direct_effect": direct,
            "indirect_effect": indirect,
            "num_backdoor_controls": len(backdoor),
            "num_mediators": len(mediators),
            "total_controls": total_estimate["controls"],
            "direct_controls": direct_estimate["controls"],
            "theta_low": total_estimate["theta_low"],
            "theta_high": total_estimate["theta_high"],
        }
    return rows


def run_dataset(name: str, output_dir: Path, n: int, seed: int) -> dict:
    dataset = load_dataset(name, n=n, seed=seed)
    train, test = train_test_split(dataset.frame, test_size=0.35, random_state=seed)
    model_features = [f for f in dataset.features if f not in dataset.train_without]
    model = RandomForestRegressor(
        n_estimators=160,
        min_samples_leaf=12,
        random_state=seed,
        n_jobs=1,
    )
    model.fit(train[model_features], train[dataset.outcome])

    scored = test.copy()
    scored["prediction"] = model.predict(test[model_features])
    effects = cafe_scores(
        scored,
        features=dataset.features,
        outcome=dataset.outcome,
        edges=dataset.edges,
        seed=seed,
    )
    fuzzing = causal_fuzzing_effect(
        scored,
        model=model,
        model_features=model_features,
        features=dataset.features,
        edges=dataset.edges,
        target_feature=dataset.target_feature,
        seed=seed,
    )
    ranking = sorted(effects, key=lambda f: effects[f]["total_effect"], reverse=True)
    direct_ranking = sorted(
        effects, key=lambda f: effects[f]["direct_effect"], reverse=True
    )
    target = dataset.target_feature
    payload = {
        "dataset": dataset.name,
        "method": "cafe",
        "target_feature": target,
        "expected_top_feature": dataset.expected_top_feature,
        "expected_low_direct_feature": dataset.expected_low_direct_feature,
        "features": dataset.features,
        "model_features": model_features,
        "effects": effects,
        "ranking": ranking,
        "direct_ranking": direct_ranking,
        "target_total_rank": ranking.index(target) + 1,
        "target_direct_rank": direct_ranking.index(target) + 1,
        "target_total_effect": effects[target]["total_effect"],
        "target_direct_effect": effects[target]["direct_effect"],
        "target_indirect_effect": effects[target]["indirect_effect"],
        "causal_fuzzing": fuzzing,
        "cafe_model_query_count": int(len(scored)),
        "fuzzing_model_query_count": fuzzing["model_query_count"],
        "fuzzing_relative_total_error": float(
            abs(effects[target]["total_effect"] - fuzzing["total_effect"])
            / max(abs(fuzzing["total_effect"]), 1e-12)
        ),
        "prediction_r2": float(model.score(test[model_features], test[dataset.outcome])),
    }
    if dataset.name == "heart_disease":
        young = scored[scored["age"] <= 50]
        older = scored[scored["age"] > 50]
        subgroup_feature = "bmi"
        young_effects = cafe_scores(
            young,
            features=dataset.features,
            outcome=dataset.outcome,
            edges=dataset.edges,
            seed=seed,
        )[subgroup_feature]
        older_effects = cafe_scores(
            older,
            features=dataset.features,
            outcome=dataset.outcome,
            edges=dataset.edges,
            seed=seed,
        )[subgroup_feature]
        payload["subgroup_unlearning"] = {
            "feature": subgroup_feature,
            "split": "age > 50 vs age <= 50",
            "age_le_50": young_effects,
            "age_gt_50": older_effects,
            "direct_gap_abs": float(
                abs(older_effects["direct_effect"] - young_effects["direct_effect"])
            ),
            "indirect_gap": float(
                older_effects["indirect_effect"] - young_effects["indirect_effect"]
            ),
            "total_gap": float(
                older_effects["total_effect"] - young_effects["total_effect"]
            ),
        }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / f"{dataset.name}_cafe.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True)
    )
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--datasets", nargs="+", default=["heart_disease", "performance"])
    parser.add_argument("--output-dir", default="outputs/method")
    parser.add_argument("--n", type=int, default=10_000)
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    summary = {
        name: run_dataset(name, output_dir=output_dir, n=args.n, seed=args.seed)
        for name in args.datasets
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True))
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
