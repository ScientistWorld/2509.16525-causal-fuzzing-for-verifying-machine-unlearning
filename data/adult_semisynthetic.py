"""Visible Adult-Income task family: semi-synthetic tasks on the real UCI Adult data.

The paper evaluates CAFÉ on the real Adult Income data with the causal graph
of Chiappa (2019). Real data carry no ground truth for causal influence, so
the scored tasks keep the real data where they can and model only what exact
ground truth requires:

* Real rows (``adult.data``, fetched by ``scripts/download.sh``) supply each
  root attribute's marginal (age, sex, race, native country; drawn
  independently, as the graph has no edges between them) and the exogenous
  noise of the count attributes (education years, weekly hours), as the real
  rows' standardized residuals.
* The structural mechanism of every downstream attribute (married,
  education, self-employment, professional/managerial occupation, weekly
  hours, and the >50K income label) is fitted on the real rows (here:
  logistic / linear regressions on a quadratic basis).
* Per task, the dependence of every downstream attribute on each prohibited
  attribute (sex, race, native country) is rescaled and shifted along each
  path (random sign, so mediated influences can partly cancel); a prohibited
  attribute can also have no causal path at all (an exact-zero control).

The audited model is a classifier trained on the generated rows without the
prohibited attributes (or, in failed unlearnings, still with sex); its output
is the predicted probability of income > 50K. The hidden test slice uses the
other half of UCI Adult, different mechanism models and its own seeds.
"""

from __future__ import annotations

import warnings
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "downloads" / "uci_adult" / "adult.data"

COLUMNS = [
    "age", "workclass", "fnlwgt", "education", "education_num", "marital_status", "occupation",
    "relationship", "race", "sex", "capital_gain", "capital_loss", "hours_per_week", "native_country", "income",
]
FEATURES = [
    "age",
    "sex",
    "race",
    "native_country",
    "married",
    "education_num",
    "self_employed",
    "professional_job",
    "hours_per_week",
]
ROOTS = ["age", "sex", "race", "native_country"]
PROHIBITED = ["sex", "race", "native_country"]
REFERENCE_VALUE = {"sex": 1.0, "race": 1.0, "native_country": 1.0}
BINARY_NODES = ["married", "self_employed", "professional_job"]
COUNT_NODES = {"education_num": (1.0, 16.0), "hours_per_week": (1.0, 99.0)}
PARENTS = {
    "married": ROOTS,
    "education_num": ROOTS + ["married"],
    "self_employed": ROOTS + ["married", "education_num"],
    "professional_job": ROOTS + ["married", "education_num"],
    "hours_per_week": ROOTS + ["married", "education_num", "self_employed", "professional_job"],
    "income": FEATURES,
}
DOWNSTREAM = ["married", "education_num", "self_employed", "professional_job", "hours_per_week", "income"]


def _sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -40.0, 40.0)))


def load_adult(path: Path = SOURCE) -> pd.DataFrame:
    """Real UCI Adult rows (missing values dropped), numerically encoded."""

    if not path.is_file():
        raise FileNotFoundError(f"{path} not found: run scripts/download.sh (UCI Adult) first")
    raw = pd.read_csv(path, header=None, names=COLUMNS, skipinitialspace=True, na_values="?", comment="|")
    raw = raw.dropna().reset_index(drop=True)
    text = lambda col: raw[col].astype(str).str.strip()  # noqa: E731
    return pd.DataFrame(
        {
            "age": raw["age"].astype(float),
            "sex": (text("sex") == "Male").astype(float),
            "race": (text("race") == "White").astype(float),
            "native_country": (text("native_country") == "United-States").astype(float),
            "married": text("marital_status").isin(["Married-civ-spouse", "Married-AF-spouse"]).astype(float),
            "education_num": raw["education_num"].astype(float),
            "self_employed": text("workclass").isin(["Self-emp-not-inc", "Self-emp-inc"]).astype(float),
            "professional_job": text("occupation").isin(["Exec-managerial", "Prof-specialty"]).astype(float),
            "hours_per_week": raw["hours_per_week"].astype(float),
            "income": text("income").str.rstrip(".").eq(">50K").astype(float),
        }
    )


class _QuadraticBasis:
    """Standardized parents plus all squares and pairwise products."""

    def __init__(self, x: np.ndarray):
        self.mean = x.mean(axis=0)
        self.std = x.std(axis=0) + 1e-9

    def __call__(self, x: np.ndarray) -> np.ndarray:
        z = (x - self.mean) / self.std
        d = z.shape[1]
        cols = [z] + [z[:, i : i + 1] * z[:, i:] for i in range(d)]
        return np.hstack(cols)


class _Mechanisms:
    def __init__(self, real: pd.DataFrame):
        from sklearn.linear_model import LinearRegression, LogisticRegression

        self.real = real
        self.models = {}
        self.mean_scale = {}
        self.residuals = {}
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            for node in DOWNSTREAM:
                x = real[PARENTS[node]].to_numpy(dtype=float)
                y = real[node].to_numpy(dtype=float)
                basis = _QuadraticBasis(x)
                if node in COUNT_NODES:
                    model = LinearRegression().fit(basis(x), y)
                    resid = y - model.predict(basis(x))
                    sigma = float(np.std(resid))
                    self.mean_scale[node] = sigma
                    self.residuals[node] = resid / sigma
                else:
                    model = LogisticRegression(C=1.0, max_iter=3000).fit(basis(x), y.astype(int))
                self.models[node] = (basis, model)

    def raw(self, node, x):
        basis, model = self.models[node]
        if node in COUNT_NODES:
            return model.predict(basis(x))
        return model.decision_function(basis(x))


