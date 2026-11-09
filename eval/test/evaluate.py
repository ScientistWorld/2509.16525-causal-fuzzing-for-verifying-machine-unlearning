"""Hidden test slice: score every registered verifier on held-out tasks.

Usage: python -m eval.test.evaluate [--scores scoring/scores_test.json]
Verifiers are discovered as scripts/verifiers/*.sh; no method name is
hard-coded and no method code is imported.
"""

from __future__ import annotations

from eval.test.harness import run_cli
from eval.test.tasks import build_tasks


def main(argv=None) -> None:
    run_cli("test", build_tasks, "scoring/scores_test.json", argv)


if __name__ == "__main__":
    main()
