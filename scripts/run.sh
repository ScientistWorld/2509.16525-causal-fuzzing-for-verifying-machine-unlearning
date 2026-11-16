#!/bin/bash
# TEMPORARY (final hardening job): runs every hardening verifier (reference,
# seeds, honest variants, baselines, shortcuts) through the hidden test and the
# honest ones through the visible train slice, ranks them, then regenerates the
# official score files from the reference verifiers and validates.
set -uo pipefail
cd /home/user
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
bash scripts/download.sh
bash notes/hardening/run_hardening.sh
