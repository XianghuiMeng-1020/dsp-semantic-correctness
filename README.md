# DSP Semantic Correctness for Generated Code

Code accompanying "Executable Is Not Signal-Processing Correct: Specification
versus Reference Testing of Generated DSP Code" (ICASSP 2027).

Generated digital signal processing (DSP) programs can execute, return a
finite array of the expected shape, and pass ordinary software checks while
still violating a theory-defined signal-processing identity. On design tasks
that admit more than one valid realization, agreement with a single gold
implementation is not itself a complete definition of correctness. This
repository provides the frozen semantic contracts and the extracted
generated implementations needed to reproduce every published count.

## Why this matters

Three correctness layers are easy to conflate:

- **Executable / software correctness.** The routine runs, returns a finite
  array of the expected shape, and passes coarse type or range checks.
- **Differential / reference correctness.** The output agrees with a trusted
  implementation. This is a legitimate proxy when the task has a unique
  correct output.
- **DSP semantic correctness.** The implementation satisfies a named
  identity or specification, written independently of any model output. On
  tasks with a non-unique correct answer (classical filter design, for
  instance), this is the only object that characterizes correctness.

## What this repository provides

- Frozen semantic contracts for the primary prospective filter-specification
  arm (Arm N) and three supporting arms: a historical spectral/filter suite
  (Arm H), a frozen convolution/correlation holdout (Arm P), and a frozen
  sampling/resampling suite (Arm B).
- The extracted implementations from every scored generation in all four
  arms.
- A single entry point that re-scores every generation against the frozen
  contracts and checks the result against every count published in the
  paper.

Model generation itself is not shipped: re-running the study against new
models would require live API access and is outside this release. Every
number below is computed deterministically from the already-generated code
that is included in `data/`.

## Main empirical findings

The four arms are reported separately and are never pooled.

| Arm | Family | Design | Headline evidence | Tasks | Models |
| --- | --- | --- | --- | ---: | ---: |
| N (primary) | FIR/IIR filter design | frozen before generation | 9 programs satisfy the mask while disagreeing with a valid reference | 4/4 | 2/3 |
| H | spectral / filter identities | historical confirmatory | CORE 16/144 | 4/12 | 3/3 |
| P | convolution / correlation | frozen before generation | CORE 11/48 | 1/4 | 3/3 |
| B | sampling / resampling | frozen before generation | CORE 9/48 (conservative; 11/48 original) | 3/4 | 2/3 |

Arm N is the central result: classical FIR and IIR filter design admits many
coefficient vectors that satisfy the same passband/stopband/stability mask.
Nine naturally generated programs satisfy the frozen specification while
disagreeing with the selected valid reference by more than the frozen
tolerance — a single-reference rule would reject programs that a DSP
specification accepts. Before any natural generation, the same contracts
accepted 12/12 independently constructed valid controls and rejected 12/12
mechanism mutants.

Arms H, P, and B test whether executable, software-eligible programs can
violate defining identities outside filter design (spectral normalization,
delay sign, alias mapping, resampling gain). Differential testing remains
strong on these unique-output tasks: a trusted reference detects 15/16,
11/11, and 11/11 of the respective CORE cases. Arm B's preferred count
excludes two DC-preservation cases whose residual matches an unpadded
polyphase-FIR transient on a short constant; both readings are reproduced
below.

## DSP mechanisms

Arm N: FIR/IIR passband, stopband, and pole-radius stability specifications.
Arm H: spectral normalization (Parseval scaling, one-sided versus two-sided
density, window-power periodograms, frequency-response decibels). Arm P:
correlation delay and sign convention. Arm B: alias-frequency mapping,
spectral images under zero insertion, and resampling DC/interpolation gain.

## Quick start

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Unix:    source .venv/bin/activate
pip install -r requirements.txt
python scripts/reproduce_all.py
```

## Reproducing the results

`python scripts/reproduce_all.py` re-executes every generated function under
a restricted namespace (`numpy`/`scipy` only), scores it against the frozen
contracts, and checks the result against every published count. It should
end with:

```text
ALL_PUBLISHED_COUNTS_MATCH: YES
```

Arm N scoring additionally recomputes the coefficient/`(b, a)` vector for
each eligible generation and its relative-L2 distance to the frozen valid
control, reproducing the specification-pass / reference-concordance
quadrant used to identify the nine Q2 (specification-valid,
reference-discordant) witnesses. The historical (Arm H) summary is obtained
from the frozen confirmatory table after applying the published
artifact-adjustment list; Arm P, Arm B, and Arm N are re-executed directly
from extracted code against the frozen contracts. Wilson 95% intervals are
recomputed by the same formula used in the study.

## Repository structure

```text
README.md
LICENSE
requirements.txt
src/
    contracts_arm_n.py         Arm N: FIR/IIR filter-specification contracts
    contracts_conv_corr.py     Arm P: convolution/correlation contracts
    contracts_samp_resamp.py   Arm B: sampling/resampling contracts
    runtime.py                 restricted-namespace exec + generic scorer
    stats.py                   Wilson score interval
scripts/
    reproduce_all.py           single entry point; reproduces every count
data/
    arm_n_generations.json         Arm N: all 48 scored generations
    arm_n_valid_controls/          Arm N: 12 pre-generation valid controls
    arm_n_mutants/                 Arm N: 12 pre-generation mechanism mutants
    arm_n_thresholds.json          Arm N: frozen numerical floors
    historical_generations.csv     Arm H: all 144 scored generations
    historical_artifact_adjustment.json
    historical_control_residuals.json
    historical_mutant_residuals.json
    historical_thresholds.json
    arm_p_generations.json         Arm P: all 48 scored generations
    arm_b_generations.json         Arm B: all 48 scored generations
```

## Reproducibility notes

- Semantic contracts, thresholds, valid controls, and mechanism mutants were
  frozen before the corresponding generations were scored.
- Scoring is deterministic given the extracted implementations and the
  frozen contracts. One Arm N generation does not terminate; scoring wraps
  each call in a 15-second process timeout and records a hang as an
  execution failure, exactly as in the original harness.
- Raw provider transcripts and API credentials are not included; the code
  strings in `data/*.json` are the immutable extracted implementations that
  were scored.
- Arm totals must not be added into a single prevalence estimate. Each arm's
  CORE or Q2 count is an existence result on its own frozen design, not a
  sample from a shared population.

## Citation

A formal citation will be added after publication. In the meantime, please
cite the ICASSP 2027 paper "Executable Is Not Signal-Processing Correct:
Specification versus Reference Testing of Generated DSP Code" by Xianghui
Meng and Jionghao Lin.
