"""Honest weaker variant: remove total/mediated estimation, keep direct contrasts."""

from pathlib import Path
import json

from method import cafe

original_scores = cafe.cafe_scores


def direct_only_scores(*args, **kwargs):
    effects = original_scores(*args, **kwargs)
    for effect in effects.values():
        effect['total_effect'] = effect['direct_effect']
        effect['indirect_effect'] = 0.0
    return effects


def main():
    cafe.cafe_scores = direct_only_scores
    output = Path('outputs/method')
    for name in ('heart_disease', 'performance'):
        cafe.run_dataset(name, output_dir=output, n=10000, seed=7)


if __name__ == '__main__':
    main()
