#!/bin/bash
# Run the visible and held-out evaluation slices against all discovered method
# artifacts in outputs/.

set -e

cd /home/user

bash scripts/evaluate_train.sh outputs
bash scripts/evaluate_test.sh outputs
