"""Rank audit submissions with the user-specified variance-normalized rule."""

from __future__ import annotations
import json
import math
import statistics
from pathlib import Path

ROOT = Path('/home/user')
AUDIT = ROOT / 'redteam'


def main():
    reference = json.loads((AUDIT / 'reference_original/scores_test.json').read_text())
    weights = json.loads((ROOT / 'scoring/reference.json').read_text())
    cases = {}
    for path in sorted(AUDIT.glob('*/scores_test.json')):
        if path.parent.name != 'reference_original':
            cases[path.parent.name] = json.loads(path.read_text())
    specs = []
    for experiment, body in weights['experiments'].items():
        for metric, spec in body['metrics'].items():
            specs.append((experiment, metric, body.get('weight', 1.0),
                          abs(spec['coefficient']), 1 if spec['higher_is_better'] else -1))
    ref = lambda exp, metric: reference['experiments'][exp]['results']['cafe'][metric]
    val = lambda case, exp, metric: cases[case]['experiments'][exp]['results']['cafe'][metric]
    cohorts = {'all_audit_attempts': list(cases),
               'honest_variants': [case for case in cases if not case.startswith('shortcut_')]}
    summary = {'normalization': 'population standard deviation over the listed cohort and the saved reference; zero-variance metrics contribute zero',
               'anchor': 'original scoring/scores_test.json cafe results', 'cohorts': {}}
    for label, members in cohorts.items():
        scales = {}
        for exp, metric, *_ in specs:
            scales[(exp, metric)] = statistics.pstdev([ref(exp, metric)] + [val(case, exp, metric) for case in members])
        ranked = {}
        for case in cases:
            terms = {}
            for exp, metric, weight, coefficient, direction in specs:
                sigma = scales[(exp, metric)]
                delta = direction * (val(case, exp, metric) - ref(exp, metric))
                terms[f'{exp}/{metric}'] = weight * coefficient * delta / sigma if sigma else 0.0
            ranked[case] = {'score_vs_reference': sum(terms.values()), 'terms': terms}
        seeds = [ranked[f'reference_seed{seed}']['score_vs_reference'] for seed in (7, 11, 19)
                 if f'reference_seed{seed}' in ranked]
        summary['cohorts'][label] = {
            'members': members, 'scores': ranked,
            'metric_sigma': {f'{exp}/{metric}': value for (exp, metric), value in scales.items()},
            'reference_seed_scores': seeds,
            'reference_seed_spread': max(seeds) - min(seeds) if seeds else None}
    summary['raw_test_metrics'] = {case: cases[case]['experiments'] for case in cases}
    (AUDIT / 'summary.json').write_text(json.dumps(summary, indent=2, sort_keys=True) + '\n')
    for label, cohort in summary['cohorts'].items():
        print(label, 'seed_spread=', cohort['reference_seed_spread'])
        for case, body in sorted(cohort['scores'].items(), key=lambda pair: pair[1]['score_vs_reference'], reverse=True):
            print(f"{case:36s} {body['score_vs_reference']:+.9f}")


if __name__ == '__main__':
    main()
