#!/bin/bash
# Standard reproduction job: generate method/baseline artifacts, score them,
# and validate the main reproduction claim.

set -e

cd /home/user

bash scripts/reproduce.sh
bash scripts/evaluate.sh outputs
bash scripts/evaluate_train.sh outputs
bash scripts/evaluate_test.sh outputs
python validate.py --compare --post-reproducer
