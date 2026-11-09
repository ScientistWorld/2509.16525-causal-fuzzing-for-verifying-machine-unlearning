#!/bin/bash
# Hardening shortcut 'constant_answers' (notes/hardening/shortcuts.py).
# Verifier entry point, invoked by the evaluator as:
#   bash shortcut_constant_answers.sh <tasks_dir> <answers.json>
# with UNLEARN_ORACLE_ADDRESS / UNLEARN_ORACLE_AUTHKEY set (black-box oracle).
set -euo pipefail
python notes/hardening/shortcuts.py --kind constant_answers --tasks-dir "$1" --output "$2"
