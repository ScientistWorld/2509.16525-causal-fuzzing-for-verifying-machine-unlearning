#!/bin/bash
# Reference CAFÉ, response-model seed 11.
# Verifier entry point, invoked by the evaluator as:
#   bash cafe_seed11.sh <tasks_dir> <answers.json>
# with UNLEARN_ORACLE_ADDRESS / UNLEARN_ORACLE_AUTHKEY set (black-box oracle).
set -euo pipefail
python -m method.cafe --tasks-dir "$1" --output "$2" --seed 11
