"""CAFÉ causal influence estimator for black-box model predictions."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict, deque
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

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


def _standardized_linear_effect(
    frame: pd.DataFrame, prediction_col: str, feature: str, controls: list[str]
) -> float:
    """Estimate an adjusted effect as the standardized coefficient of feature.

    This implements the CAFÉ backdoor adjustment in a compact finite-sample
    form: total effect adjusts for a valid backdoor set, while direct effect
    additionally adjusts for mediators on directed paths to the outcome.
    """

    columns = [feature] + [c for c in controls if c != feature]
    x = frame[columns].to_numpy(dtype=float)
    y = frame[prediction_col].to_numpy(dtype=float)
    if np.std(x[:, 0]) < 1e-10 or np.std(y) < 1e-10:
        return 0.0
    reg = make_pipeline(StandardScaler(), LinearRegression())
    reg.fit(x, y)
    return float(abs(reg.named_steps["linearregression"].coef_[0]))


def cafe_scores(
    frame: pd.DataFrame,
    features: list[str],
    outcome: str,
    edges: list[tuple[str, str]],
    prediction_col: str = "prediction",
) -> dict[str, dict[str, float | int]]:
    rows: dict[str, dict[str, float | int]] = {}
    for feature in features:
        backdoor = [p for p in _parents(edges, feature) if p in features]
        mediators = [
            d for d in _descendants(edges, feature) if d in features and d != outcome
        ]
        total = _standardized_linear_effect(frame, prediction_col, feature, backdoor)
        direct = _standardized_linear_effect(
            frame, prediction_col, feature, backdoor + mediators
        )
        indirect = max(total - direct, 0.0)
        rows[feature] = {
            "total_effect": total,
            "direct_effect": direct,
            "indirect_effect": indirect,
            "num_backdoor_controls": len(backdoor),
            "num_mediators": len(mediators),
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
        "prediction_r2": float(model.score(test[model_features], test[dataset.outcome])),
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
