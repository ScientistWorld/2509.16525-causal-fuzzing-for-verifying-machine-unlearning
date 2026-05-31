"""Evaluate verifier artifacts without importing method code."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from eval.train.evaluate import evaluate as evaluate_artifacts


def evaluate(outputs_dir: Path) -> dict:
    """Score every compatible method artifact under an outputs directory.

    The train-slice evaluator contains the generic artifact discovery and metric
    logic. The top-level score file keeps the same metrics but omits the slice
    marker so it mirrors ``scoring/reference.json``.
    """

    scores = evaluate_artifacts(outputs_dir)
    scores.pop("_slice", None)
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
