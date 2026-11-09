"""Public semi-synthetic structural causal models (the visible task families).

Two families follow the paper's semi-synthetic settings (Fig. 2):

* ``heart_disease``: age, smoking, exercise, bmi, blood_pressure -> risk, plus a
  ``family_history`` control. ``smoking`` is the paper's unlearning target: the
  audited model is trained without it, yet it still moves exercise, BMI and
  blood pressure, which the model does use. As in the paper's Fig. 7, BMI's
  mediated influence (via blood pressure) is much larger above age 50: the
  BMI -> blood-pressure slope and blood pressure's weight on risk both grow
  with age. In drawn instances BMI's direct weight may also differ by age
  (``c_bmi_old``), and every drawn instance has its own outcome scale
  (``out_scale``); the canonical instance has neither.
* ``performance``: gender, education_years, experience_years, income -> score,
  plus a ``region`` control. ``gender`` is the paper's unlearning target.

Each family is parameterised: ``draw_params`` samples coefficients for a task
instance, ``canonical_params`` reproduces the original fixed generator used by
the first reproduction. The control feature is always removed from the audited
model; depending on the draw it either reaches a model input through a mediator
(residual influence) or has no path to any model input at all (no residual
influence, although the graph still lists the edge).

``features(noise, do=...)`` evaluates the structural equations row by row from
exogenous noise, so the same noise with an intervention gives unit-level
counterfactuals. Only the visible (train) slice uses these exact equations; the
hidden test slice uses different functional forms over the same graphs.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def _sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-x))


def _standardize(values: np.ndarray) -> np.ndarray:
    values = np.asarray(values, dtype=float)
    return (values - values.mean()) / (values.std() + 1e-8)


class _SCM:
    name: str
    features: list[str]
    binary_features: list[str]
    outcome: str
    edges: list[tuple[str, str]]
    target: str
    control: str
    subgroups: dict = {}
    subgroup_features: list[str] = []

    def __init__(self, params: dict):
        self.params = dict(params)

    @property
    def unlearned(self) -> list[str]:
        return [self.target, self.control]

    @staticmethod
    def _value(n: int, name: str, do: dict, compute):
        if name in do:
            return np.full(n, float(do[name]))
        return compute()


class HeartDiseaseSCM(_SCM):
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

    @staticmethod
    def canonical_params(control_active: bool = False) -> dict:
        return {
            "fh_rate": 0.3,
            "s0": float(np.log(0.42 / 0.58)),
            "s_age": 0.0,
            "e_s": -1.15,
            "e_a": -0.004,
            "b_a": 0.025,
            "b_s": 6.4,
            "b_e": -0.75,
            "p_a": 0.16,
            "p_b": 0.7,
            "p_ab": 0.22,
            "p_s": 12.0,
            "p_e": -1.6,
            "p_f": 11.0 if control_active else 0.0,
            "c_age": 0.06,
            "c_bmi": 1.15,
            "c_bp": 0.95,
            "c_old": 0.8,
            "c_ex": 0.55,
            "c_sm": 0.12,
            "c_fh": 0.35,
            "c_bmi_old": 0.0,
            "out_scale": 1.0,
        }

    @staticmethod
    def draw_params(rng: np.random.Generator, control_active: bool) -> dict:
        u = rng.uniform
        return {
            "fh_rate": u(0.2, 0.4),
            "s0": u(-0.8, 0.2),
            "s_age": u(-0.5, 0.5),
            "e_s": u(-1.6, -0.7),
            "e_a": u(-0.012, 0.0),
            "b_a": u(0.0, 0.05),
            "b_s": u(3.5, 7.5),
            "b_e": u(-1.0, -0.4),
            "p_a": u(0.08, 0.25),
            "p_b": u(0.4, 1.0),
            "p_ab": u(0.05, 0.3),
            "p_s": u(6.0, 14.0),
            "p_e": u(-2.2, -1.0),
            "p_f": u(8.0, 14.0) if control_active else 0.0,
            "c_age": u(0.0, 0.15),
            "c_bmi": u(0.7, 1.4),
            "c_bp": u(0.6, 1.2),
            "c_old": u(0.3, 1.2),
            "c_ex": u(0.3, 0.8),
            "c_sm": u(0.0, 0.3),
            "c_fh": u(0.2, 0.5),
            "c_bmi_old": u(-0.5, 0.5),
            "out_scale": float(np.exp(u(np.log(0.3), np.log(4.0)))),
        }

    @staticmethod
    def draw_noise(rng: np.random.Generator, n: int) -> dict[str, np.ndarray]:
        return {
            "age": rng.normal(size=n),
            "family_history": rng.uniform(size=n),
            "smoking": rng.uniform(size=n),
            "exercise": rng.normal(size=n),
            "bmi": rng.normal(size=n),
            "blood_pressure": rng.normal(size=n),
            "risk": rng.normal(size=n),
        }

    def features_frame(self, noise: dict, do: dict | None = None) -> pd.DataFrame:
        do = do or {}
        p = self.params
        n = len(noise["age"])
        v = self._value
        age = v(n, "age", do, lambda: np.clip(52.0 + 12.0 * noise["age"], 20.0, 85.0))
        family_history = v(
            n, "family_history", do, lambda: (noise["family_history"] < p["fh_rate"]).astype(float)
        )
        smoking = v(
            n,
            "smoking",
            do,
            lambda: (noise["smoking"] < _sigmoid(p["s0"] + p["s_age"] * (age - 52.0) / 12.0)).astype(float),
        )
        exercise = v(
            n,
            "exercise",
            do,
            lambda: np.clip(
                4.8 + p["e_s"] * smoking + p["e_a"] * (age - 50.0) + 1.4 * noise["exercise"], 0.0, 9.0
            ),
        )
        bmi = v(
            n,
            "bmi",
            do,
            lambda: 24.0
            + p["b_a"] * (age - 50.0)
            + p["b_s"] * smoking
            + p["b_e"] * exercise
            + 1.2 * noise["bmi"],
        )
        blood_pressure = v(
            n,
            "blood_pressure",
            do,
            lambda: 140.0
            + p["p_a"] * age
            + (p["p_b"] + p["p_ab"] * np.maximum(age - 50.0, 0.0)) * (bmi - 24.0)
            + p["p_s"] * smoking
            + p["p_e"] * exercise
            + p["p_f"] * family_history
            + 4.5 * noise["blood_pressure"],
        )
        return pd.DataFrame(
            {
                "age": age,
                "smoking": smoking,
                "exercise": exercise,
                "bmi": bmi,
                "blood_pressure": blood_pressure,
                "family_history": family_history,
            }
        )

    def outcome_values(self, frame: pd.DataFrame, noise: dict) -> np.ndarray:
        p = self.params
        older = (frame["age"].to_numpy() > 50).astype(float)
        bp = _standardize(frame["blood_pressure"])
        bmi = _standardize(frame["bmi"])
        return p["out_scale"] * (
            p["c_age"] * _standardize(frame["age"])
            + p["c_bmi"] * bmi
            + p["c_bmi_old"] * older * bmi
            + p["c_bp"] * bp
            + p["c_old"] * older * bp
            - p["c_ex"] * _standardize(frame["exercise"])
            + p["c_sm"] * frame["smoking"].to_numpy()
            + p["c_fh"] * frame["family_history"].to_numpy()
            + 0.22 * noise["risk"]
        )


class PerformanceSCM(_SCM):
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
    def canonical_params(control_active: bool = False) -> dict:
        return {
            "g_rate": 0.48,
            "r_rate": 0.5,
            "ed_g": 1.9,
            "ex_e": 1.25,
            "ex_g": 1.3,
            "in_e": 2200.0,
            "in_x": 1450.0,
            "in_g": 3200.0,
            "in_r": 5000.0 if control_active else 0.0,
            "c_e": 1.45,
            "c_x": 0.82,
            "c_i": 0.92,
            "c_g": 0.03,
            "c_r": 0.3,
            "out_scale": 1.0,
        }

    @staticmethod
    def draw_params(rng: np.random.Generator, control_active: bool) -> dict:
        u = rng.uniform
        return {
            "g_rate": u(0.4, 0.55),
            "r_rate": u(0.35, 0.65),
            "ed_g": u(1.0, 2.6),
            "ex_e": u(0.8, 1.6),
            "ex_g": u(0.5, 2.0),
            "in_e": u(1500.0, 3000.0),
            "in_x": u(900.0, 2000.0),
            "in_g": u(1500.0, 4500.0),
            "in_r": u(3000.0, 7000.0) if control_active else 0.0,
            "c_e": u(1.0, 1.8),
            "c_x": u(0.5, 1.1),
            "c_i": u(0.6, 1.2),
            "c_g": u(0.0, 0.1),
            "c_r": u(0.2, 0.5),
            "out_scale": float(np.exp(u(np.log(0.3), np.log(4.0)))),
        }

    @staticmethod
    def draw_noise(rng: np.random.Generator, n: int) -> dict[str, np.ndarray]:
        return {
            "gender": rng.uniform(size=n),
            "region": rng.uniform(size=n),
            "education_years": rng.normal(size=n),
            "experience_years": rng.normal(size=n),
            "income": rng.normal(size=n),
            "score": rng.normal(size=n),
        }

    def features_frame(self, noise: dict, do: dict | None = None) -> pd.DataFrame:
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
            lambda: np.clip(11.0 + p["ed_g"] * gender + 1.4 * noise["education_years"], 6.0, 20.0),
        )
        experience = v(
            n,
            "experience_years",
            do,
            lambda: np.clip(
                2.0 + p["ex_e"] * education + p["ex_g"] * gender + 2.0 * noise["experience_years"],
                0.0,
                35.0,
            ),
        )
        income = v(
            n,
            "income",
            do,
            lambda: 18_000.0
            + p["in_e"] * education
            + p["in_x"] * experience
            + p["in_g"] * gender
            + p["in_r"] * region
            + 5_000.0 * noise["income"],
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

    def outcome_values(self, frame: pd.DataFrame, noise: dict) -> np.ndarray:
        p = self.params
        return p["out_scale"] * (
            p["c_e"] * _standardize(frame["education_years"])
            + p["c_x"] * _standardize(frame["experience_years"])
            + p["c_i"] * _standardize(frame["income"])
            + p["c_g"] * frame["gender"].to_numpy()
            + p["c_r"] * frame["region"].to_numpy()
            + 0.25 * noise["score"]
        )


FAMILIES = {cls.name: cls for cls in (HeartDiseaseSCM, PerformanceSCM)}


def sample_dataset(name: str, n: int = 10_000, seed: int = 7, control_active: bool = False):
    """Convenience: one observational sample (features + outcome) of a family."""

    cls = FAMILIES[name]
    rng = np.random.default_rng(seed)
    scm = cls(cls.canonical_params(control_active))
    noise = cls.draw_noise(rng, n)
    frame = scm.features_frame(noise)
    frame[cls.outcome] = scm.outcome_values(frame, noise)
    return scm, frame
