#!/bin/bash
set -euo pipefail
cd /home/user
folder=redteam/shortcut_baseline_move
python -m redteam.candidate shortcut_baseline_move > "$folder/method.log" 2>&1
# The method process has exited; the normal evaluator runs with no arguments.
bash scripts/evaluate_train.sh > "$folder/train.log" 2>&1
cp scoring/scores_train.json "$folder/scores_train.json"
bash scripts/evaluate_test.sh > "$folder/test.log" 2>&1
cp scoring/scores_test.json "$folder/scores_test.json"
printf '{"status": "completed", "test_command": "bash scripts/evaluate_test.sh"}\n' > "$folder/completed.json"
