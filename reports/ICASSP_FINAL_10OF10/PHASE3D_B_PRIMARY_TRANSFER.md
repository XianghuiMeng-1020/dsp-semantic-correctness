# PHASE 3D-B — Primary prospective valid-realization transfer

Catalogs and thresholds were frozen before scoring. H_VALID was not used to select
catalogs or \(\tau\). Coefficient and response are separate. Reference rejection is
not evidence of invalidity.

## Coefficient

- Pooled transfer: `0.107492` (66 / 614)
- Task-macro mean / median: `0.105569` / `0.047619`
- Min / max: `0` / `0.5`
- Tasks ≥95% / 75–95% / <75%: 0 / 0 / 20
- FIR / IIR macro: `0.118315` / `0.0545877`
- Loose / tight: `0.0997928` / `0.111346`
- LP / HP / BP / BS: `0.0538049` / `0.148689` / `0.130357` / `0.09375`
- Verdict: `PROSPECTIVE_TRANSFER_STRONG_FAILURE`

| task | H_VALID n | K*_base | tau_maxsafe | accepted | rejected | transfer | external FRR |
| ---- | --------: | ------: | ----------: | -------: | -------: | -------: | -----------: |
| fir_bp_loose_16k | 42 | 49 | 0.0514138 | 2 | 40 | 0.047619 | 0.952381 |
| fir_bp_loose_8k | 42 | 48 | 0.0514138 | 1 | 41 | 0.0238095 | 0.97619 |
| fir_bp_tight_16k | 20 | 21 | 0.197218 | 6 | 14 | 0.3 | 0.7 |
| fir_bp_tight_8k | 20 | 23 | 0.197218 | 3 | 17 | 0.15 | 0.85 |
| fir_bs_loose_16k | 40 | 21 | 0.353604 | 2 | 38 | 0.05 | 0.95 |
| fir_bs_loose_8k | 40 | 19 | 0.353604 | 13 | 27 | 0.325 | 0.675 |
| fir_bs_tight_16k | 13 | 112 | 0.00236357 | 0 | 13 | 0 | 1 |
| fir_bs_tight_8k | 13 | 113 | 0.00236357 | 0 | 13 | 0 | 1 |
| fir_hp_loose_16k | 41 | 23 | 0.220554 | 1 | 40 | 0.0243902 | 0.97561 |
| fir_hp_loose_8k | 41 | 38 | 0.0340684 | 8 | 33 | 0.195122 | 0.804878 |
| fir_hp_tight_16k | 24 | 17 | 0.154655 | 3 | 21 | 0.125 | 0.875 |
| fir_hp_tight_8k | 24 | 20 | 0.154655 | 12 | 12 | 0.5 | 0.5 |
| fir_lp_loose_16k | 44 | 41 | 0.0351523 | 2 | 42 | 0.0454545 | 0.954545 |
| fir_lp_loose_8k | 44 | 42 | 0.0351523 | 3 | 41 | 0.0681818 | 0.931818 |
| fir_lp_tight_16k | 26 | 84 | 0.00254358 | 0 | 26 | 0 | 1 |
| fir_lp_tight_8k | 26 | 84 | 0.00254358 | 1 | 25 | 0.0384615 | 0.961538 |
| iir_hp_loose_8k | 42 | 17 | 0.0761228 | 2 | 40 | 0.047619 | 0.952381 |
| iir_hp_tight_8k | 13 | 19 | 0.00581006 | 0 | 13 | 0 | 1 |
| iir_lp_loose_8k | 41 | 15 | 0.127917 | 7 | 34 | 0.170732 | 0.829268 |
| iir_lp_tight_8k | 18 | 19 | 1.80162e-05 | 0 | 18 | 0 | 1 |

## Response

- Pooled transfer: `0.952769` (585 / 614)
- Task-macro mean / median: `0.946169` / `1`
- Tasks ≥95% / <75%: 15 / 1
- FIR / IIR macro: `0.94643` / `0.945122`
- Verdict: `PROSPECTIVE_TRANSFER_MIXED`

| task | H_VALID n | K*_base | tau_maxsafe | accepted | rejected | transfer | external FRR |
| ---- | --------: | ------: | ----------: | -------: | -------: | -------: | -----------: |
| fir_bp_loose_16k | 42 | 18 | 0.0152183 | 42 | 0 | 1 | 0 |
| fir_bp_loose_8k | 42 | 18 | 0.0152253 | 42 | 0 | 1 | 0 |
| fir_bp_tight_16k | 20 | 83 | 0.00127269 | 15 | 5 | 0.75 | 0.25 |
| fir_bp_tight_8k | 20 | 81 | 0.00127269 | 14 | 6 | 0.7 | 0.3 |
| fir_bs_loose_16k | 40 | 26 | 0.0191565 | 39 | 1 | 0.975 | 0.025 |
| fir_bs_loose_8k | 40 | 26 | 0.0191565 | 39 | 1 | 0.975 | 0.025 |
| fir_bs_tight_16k | 13 | 4 | 0.00780945 | 13 | 0 | 1 | 0 |
| fir_bs_tight_8k | 13 | 4 | 0.00780945 | 13 | 0 | 1 | 0 |
| fir_hp_loose_16k | 41 | 17 | 0.0168909 | 40 | 1 | 0.97561 | 0.0243902 |
| fir_hp_loose_8k | 41 | 17 | 0.0168909 | 40 | 1 | 0.97561 | 0.0243902 |
| fir_hp_tight_16k | 24 | 49 | 0.00213034 | 21 | 3 | 0.875 | 0.125 |
| fir_hp_tight_8k | 24 | 48 | 0.00240206 | 22 | 2 | 0.916667 | 0.0833333 |
| fir_lp_loose_16k | 44 | 25 | 0.0105763 | 44 | 0 | 1 | 0 |
| fir_lp_loose_8k | 44 | 25 | 0.0105763 | 44 | 0 | 1 | 0 |
| fir_lp_tight_16k | 26 | 2 | 0.00706492 | 26 | 0 | 1 | 0 |
| fir_lp_tight_8k | 26 | 2 | 0.00685937 | 26 | 0 | 1 | 0 |
| iir_hp_loose_8k | 42 | 2 | 0.0457475 | 42 | 0 | 1 | 0 |
| iir_hp_tight_8k | 13 | 1 | 0.00961864 | 13 | 0 | 1 | 0 |
| iir_lp_loose_8k | 41 | 4 | 0.0246051 | 32 | 9 | 0.780488 | 0.219512 |
| iir_lp_tight_8k | 18 | 1 | 0.0108603 | 18 | 0 | 1 | 0 |

## Midpoint-threshold sensitivity

- Coefficient: `ROBUST_TO_THRESHOLD_CHOICE`
- Response: `ROBUST_TO_THRESHOLD_CHOICE`

Primary remains `tau_maxsafe`.
