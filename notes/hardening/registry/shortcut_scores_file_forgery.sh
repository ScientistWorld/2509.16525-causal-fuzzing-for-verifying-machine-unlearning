#!/bin/bash
# Hardening shortcut 'scores_file_forgery' (notes/hardening/shortcuts.py).
# Verifier entry point, invoked by the evaluator as:
#   bash shortcut_scores_file_forgery.sh <tasks_dir> <answers.json>
# with UNLEARN_ORACLE_ADDRESS / UNLEARN_ORACLE_AUTHKEY set (black-box oracle).
set -euo pipefail
python notes/hardening/shortcuts.py --kind scores_file_forgery --tasks-dir "$1" --output "$2"
