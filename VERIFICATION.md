> **Superseded.** This file describes the gym before the final hardening iteration (artifact re-scoring evaluator, old metrics). The current protocol, metrics and evidence are in `HARDENING.md`, `briefing/evaluation.md` and `scoring/`.

# Verification Report

## Initial Assessment

The workspace started at `secondary_claims` with completed CPU scheduler jobs, populated method, baseline, evaluation, and scoring artifacts, and a plausible reproduction of the core and subgroup claims. The claimed milestone was justified for the three validated experiments: two feature-unlearning settings and one Heart-Disease subgroup-unlearning setting.

## Issues Found

- Critical: `scoring/reference.json`, `scoring/TARGETS.md`, `scoring/EXPERIMENTS.md`, and the train/test evaluators advertised a new `graph_misspecification_robustness` experiment, but `scores.json`, `scores_train.json`, and `scores_test.json` did not contain that experiment. A gym target without a scored result would give future agents an inconsistent scoring contract.
- Minor: `MILESTONES.md` and `PROGRESS.md` still described graph-robustness validation as pending, which conflicted with a final `done` state.

## Fixes Applied

- Removed the unvalidated graph-robustness experiment from the public scoring contract and train/test evaluators, restoring consistency with the validated three-experiment score files.
- Updated `scoring/TARGETS.md`, `scoring/EXPERIMENTS.md`, `scoring/CONSTRAINTS.md`, `MILESTONES.md`, and `PROGRESS.md` so they describe only experiments that are actually scored.
- Reran `scripts/evaluate.sh outputs`, `scripts/evaluate_train.sh outputs`, `scripts/evaluate_test.sh outputs`, `python -m py_compile eval/train/evaluate.py eval/test/evaluate.py eval/evaluate_outputs.py`, and `python validate.py --compare --post-reproducer`. All checks passed.

## Final Judgment

The workspace is ready to serve as a research gym at `secondary_claims`. Improve-mode agents can reproduce and compare against the existing method and baseline artifacts; from-scratch agents can use the method-agnostic problem, data, and evaluation files without relying on `method/`. The main limitation is scope: the gym uses reconstructed semi-synthetic datasets and does not yet score the paper's broader graph-robustness or real-world benchmark claims.

- Milestone: secondary_claims
- Ready for gym use: yes
- Confidence: high
- Key limitation: reconstructed semi-synthetic data only
