"""Prepare on-disk candidate submissions using the scientist-visible contract.

Cached artifacts are legitimate reference computations, reused when only the
submission/report changes. No candidate reads test scores or eval/test code.
"""

from __future__ import annotations

import argparse
import copy
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path('/home/user')
AUDIT = ROOT / 'redteam'
DATASETS = ('heart_disease', 'performance')


def read(path):
    return json.loads(Path(path).read_text())


def write(path, payload):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + '\n')


def reset_outputs():
    output = ROOT / 'outputs'
    if output.exists():
        shutil.rmtree(output)
    (output / 'method').mkdir(parents=True)
    (output / 'baseline').mkdir(parents=True)
    for path in (AUDIT / 'reference_original' / 'baseline').glob('*.json'):
        shutil.copy2(path, output / 'baseline' / path.name)


def reference_artifacts():
    source = AUDIT / 'reference_original' / 'method'
    if not source.exists():
        # A standalone shortcut run can rebuild its cache from visible code.
        subprocess.run([sys.executable, '-m', 'method.cafe', '--n', '10000',
                        '--seed', '7', '--output-dir', str(source)], check=True, cwd=ROOT)
    return {name: read(source / f'{name}_cafe.json') for name in DATASETS}


def refresh_fields(artifact):
    effects = artifact['effects']
    features = artifact['features']
    target = artifact['target_feature']
    ranking = sorted(features, key=lambda f: effects[f]['total_effect'], reverse=True)
    direct = sorted(features, key=lambda f: effects[f]['direct_effect'], reverse=True)
    artifact['ranking'] = ranking
    artifact['direct_ranking'] = direct
    artifact['target_total_rank'] = ranking.index(target) + 1
    artifact['target_direct_rank'] = direct.index(target) + 1
    for kind in ('total', 'direct', 'indirect'):
        artifact[f'target_{kind}_effect'] = effects[target][f'{kind}_effect']


def write_artifacts(artifacts):
    for name, payload in artifacts.items():
        write(ROOT / 'outputs' / 'method' / f'{name}_cafe.json', payload)


