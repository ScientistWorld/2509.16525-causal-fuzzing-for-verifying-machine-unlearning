#!/bin/bash
# Hardening shortcut 'overbudget_bruteforce' (notes/hardening/shortcuts.py).
# Verifier entry point, invoked by the evaluator as:
#   bash shortcut_overbudget_bruteforce.sh <tasks_dir> <answers.json>
# with UNLEARN_ORACLE_ADDRESS / UNLEARN_ORACLE_AUTHKEY set (black-box oracle).
set -euo pipefail
python notes/hardening/shortcuts.py --kind overbudget_bruteforce --tasks-dir "$1" --output "$2"
