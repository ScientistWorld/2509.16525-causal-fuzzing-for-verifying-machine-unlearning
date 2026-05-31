# Scientist Constraints

## Data
Use the provided semi-synthetic generators in `data/synthetic_causal.py` with the same named experiments and target features. External data must not be added to these two scored experiments because the benchmark measures residual-influence verification on fixed causal structures.

## Audited Model
Keep the black-box audited predictor family and target-feature omission used by `scripts/reproduce.sh`. The paper's question is verification after direct unlearning, not improving the predictor by exposing the removed feature.

## Evaluation
Do not edit `eval/` or `scripts/evaluate.sh` when reporting improved method scores. Evaluation must consume output artifacts in the same format and must not import from `method/`.

## Compliance Checklist
- [ ] Scored experiments are `heart_disease_feature_unlearning` and `performance_feature_unlearning`.
- [ ] The removed target feature is not used as an input to the audited predictor.
- [ ] No external data are added to the scored experiments.
- [ ] `scripts/evaluate.sh` runs without importing from `method/`.
