"""Direct-only attribution baseline (permutation-importance style check).

Representative of the paper's direct/associational baselines (permutation
importance, SHAP): each feature is switched between its two contrast values
while every other input keeps its observed value, and the change in the
black-box output is reported as the feature's influence. Nothing is
propagated to downstream variables, so total == direct and no mediated
influence is ever reported. Rows are subsampled to fit the query budget.

Run as a verifier:  python -m baseline.direct_permutation --tasks-dir DIR --output answers.json
"""

from __future__ import annotations

import argparse

import numpy as np
import pandas as pd

from data.blackbox import BlackBox
from data.causal_graph import load_tasks, subgroup_mask, write_answers


def row_allocation(spec: dict, queries_per_row: int, budget: int) -> dict[str, int]:
    weights = {f: (2 if f in spec.get("subgroup_features", []) else 1) for f in spec["estimate_features"]}
    unit = budget // (queries_per_row * sum(weights.values()))
    return {f: max(1, min(spec["n_rows"], unit * w)) for f, w in weights.items()}


def direct_contrasts(spec, audit, blackbox, feature, rows):
    lo, hi = spec["interventions"][feature]
    sample = audit.iloc[rows]
    low, high = sample.copy(), sample.copy()
    low[feature] = lo
    high[feature] = hi
    preds = blackbox.predict(pd.concat([low, high], ignore_index=True))
    return preds[len(rows) :] - preds[: len(rows)]


def estimate_task(spec: dict, audit: pd.DataFrame, blackbox: BlackBox, seed: int = 7) -> dict:
    rng = np.random.default_rng(seed)
    allocation = row_allocation(spec, 2, blackbox.remaining)
    effects, per_row = {}, {}
    for feature in spec["estimate_features"]:
        rows = np.sort(rng.choice(len(audit), size=allocation[feature], replace=False))
        contrast = direct_contrasts(spec, audit, blackbox, feature, rows)
        per_row[feature] = (rows, contrast)
        value = float(contrast.mean())
        effects[feature] = {"total": value, "direct": value}
    answer = {"effects": effects}
    if spec.get("subgroups"):
        answer["subgroup_effects"] = {}
        for name, rule in spec["subgroups"].items():
            mask = subgroup_mask(audit, rule)
            group = {}
            for feature in spec["subgroup_features"]:
                rows, contrast = per_row[feature]
                inside = mask[rows]
                value = float(contrast[inside].mean()) if inside.any() else 0.0
                group[feature] = {"total": value, "direct": value}
            answer["subgroup_effects"][name] = group
    return answer


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--tasks-dir", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args(argv)
    answers = {}
    for spec, audit in load_tasks(args.tasks_dir):
        answers[spec["task_id"]] = estimate_task(spec, audit, BlackBox(spec), seed=args.seed)
    write_answers(args.output, answers)


if __name__ == "__main__":
    main()
