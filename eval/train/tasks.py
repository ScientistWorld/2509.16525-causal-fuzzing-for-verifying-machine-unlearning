"""Visible train tasks built from the public families in data/synthetic_causal.py.

Task 00 of each family is the paper-style canonical instance (original fixed
coefficients, random-forest audited model, target removed, control without a
residual path). The others draw coefficients, audited-model architecture,
control activity and whether the target's direct input was actually removed.
The hidden test slice uses the same graphs and protocol but different
structural forms and seeds.
"""

from __future__ import annotations

from data.synthetic_causal import HeartDiseaseSCM, PerformanceSCM
from eval.train.harness import build_task

ARCHITECTURES = ("random_forest", "mlp", "gradient_boosting", "linear")
N_TOTAL, N_AUDIT = 10_000, 3_500
TASKS_PER_FAMILY = 6


def _plan(smoke: bool):
    families = ((HeartDiseaseSCM, 1_000, 0), (PerformanceSCM, 2_000, 1))
    plan = []
    for family, seed_base, offset in families:
        count = 1 if smoke else TASKS_PER_FAMILY
        for i in range(count):
            canonical = i == 0
            plan.append(
                {
                    "task_id": f"{family.name}_{i:02d}",
                    "family": family,
                    "seed": seed_base + 17 * i,
                    "architecture": "random_forest" if canonical else ARCHITECTURES[(i + offset) % 4],
                    "control_active": False if canonical else (i % 2 == 1),
                    "target_retained": False if canonical else (i % 3 == 2),
                    "params": family.canonical_params(False) if canonical else None,
                }
            )
    return plan


def build_tasks(smoke: bool = False, log=None) -> dict:
    n_total, n_audit = (2_000, 700) if smoke else (N_TOTAL, N_AUDIT)
    tasks = {}
    for item in _plan(smoke):
        tasks[item["task_id"]] = build_task(
            item["task_id"],
            item["family"],
            item["seed"],
            item["architecture"],
            item["control_active"],
            item["target_retained"],
            n_total=n_total,
            n_audit=n_audit,
            params=item["params"],
        )
        if log is not None:
            log(f"built {item['task_id']} ({item['architecture']})")
    return tasks
