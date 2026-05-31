# Train/Test Evaluation Design Notes

## Checks
- Read `eval/train/`, `eval/test/`, `scripts/evaluate_train.sh`, `scripts/evaluate_test.sh`, `scoring/reference.json`, the existing output artifact shape, and the relevant paper sections on mediated residual influence, subgroup effects, and query efficiency.
- Confirmed both train and test evaluators read method output artifacts from disk and do not import or regenerate `method/`.
- Confirmed `evaluate_test.sh` invokes `eval.test.evaluate` and writes `scoring/scores_test.json`; `evaluate_train.sh` invokes `eval.train.evaluate` and writes `scoring/scores_train.json`.
- Grepped for train/test cross-imports, hardcoded method defaults, and paper-agreement metric names; none were found.
- Confirmed `scoring/scores_train.json` and `scoring/scores_test.json` are absent.

## Changes
- Added explicit `_slice` markers to train and test score artifacts so stale or miswired outputs are easier to distinguish during runner validation.
- Capped `query_ratio_vs_fuzzing` at 10.0 and return 0.0 when either query count is non-positive. This keeps query efficiency as a machine-independent constraint while preventing a method from winning that metric by reporting a zero or tiny CAFÉ query count.
- Added the required `description` field to every metric in `scoring/reference.json`; the descriptions frame the metrics as scientific quantities rather than agreement with the paper.

## Runtime Concerns For Next Iteration
- The train/test split is a metric split over the same method artifacts, not a new data split. That is appropriate for this small semi-synthetic reproduction, but the runner should check that test primary metrics differ from train for the existing artifacts.
- The evaluators trust the artifact schema; a future method that emits fabricated effect values could still game both slices. A stronger future pass could add schema-level consistency checks against stored raw intervention summaries if those artifacts become available.
- I did not run the Python evaluators or `validate.py` because this iteration is source-only. I only ran `bash -n` and static greps.
