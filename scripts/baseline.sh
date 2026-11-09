#!/bin/bash
# Run the baselines on the visible tasks through the evaluator-owned oracle:
#   direct_permutation - direct-only attribution check (paper's SHAP /
#                        permutation-importance family)
#   causal_fuzzing     - paper Algorithm 1 within the same query budget
#
# Usage: bash scripts/baseline.sh [name ...]

set -e

cd /home/user

NAMES=("$@")
if [ ${#NAMES[@]} -eq 0 ]; then
  NAMES=(direct_permutation causal_fuzzing)
fi

mkdir -p outputs
python -m eval.train.evaluate --methods "${NAMES[@]}" --scores outputs/baseline_train_scores.json
