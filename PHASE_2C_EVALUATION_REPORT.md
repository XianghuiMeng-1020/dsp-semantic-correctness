# PHASE 2C — Invalid generation and evaluation

Labels were frozen before scoring. Specifications, floors, and the
Phase 2B valid set were not changed. No LLM draws. No manuscript edits.

Invalid admission: \(S_t(h)=0\) only.

## 1. Invalid counts by mechanism

**144** `invalid-by-construction` occupants. **0** leaked (\(S_t=1\)).
**16** not applicable (M4 on FIR). **0** skipped.

| Mechanism | n | Applicable tasks |
|---|---:|---|
| M1 band swap | 20 | all |
| M2 cutoff into constrained band | 20 | all |
| M3 order too short | 20 | all |
| M4 unstable pole | 4 | IIR only |
| M5 Nyquist as 1 Hz | 20 | all |
| M6 pass gain collapse | 20 | all |
| M7 wrong sampling rate | 20 | all |
| M8 type mismatch | 20 | all |

Target \(20\times 7+4=144\) met.

## 2. Valid / invalid label audit

| Set | n | Checker | Errors |
|---|---:|---|---|
| Suite N valid-by-construction | 416 | 416/416 \(S_t=1\) | 0 |
| Suite N invalid-by-construction | 144 | 144/144 \(S_t=0\) | 0 |
| Suite S valids (canonical + alternate) | 12 | 12/12 \(S_t=1\) | 0 |
| Suite S mutants | 16 | 16/16 \(S_t=0\) | 0 |

\[
\mathrm{FRR}_S=0/416=0,\qquad \mathrm{FAR}_S=0/144=0
\]

Construction pipeline is intact.

## 3. Table-ready results

### Table 2 — Reference rejection (\(\tau_R=0.05\))

| Suite | n | \(\mathrm{FRR}_{\mathrm{ref}}\) | \(\mathrm{FRR}_{\mathrm{ref}}^{\mathrm{any3}}\) | task-level disagreement | \(P(d_{\mathrm{coeff}}>\tau_R)\) |
|---|---:|---:|---:|---:|---:|
| S | 12 | 0/12 = 0.000 | — | — | 0.000 |
| N all | 416 | 374/416 = 0.899 | 346/416 = 0.832 | 20/20 = 1.000 | 0.899 |
| N FIR | 340 | 302/340 = 0.888 | 274/340 = 0.806 | — | 0.888 |
| N IIR | 76 | 72/76 = 0.947 | 72/76 = 0.947 | — | 0.947 |
| N loose | 210 | 183/210 = 0.871 | 177/210 = 0.843 | — | 0.871 |
| N tight | 206 | 191/206 = 0.927 | 169/206 = 0.820 | — | 0.927 |

\(\mathrm{FRR}_{\mathrm{ref}}^{\mathrm{any3}}\): rejected only if
\(d_{\mathrm{coeff}}>\tau_R\) versus every available library occupant among
`firwin` / `remez` / `firls` (or the IIR library set).

### Diversity (vs canonical \(h_r\); pairwise in last columns)

| Task | n | med \(d_{\mathrm{coeff}}\) | max \(d_{\mathrm{coeff}}\) | frac \(>\tau_R\) | med band RMSE | med full RMSE | pairwise med \(d\) | pairwise frac \(>\tau_R\) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| fir_lp_loose_8k | 21 | 1.000 | 1.454 | 0.857 | 0.00315 | 0.0666 | 1.442 | 0.986 |
| fir_lp_tight_8k | 21 | 1.001 | 1.544 | 0.952 | 0.00165 | 0.0315 | 1.401 | 0.995 |
| fir_lp_loose_16k | 21 | 1.000 | 1.516 | 0.857 | 0.00315 | 0.0655 | 1.544 | 0.981 |
| fir_lp_tight_16k | 21 | 1.003 | 1.428 | 0.952 | 0.00165 | 0.0316 | 1.410 | 0.986 |
| fir_hp_loose_8k | 22 | 1.000 | 1.453 | 0.727 | 0.00335 | 0.0457 | 1.434 | 0.948 |
| fir_hp_tight_8k | 21 | 1.294 | 1.479 | 0.952 | 0.00115 | 0.0250 | 1.412 | 0.995 |
| fir_hp_loose_16k | 22 | 1.000 | 1.454 | 0.773 | 0.00335 | 0.0548 | 1.530 | 0.965 |
| fir_hp_tight_16k | 21 | 1.001 | 1.769 | 0.952 | 0.00114 | 0.0276 | 1.428 | 0.981 |
| fir_bp_loose_8k | 21 | 1.000 | 1.860 | 0.905 | 0.01015 | 0.0973 | 1.518 | 0.990 |
| fir_bp_tight_8k | 21 | 1.001 | 1.925 | 0.905 | 0.00265 | 0.0363 | 1.503 | 0.995 |
| fir_bp_loose_16k | 21 | 1.001 | 1.860 | 0.905 | 0.01010 | 0.1217 | 1.510 | 0.995 |
| fir_bp_tight_16k | 21 | 1.002 | 1.925 | 0.905 | 0.00265 | 0.0381 | 1.446 | 0.981 |
| fir_bs_loose_8k | 22 | 1.000 | 1.502 | 0.909 | 0.01106 | 0.0768 | 1.484 | 0.983 |
| fir_bs_tight_8k | 21 | 1.001 | 1.494 | 0.857 | 0.00237 | 0.0312 | 1.426 | 0.986 |
| fir_bs_loose_16k | 22 | 1.000 | 1.502 | 0.909 | 0.01105 | 0.0760 | 1.471 | 0.987 |
| fir_bs_tight_16k | 21 | 1.013 | 1.498 | 0.905 | 0.00237 | 0.0240 | 1.419 | 0.990 |
| iir_lp_loose_8k | 19 | 1.001 | 2.405 | 0.947 | 0.02891 | 0.1734 | 1.386 | 1.000 |
| iir_lp_tight_8k | 19 | 2.191 | 9.056 | 0.947 | 0.00577 | 0.1210 | 1.533 | 0.994 |
| iir_hp_loose_8k | 19 | 1.251 | 14.500 | 0.947 | 0.02506 | 0.1677 | 1.366 | 0.994 |
| iir_hp_tight_8k | 19 | 1.859 | 12.140 | 0.947 | 0.00594 | 0.0692 | 1.163 | 0.994 |

