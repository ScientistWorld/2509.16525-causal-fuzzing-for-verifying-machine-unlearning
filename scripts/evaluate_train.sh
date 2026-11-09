#!/bin/bash
# Visible train slice: same protocol and metrics as the hidden test, on the
# visible task families in data/synthetic_causal.py. Runs every verifier
# registered as scripts/verifiers/*.sh and writes scoring/scores_train.json.
#
# Optional: $1 = alternative verifier registry directory.

set -e

cd /home/user

mkdir -p scoring

if [ -n "${1:-}" ]; then
  python -m eval.train.evaluate --verifiers-dir "$1" --scores scoring/scores_train.json
else
  python -m eval.train.evaluate --scores scoring/scores_train.json
fi
