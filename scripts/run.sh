#!/bin/bash
# TEMPORARY (calibration job for the new Adult-Income experiment): smoke-test
# the evaluator on every family, then print the Adult truth distribution and
# score key verifiers on the Adult tasks of both slices.
set -uo pipefail
cd /home/user
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
OUT=notes/hardening/adult_calibration
REG=notes/hardening/registry
mkdir -p "$OUT"
echo "=== smoke $(date -u +%FT%TZ)"
python -m eval.test.evaluate --smoke --verifiers-dir "$REG" \
  --methods cafe variant_abduction_half variant_full_adjust direct_permutation causal_fuzzing shortcut_overbudget_bruteforce \
  --scores "$OUT/smoke_test.json" || echo "SMOKE TEST FAILED"
python -m eval.train.evaluate --smoke --methods cafe direct_permutation causal_fuzzing --scores "$OUT/smoke_train.json" \
  || echo "SMOKE TRAIN FAILED"
echo "=== adult test $(date -u +%FT%TZ)"
python notes/hardening/adult_diag.py test "$OUT" cafe direct_permutation causal_fuzzing variant_abduction_half \
  variant_full_adjust variant_hgb variant_probe_direct shortcut_cafe_shrink_unlearned shortcut_cafe_assume_unlearned \
  || echo "ADULT TEST FAILED"
echo "=== adult train $(date -u +%FT%TZ)"
python notes/hardening/adult_diag.py train "$OUT" cafe direct_permutation causal_fuzzing variant_abduction_half variant_full_adjust \
  || echo "ADULT TRAIN FAILED"
echo "=== done $(date -u +%FT%TZ)"
