# Verification Report

## Initial Assessment

The workspace started at `secondary_claims` with completed CPU scheduler jobs, populated method/baseline/evaluation artifacts, and passing validation. The claimed milestone was justified: the implementation runs the paper's causal residual-influence verification procedure on two semi-synthetic feature-unlearning settings and one subgroup-unlearning setting, and the scores support the core and secondary claims.

## Issues Found

- Minor: `eval/evaluate_outputs.py` was hardcoded to the reproduced `cafe` and `direct_permutation` artifacts, so a future method with the same artifact schema but a different method name would not be scored by `scripts/evaluate.sh`.
- Minor: several method-agnostic or method-safe docs referred to the paper/proposed method or "fast estimator" where generic benchmark language was clearer.
- Minor: `scoring/reference.json` encoded qualitative figure/ranking claims and a query-count substitute for runtime without an explicit `notes` explanation.

## Fixes Applied

- Rewired `eval/evaluate_outputs.py` to reuse the generic artifact discovery and scoring logic from `eval.train.evaluate`, while omitting the train-slice marker in `scoring/scores.json`.
- Cleaned method-agnostic wording in `briefing/evaluation.md`, `scoring/EXPERIMENTS.md`, `scoring/TARGETS.md`, `scoring/CONSTRAINTS.md`, and `data/` docstrings.
- Added `notes` fields to each experiment in `scoring/reference.json` explaining qualitative reference targets and the machine-independent query-count efficiency metric.
- Reran `scripts/evaluate.sh`, `scripts/evaluate_train.sh`, `scripts/evaluate_test.sh`, and `python validate.py --compare --post-reproducer`; all checks passed and reproduced scores remained stable.

## Final Judgment

The workspace is ready to serve as a research gym. Improve-mode agents can run the packaged method and compare against the existing scores; from-scratch agents can use the method-agnostic problem, data, and evaluation files without seeing the paper's implementation. The main limitation is scope: the gym uses reconstructed semi-synthetic datasets rather than the full set of real-world benchmarks from the paper.

- Milestone: secondary_claims
- Ready for gym use: yes
- Confidence: high
- Key limitation: reconstructed semi-synthetic data only
