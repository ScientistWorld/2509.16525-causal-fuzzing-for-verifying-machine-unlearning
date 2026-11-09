#!/bin/bash
# Hardening shortcut 'cafe_zero_direct_gap' (notes/hardening/shortcuts.py).
# Verifier entry point, invoked by the evaluator as:
#   bash shortcut_cafe_zero_direct_gap.sh <tasks_dir> <answers.json>
# with UNLEARN_ORACLE_ADDRESS / UNLEARN_ORACLE_AUTHKEY set (black-box oracle).
set -euo pipefail
python notes/hardening/shortcuts.py --kind cafe_zero_direct_gap --tasks-dir "$1" --output "$2"
