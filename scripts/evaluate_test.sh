#!/bin/bash
# Hidden test slice. Runs with no arguments: builds the held-out tasks inside
# eval/test/ (data, audited black-box models, contrasts, query budget, exact
# ground truth), runs EVERY verifier registered as scripts/verifiers/*.sh
# against a counted prediction oracle, and recomputes all metrics from the
# raw effect estimates. Writes scoring/scores_test.json. Never retrains a
# method and never imports method code.
#
# Optional: $1 = alternative verifier registry directory.

set -e

cd /home/user

mkdir -p scoring

if [ -n "${1:-}" ]; then
  python -m eval.test.evaluate --verifiers-dir "$1" --scores scoring/scores_test.json
else
  python -m eval.test.evaluate --scores scoring/scores_test.json
fi
