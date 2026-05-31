#!/bin/bash
# Reproduce the paper's results end-to-end.
#
# This script runs inside the compute container, generates baseline and method
# artifacts, then calls scripts/evaluate.sh once on the combined outputs.
#
# Assumes:
#   - Container is built (environment/container.sif)
#   - Data and models are downloaded (via scripts/download.sh)
#   - Working directory is /home/user
#
# This is the "gold standard" reproduction — 
# You do not need to run this, but keep this in good shape
# so other agents can easily run a full loop of reproduction and get the paper's numbers.

set -e

cd /home/user

rm -rf outputs
mkdir -p outputs

bash scripts/baseline.sh heart_disease performance
bash scripts/method.sh heart_disease performance
bash scripts/evaluate.sh outputs
