#!/bin/bash
# Hardening variant 'full_adjust' (notes/hardening/variants.py).
# Verifier entry point, invoked by the evaluator as:
#   bash variant_full_adjust.sh <tasks_dir> <answers.json>
# with UNLEARN_ORACLE_ADDRESS / UNLEARN_ORACLE_AUTHKEY set (black-box oracle).
set -euo pipefail
python notes/hardening/variants.py --variant full_adjust --tasks-dir "$1" --output "$2"
