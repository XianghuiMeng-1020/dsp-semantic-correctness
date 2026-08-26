> **ARCHIVED historical record.** These numbers are not the ICASSP 2027 final results. See the repository root `README.md` and `python -m experiments.icassp_10of10.run_all`.

# PHASE 2B — Constructed valid occupant generation

Suite N only. Admission rule: \(S_t(h)=1\). No mutants. No LLM draws.
No manuscript edits. Specifications and floors were not changed.

Search objective was specification membership only. Coefficient distance
to the canonical reference was measured after admission. No occupant was
accepted or rejected because it was close to, or far from, \(h_r\).

Canonical \(h_r\): shortest-odd Hamming `firwin` (FIR) or lowest-order
`butter` (IIR) that meets \(S_t\). Seed for random-valid: `20260826`.

Independent recheck of every written occupant: **416/416** \(S_t=1\).

## 1. Number of valid occupants

**Overall: 416** (`valid-by-construction`)

| Source | Kept after dedup |
|---|---|
| library | 92 |
| first_principles | 24 |
| random | 300 |

| Task | n | library | first_principles | random |
|---|---:|---:|---:|---:|
| fir_lp_loose_8k | 21 | 5 | 1 | 15 |
| fir_lp_tight_8k | 21 | 5 | 1 | 15 |
| fir_lp_loose_16k | 21 | 5 | 1 | 15 |
| fir_lp_tight_16k | 21 | 5 | 1 | 15 |
| fir_hp_loose_8k | 22 | 5 | 2 | 15 |
| fir_hp_tight_8k | 21 | 5 | 1 | 15 |
| fir_hp_loose_16k | 22 | 5 | 2 | 15 |
| fir_hp_tight_16k | 21 | 5 | 1 | 15 |
| fir_bp_loose_8k | 21 | 5 | 1 | 15 |
| fir_bp_tight_8k | 21 | 4 | 2 | 15 |
| fir_bp_loose_16k | 21 | 5 | 1 | 15 |
| fir_bp_tight_16k | 21 | 4 | 2 | 15 |
| fir_bs_loose_8k | 22 | 5 | 2 | 15 |
| fir_bs_tight_8k | 21 | 4 | 2 | 15 |
| fir_bs_loose_16k | 22 | 5 | 2 | 15 |
| fir_bs_tight_16k | 21 | 4 | 2 | 15 |
| iir_lp_loose_8k | 19 | 4 | 0 | 15 |
| iir_lp_tight_8k | 19 | 4 | 0 | 15 |
| iir_hp_loose_8k | 19 | 4 | 0 | 15 |
| iir_hp_tight_8k | 19 | 4 | 0 | 15 |

First-principles is FIR only. Several shortest/same-order pairs were
collapsed by the duplicate filter (relative coefficient distance
\(\le 0.01\) and full-grid \(|H|\) RMSE \(\le 10^{-3}\)).

Every loose FIR task has \(\ge 8\) valids.

## 2. Acceptance rates

| Stream | Attempts | Accepted (pre-dedup / kept) | Rate |
|---|---:|---:|---:|
| library methods | 96 | 92 / 92 | 0.958 |
| random-valid | 556 | 300 / 300 | 0.540 |

Library rate is method-feasibility (one search per method per task).
Random rate is draws that met \(S_t=1\) and were not near-duplicates.

**Method-infeasible (not forced into \(\mathcal{V}_t\)):**

- library `firwin2`: `fir_bp_tight_8k`, `fir_bp_tight_16k`, `fir_bs_tight_8k`, `fir_bs_tight_16k`
- first-principles `frequency_sampling/sameorder`: 12 FIR tasks (all tight LP/HP and all BP/BS)

## 3. Low occupancy tasks

None. Random search reached 15 accepted on every task (cap 400).
No task was flagged `low_occupancy`.

## 4. Diversity statistics

Distances are to the task canonical \(h_r\), min-length relative
\(\ell_2\) as in paper \(R\), \(\tau_R=0.05\). Measured after admission.

