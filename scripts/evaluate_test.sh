#!/bin/bash
# Held-out test-slice evaluator. Mirrors scripts/evaluate.sh's artifact
# contract and scores the same method entries present in scores_train.json when
# that file exists.

set -e

cd /home/user

mkdir -p scoring

python -m eval.test.evaluate \
  --outputs-dir "${1:-outputs}" \
  --scores scoring/scores_test.json \
  --train-scores scoring/scores_train.json
