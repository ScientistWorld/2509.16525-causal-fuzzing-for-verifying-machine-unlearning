"""Visible train tasks built from the public families in data/synthetic_causal.py.

Task 00 of each family is the paper-style canonical instance (original fixed
coefficients, random-forest audited model, target removed, control without a
residual path). The others draw coefficients, audited-model architecture,
control activity and whether the target's direct input was actually removed;
in a third of the Heart-Disease tasks the age modulation of BMI's mediated
influence is mirrored (amplified at age <= 50 instead of above 50). The
hidden test slice uses the same graphs, protocol and task count but different
structural forms and seeds.

The Adult-Income tasks (data/adult_semisynthetic.py) are semi-synthetic on the
real UCI Adult training file; task 00 is the paper-style instance (the fitted
real dependencies, sex removed from the audited classifier). The hidden slice
uses the other UCI Adult file and different mechanism models.
"""

from __future__ import annotations

from data.adult_semisynthetic import AdultIncomeSCM
from data.synthetic_causal import HeartDiseaseSCM, HeartDiseaseYoungAmplifiedSCM, PerformanceSCM
from eval.train.harness import build_task

ARCHITECTURES = ("random_forest", "mlp", "gradient_boosting", "linear")
N_TOTAL, N_AUDIT = 10_000, 3_500
TASKS_PER_FAMILY = 12
ADULT_TASKS, ADULT_TOTAL = 24, 15_000


def _plan(smoke: bool):
    families = ((HeartDiseaseSCM, 1_000, 0), (PerformanceSCM, 2_000, 1))
    plan = []
    for family, seed_base, offset in families:
        count = 1 if smoke else TASKS_PER_FAMILY
        for i in range(count):
            canonical = i == 0
            scm_cls = family
            if family is HeartDiseaseSCM and not canonical and i % 3 == 1:
                scm_cls = HeartDiseaseYoungAmplifiedSCM
            plan.append(
                {
                    "task_id": f"{family.name}_{i:02d}",
                    "family": scm_cls,
                    "seed": seed_base + 17 * i,
                    "architecture": "random_forest" if canonical else ARCHITECTURES[(i + offset) % 4],
                    "control_active": False if canonical else (i % 2 == 1),
                    "target_retained": False if canonical else (i % 3 == 2),
                    "params": family.canonical_params(False) if canonical else None,
                }
            )
    for i in range(1 if smoke else ADULT_TASKS):
        canonical = i == 0
        plan.append(
            {
                "task_id": f"adult_income_{i:02d}",
                "family": AdultIncomeSCM,
                "seed": 3_000 + 23 * i,
                "architecture": "random_forest" if canonical else ARCHITECTURES[(i + 1) % 4],
                "control_active": True if canonical else (i // 4 + i) % 2 == 1,
                "target_retained": False if canonical else i % 3 == 1,
                "params": AdultIncomeSCM.canonical_params() if canonical else None,
                "n_total": ADULT_TOTAL,
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
            n_total=item.get("n_total", n_total) if not smoke else n_total,
            n_audit=n_audit,
            params=item["params"],
        )
        if log is not None:
            log(f"built {item['task_id']} ({item['architecture']})")
    return tasks
