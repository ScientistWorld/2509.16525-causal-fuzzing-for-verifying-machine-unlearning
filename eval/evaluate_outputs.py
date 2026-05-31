"""Evaluate method artifacts without importing method code."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def _load(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Missing artifact: {path}")
    return json.loads(path.read_text())


def _rank_score(rank: int, n_features: int) -> float:
    if n_features <= 1:
        return 1.0
    return float((n_features - rank) / (n_features - 1))


def evaluate(outputs_dir: Path) -> dict:
    method_dir = outputs_dir / "method"
    baseline_dir = outputs_dir / "baseline"
    scores = {"experiments": {}}

    for dataset in ["heart_disease", "performance"]:
        cafe = _load(method_dir / f"{dataset}_cafe.json")
        baseline = _load(baseline_dir / f"{dataset}_direct_permutation.json")
        exp_name = f"{dataset}_feature_unlearning"
        n_features = len(cafe["features"])
        target_indirect = float(cafe["target_indirect_effect"])
        total = float(cafe["target_total_effect"])
        indirect_fraction = target_indirect / max(total, 1e-12)
        indirect_detected = 1.0 if indirect_fraction >= 0.5 and target_indirect > 0.05 else 0.0
        direct_near_zero = 1.0 if float(cafe["target_direct_effect"]) <= 0.15 * max(total, 1e-12) else 0.0
        scores["experiments"][exp_name] = {
            "results": {
                "direct_permutation": {
                    "target_rank": float(baseline["target_total_rank"]),
                    "rank_score": _rank_score(int(baseline["target_total_rank"]), n_features),
                    "indirect_detected": 0.0,
                    "direct_unlearned": 1.0,
                },
                "cafe": {
                    "target_rank": float(cafe["target_total_rank"]),
                    "rank_score": _rank_score(int(cafe["target_total_rank"]), n_features),
                    "indirect_detected": indirect_detected,
                    "direct_unlearned": direct_near_zero,
                },
            }
        }
    return scores


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outputs-dir", default="outputs")
    parser.add_argument("--scores", default="scoring/scores.json")
    args = parser.parse_args()
    scores = evaluate(Path(args.outputs_dir))
    score_path = Path(args.scores)
    score_path.parent.mkdir(parents=True, exist_ok=True)
    score_path.write_text(json.dumps(scores, indent=2, sort_keys=True))
    print(json.dumps(scores, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
