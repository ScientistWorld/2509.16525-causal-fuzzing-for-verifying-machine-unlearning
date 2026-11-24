# Causal Fuzzing for Verifying Machine Unlearning

<!-- scope-note -->
> [!NOTE]
> **Not a full reproduction of the paper.** This environment keeps the paper's core problem at a reduced scale so it is easy to run. It measures an AI scientist's idea and how well it is carried out, not the full research loop.

| This paper | Scientist World, the framework this environment belongs to |
|:---:|:---:|
| <a href="https://arxiv.org/abs/2509.16525"><img alt="This paper on arXiv" src="https://img.shields.io/badge/arXiv-2509.16525-b31b1b?logo=arxiv&logoColor=white"></a> | <a href="https://arxiv.org/abs/2611.08478"><img alt="Scientist World on arXiv" src="https://img.shields.io/badge/arXiv-2611.08478-b31b1b?logo=arxiv&logoColor=white"></a> <a href="https://github.com/zlab-princeton/scientist_world"><img alt="Scientist World code" src="https://img.shields.io/badge/Code-Scientist_World-181717?logo=github&logoColor=white"></a> <a href="https://github.com/zlab-princeton/scientist_world_cli"><img alt="Command line code" src="https://img.shields.io/badge/Code-Command_line-181717?logo=github&logoColor=white"></a> |

| **Paper ID** | [2509.16525](https://arxiv.org/abs/2509.16525) |
|:---|:---|
| **Domain** | Machine unlearning verification / causal inference / tabular ML |
| **TL;DR** | The paper verifies whether black-box models still use supposedly unlearned features by measuring direct and mediated causal influence. |

## Summary

The paper argues that conventional feature-attribution and fairness tests can miss residual influence after unlearning because they focus on direct or associational effects. CAFÉ uses a supplied causal graph to estimate total, direct, and indirect influence of unlearning targets from black-box model predictions. The evaluation spans semi-synthetic and real-world tabular datasets and shows that mediated effects can remain even when the target feature is omitted from the audited model.

## Problem

How can a deployed black-box tabular ML model be audited to determine whether a specified feature or feature-subgroup target still influences predictions after unlearning?

## The paper's method

The paper introduces CAFÉ, a black-box unlearning verifier that estimates whether an unlearning target retains direct or indirect causal influence on model predictions.

## Key results of the paper

- On the Heart-Disease semi-synthetic setting, the paper reports that smoking is the most influential feature under ground truth and CAFÉ, while conventional baselines rank it near the bottom.
- On the Performance setting, standard fairness metrics and direct checks miss substantial mediated influence for gender after direct unlearning.
- Table 3 reports CAFÉ running in roughly 0.026-0.030 seconds across LR, RF, and NN settings, much faster than causal fuzzing and most attribution baselines.

## Leaderboard

FNI of AI scientists on this paper, grader-verified. 0 matches the paper's method, higher is better.

| Model | Innovate |
|---|---:|
| `gpt-5.6-sol-xhigh` | +134.4 |
| `gpt-5.5-xhigh` | +114.5 |
| `gpt-5.6-terra-xhigh` | +73.8 |
| `gpt-5.6-luna-xhigh` | +16.7 |

`innovate`: the model designs its own method. `improve`: it starts from the paper's method.

## Run it

```bash
pip install sciworld
sw research 2509.16525 --mode innovate --agent claude-code
sw evaluate 2509.16525
```

## More

The full problem statement, method notes, evaluation protocol and reproduction log are in [DETAILS.md](DETAILS.md).

