#!/bin/bash
# Hardening shortcut 'flag_all_unlearned' (notes/hardening/shortcuts.py).
# Verifier entry point, invoked by the evaluator as:
#   bash shortcut_flag_all_unlearned.sh <tasks_dir> <answers.json>
# with UNLEARN_ORACLE_ADDRESS / UNLEARN_ORACLE_AUTHKEY set (black-box oracle).
set -euo pipefail
python notes/hardening/shortcuts.py --kind flag_all_unlearned --tasks-dir "$1" --output "$2"
