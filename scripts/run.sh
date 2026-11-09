#!/bin/bash
# Hardening job: smoke checks, all hardening verifiers through the hidden
# test (and honest ones through the visible train slice), ranking analysis,
# then the official score files for the registered verifiers and validation.

set -euo pipefail

cd /home/user

export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1

bash notes/hardening/run_hardening.sh
