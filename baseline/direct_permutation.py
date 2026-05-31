"""Direct-only attribution baseline for unlearning verification."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split

from data.synthetic_causal import load_dataset


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
    result = permutation_importance(
        model,
        test[model_features],
        test[dataset.outcome],
        n_repeats=8,
        random_state=seed,
        n_jobs=1,
    )
    scores = {feature: float(abs(score)) for feature, score in zip(model_features, result.importances_mean)}
    for omitted in dataset.train_without:
        scores[omitted] = 0.0
    ranking = sorted(dataset.features, key=lambda f: scores[f], reverse=True)
    target = dataset.target_feature
    payload = {
        "dataset": dataset.name,
        "method": "direct_permutation",
        "target_feature": target,
        "expected_top_feature": dataset.expected_top_feature,
        "features": dataset.features,
        "importance": scores,
        "ranking": ranking,
        "target_total_rank": ranking.index(target) + 1,
        "target_total_effect": scores[target],
        "prediction_r2": float(model.score(test[model_features], test[dataset.outcome])),
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / f"{dataset.name}_direct_permutation.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True)
    )
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--datasets", nargs="+", default=["heart_disease", "performance"])
    parser.add_argument("--output-dir", default="outputs/baseline")
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