def constant_shortcut():
    # Target identities and expected answers are public generator metadata.
    # This shortcut does not fit a predictor or compute any causal effects.
    from data.synthetic_causal import load_dataset
    artifacts = {}
    for name in DATASETS:
        dataset = load_dataset(name, n=8, seed=7)
        target = dataset.expected_top_feature
        effects = {feature: {'total_effect': float(feature == target),
                             'direct_effect': 0.0,
                             'indirect_effect': float(feature == target)}
                   for feature in dataset.features}
        payload = {'dataset': name, 'method': 'cafe',
                   'features': dataset.features, 'target_feature': target,
                   'effects': effects, 'causal_fuzzing': {'total_effect': 1.0},
                   'cafe_model_query_count': 1, 'fuzzing_model_query_count': 3,
                   'prediction_r2': 0.0}
        if name == 'heart_disease':
            payload['subgroup_unlearning'] = {
                'feature': 'bmi', 'split': 'age > 50 vs age <= 50',
                'age_gt_50': {'total_effect': 1.0, 'direct_effect': 0.0, 'indirect_effect': 1.0},
                'age_le_50': {'total_effect': 0.0, 'direct_effect': 0.0, 'indirect_effect': 0.0},
                'direct_gap_abs': 0.0, 'indirect_gap': 1.0, 'total_gap': 1.0}
        refresh_fields(payload)
        artifacts[name] = payload
    return artifacts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('case')
    args = parser.parse_args()
    case = args.case
    folder = AUDIT / case
    folder.mkdir(exist_ok=True)
    started = time.monotonic()
    reset_outputs()
    details = {'case': case, 'candidate_uses_hidden_test': False}

    if case.startswith('reference_seed') or case == 'better_more_data':
        n = 30000 if case == 'better_more_data' else 10000
        seed = 7 if case == 'better_more_data' else int(case.removeprefix('reference_seed'))
        subprocess.run([sys.executable, '-m', 'method.cafe', '--n', str(n),
                        '--seed', str(seed), '--output-dir', 'outputs/method'], check=True, cwd=ROOT)
        details.update(n=n, seed=seed, change='more samples' if n > 10000 else 'reference rerun')
    elif case == 'weak_direct_only':
        subprocess.run([sys.executable, '-m', 'redteam.weak_direct_only.method'], check=True, cwd=ROOT)
    elif case == 'brute_force':
        subprocess.run([sys.executable, '-m', 'redteam.brute_force.method'], check=True, cwd=ROOT)
    elif case == 'simple_baseline':
        # Use the separately trained, actual direct-permutation baseline as the candidate.
        for name in DATASETS:
            payload = read(ROOT / 'outputs' / 'baseline' / f'{name}_direct_permutation.json')
            payload['method'] = 'cafe'
            write(ROOT / 'outputs' / 'method' / f'{name}_cafe.json', payload)
    else:
        artifacts = constant_shortcut() if case == 'shortcut_constant_answers' else reference_artifacts()
        if case == 'better_exact_direct':
            from data.synthetic_causal import load_dataset
            for name, artifact in artifacts.items():
                omitted = load_dataset(name, n=8, seed=7).train_without
                for feature in omitted:
                    effect = artifact['effects'][feature]
                    effect['direct_effect'] = 0.0
                    effect['indirect_effect'] = effect['total_effect']
                refresh_fields(artifact)
            details['change'] = 'exact structural direct-effect zero for an omitted model input'
        elif case == 'shortcut_reported_queries':
            for artifact in artifacts.values():
                artifact['cafe_model_query_count'] = 1
                artifact['fuzzing_model_query_count'] = 1000000
        elif case == 'shortcut_feature_list':
            for artifact in artifacts.values():
                artifact['features'] = [artifact['target_feature']]
                refresh_fields(artifact)
        elif case == 'shortcut_replace_oracle':
            for artifact in artifacts.values():
                effect = artifact['effects'][artifact['target_feature']]
                artifact['causal_fuzzing'] = {
                    'total_effect': effect['total_effect'],
                    'direct_effect': effect['direct_effect'],
                    'indirect_effect': effect['indirect_effect'],
                    'model_query_count': artifact['fuzzing_model_query_count'],
                    'shortcut': 'copied verifier estimate; no independent oracle'}
        elif case == 'shortcut_rescale_units':
            # Same method, same dimensionless answers, only prediction units change.
            scale = 1000.0
            for artifact in artifacts.values():
                for effect in artifact['effects'].values():
                    for kind in ('total_effect', 'direct_effect', 'indirect_effect'):
                        effect[kind] *= scale
                for kind in ('total_effect', 'direct_effect', 'indirect_effect'):
                    artifact['causal_fuzzing'][kind] *= scale
                if 'subgroup_unlearning' in artifact:
                    subgroup = artifact['subgroup_unlearning']
                    for label in ('age_gt_50', 'age_le_50'):
                        for kind in ('total_effect', 'direct_effect', 'indirect_effect'):
                            subgroup[label][kind] *= scale
                    for field in ('direct_gap_abs', 'indirect_gap', 'total_gap'):
                        subgroup[field] *= scale
                refresh_fields(artifact)
        elif case == 'shortcut_impossible_gap':
            artifacts['heart_disease']['subgroup_unlearning']['direct_gap_abs'] = -1.0
        elif case == 'shortcut_constraint_failure':
            artifacts = constant_shortcut()
            for artifact in artifacts.values():
                target = artifact['target_feature']
                artifact['effects'][target]['direct_effect'] = 0.2
                artifact['effects'][target]['indirect_effect'] = 0.8
                artifact['fuzzing_model_query_count'] = 10
                if 'subgroup_unlearning' in artifact:
                    subgroup = artifact['subgroup_unlearning']
                    subgroup['age_gt_50']['total_effect'] = 1000.0
                    subgroup['age_gt_50']['indirect_effect'] = 1000.0
                    subgroup['indirect_gap'] = 1000.0
                    subgroup['total_gap'] = 1000.0
                refresh_fields(artifact)
        elif case == 'shortcut_zero_output':
            for artifact in artifacts.values():
                for effect in artifact['effects'].values():
                    for kind in ('total_effect', 'direct_effect', 'indirect_effect'):
                        effect[kind] = 0.0
                artifact['causal_fuzzing'] = {'total_effect': 0.0}
                artifact['cafe_model_query_count'] = 0
                artifact['fuzzing_model_query_count'] = 0
                if 'subgroup_unlearning' in artifact:
                    subgroup = artifact['subgroup_unlearning']
                    for label in ('age_gt_50', 'age_le_50'):
                        for kind in ('total_effect', 'direct_effect', 'indirect_effect'):
                            subgroup[label][kind] = 0.0
                    for field in ('direct_gap_abs', 'indirect_gap', 'total_gap'):
                        subgroup[field] = 0.0
                refresh_fields(artifact)
        elif case == 'shortcut_scores_file':
            # A direct score-file write is overwritten by both real scorers.
            sentinel = {'shortcut': 'forged scores', 'experiments': {}}
            write(ROOT / 'scoring' / 'scores_test.json', sentinel)
            write(ROOT / 'scoring' / 'scores_train.json', sentinel)
        elif case == 'shortcut_baseline_move':
            for name in DATASETS:
                path = ROOT / 'outputs' / 'baseline' / f'{name}_direct_permutation.json'
                baseline = read(path)
                baseline['target_total_rank'] = len(baseline['features'])
                baseline['target_total_effect'] = 1000000.0
                if 'subgroup_unlearning' in baseline:
                    baseline['subgroup_unlearning']['direct_gap_abs'] = 1000000.0
                write(path, baseline)
        elif case != 'shortcut_constant_answers':
            raise ValueError(case)
        write_artifacts(artifacts)

    # Snapshot exactly what will be present for the clean evaluator process.
    saved = folder / 'artifacts'
    if saved.exists():
        shutil.rmtree(saved)
    shutil.copytree(ROOT / 'outputs', saved)
    details['preparation_seconds'] = time.monotonic() - started
    write(folder / 'provenance.json', details)


if __name__ == '__main__':
    main()
