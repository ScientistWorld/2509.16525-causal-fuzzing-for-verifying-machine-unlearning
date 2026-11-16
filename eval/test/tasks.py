"""Hidden test tasks: held-out structural causal models over the public graphs.

The graphs, variable meanings, unlearning targets, controls and subgroups match
the visible families, but the structural equations use different functional
forms and noise, and every instance is drawn from seeds that exist only here.
In a third of the Heart-Disease instances the age modulation of BMI's mediated
influence is mirrored (amplified below age 50), so the sign of the subgroup gap
must be measured, not assumed. The Adult-Income instances (eval/test/adult.py)
are semi-synthetic on the held-out half of the real UCI Adult data.
Self-contained: imports nothing from data/, method/ or eval/train/.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from eval.test.adult import HeldOutAdult
from eval.test.harness import build_task


def _sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def _z(values):
    values = np.asarray(values, dtype=float)
    return (values - values.mean()) / (values.std() + 1e-8)


def _softplus(x):
    return np.logaddexp(0.0, x)


class _Family:
    subgroups: dict = {}
    subgroup_features: list = []

    def __init__(self, params):
        self.params = dict(params)

    @property
    def unlearned(self):
        return [self.target, self.control]

    @staticmethod
    def _value(n, name, do, compute):
        if name in do:
            return np.full(n, float(do[name]))
        return compute()


class HeldOutHeart(_Family):
    name = "heart_disease"
    features = ["age", "smoking", "exercise", "bmi", "blood_pressure", "family_history"]
    binary_features = ["smoking", "family_history"]
    outcome = "risk"
    edges = [
        ("age", "smoking"),
        ("age", "exercise"),
        ("age", "bmi"),
        ("age", "blood_pressure"),
        ("smoking", "exercise"),
        ("smoking", "bmi"),
        ("smoking", "blood_pressure"),
        ("exercise", "bmi"),
        ("exercise", "blood_pressure"),
        ("bmi", "blood_pressure"),
        ("family_history", "blood_pressure"),
        ("age", "risk"),
        ("smoking", "risk"),
        ("exercise", "risk"),
        ("bmi", "risk"),
        ("blood_pressure", "risk"),
        ("family_history", "risk"),
    ]
    target = "smoking"
    control = "family_history"
    subgroups = {
        "older": {"feature": "age", "op": ">", "threshold": 50.0},
        "younger": {"feature": "age", "op": "<=", "threshold": 50.0},
    }
    subgroup_features = ["bmi", "blood_pressure"]
    # +1: mediation via blood pressure amplified above age 50; -1: below it.
    amplified_direction = 1.0

    @classmethod
    def draw_params(cls, rng, control_active):
        u = rng.uniform
        return {
            "sg_dir": float(cls.amplified_direction),
            "fh_rate": u(0.2, 0.4),
            "s0": u(-0.9, 0.1),
            "s_age": u(-0.6, 0.6),
            "e_s": u(-1.7, -0.6),
            "e_a": u(-0.015, 0.0),
            "b_a": u(0.0, 0.06),
            "b_s": u(3.0, 7.0),
            "b_e": u(-1.1, -0.4),
            "b_q": u(0.0, 0.12),
            "p_a": u(0.08, 0.25),
            "p_b": u(0.3, 1.1),
            "p_ab": u(0.04, 0.25),
            "p_s": u(5.0, 13.0),
            "p_e": u(-2.4, -0.9),
            "p_f": u(8.0, 15.0) if control_active else 0.0,
            "c_age": u(0.0, 0.2),
            "c_bmi": u(0.6, 1.4),
            "c_bp": u(0.6, 1.3),
            "c_old": u(0.3, 1.3),
            "c_ex": u(0.25, 0.8),
            "c_sm": u(0.0, 0.35),
            "c_fh": u(0.2, 0.6),
            "c_int": u(-0.25, 0.25),
            "c_bmi_old": u(-0.6, 0.6),
            "out_scale": float(np.exp(u(np.log(0.25), np.log(5.0)))),
        }

    @staticmethod
    def draw_noise(rng, n):
        return {
            "age": rng.normal(size=n),
            "family_history": rng.uniform(size=n),
            "smoking": rng.uniform(size=n),
            "exercise": rng.standard_t(5, size=n) * np.sqrt(3.0 / 5.0),
            "bmi": rng.normal(size=n),
            "blood_pressure": rng.normal(size=n),
            "risk": rng.normal(size=n),
        }

    def features_frame(self, noise, do=None):
        do = do or {}
        p = self.params
        n = len(noise["age"])
        v = self._value
        age = v(n, "age", do, lambda: np.clip(53.0 + 13.0 * noise["age"], 20.0, 88.0))
        fh = v(n, "family_history", do, lambda: (noise["family_history"] < p["fh_rate"]).astype(float))
        smoking = v(
            n,
            "smoking",
            do,
            lambda: (noise["smoking"] < _sigmoid(p["s0"] + p["s_age"] * (age - 53.0) / 13.0)).astype(float),
        )
        exercise = v(
            n,
            "exercise",
            do,
            lambda: np.clip(
                5.0
                + p["e_s"] * smoking
                + p["e_a"] * (age - 50.0)
                + 0.35 * np.sin((age - 20.0) / 8.0)
                + 1.3 * noise["exercise"],
                0.0,
                9.0,
            ),
        )
        bmi = v(
            n,
            "bmi",
            do,
            lambda: 23.5
            + p["b_a"] * (age - 50.0)
            + p["b_s"] * smoking
            + p["b_e"] * exercise
            + p["b_q"] * (exercise - 5.0) ** 2
            + 1.2 * (1.0 + 0.15 * smoking) * noise["bmi"],
        )
        direction = p["sg_dir"]
        bp = v(
            n,
            "blood_pressure",
            do,
            lambda: 135.0
            + p["p_a"] * age
            + (p["p_b"] + p["p_ab"] * 5.0 * _softplus(direction * (age - 50.0) / 5.0)) * (bmi - 23.5)
            + p["p_s"] * smoking
            + p["p_e"] * exercise
            + p["p_f"] * fh
            + 4.5 * noise["blood_pressure"],
        )
        return pd.DataFrame(
            {
                "age": age,
                "smoking": smoking,
                "exercise": exercise,
                "bmi": bmi,
                "blood_pressure": bp,
                "family_history": fh,
            }
        )

    def outcome_values(self, frame, noise):
        p = self.params
        age = frame["age"].to_numpy()
        bp = frame["blood_pressure"].to_numpy()
        return p["out_scale"] * (
            p["c_age"] * _z(age)
            + p["c_bmi"] * _z(frame["bmi"])
            + p["c_bmi_old"] * _sigmoid((age - 50.0) / 3.0) * _z(frame["bmi"])
            + p["c_bp"] * _z(bp)
            + p["c_old"] * _sigmoid(p["sg_dir"] * (age - 50.0) / 3.0) * _z(bp)
            - p["c_ex"] * _z(frame["exercise"])
            + p["c_sm"] * frame["smoking"].to_numpy()
            + p["c_fh"] * frame["family_history"].to_numpy()
            + p["c_int"] * np.tanh(_z(frame["bmi"])) * _z(bp)
            + 0.25 * noise["risk"]
        )


class HeldOutHeartYoungAmplified(HeldOutHeart):
    """Mirrored age modulation: mediation via blood pressure amplified at younger ages."""

    amplified_direction = -1.0


class HeldOutPerformance(_Family):
    name = "performance"
    features = ["gender", "education_years", "experience_years", "income", "region"]
    binary_features = ["gender", "region"]
    outcome = "score"
    edges = [
        ("gender", "education_years"),
        ("gender", "experience_years"),
        ("gender", "income"),
        ("education_years", "experience_years"),
        ("education_years", "income"),
        ("experience_years", "income"),
        ("region", "income"),
        ("gender", "score"),
        ("education_years", "score"),
        ("experience_years", "score"),
        ("income", "score"),
        ("region", "score"),
    ]
    target = "gender"
    control = "region"

    @staticmethod
    def draw_params(rng, control_active):
        u = rng.uniform
        return {
            "g_rate": u(0.38, 0.56),
            "r_rate": u(0.3, 0.7),
            "ed_g": u(0.9, 2.5),
            "ex_e": u(0.7, 1.5),
            "ex_g": u(0.4, 2.0),
            "ex_q": u(0.0, 0.06),
            "in_e": u(1400.0, 3000.0),
            "in_x": u(700.0, 1800.0),
            "in_xx": u(0.0, 25.0),
            "in_g": u(1500.0, 4800.0),
            "in_r": u(3000.0, 7500.0) if control_active else 0.0,
            "c_e": u(0.9, 1.8),
            "c_x": u(0.4, 1.1),
            "c_i": u(0.6, 1.3),
            "c_g": u(0.0, 0.12),
            "c_r": u(0.2, 0.5),
            "out_scale": float(np.exp(u(np.log(0.25), np.log(5.0)))),
        }

    @staticmethod
    def draw_noise(rng, n):
        return {
            "gender": rng.uniform(size=n),
            "region": rng.uniform(size=n),
            "education_years": rng.normal(size=n),
            "experience_years": rng.normal(size=n),
            "income": rng.normal(size=n),
            "score": rng.normal(size=n),
        }

    def features_frame(self, noise, do=None):
        do = do or {}
        p = self.params
        n = len(noise["gender"])
        v = self._value
        gender = v(n, "gender", do, lambda: (noise["gender"] < p["g_rate"]).astype(float))
        region = v(n, "region", do, lambda: (noise["region"] < p["r_rate"]).astype(float))
        education = v(
            n,
            "education_years",
            do,
            lambda: np.clip(10.5 + p["ed_g"] * gender + 1.5 * noise["education_years"], 6.0, 20.0),
        )
        experience = v(
            n,
            "experience_years",
            do,
            lambda: np.clip(
                1.0
                + p["ex_e"] * education
                + p["ex_g"] * gender
                + p["ex_q"] * (education - 12.0) ** 2
                + 2.2 * noise["experience_years"],
                0.0,
                35.0,
            ),
        )
        income = v(
            n,
            "income",
            do,
            lambda: 15_000.0
            + p["in_e"] * education
            + p["in_x"] * experience
            + p["in_xx"] * experience**2
            + p["in_g"] * gender
            + p["in_r"] * region
            + 4_500.0 * (1.0 + 0.02 * experience) * noise["income"],
        )
        return pd.DataFrame(
            {
                "gender": gender,
                "education_years": education,
                "experience_years": experience,
                "income": income,
                "region": region,
            }
        )

    def outcome_values(self, frame, noise):
        p = self.params
        return p["out_scale"] * (
            p["c_e"] * _z(frame["education_years"])
            + p["c_x"] * _z(np.sqrt(frame["experience_years"].to_numpy() + 1.0))
            + p["c_i"] * _z(np.log(np.maximum(frame["income"].to_numpy(), 2_000.0)))
            + p["c_g"] * frame["gender"].to_numpy()
            + p["c_r"] * frame["region"].to_numpy()
            + 0.3 * noise["score"]
        )


ARCHITECTURES = ("random_forest", "mlp", "gradient_boosting", "linear")
N_TOTAL, N_AUDIT = 10_000, 3_500
TASKS_PER_FAMILY = 12
ADULT_TASKS, ADULT_TOTAL = 16, 15_000


def _plan(smoke: bool):
    if smoke:
        return [
            ("heart_disease_00", HeldOutHeart, 91_730_011, "random_forest", True, False),
            ("performance_00", HeldOutPerformance, 44_200_173, "linear", False, True),
            ("adult_income_00", HeldOutAdult, 63_018_427, "mlp", True, False),
        ]
    plan = []
    for i in range(TASKS_PER_FAMILY):
        plan.append(
            (
                f"heart_disease_{i:02d}",
                HeldOutHeartYoungAmplified if i % 3 == 2 else HeldOutHeart,
                91_730_011 + 7_919 * i,
                ARCHITECTURES[i % 4],
                (i % 4) in (1, 2),
                i % 3 == 1,
            )
        )
    for i in range(TASKS_PER_FAMILY):
        plan.append(
            (
                f"performance_{i:02d}",
                HeldOutPerformance,
                44_200_173 + 6_271 * i,
                ARCHITECTURES[(i + 1) % 4],
                (i % 4) in (0, 3),
                i % 3 == 2,
            )
        )
    for i in range(ADULT_TASKS):
        plan.append(
            (
                f"adult_income_{i:02d}",
                HeldOutAdult,
                63_018_427 + 5_903 * i,
                ARCHITECTURES[i % 4],
                (i // 4 + i) % 2 == 0,
                i % 3 == 2,
            )
        )
    return plan


def build_tasks(smoke: bool = False, log=None) -> dict:
    n_total, n_audit = (2_000, 700) if smoke else (N_TOTAL, N_AUDIT)
    tasks = {}
    for task_id, family, seed, architecture, control_active, target_retained in _plan(smoke):
        adult = family is HeldOutAdult
        tasks[task_id] = build_task(
            task_id,
            family,
            seed,
            architecture,
            control_active,
            target_retained,
            n_total=(ADULT_TOTAL if not smoke else 3_000) if adult else n_total,
            n_audit=n_audit if not adult or smoke else N_AUDIT,
        )
        if log is not None:
            log(f"built {task_id} ({architecture})")
    return tasks
