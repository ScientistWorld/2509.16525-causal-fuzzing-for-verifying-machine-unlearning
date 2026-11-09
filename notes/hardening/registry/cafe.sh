#!/bin/bash
# Reference CAFÉ, seed 7 (same as scripts/verifiers/cafe.sh).
# Verifier entry point, invoked by the evaluator as:
#   bash cafe.sh <tasks_dir> <answers.json>
# with UNLEARN_ORACLE_ADDRESS / UNLEARN_ORACLE_AUTHKEY set (black-box oracle).
set -euo pipefail
python -m method.cafe --tasks-dir "$1" --output "$2" --seed 7
