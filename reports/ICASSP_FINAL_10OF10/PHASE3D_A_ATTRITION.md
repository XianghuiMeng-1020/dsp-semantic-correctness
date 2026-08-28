# PHASE 3D-A — Generation attrition

| task | generator | attempts | generation errors | grid-screen fail | continuous valid | continuous invalid | undecided | exact duplicates | H_VALID admitted |
| ---- | --------- | -------: | ----------------: | ---------------: | ---------------: | -----------------: | --------: | ---------------: | ---------------: |
| fir_bp_loose_16k | F1_remez | 12 | 0 | 0 | 12 | 0 | 0 | 1 | 11 |
| fir_bp_loose_16k | F2_firls | 12 | 0 | 0 | 12 | 0 | 0 | 1 | 11 |
| fir_bp_loose_16k | F3_freqsamp | 12 | 0 | 1 | 11 | 0 | 0 | 0 | 11 |
| fir_bp_loose_16k | F4_window | 12 | 0 | 3 | 9 | 0 | 0 | 0 | 9 |
| fir_bp_loose_8k | F1_remez | 12 | 0 | 0 | 12 | 0 | 0 | 1 | 11 |
| fir_bp_loose_8k | F2_firls | 12 | 0 | 0 | 12 | 0 | 0 | 1 | 11 |
| fir_bp_loose_8k | F3_freqsamp | 12 | 0 | 1 | 11 | 0 | 0 | 0 | 11 |
| fir_bp_loose_8k | F4_window | 12 | 0 | 3 | 9 | 0 | 0 | 0 | 9 |
| fir_bp_tight_16k | F1_remez | 12 | 0 | 3 | 9 | 0 | 0 | 0 | 9 |
| fir_bp_tight_16k | F2_firls | 12 | 0 | 5 | 7 | 0 | 0 | 0 | 7 |
| fir_bp_tight_16k | F3_freqsamp | 12 | 0 | 11 | 1 | 0 | 0 | 0 | 1 |
| fir_bp_tight_16k | F4_window | 12 | 0 | 8 | 4 | 0 | 0 | 1 | 3 |
| fir_bp_tight_8k | F1_remez | 12 | 0 | 3 | 9 | 0 | 0 | 0 | 9 |
| fir_bp_tight_8k | F2_firls | 12 | 0 | 5 | 7 | 0 | 0 | 0 | 7 |
| fir_bp_tight_8k | F3_freqsamp | 12 | 0 | 11 | 1 | 0 | 0 | 0 | 1 |
| fir_bp_tight_8k | F4_window | 12 | 0 | 8 | 4 | 0 | 0 | 1 | 3 |
| fir_bs_loose_16k | F1_remez | 12 | 0 | 0 | 12 | 0 | 0 | 1 | 11 |
| fir_bs_loose_16k | F2_firls | 12 | 0 | 0 | 12 | 0 | 0 | 1 | 11 |
| fir_bs_loose_16k | F3_freqsamp | 12 | 0 | 1 | 11 | 0 | 0 | 0 | 11 |
| fir_bs_loose_16k | F4_window | 12 | 0 | 4 | 8 | 0 | 0 | 1 | 7 |
| fir_bs_loose_8k | F1_remez | 12 | 0 | 0 | 12 | 0 | 0 | 1 | 11 |
| fir_bs_loose_8k | F2_firls | 12 | 0 | 0 | 12 | 0 | 0 | 1 | 11 |
| fir_bs_loose_8k | F3_freqsamp | 12 | 0 | 1 | 11 | 0 | 0 | 0 | 11 |
| fir_bs_loose_8k | F4_window | 12 | 0 | 4 | 8 | 0 | 0 | 1 | 7 |
| fir_bs_tight_16k | F1_remez | 12 | 0 | 6 | 6 | 0 | 0 | 0 | 6 |
| fir_bs_tight_16k | F2_firls | 12 | 0 | 6 | 6 | 0 | 0 | 1 | 5 |
| fir_bs_tight_16k | F3_freqsamp | 12 | 0 | 12 | 0 | 0 | 0 | 0 | 0 |
| fir_bs_tight_16k | F4_window | 12 | 0 | 9 | 3 | 0 | 0 | 1 | 2 |
| fir_bs_tight_8k | F1_remez | 12 | 0 | 6 | 6 | 0 | 0 | 0 | 6 |
| fir_bs_tight_8k | F2_firls | 12 | 0 | 6 | 6 | 0 | 0 | 1 | 5 |
| fir_bs_tight_8k | F3_freqsamp | 12 | 0 | 12 | 0 | 0 | 0 | 0 | 0 |
| fir_bs_tight_8k | F4_window | 12 | 0 | 9 | 3 | 0 | 0 | 1 | 2 |
| fir_hp_loose_16k | F1_remez | 12 | 3 | 0 | 9 | 0 | 0 | 1 | 8 |
| fir_hp_loose_16k | F2_firls | 12 | 0 | 0 | 12 | 0 | 0 | 1 | 11 |
| fir_hp_loose_16k | F3_freqsamp | 12 | 0 | 0 | 12 | 0 | 0 | 0 | 12 |
| fir_hp_loose_16k | F4_window | 12 | 0 | 2 | 10 | 0 | 0 | 0 | 10 |
| fir_hp_loose_8k | F1_remez | 12 | 3 | 0 | 9 | 0 | 0 | 1 | 8 |
| fir_hp_loose_8k | F2_firls | 12 | 0 | 0 | 12 | 0 | 0 | 1 | 11 |
| fir_hp_loose_8k | F3_freqsamp | 12 | 0 | 0 | 12 | 0 | 0 | 0 | 12 |
| fir_hp_loose_8k | F4_window | 12 | 0 | 2 | 10 | 0 | 0 | 0 | 10 |
| fir_hp_tight_16k | F1_remez | 12 | 0 | 2 | 10 | 0 | 0 | 0 | 10 |
| fir_hp_tight_16k | F2_firls | 12 | 0 | 3 | 9 | 0 | 0 | 1 | 8 |
| fir_hp_tight_16k | F3_freqsamp | 12 | 0 | 10 | 2 | 0 | 0 | 0 | 2 |
| fir_hp_tight_16k | F4_window | 12 | 0 | 8 | 4 | 0 | 0 | 0 | 4 |
| fir_hp_tight_8k | F1_remez | 12 | 0 | 2 | 10 | 0 | 0 | 0 | 10 |
| fir_hp_tight_8k | F2_firls | 12 | 0 | 3 | 9 | 0 | 0 | 1 | 8 |
| fir_hp_tight_8k | F3_freqsamp | 12 | 0 | 10 | 2 | 0 | 0 | 0 | 2 |
| fir_hp_tight_8k | F4_window | 12 | 0 | 8 | 4 | 0 | 0 | 0 | 4 |
| fir_lp_loose_16k | F1_remez | 12 | 0 | 0 | 12 | 0 | 0 | 1 | 11 |
| fir_lp_loose_16k | F2_firls | 12 | 0 | 0 | 12 | 0 | 0 | 1 | 11 |
| fir_lp_loose_16k | F3_freqsamp | 12 | 0 | 0 | 12 | 0 | 0 | 0 | 12 |
| fir_lp_loose_16k | F4_window | 12 | 0 | 2 | 10 | 0 | 0 | 0 | 10 |
| fir_lp_loose_8k | F1_remez | 12 | 0 | 0 | 12 | 0 | 0 | 1 | 11 |
| fir_lp_loose_8k | F2_firls | 12 | 0 | 0 | 12 | 0 | 0 | 1 | 11 |
| fir_lp_loose_8k | F3_freqsamp | 12 | 0 | 0 | 12 | 0 | 0 | 0 | 12 |
| fir_lp_loose_8k | F4_window | 12 | 0 | 2 | 10 | 0 | 0 | 0 | 10 |
| fir_lp_tight_16k | F1_remez | 12 | 0 | 2 | 10 | 0 | 0 | 0 | 10 |
| fir_lp_tight_16k | F2_firls | 12 | 0 | 3 | 9 | 0 | 0 | 0 | 9 |
| fir_lp_tight_16k | F3_freqsamp | 12 | 0 | 9 | 3 | 0 | 0 | 0 | 3 |
| fir_lp_tight_16k | F4_window | 12 | 0 | 8 | 4 | 0 | 0 | 0 | 4 |
| fir_lp_tight_8k | F1_remez | 12 | 0 | 2 | 10 | 0 | 0 | 0 | 10 |
| fir_lp_tight_8k | F2_firls | 12 | 0 | 3 | 9 | 0 | 0 | 0 | 9 |
| fir_lp_tight_8k | F3_freqsamp | 12 | 0 | 9 | 3 | 0 | 0 | 0 | 3 |
| fir_lp_tight_8k | F4_window | 12 | 0 | 8 | 4 | 0 | 0 | 0 | 4 |
| iir_hp_loose_8k | I1_butter | 12 | 0 | 2 | 10 | 0 | 0 | 0 | 10 |
| iir_hp_loose_8k | I2_cheby1 | 12 | 0 | 2 | 10 | 0 | 0 | 0 | 10 |
| iir_hp_loose_8k | I3_cheby2 | 12 | 0 | 0 | 12 | 0 | 0 | 0 | 12 |
| iir_hp_loose_8k | I4_ellip | 12 | 0 | 2 | 10 | 0 | 0 | 0 | 10 |
| iir_hp_tight_8k | I1_butter | 12 | 0 | 11 | 1 | 0 | 0 | 0 | 1 |
| iir_hp_tight_8k | I2_cheby1 | 12 | 0 | 8 | 4 | 0 | 0 | 0 | 4 |
| iir_hp_tight_8k | I3_cheby2 | 12 | 0 | 11 | 1 | 0 | 0 | 0 | 1 |
| iir_hp_tight_8k | I4_ellip | 12 | 0 | 5 | 7 | 0 | 0 | 0 | 7 |
| iir_lp_loose_8k | I1_butter | 12 | 0 | 1 | 11 | 0 | 0 | 0 | 11 |
| iir_lp_loose_8k | I2_cheby1 | 12 | 0 | 2 | 10 | 0 | 0 | 0 | 10 |
| iir_lp_loose_8k | I3_cheby2 | 12 | 0 | 2 | 10 | 0 | 0 | 0 | 10 |
| iir_lp_loose_8k | I4_ellip | 12 | 0 | 2 | 10 | 0 | 0 | 0 | 10 |
| iir_lp_tight_8k | I1_butter | 12 | 0 | 12 | 0 | 0 | 0 | 0 | 0 |
| iir_lp_tight_8k | I2_cheby1 | 12 | 0 | 8 | 4 | 0 | 0 | 0 | 4 |
| iir_lp_tight_8k | I3_cheby2 | 12 | 0 | 6 | 6 | 0 | 0 | 0 | 6 |
| iir_lp_tight_8k | I4_ellip | 12 | 0 | 4 | 8 | 0 | 0 | 0 | 8 |

