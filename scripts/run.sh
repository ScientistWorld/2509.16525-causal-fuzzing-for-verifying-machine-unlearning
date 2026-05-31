#!/bin/bash
# Standard reproduction job: generate method/baseline artifacts, score them,
# and validate the main reproduction claim.

set -e

cd /home/user

bash scripts/reproduce.sh
bash scripts/evaluate.sh outputs
python validate.py --compare --post-reproducer
