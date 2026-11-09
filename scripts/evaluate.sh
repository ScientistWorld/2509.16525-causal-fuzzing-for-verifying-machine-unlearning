#!/bin/bash
# Standard evaluation: score every registered verifier (scripts/verifiers/*.sh)
# on the visible tasks and write scoring/scores.json (same metrics and keys as
# scoring/reference.json). Uses only eval/ (plus the public task families in
# data/); never imports method/.
#
# A verifier is any script scripts/verifiers/<name>.sh called as
#   bash <name>.sh <tasks_dir> <answers.json>
# that writes {"tasks": {task_id: {"effects": {feature: {"total", "direct"}},
# "subgroup_effects": {group: {feature: {"total", "direct"}}}}}}; see
# briefing/evaluation.md.
#
# Optional: $1 = alternative verifier registry directory.

set -e

cd /home/user

mkdir -p scoring

if [ -n "${1:-}" ]; then
  python -m eval.evaluate_outputs --verifiers-dir "$1" --scores scoring/scores.json
else
  python -m eval.evaluate_outputs --scores scoring/scores.json
fi
