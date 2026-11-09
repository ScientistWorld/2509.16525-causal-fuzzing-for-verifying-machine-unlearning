#!/bin/bash
# Download all data and models needed for this environment.
#
# Estimated total download size: 0 GB
# Estimated disk usage after extraction: 0 GB
#
# Every task is generated procedurally: the visible task families live in
# data/synthetic_causal.py and the hidden ones in eval/test/, and the audited
# black-box models are trained by the evaluator from those samples with
# fixed seeds. There are no external datasets or pretrained weights to fetch;
# Python packages are installed by environment/setup.sh.

set -e

cd /home/user

mkdir -p data/downloads
echo "Nothing to download: all tasks are generated from code (data/synthetic_causal.py, eval/)."
