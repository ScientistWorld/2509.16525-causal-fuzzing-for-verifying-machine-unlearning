#!/bin/bash
# Hardening variant 'direct_only' (notes/hardening/variants.py).
# Verifier entry point, invoked by the evaluator as:
#   bash variant_direct_only.sh <tasks_dir> <answers.json>
# with UNLEARN_ORACLE_ADDRESS / UNLEARN_ORACLE_AUTHKEY set (black-box oracle).
set -euo pipefail
python notes/hardening/variants.py --variant direct_only --tasks-dir "$1" --output "$2"
