"""Hidden Adult-Income task family: semi-synthetic tasks on the real UCI Adult data.

Real-data part. The held-out half of UCI Adult (``adult.test``, fetched by
``scripts/download.sh``) supplies every root attribute (age, sex, race,
native country; each drawn from its real marginal, the roots independent of
one another as the causal graph states) and the exogenous noise of the
count-valued attributes (education years, weekly hours: the real rows'
standardized residuals, so their heaping and skew are the real ones). The
structural mechanism of every downstream attribute is fitted on the same real
rows here, with gradient boosting (logistic for binary attributes,
heteroscedastic location-scale for counts). The causal graph is the one the
paper takes for Adult from Chiappa (2019): age, sex, race and native country
-> marital status -> education -> work class and occupation -> hours -> income.

Semi-synthetic part (needed for exact ground truth). Per task, the evaluator
rescales the fitted dependence of every downstream attribute on each
prohibited attribute (sex, race, native country), adds hidden path shifts of
random sign (mediated influences can partly cancel), and in some tasks
switches a prohibited attribute's paths off entirely (an exact-zero control).
Income labels are drawn from the fitted outcome mechanism, the audited
classifier is trained without the prohibited attributes (or, in failed
unlearnings, still with sex), and the ground truth is read off that
classifier on counterfactual rows propagated with each row's own noise.

Self-contained: imports nothing from data/, method/ or eval/train/.
"""

from __future__ import annotations

import warnings
from pathlib import Path

import numpy as np
import pandas as pd

WORKSPACE = Path(__file__).resolve().parents[2]
SOURCE = WORKSPACE / "data" / "downloads" / "uci_adult" / "adult.test"

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
REFERENCE_VALUE = {"sex": 1.0, "race": 1.0, "native_country": 1.0}  # majority category
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


def load_real_rows(path: Path = SOURCE) -> pd.DataFrame:
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


class _Mechanisms:
    """Structural mechanisms fitted on the real rows (fixed for the whole slice)."""

    def __init__(self, real: pd.DataFrame, seed: int = 20_517):
        from sklearn.ensemble import HistGradientBoostingClassifier, HistGradientBoostingRegressor

        self.real = real
        self.models = {}
        self.scale_models = {}
        self.mean_scale = {}
        self.residuals = {}
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            for node in DOWNSTREAM:
                parents = PARENTS[node]
                x = real[parents].to_numpy(dtype=float)
                y = real[node].to_numpy(dtype=float)
                if node in COUNT_NODES:
                    mean = HistGradientBoostingRegressor(
                        max_iter=200, learning_rate=0.06, max_leaf_nodes=15, min_samples_leaf=40, random_state=seed
                    ).fit(x, y)
                    resid = y - mean.predict(x)
                    spread = HistGradientBoostingRegressor(
                        max_iter=100, learning_rate=0.06, max_leaf_nodes=7, min_samples_leaf=150, random_state=seed + 1
                    ).fit(self._reference(x, parents), np.abs(resid))
                    self.models[node] = mean
                    self.scale_models[node] = (spread, 0.25 * float(np.std(resid)))
                    sigma = self.sigma(node, x, parents)
                    self.mean_scale[node] = float(np.mean(sigma))
                    self.residuals[node] = resid / sigma
                else:
                    self.models[node] = HistGradientBoostingClassifier(
                        max_iter=200, learning_rate=0.06, max_leaf_nodes=15, min_samples_leaf=40, random_state=seed
                    ).fit(x, y.astype(int))
                seed += 7

    @staticmethod
    def _reference(x: np.ndarray, parents: list[str]) -> np.ndarray:
        out = np.array(x, dtype=float, copy=True)
        for b in PROHIBITED:
            if b in parents:
                out[:, parents.index(b)] = REFERENCE_VALUE[b]
        return out

    def sigma(self, node, x, parents):
        spread, floor = self.scale_models[node]
        return np.maximum(spread.predict(self._reference(x, parents)) * np.sqrt(np.pi / 2.0), floor)

    def raw(self, node, x):
        model = self.models[node]
        if node in COUNT_NODES:
            return model.predict(x)
        return model.decision_function(x)


_MECHANISMS: _Mechanisms | None = None


def mechanisms() -> _Mechanisms:
    global _MECHANISMS
    if _MECHANISMS is None:
        _MECHANISMS = _Mechanisms(load_real_rows())
    return _MECHANISMS


class HeldOutAdult:
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
    def draw_params(rng, control_active):
        """Per-task path strengths of the prohibited attributes.

        ``k[b]`` rescales the fitted real dependence of every downstream
        attribute on ``b``; ``a[b][v]`` is an extra shift of random sign on
        the path b -> v (logit units for binary attributes, residual-scale
        units for counts), so mediated influences can partly cancel. sex (the
        unlearning target) always has its real paths. race (the control) has
        none unless ``control_active``, and then moderate or strong paths;
        native country has none (1/4), moderate (3/8) or strong (3/8) paths.
        "None" means k = a = 0: no causal path to the audited model at all.
        Moderate paths put the residual influence around the verification
        threshold.
        """

        def strength(mode):
            if mode == "target":
                return float(rng.uniform(0.5, 1.5)), float(rng.uniform(0.0, 0.4))
            if mode == "moderate":
                return float(rng.uniform(0.15, 0.6)), float(rng.uniform(0.0, 0.15))
            if mode == "strong":
                return float(rng.uniform(0.6, 2.0)), float(rng.uniform(0.0, 0.6))
            return 0.0, 0.0

        race_draw, country_draw = float(rng.uniform()), float(rng.uniform())
        modes = {
            "sex": "target",
            "race": ("moderate" if race_draw < 0.5 else "strong") if control_active else "none",
            "native_country": "none" if country_draw < 0.25 else ("moderate" if country_draw < 0.625 else "strong"),
        }
        k, a = {}, {}
        for b in PROHIBITED:
            k[b], spread = strength(modes[b])
            a[b] = {v: float(rng.normal(0.0, spread)) if spread > 0 else 0.0 for v in DOWNSTREAM}
        shift = {v: float(rng.uniform(-0.25, 0.25)) for v in DOWNSTREAM}
        return {"k": k, "a": a, "shift": shift, "modes": modes}

    @staticmethod
    def draw_noise(rng, n):
        mech = mechanisms()
        real = mech.real
        m = len(real)
        source = rng.integers(m, size=n)  # age and count residuals of one real person
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

    def _index(self, node, values) -> tuple[np.ndarray, list[str]]:
        parents = PARENTS[node]
        return np.column_stack([values[p] for p in parents]).astype(float), parents

    def _structural(self, node, values) -> np.ndarray:
        """Task mechanism of ``node`` (logit or conditional mean)."""

        mech = mechanisms()
        x, parents = self._index(node, values)
        ref = mech._reference(x, parents)
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
                x, parents = self._index(node, values)
                level = self._structural(node, values) + mech.sigma(node, x, parents) * noise["e_" + node]
                lo, hi = COUNT_NODES[node]
                values[node] = np.clip(np.rint(level), lo, hi)
            else:
                values[node] = (noise["u_" + node] < _sigmoid(self._structural(node, values))).astype(float)
        return pd.DataFrame({f: values[f] for f in FEATURES})

    def outcome_values(self, frame, noise):
        values = {f: frame[f].to_numpy(dtype=float) for f in FEATURES}
        return (noise["u_income"] < _sigmoid(self._structural("income", values))).astype(float)
