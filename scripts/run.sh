#!/bin/bash
# Temporary audit job entry point, restored after the job.
set -euo pipefail
cd /home/user
bash redteam/run_all.sh
