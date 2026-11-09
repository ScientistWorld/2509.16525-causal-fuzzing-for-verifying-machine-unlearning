"""Honest exhaustive intervention baseline over every row and feature value.

Uses only scientist-visible method/data modules. All low/high values of each
feature are enumerated on all held-out rows; descendants are propagated through
the learned structural models. This trades model queries for computation.
"""

from pathlib import Path
import json
import time

import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

from data.synthetic_causal import load_dataset
from method.cafe import (_fit_structural_models, _parents, _descendants,
                         _topological_order, _intervention_values,
                         causal_fuzzing_effect)


def enumerate_effects(frame, dataset, model, model_features, structural):
    effects = {}
    queries = 0
    for feature in dataset.features:
        lo, hi = _intervention_values(frame[feature])
        direct_predictions = []
        total_predictions = []
        descendants = _descendants(dataset.edges, feature)
        for value in (lo, hi):
            direct_rows = frame.copy()
            direct_rows[feature] = value
            direct_predictions.append(model.predict(direct_rows[model_features]))
            queries += len(frame)
            total_rows = direct_rows.copy()
            changed = {feature}
            for node in _topological_order(dataset.features, dataset.edges):
                if node not in descendants or node not in structural:
                    continue
                parents = [p for p in _parents(dataset.edges, node) if p in dataset.features]
                if changed.intersection(parents):
                    total_rows[node] = structural[node].predict(total_rows[parents])
                    changed.add(node)
            total_predictions.append(model.predict(total_rows[model_features]))
            queries += len(frame)
        direct = float(np.mean(np.abs(direct_predictions[1] - direct_predictions[0])))
        total = float(np.mean(np.abs(total_predictions[1] - total_predictions[0])))
        effects[feature] = {'total_effect': total, 'direct_effect': direct,
                            'indirect_effect': max(total - direct, 0.0)}
    return effects, queries


def main():
    output = Path('outputs/method')
    started = time.monotonic()
    for name in ('heart_disease', 'performance'):
        dataset = load_dataset(name, n=10000, seed=7)
        train, test = train_test_split(dataset.frame, test_size=0.35, random_state=7)
        model_features = [f for f in dataset.features if f not in dataset.train_without]
        model = RandomForestRegressor(n_estimators=160, min_samples_leaf=12, random_state=7, n_jobs=1)
        model.fit(train[model_features], train[dataset.outcome])
        structural = _fit_structural_models(test, dataset.features, dataset.edges)
        effects, queries = enumerate_effects(test, dataset, model, model_features, structural)
        # Independent original random-intervention oracle, fully accounted.
        fuzzing = causal_fuzzing_effect(test, model, model_features, dataset.features,
                                        dataset.edges, dataset.target_feature, seed=7)
        payload = {'dataset': name, 'method': 'cafe', 'target_feature': dataset.target_feature,
                   'features': dataset.features, 'effects': effects,
                   'causal_fuzzing': fuzzing, 'cafe_model_query_count': queries,
                   'fuzzing_model_query_count': fuzzing['model_query_count'],
                   'prediction_r2': float(model.score(test[model_features], test[dataset.outcome]))}
        if name == 'heart_disease':
            subgroup = {'feature': 'bmi', 'split': 'age > 50 vs age <= 50'}
            for label, frame in [('age_le_50', test[test.age <= 50]), ('age_gt_50', test[test.age > 50])]:
                local_structural = _fit_structural_models(frame, dataset.features, dataset.edges)
                local, local_queries = enumerate_effects(frame, dataset, model, model_features, local_structural)
                subgroup[label] = local['bmi']
                payload['cafe_model_query_count'] += local_queries
            subgroup['direct_gap_abs'] = abs(subgroup['age_gt_50']['direct_effect'] - subgroup['age_le_50']['direct_effect'])
            for kind in ('total', 'indirect'):
                subgroup[f'{kind}_gap'] = subgroup['age_gt_50'][f'{kind}_effect'] - subgroup['age_le_50'][f'{kind}_effect']
            payload['subgroup_unlearning'] = subgroup
        (output / f'{name}_cafe.json').write_text(json.dumps(payload, indent=2, sort_keys=True))
    print(json.dumps({'enumeration_seconds': time.monotonic() - started}))


if __name__ == '__main__':
    main()
