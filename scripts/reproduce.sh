#!/bin/bash
# Reproduce the paper's results end-to-end on the visible tasks: the
# evaluator builds the semi-synthetic tasks and audited black-box models,
# runs CAFÉ and the baselines (every scripts/verifiers/*.sh) against the
# counted oracle, and writes scoring/scores.json. No training step is needed
# by any verifier. Takes ~10-15 CPU minutes.

set -e

cd /home/user

bash scripts/evaluate.sh