| Task | n | median \(d_{\mathrm{coeff}}\) | max \(d_{\mathrm{coeff}}\) | frac \(d_{\mathrm{coeff}}>\tau_R\) | median band RMSE | median full RMSE |
|---|---:|---:|---:|---:|---:|---:|
| fir_lp_loose_8k | 21 | 1.000 | 1.454 | 0.857 | 0.00315 | 0.0666 |
| fir_lp_tight_8k | 21 | 1.001 | 1.544 | 0.952 | 0.00165 | 0.0315 |
| fir_lp_loose_16k | 21 | 1.000 | 1.516 | 0.857 | 0.00315 | 0.0655 |
| fir_lp_tight_16k | 21 | 1.003 | 1.428 | 0.952 | 0.00165 | 0.0316 |
| fir_hp_loose_8k | 22 | 1.000 | 1.453 | 0.727 | 0.00335 | 0.0457 |
| fir_hp_tight_8k | 21 | 1.294 | 1.479 | 0.952 | 0.00115 | 0.0250 |
| fir_hp_loose_16k | 22 | 1.000 | 1.454 | 0.773 | 0.00335 | 0.0548 |
| fir_hp_tight_16k | 21 | 1.001 | 1.769 | 0.952 | 0.00114 | 0.0276 |
| fir_bp_loose_8k | 21 | 1.000 | 1.860 | 0.905 | 0.01015 | 0.0973 |
| fir_bp_tight_8k | 21 | 1.001 | 1.925 | 0.905 | 0.00265 | 0.0363 |
| fir_bp_loose_16k | 21 | 1.001 | 1.860 | 0.905 | 0.01010 | 0.1217 |
| fir_bp_tight_16k | 21 | 1.002 | 1.925 | 0.905 | 0.00265 | 0.0381 |
| fir_bs_loose_8k | 22 | 1.000 | 1.502 | 0.909 | 0.01106 | 0.0768 |
| fir_bs_tight_8k | 21 | 1.001 | 1.494 | 0.857 | 0.00237 | 0.0312 |
| fir_bs_loose_16k | 22 | 1.000 | 1.502 | 0.909 | 0.01105 | 0.0760 |
| fir_bs_tight_16k | 21 | 1.013 | 1.498 | 0.905 | 0.00237 | 0.0240 |
| iir_lp_loose_8k | 19 | 1.001 | 2.405 | 0.947 | 0.02891 | 0.1734 |
| iir_lp_tight_8k | 19 | 2.191 | 9.056 | 0.947 | 0.00577 | 0.1210 |
| iir_hp_loose_8k | 19 | 1.251 | 14.500 | 0.947 | 0.02506 | 0.1677 |
| iir_hp_tight_8k | 19 | 1.859 | 12.140 | 0.947 | 0.00594 | 0.0692 |

Same-order subset (descriptive only): 67 occupants; 25/67 have
\(d_{\mathrm{coeff}}>\tau_R\).

## 5. \(\mathrm{FRR}_{\mathrm{ref}}\) (descriptive only)

\[
\mathrm{FRR}_{\mathrm{ref}}
=\frac{\#\{h:\ \mathrm{label}=\mathrm{valid},\ d_{\mathrm{coeff}}(h,h_r)>\tau_R\}}
{\#\{h:\ \mathrm{label}=\mathrm{valid}\}}
=374/416=0.899
\]

By source (descriptive): library 62/92 = 0.674; first-principles
14/24 = 0.583; random 298/300 = 0.993.

No hypothesis test. No claim. No table of oracles.

## Files created

| Path | Role |
|---|---|
| `src/filter_geom.py` | Mechanical cutoffs and band geometry |
| `src/valid_metrics.py` | Post-admission \(d_{\mathrm{coeff}}\) and \(\lvert H\rvert\) RMSE |
| `src/valid_designers.py` | Canonical, library, random-valid designers |
| `src/valid_first_principles.py` | Windowed-sinc and frequency-sampling search |
| `src/first_principles_fir.py` | Added highpass helpers (numpy only) |
| `scripts/generate_valid_occupants.py` | Generation driver |
| `data/valid/canonical/` | 20 canonical \(h_r\) |
| `data/valid/library/` | 92 library occupants + sidecars |
| `data/valid/first_principles/` | 24 first-principles occupants + sidecars |
| `data/valid/random/` | 300 random-valid occupants + sidecars |
| `data/valid/manifest.json` | Combined manifests |
| `data/valid/stats.json` | Counts, rates, diversity |

## Failures

None that block the phase.

`firwin2` on four tight BP/BS tasks and same-order frequency sampling
on twelve FIR tasks are recorded as method-infeasible.

## Recommendation

**READY_FOR_PHASE_2C**

Phase 2C may generate M1–M8 invalids. Do not start evaluation tables
or manuscript edits in that phase unless separately authorized.