## Invalid mutations

| task | mutation | eligible progenitors | attempts | certified invalid | remained valid | undecided | duplicates | admitted |
| ---- | -------- | -------------------: | -------: | ----------------: | -------------: | --------: | ---------: | -------: |
| fir_bp_loose_16k | M1 | 42 | 168 | 0 | 168 | 0 | 0 | 0 |
| fir_bp_loose_16k | M2 | 42 | 168 | 0 | 168 | 0 | 0 | 0 |
| fir_bp_loose_8k | M1 | 42 | 168 | 0 | 168 | 0 | 0 | 0 |
| fir_bp_loose_8k | M2 | 42 | 168 | 0 | 168 | 0 | 0 | 0 |
| fir_bp_tight_16k | M1 | 20 | 80 | 3 | 77 | 0 | 0 | 3 |
| fir_bp_tight_16k | M2 | 20 | 80 | 21 | 59 | 0 | 0 | 20 |
| fir_bp_tight_8k | M1 | 20 | 80 | 2 | 78 | 0 | 0 | 2 |
| fir_bp_tight_8k | M2 | 20 | 80 | 21 | 59 | 0 | 1 | 19 |
| fir_bs_loose_16k | M1 | 40 | 160 | 0 | 160 | 0 | 0 | 0 |
| fir_bs_loose_16k | M2 | 40 | 160 | 0 | 160 | 0 | 0 | 0 |
| fir_bs_loose_8k | M1 | 40 | 160 | 0 | 160 | 0 | 0 | 0 |
| fir_bs_loose_8k | M2 | 40 | 160 | 0 | 160 | 0 | 0 | 0 |
| fir_bs_tight_16k | M1 | 13 | 52 | 3 | 49 | 0 | 0 | 3 |
| fir_bs_tight_16k | M2 | 13 | 52 | 11 | 41 | 0 | 0 | 11 |
| fir_bs_tight_8k | M1 | 13 | 52 | 1 | 51 | 0 | 0 | 1 |
| fir_bs_tight_8k | M2 | 13 | 52 | 13 | 39 | 0 | 0 | 13 |
| fir_hp_loose_16k | M1 | 41 | 164 | 0 | 164 | 0 | 0 | 0 |
| fir_hp_loose_16k | M2 | 41 | 164 | 0 | 164 | 0 | 0 | 0 |
| fir_hp_loose_8k | M1 | 41 | 164 | 0 | 164 | 0 | 0 | 0 |
| fir_hp_loose_8k | M2 | 41 | 164 | 0 | 164 | 0 | 0 | 0 |
| fir_hp_tight_16k | M1 | 24 | 96 | 6 | 90 | 0 | 0 | 6 |
| fir_hp_tight_16k | M2 | 24 | 96 | 24 | 72 | 0 | 0 | 24 |
| fir_hp_tight_8k | M1 | 24 | 96 | 5 | 91 | 0 | 0 | 5 |
| fir_hp_tight_8k | M2 | 24 | 96 | 23 | 73 | 0 | 0 | 23 |
| fir_lp_loose_16k | M1 | 44 | 176 | 0 | 176 | 0 | 0 | 0 |
| fir_lp_loose_16k | M2 | 44 | 176 | 0 | 176 | 0 | 0 | 0 |
| fir_lp_loose_8k | M1 | 44 | 176 | 0 | 176 | 0 | 0 | 0 |
| fir_lp_loose_8k | M2 | 44 | 176 | 0 | 176 | 0 | 0 | 0 |
| fir_lp_tight_16k | M1 | 26 | 104 | 5 | 99 | 0 | 0 | 3 |
| fir_lp_tight_16k | M2 | 26 | 104 | 29 | 75 | 0 | 0 | 26 |
| fir_lp_tight_8k | M1 | 26 | 104 | 3 | 101 | 0 | 0 | 3 |
| fir_lp_tight_8k | M2 | 26 | 104 | 27 | 77 | 0 | 0 | 26 |
| iir_hp_loose_8k | M1 | 42 | 168 | 31 | 137 | 0 | 0 | 24 |
| iir_hp_loose_8k | M2 | 42 | 168 | 10 | 158 | 0 | 0 | 6 |
| iir_hp_tight_8k | M1 | 13 | 52 | 21 | 31 | 0 | 0 | 13 |
| iir_hp_tight_8k | M2 | 13 | 52 | 12 | 40 | 0 | 0 | 10 |
| iir_lp_loose_8k | M1 | 41 | 164 | 28 | 136 | 0 | 0 | 22 |
| iir_lp_loose_8k | M2 | 41 | 164 | 16 | 148 | 0 | 0 | 11 |
| iir_lp_tight_8k | M1 | 18 | 72 | 56 | 16 | 0 | 0 | 18 |
| iir_lp_tight_8k | M2 | 18 | 72 | 36 | 36 | 0 | 0 | 18 |
