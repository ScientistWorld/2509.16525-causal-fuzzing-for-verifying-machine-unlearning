# Scoring audit plan

All candidate construction uses scientist-visible code and metadata. Hidden
evaluation runs in a separate, ordinary Python process after candidate generation
has exited, via `bash scripts/evaluate_test.sh` with **no arguments**. No candidate
modifies the evaluator, Python environment, process, or imports. Output artifacts
are the only submission interface used. Multiple such submissions share one CPU
job; the evaluator retains no process state between submissions.

Reference: preserve the supplied trained artifacts, and rerun n=10,000 at seeds
7, 11, and 19. Honest checks: n=30,000 with the original procedure; exact direct
zero for structurally omitted inputs; direct-only ablation; separately computed
direct permutation baseline; exhaustive low/high interventions on every row.

Shortcuts: constant answers from public generator metadata; invented query
counts; remove competing features from the declared feature list; replace the
independent oracle by the verifier's answer; change prediction units; negative
absolute gaps; fail the direct-unlearning constraint while maximizing other
metrics; zero outputs; write scores directly; worsen the baseline artifact.

Each folder's `run.sh` builds its candidate through `redteam/candidate.py`, runs
visible training evaluation, then runs the unmodified hidden evaluation with no
arguments, and saves both score files and the exact submitted artifacts. Small
JSON evidence is committed. Verbose logs and temporary restoration snapshots are
ignored by `redteam/.gitignore`.

The scalar rank depends on the population of attempts through its metric
standard deviations. `summary.json` therefore provides both an explicit complete
audit cohort and an honest-only sensitivity cohort, with all metric terms and
standard deviations. Signs come from `higher_is_better`; coefficients are used
only by their absolute values. The saved original test result is the zero anchor.
