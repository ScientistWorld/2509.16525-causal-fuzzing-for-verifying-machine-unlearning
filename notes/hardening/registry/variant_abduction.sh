#!/bin/bash
# Hardening variant 'abduction' (notes/hardening/variants.py).
# Verifier entry point, invoked by the evaluator as:
#   bash variant_abduction.sh <tasks_dir> <answers.json>
# with UNLEARN_ORACLE_ADDRESS / UNLEARN_ORACLE_AUTHKEY set (black-box oracle).
set -euo pipefail
python notes/hardening/variants.py --variant abduction --tasks-dir "$1" --output "$2"