### Table 3 — Verification vs constructed labels

Suite N universe: 416 valid + 144 invalid.

| Oracle | Rule | FRR | FAR |
|---|---|---:|---:|
| A | \(d_{\mathrm{coeff}}(h,h_r)\le 0.05\) | 374/416 = 0.899 | 0/144 = 0.000 |
| B | spec-band \(\lvert H\rvert\) RMSE \(\le\) same-order library pair max \(+10^{-8}\) | 28/416 = 0.067 | 0/144 = 0.000 |
| C | \(S_t=1\) | 0/416 = 0.000 | 0/144 = 0.000 |

Suite S universe: 12 valid + 16 invalid. Oracle B is undefined (not a filter mask).

| Oracle | FRR | FAR |
|---|---:|---:|
| A (output vs canonical) | 0/12 = 0.000 | 0/16 = 0.000 |
| C (\(S_t\)) | 0/12 = 0.000 | 0/16 = 0.000 |

Six Suite N tasks had no same-order library pair; Oracle B used the
all-library pairwise max on those tasks.

### Table 4 — Ablations (\(\mathrm{FRR}_{\mathrm{ref}}\) on Suite N valids)

| Knob | n scored | \(\mathrm{FRR}_{\mathrm{ref}}\) |
|---|---:|---:|
| \(\tau_R=0.01\) | 416 | 388/416 = 0.933 |
| \(\tau_R=0.05\) | 416 | 374/416 = 0.899 |
| \(\tau_R=0.10\) | 416 | 363/416 = 0.873 |
| phase free | 416 | 374/416 = 0.899 |
| phase Type-I linear | 340 | 302/340 = 0.888 |
| order free | 416 | 374/416 = 0.899 |
| order = canonical | 67 | 25/67 = 0.373 |

Thresholds were not retuned.

## 4. Unexpected findings

1. Oracle B FRR (0.067) is far below Oracle A FRR (0.899). Valids that
   meet the mask have small spec-band \(\lvert H\rvert\) RMSE to \(h_r\)
   even when coefficients do not match.

2. The linear-phase subset equals the FIR slice (340/340 constructed FIR
   occupants are Type I). The ablation does not add an independent FIR
   restriction on this generated set.

3. Locking order to the canonical length/order drops \(\mathrm{FRR}_{\mathrm{ref}}\)
   from 0.899 to 0.373 (25/67). Free-order occupants dominate the
   coefficient disagreement.

4. Tight masks have higher, not lower, \(\mathrm{FRR}_{\mathrm{ref}}\)
   (0.927 vs 0.871 loose).

## 5. Frozen hypothesis

**Supported.**

Claim: reference matching is a realization diagnostic; specification-set
membership is semantic correctness when \(\lvert\mathcal{V}_t\rvert>1\).

- Suite S (unique maps): \(R\) and \(S\) agree. \(\mathrm{FRR}_{\mathrm{ref}}=\mathrm{FRR}_S=\mathrm{FAR}_S=0\).
- Suite N (non-unique masks): \(S\) separates constructed labels
  (\(\mathrm{FRR}_S=\mathrm{FAR}_S=0\)). \(R\) rejects 374/416 valids.
  Disagreement occurs on 20/20 tasks, including tight masks.
- Oracle A coincides with \(R\). Oracle C coincides with constructed
  labels. Oracle B does not recover the coefficient disagreement.

## Files

| Path | Role |
|---|---|
| `src/mutants.py` | M1–M8 constructors |
| `src/oracles.py` | Oracle A / B |
| `scripts/generate_invalids.py` | Invalid writer |
| `scripts/evaluate_phase2c.py` | Evaluation |
| `data/invalid/` | 144 mutants + manifests |
| `data/phase2c/evaluation.json` | Numeric source for this report |
