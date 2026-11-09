#!/bin/bash
# Hardening variant 'no_backdoor' (notes/hardening/variants.py).
# Verifier entry point, invoked by the evaluator as:
#   bash variant_no_backdoor.sh <tasks_dir> <answers.json>
# with UNLEARN_ORACLE_ADDRESS / UNLEARN_ORACLE_AUTHKEY set (black-box oracle).
set -euo pipefail
python notes/hardening/variants.py --variant no_backdoor --tasks-dir "$1" --output "$2"
