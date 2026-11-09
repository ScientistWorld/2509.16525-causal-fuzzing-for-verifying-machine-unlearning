"""Visible train slice: score every registered verifier on the visible tasks.

Usage: python -m eval.train.evaluate [--scores scoring/scores_train.json]
Verifiers are discovered as scripts/verifiers/*.sh (override with
--verifiers-dir, restrict with --methods). No method code is imported.
"""

from __future__ import annotations

from eval.train.harness import run_cli
from eval.train.tasks import build_tasks


def main(argv=None) -> None:
    run_cli("train", build_tasks, "scoring/scores_train.json", argv)


if __name__ == "__main__":
    main()