_MECHANISMS: _Mechanisms | None = None


def mechanisms() -> _Mechanisms:
    global _MECHANISMS
    if _MECHANISMS is None:
        _MECHANISMS = _Mechanisms(load_adult())
    return _MECHANISMS


def _reference(x: np.ndarray, parents: list[str]) -> np.ndarray:
    out = np.array(x, dtype=float, copy=True)
    for b in PROHIBITED:
        if b in parents:
            out[:, parents.index(b)] = REFERENCE_VALUE[b]
    return out


class AdultIncomeSCM:
    """Public Adult-Income family (see the module docstring)."""

    name = "adult_income"
    task_kind = "classification"
    features = list(FEATURES)
    binary_features = ["sex", "race", "native_country", "married", "self_employed", "professional_job"]
    outcome = "income"
    edges = [(p, node) for node in DOWNSTREAM for p in PARENTS[node]]
    target = "sex"
    subgroups: dict = {}
    subgroup_features: list = []

    def __init__(self, params):
        self.params = dict(params)

    @property
    def unlearned(self):
        return list(PROHIBITED)

    @staticmethod
    def canonical_params(control_active: bool = True):
        """Paper-style instance: the fitted real dependencies, unshifted."""

        return {
            "k": {b: 1.0 for b in PROHIBITED},
            "a": {b: {v: 0.0 for v in DOWNSTREAM} for b in PROHIBITED},
            "shift": {v: 0.0 for v in DOWNSTREAM},
        }

    @staticmethod
    def draw_params(rng, control_active):
        active = {"sex": True, "race": bool(control_active), "native_country": bool(rng.uniform() < 0.67)}
        k, a = {}, {}
        for b in PROHIBITED:
            if active[b]:
                k[b] = float(rng.uniform(0.5, 1.5) if b == "sex" else rng.uniform(0.3, 2.5))
                spread = float(rng.uniform(0.0, 0.6) if b == "sex" else rng.uniform(0.0, 1.0))
                a[b] = {v: float(rng.normal(0.0, spread)) for v in DOWNSTREAM}
            else:
                k[b] = 0.0
                a[b] = {v: 0.0 for v in DOWNSTREAM}
        shift = {v: float(rng.uniform(-0.35, 0.35)) for v in DOWNSTREAM}
        return {"k": k, "a": a, "shift": shift}

    @staticmethod
    def draw_noise(rng, n):
        mech = mechanisms()
        real = mech.real
        m = len(real)
        source = rng.integers(m, size=n)
        noise = {
            "age": real["age"].to_numpy(dtype=float)[source],
            "sex": real["sex"].to_numpy(dtype=float)[rng.integers(m, size=n)],
            "race": real["race"].to_numpy(dtype=float)[rng.integers(m, size=n)],
            "native_country": real["native_country"].to_numpy(dtype=float)[rng.integers(m, size=n)],
        }
        for node in COUNT_NODES:
            noise["e_" + node] = mech.residuals[node][source]
        for node in BINARY_NODES + ["income"]:
            noise["u_" + node] = rng.uniform(size=n)
        return noise

    def _structural(self, node, values) -> np.ndarray:
        mech = mechanisms()
        parents = PARENTS[node]
        x = np.column_stack([values[p] for p in parents]).astype(float)
        ref = _reference(x, parents)
        base = mech.raw(node, ref)
        unit = mech.mean_scale.get(node, 1.0)
        out = base + self.params["shift"][node] * unit
        for b in PROHIBITED:
            j = parents.index(b)
            k, a = self.params["k"][b], self.params["a"][b][node]
            if k == 0.0 and a == 0.0:
                continue
            with_b = ref.copy()
            with_b[:, j] = x[:, j]
            out = out + k * (mech.raw(node, with_b) - base) + a * unit * (x[:, j] - REFERENCE_VALUE[b])
        return out

    def features_frame(self, noise, do=None):
        do = do or {}
        n = len(noise["age"])
        mech = mechanisms()
        values = {}
        for node in FEATURES:
            if node in do:
                values[node] = np.full(n, float(do[node]))
            elif node in ROOTS:
                values[node] = np.asarray(noise[node], dtype=float)
            elif node in COUNT_NODES:
                level = self._structural(node, values) + mech.mean_scale[node] * noise["e_" + node]
                lo, hi = COUNT_NODES[node]
                values[node] = np.clip(np.rint(level), lo, hi)
            else:
                values[node] = (noise["u_" + node] < _sigmoid(self._structural(node, values))).astype(float)
        return pd.DataFrame({f: values[f] for f in FEATURES})

    def outcome_values(self, frame, noise):
        values = {f: frame[f].to_numpy(dtype=float) for f in FEATURES}
        return (noise["u_income"] < _sigmoid(self._structural("income", values))).astype(float)
