# DSP Semantic Correctness for Generated Code

Generated digital signal processing (DSP) programs can execute and satisfy ordinary software checks while violating theory-defined signal-processing identities. This repository provides the minimal scoring code and frozen extracted implementations needed to reproduce that finding.

## Why this matters

Three correctness layers are easy to conflate:

- **Executable / software correctness.** The routine runs, returns a finite array of the expected shape, and passes coarse type or range checks.
- **Differential / reference correctness.** The output is close to a trusted implementation when a unique algebraic residual exists.
- **DSP semantic correctness.** The implementation obeys a named identity: an observable, a reference quantity, a valid domain, and a tolerance written independently of model outputs.

Differential comparison is strong when a trusted implementation exists. Semantic contracts add an explicit DSP-level specification of the identity that failed. They are not offered as a universally higher-recall detector.

## What this repository provides

- Frozen semantic contracts for a historical spectral/filter suite and two prospective families (convolution/correlation; sampling/resampling).
- Extracted implementations from the completed generation runs.
- A single reproduction entry point that recomputes the published CORE summaries.

Model generation itself is not shipped. Re-running the study against new models would require an external API and is outside this release.

## Main empirical findings

The three arms are reported separately and are not pooled.

| Arm | Family | Design | CORE | Tasks | Models | Software | Differential |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| Historical | spectral / filter | confirmatory | 16/144 | 4/12 | 3/3 | 0/16 | 15/16 |
| Prospective | convolution / correlation | frozen before generation | 11/48 | 1/4 | 3/3 | 0/11 | 11/11 |
| Prospective | sampling / resampling | sequential, frozen before generation | 11/48 | 3/4 | 3/3 | 0/11 | 11/11 |

The historical event is mechanism-selective: eight of twelve tasks contribute no validated CORE, valid-control evaluations show 0/113 observed false positives, and 13/13 controlled mutants are detected. Removing the highest-failure task leaves 11/132. The first prospective arm concentrates in one delay-sign / correlation-order task. The second prospective arm covers both predefined mechanism groups, with task counts 1/12, 0/12, 3/12, and 7/12. The contribution is the explicit theory-grounded correctness layer, not universal superiority over differential checking.

## DSP mechanisms

Representative identities include spectral normalization (Parseval scaling, one-sided versus two-sided density, window-power periodograms, frequency-response decibels), correlation delay and sign, alias-frequency mapping, spectral images of a zero inserter, and resampling DC gain.

## Quick start

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Unix:    source .venv/bin/activate
pip install -r requirements.txt
python scripts/reproduce_all.py
```

## Reproducing the results

`python scripts/reproduce_all.py` should print:

```text
Historical validated CORE: 16/144
Prospective convolution/correlation CORE: 11/48
Prospective sampling/resampling CORE: 11/48
ALL_PUBLISHED_COUNTS_MATCH: YES
```

The historical summary is obtained from the frozen confirmatory table after applying the published artifact-adjustment list. Prospective rows are re-executed from extracted code against the frozen contracts. Wilson 95% intervals are recomputed by the same formula used in the study.

## Repository structure

```text
README.md
requirements.txt
src/
    contracts_conv_corr.py
    contracts_samp_resamp.py
    runtime.py
    stats.py
scripts/
    reproduce_all.py
data/
    historical_generations.csv
    historical_artifact_adjustment.json
    historical_control_residuals.json
    historical_mutant_residuals.json
    historical_thresholds.json
    arm_p_generations.json
    arm_b_generations.json
```

## Reproducibility notes

- Semantic contracts, thresholds, and input batteries were frozen before the corresponding generations were scored.
- Prospective scoring is deterministic given the extracted implementations and the contract seeds.
- Raw provider transcripts and API credentials are not included.
- The three arm totals must not be added into a single prevalence.

## Citation

A formal citation will be added after archival publication.
