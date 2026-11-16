#!/bin/bash
# Hardening driver (resumable: per-verifier results are cached in
# notes/hardening/results/{test,train}/ and reused on rerun).
set -uo pipefail
cd /home/user
RES=notes/hardening/results
REG=notes/hardening/registry
mkdir -p "$RES"

export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1

if [ -f "$RES/smoke_ok" ]; then
  echo "=== smoke already passed, skipping"
else
echo "=== smoke $(date -u +%FT%TZ)"
python -m eval.test.evaluate --smoke --verifiers-dir "$REG" \
  --methods cafe variant_probe_direct variant_abduction direct_permutation causal_fuzzing shortcut_forged_fields shortcut_nonfinite_values shortcut_overbudget_bruteforce \
  --scores "$RES/smoke_test.json" || { echo "SMOKE TEST FAILED"; exit 1; }
python -m eval.train.evaluate --smoke --methods cafe direct_permutation causal_fuzzing --scores "$RES/smoke_train.json" \
  || { echo "SMOKE TRAIN FAILED"; exit 1; }
python - "$RES/smoke_test.json" "$RES/smoke_train.json" <<'PY' || { echo "SMOKE CHECK FAILED"; exit 1; }
import json, sys
test, train = (json.load(open(p)) for p in sys.argv[1:3])
diag = {**{f"test:{k}": v for k, v in test["_diagnostics"].items()}, **{f"train:{k}": v for k, v in train["_diagnostics"].items()}}
print(json.dumps(diag, indent=1))
must_pass = ["test:cafe", "test:variant_probe_direct", "test:variant_abduction", "test:direct_permutation",
             "test:causal_fuzzing", "test:shortcut_forged_fields", "train:cafe", "train:direct_permutation", "train:causal_fuzzing"]
must_fail = ["test:shortcut_nonfinite_values", "test:shortcut_overbudget_bruteforce"]
bad = [k for k in must_pass if diag[k]["failed_tasks"] != 0] + [k for k in must_fail if diag[k]["failed_tasks"] == 0]
print("smoke problems:", bad)
sys.exit(1 if bad else 0)
PY
touch "$RES/smoke_ok"
fi

echo "=== hidden test, all hardening verifiers $(date -u +%FT%TZ)"
python -m eval.test.evaluate --verifiers-dir "$REG" --per-method-dir "$RES/test" \
  --scores "$RES/scores_test_all.json" --details "$RES/details_test.json" || echo "HIDDEN TEST RUN FAILED"

echo "=== visible train, honest verifiers $(date -u +%FT%TZ)"
python -m eval.train.evaluate --verifiers-dir "$REG" --per-method-dir "$RES/train" \
  --methods cafe cafe_seed11 cafe_seed19 variant_probe_direct variant_hgb variant_abduction variant_abduction_half variant_full_adjust variant_cafe_half_rows variant_direct_only variant_no_backdoor direct_permutation causal_fuzzing \
  --scores "$RES/scores_train_all.json" || echo "TRAIN RUN FAILED"

echo "=== ranking $(date -u +%FT%TZ)"
python notes/hardening/rank.py || echo "RANK FAILED"

echo "=== official score files $(date -u +%FT%TZ)"
bash scripts/evaluate.sh && bash scripts/evaluate_train.sh && bash scripts/evaluate_test.sh || echo "OFFICIAL SCORING FAILED"

echo "=== validate $(date -u +%FT%TZ)"
python validate.py --compare --post-design || echo "VALIDATE FAILED"
echo "=== done $(date -u +%FT%TZ)"
