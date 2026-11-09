#!/bin/bash
set -euo pipefail
cd /home/user
cases=(reference_seed7 reference_seed11 reference_seed19 better_more_data better_exact_direct
       weak_direct_only simple_baseline brute_force shortcut_constant_answers
       shortcut_reported_queries shortcut_feature_list shortcut_replace_oracle
       shortcut_rescale_units shortcut_impossible_gap shortcut_constraint_failure
       shortcut_zero_output shortcut_scores_file shortcut_baseline_move)
restore_original_artifacts() {
  python - <<'PY'
from pathlib import Path
import shutil
root = Path('/home/user')
state = root / 'redteam/_state'
if (root / 'outputs').exists():
    shutil.rmtree(root / 'outputs')
shutil.copytree(state / 'outputs', root / 'outputs')
for name in ('scores.json', 'scores_train.json', 'scores_test.json'):
    shutil.copy2(state / name, root / 'scoring' / name)
PY
}
trap restore_original_artifacts EXIT
for case in "${cases[@]}"; do
  echo "START $case $(date -u +%FT%TZ)"
  if [ -f "redteam/$case/completed.json" ]; then
    echo "REUSE completed $case"
  elif bash "redteam/$case/run.sh"; then
    echo "OK $case $(date -u +%FT%TZ)"
  else
    echo "FAILED $case $(date -u +%FT%TZ)"
    printf '{"status": "failed"}\n' > "redteam/$case/failure.json"
  fi
done
python -m redteam.summarize | tee redteam/ranking.txt
