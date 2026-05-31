#!/bin/bash
# Visible train-slice evaluator. Mirrors scripts/evaluate.sh's artifact
# contract: the first argument is the outputs directory, defaulting to outputs.

set -e

cd /home/user

mkdir -p scoring

python -m eval.train.evaluate --outputs-dir "${1:-outputs}" --scores scoring/scores_train.json
