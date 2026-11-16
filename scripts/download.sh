#!/bin/bash
# Download all data and models needed for this environment.
#
# Estimated total download size: 0.006 GB (UCI Adult)
# Estimated disk usage after extraction: 0.006 GB
#
# The Heart-Disease and Performance task families are generated from code
# (data/synthetic_causal.py for the visible slice, eval/test/ for the hidden
# one). The Adult-Income family is semi-synthetic on the real UCI Adult Income
# data (Becker & Kohavi 1996): the visible slice uses adult.data and the
# hidden slice adult.test. The audited black-box models are trained by the
# evaluator from the task samples with fixed seeds; there are no pretrained
# weights. Python packages are installed by environment/setup.sh.
#
# Idempotent: a file that is already present with the right checksum is kept.

set -euo pipefail

cd /home/user

ADULT_DIR=data/downloads/uci_adult
ADULT_URL=https://archive.ics.uci.edu/ml/machine-learning-databases/adult
mkdir -p "$ADULT_DIR"

fetch() {  # fetch <file> <sha256>
  local file=$1 sha=$2 target="$ADULT_DIR/$1"
  if [ -s "$target" ] && echo "$sha  $target" | sha256sum -c --status; then
    echo "ok: $target"
    return
  fi
  echo "fetching $ADULT_URL/$file"
  curl -fsSL --retry 5 --retry-delay 5 -o "$target.part" "$ADULT_URL/$file" \
    || wget -q -O "$target.part" "$ADULT_URL/$file"
  mv "$target.part" "$target"
  echo "$sha  $target" | sha256sum -c
}

fetch adult.data 5b00264637dbfec36bdeaab5676b0b309ff9eb788d63554ca0a249491c86603d
fetch adult.test a2a9044bc167a35b2361efbabec64e89d69ce82d9790d2980119aac5fd7e9c05
