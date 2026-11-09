"""scores.json writer: the visible-task evaluation without the slice marker.

Runs every registered verifier (scripts/verifiers/*.sh) on the visible tasks
through the evaluator-owned oracle and writes scoring/scores.json. Method code
is never imported here.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from eval.train.evaluate import main as train_main


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verifiers-dir", default=None)
    parser.add_argument("--scores", default="scoring/scores.json")
    args = parser.parse_args()
    argv = ["--scores", args.scores]
    if args.verifiers_dir:
        argv += ["--verifiers-dir", args.verifiers_dir]
    train_main(argv)
    path = Path(args.scores)
    scores = json.loads(path.read_text())
    scores.pop("_slice", None)
    path.write_text(json.dumps(scores, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
