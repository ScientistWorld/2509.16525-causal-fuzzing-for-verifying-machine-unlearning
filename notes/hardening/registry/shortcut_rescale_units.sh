#!/bin/bash
# Hardening shortcut 'rescale_units' (notes/hardening/shortcuts.py).
# Verifier entry point, invoked by the evaluator as:
#   bash shortcut_rescale_units.sh <tasks_dir> <answers.json>
# with UNLEARN_ORACLE_ADDRESS / UNLEARN_ORACLE_AUTHKEY set (black-box oracle).
set -euo pipefail
python notes/hardening/shortcuts.py --kind rescale_units --tasks-dir "$1" --output "$2"
