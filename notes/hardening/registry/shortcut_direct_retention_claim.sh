#!/bin/bash
# Hardening shortcut 'direct_retention_claim' (notes/hardening/shortcuts.py).
# Verifier entry point, invoked by the evaluator as:
#   bash shortcut_direct_retention_claim.sh <tasks_dir> <answers.json>
# with UNLEARN_ORACLE_ADDRESS / UNLEARN_ORACLE_AUTHKEY set (black-box oracle).
set -euo pipefail
python notes/hardening/shortcuts.py --kind direct_retention_claim --tasks-dir "$1" --output "$2"
