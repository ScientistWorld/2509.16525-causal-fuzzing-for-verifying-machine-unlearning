#!/bin/bash
# Baseline: direct-only attribution check (baseline/direct_permutation.py).
# Verifier entry point, invoked by the evaluator as:
#   bash direct_permutation.sh <tasks_dir> <answers.json>
# with UNLEARN_ORACLE_ADDRESS / UNLEARN_ORACLE_AUTHKEY set (black-box oracle).
set -euo pipefail
python -m baseline.direct_permutation --tasks-dir "$1" --output "$2"
