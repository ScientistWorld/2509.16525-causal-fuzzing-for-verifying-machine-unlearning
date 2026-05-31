"""Semi-synthetic tabular datasets with known causal DAGs.

These generators define fixed residual-influence verification tasks: an
upstream target feature has little or no direct access in the audited model,
but affects model predictions through downstream mediators.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class CausalDataset:
    name: str
    features: list[str]
    outcome: str
    edges: list[tuple[str, str]]
    target_feature: str
    expected_top_feature: str
    expected_low_direct_feature: str
    train_without: list[str]
    frame: pd.DataFrame


def _standardize(values: np.ndarray) -> np.ndarray:
    values = np.asarray(values, dtype=float)
    return (values - values.mean()) / (values.std() + 1e-8)


def make_heart_disease(n: int = 10_000, seed: int = 7) -> CausalDataset:
    rng = np.random.default_rng(seed)
    age = rng.normal(52.0, 12.0, n).clip(20, 85)
    smoking = rng.binomial(1, 0.42, n)
    exercise = (rng.normal(4.8, 1.4, n) - 1.15 * smoking - 0.004 * (age - 50)).clip(0, 9)
    bmi = 24.0 + 0.025 * (age - 50) + 6.4 * smoking - 0.75 * exercise + rng.normal(0, 1.2, n)
    age_over_50 = np.maximum(age - 50, 0)
    blood_pressure = (
        104.0
        + 0.16 * age
        + (1.65 + 0.10 * age_over_50) * bmi
        + 12.0 * smoking
        - 1.6 * exercise
        + rng.normal(0, 4.5, n)
    )
    older_bp_burden = (age > 50).astype(float) * blood_pressure
    risk = (
        0.06 * _standardize(age)
        + 1.15 * _standardize(bmi)
        + 0.95 * _standardize(blood_pressure)
        + 1.35 * _standardize(older_bp_burden)
        - 0.55 * _standardize(exercise)
        + 0.12 * smoking
        + rng.normal(0, 0.22, n)
    )
    frame = pd.DataFrame(
        {
            "age": age,
            "smoking": smoking.astype(float),
            "exercise": exercise,
            "bmi": bmi,
            "blood_pressure": blood_pressure,
            "risk": risk,
        }
    )
    return CausalDataset(
        name="heart_disease",
        features=["age", "smoking", "exercise", "bmi", "blood_pressure"],
        outcome="risk",
        edges=[
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
            ("age", "risk"),
            ("smoking", "risk"),
            ("exercise", "risk"),
            ("bmi", "risk"),
            ("blood_pressure", "risk"),
        ],
        target_feature="smoking",
        expected_top_feature="smoking",
        expected_low_direct_feature="smoking",
        train_without=["smoking"],
        frame=frame,
    )


def make_performance(n: int = 10_000, seed: int = 11) -> CausalDataset:
    rng = np.random.default_rng(seed)
    gender = rng.binomial(1, 0.48, n)
    education_years = (11.0 + 1.9 * gender + rng.normal(0, 1.4, n)).clip(6, 20)
    experience_years = (
        2.0 + 1.25 * education_years + 1.3 * gender + rng.normal(0, 2.0, n)
    ).clip(0, 35)
    income = (
        18_000
        + 2_200 * education_years
        + 1_450 * experience_years
        + 3_200 * gender
        + rng.normal(0, 5_000, n)
    )
    score = (
        1.45 * _standardize(education_years)
        + 0.82 * _standardize(experience_years)
        + 0.92 * _standardize(income)
        + 0.03 * gender
        + rng.normal(0, 0.25, n)
    )
    frame = pd.DataFrame(
        {
            "gender": gender.astype(float),
            "education_years": education_years,
            "experience_years": experience_years,
            "income": income,
            "score": score,
        }
    )
    return CausalDataset(
        name="performance",
        features=["gender", "education_years", "experience_years", "income"],
        outcome="score",
        edges=[
            ("gender", "education_years"),
            ("gender", "experience_years"),
            ("education_years", "experience_years"),
            ("education_years", "income"),
            ("experience_years", "income"),
            ("gender", "score"),
            ("education_years", "score"),
            ("experience_years", "score"),
            ("income", "score"),
        ],
        target_feature="gender",
        expected_top_feature="gender",
        expected_low_direct_feature="gender",
        train_without=["gender"],
        frame=frame,
    )


def load_dataset(name: str, n: int = 10_000, seed: int = 7) -> CausalDataset:
    if name == "heart_disease":
        return make_heart_disease(n=n, seed=seed)
    if name == "performance":
        return make_performance(n=n, seed=seed)
    raise ValueError(f"Unknown dataset: {name}")
