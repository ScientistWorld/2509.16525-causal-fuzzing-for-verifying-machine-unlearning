#!/bin/bash
# Paper's method: CAFÉ (method/cafe.py).
# Verifier entry point, invoked by the evaluator as:
#   bash cafe.sh <tasks_dir> <answers.json>
# with UNLEARN_ORACLE_ADDRESS / UNLEARN_ORACLE_AUTHKEY set (black-box oracle).
set -euo pipefail
python -m method.cafe --tasks-dir "$1" --output "$2"
