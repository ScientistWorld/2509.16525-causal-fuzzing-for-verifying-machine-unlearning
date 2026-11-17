#!/bin/bash
# Reproduce the paper's results end-to-end on the visible tasks: the
# evaluator builds the semi-synthetic tasks (Heart-Disease, Performance, and
# Adult-Income on the real UCI Adult data) and the audited black-box models,
# runs CAFÉ and the baselines (every scripts/verifiers/*.sh) against the
# counted oracle, and writes scoring/scores.json. No training step is needed
# by any verifier. Takes ~5 CPU minutes.

set -e

cd /home/user

bash scripts/evaluate.sh
