#!/bin/bash
# Hardening shortcut 'cafe_prior_subgroup' (notes/hardening/shortcuts.py).
# Verifier entry point, invoked by the evaluator as:
#   bash shortcut_cafe_prior_subgroup.sh <tasks_dir> <answers.json>
# with UNLEARN_ORACLE_ADDRESS / UNLEARN_ORACLE_AUTHKEY set (black-box oracle).
set -euo pipefail
python notes/hardening/shortcuts.py --kind cafe_prior_subgroup --tasks-dir "$1" --output "$2"
