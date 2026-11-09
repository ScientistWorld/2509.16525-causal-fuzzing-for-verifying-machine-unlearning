#!/bin/bash
# Baseline: budgeted causal fuzzing (Algorithm 1).
# Verifier entry point, invoked by the evaluator as:
#   bash causal_fuzzing.sh <tasks_dir> <answers.json>
# with UNLEARN_ORACLE_ADDRESS / UNLEARN_ORACLE_AUTHKEY set (black-box oracle).
set -euo pipefail
python -m baseline.causal_fuzzing --tasks-dir "$1" --output "$2"
