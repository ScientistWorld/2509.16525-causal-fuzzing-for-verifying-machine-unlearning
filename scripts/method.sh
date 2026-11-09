#!/bin/bash
# Run the paper's method (CAFÉ, method/cafe.py) on the visible tasks through
# the evaluator-owned oracle and score it. CAFÉ needs no training; the
# evaluator calls scripts/verifiers/cafe.sh for every task.

set -e

cd /home/user

mkdir -p outputs
python -m eval.train.evaluate --methods cafe --scores outputs/cafe_train_scores.json
