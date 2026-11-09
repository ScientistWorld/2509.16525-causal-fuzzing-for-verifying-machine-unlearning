#!/bin/bash
# Hardening variant 'hgb_probe' (notes/hardening/variants.py).
# Verifier entry point, invoked by the evaluator as:
#   bash variant_hgb_probe.sh <tasks_dir> <answers.json>
# with UNLEARN_ORACLE_ADDRESS / UNLEARN_ORACLE_AUTHKEY set (black-box oracle).
set -euo pipefail
python notes/hardening/variants.py --variant hgb_probe --tasks-dir "$1" --output "$2"
