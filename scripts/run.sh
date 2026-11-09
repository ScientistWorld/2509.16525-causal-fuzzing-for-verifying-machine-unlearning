#!/bin/bash
# Reproduce the reference end to end (CPU, ~10 minutes): score the paper's
# method (CAFÉ) and the two baselines registered in scripts/verifiers/ on the
# visible tasks (scoring/scores.json, scoring/scores_train.json) and on the
# hidden test (scoring/scores_test.json), then validate the workspace.
# The hardening evidence (variants, shortcuts, paired ranking) is rerun with
# bash notes/hardening/run_hardening.sh (resumable; see HARDENING.md).

set -euo pipefail

cd /home/user

export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1

bash scripts/reproduce.sh
bash scripts/evaluate_train.sh
bash scripts/evaluate_test.sh
python validate.py --compare --post-design
