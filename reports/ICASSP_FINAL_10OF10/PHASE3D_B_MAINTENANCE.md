# PHASE 3D-B — Catalog maintenance (not a new algorithm)

Phase-3B K* is unaltered. V+ = V_base union H_VALID. Invalids remain the frozen base set.

- Coeff tasks exact / bounded: 20 / 0
- Expanded median K* coeff: 55
- Median ΔK / relative growth: 15.5 / 0.524845
- LOW / MODERATE / HIGH: 3 / 4 / 13
- Tasks with M*>0: 20; median M*=15.5; max M*=37
- Median / max J*: 21.5 / 37
- Verdict: `MIXED`

| task | K*_base | H_VALID n | K*_expanded | ΔK | relative growth | rho_base | rho_expanded |
| ---- | ------: | --------: | ----------: | -: | --------------: | -------: | -----------: |
| fir_lp_loose_8k | 42 | 44 | 76 | 34 | 0.809524 | 0.47191 | 0.571429 |
| fir_lp_tight_8k | 84 | 26 | 72 | -12 | -0.142857 | 0.807692 | 0.553846 |
| fir_lp_loose_16k | 41 | 44 | 75 | 34 | 0.829268 | 0.460674 | 0.56391 |
| fir_lp_tight_16k | 84 | 26 | 73 | -11 | -0.130952 | 0.807692 | 0.561538 |
| fir_hp_loose_8k | 38 | 41 | 65 | 27 | 0.710526 | 0.422222 | 0.496183 |
| fir_hp_tight_8k | 20 | 24 | 25 | 5 | 0.25 | 0.192308 | 0.195312 |
| fir_hp_loose_16k | 23 | 41 | 34 | 11 | 0.478261 | 0.255556 | 0.259542 |
| fir_hp_tight_16k | 17 | 24 | 25 | 8 | 0.470588 | 0.163462 | 0.195312 |
| fir_bp_loose_8k | 48 | 42 | 77 | 29 | 0.604167 | 0.551724 | 0.596899 |
| fir_bp_tight_8k | 23 | 20 | 30 | 7 | 0.304348 | 0.207207 | 0.229008 |
| fir_bp_loose_16k | 49 | 42 | 77 | 28 | 0.571429 | 0.563218 | 0.596899 |
| fir_bp_tight_16k | 21 | 20 | 26 | 5 | 0.238095 | 0.189189 | 0.198473 |
| fir_bs_loose_8k | 19 | 40 | 53 | 34 | 1.78947 | 0.211111 | 0.407692 |
| fir_bs_tight_8k | 113 | 13 | 126 | 13 | 0.115044 | 0.918699 | 0.926471 |
| fir_bs_loose_16k | 21 | 40 | 56 | 35 | 1.66667 | 0.233333 | 0.430769 |
| fir_bs_tight_16k | 112 | 13 | 125 | 13 | 0.116071 | 0.910569 | 0.919118 |
| iir_lp_loose_8k | 15 | 41 | 40 | 25 | 1.66667 | 0.789474 | 0.666667 |
| iir_lp_tight_8k | 19 | 18 | 37 | 18 | 0.947368 | 1 | 1 |
| iir_hp_loose_8k | 17 | 42 | 54 | 37 | 2.17647 | 0.894737 | 0.885246 |
| iir_hp_tight_8k | 19 | 13 | 19 | 0 | 0 | 1 | 0.59375 |

| task | original K* | prospective valid n | transfer rejected | J* added references | final catalog size |
| ---- | ----------: | ------------------: | ----------------: | ------------------: | -----------------: |
| fir_lp_loose_8k | 42 | 44 | 41 | 34 | 76 |
| fir_lp_tight_8k | 84 | 26 | 25 | 25 | 109 |
| fir_lp_loose_16k | 41 | 44 | 42 | 35 | 76 |
| fir_lp_tight_16k | 84 | 26 | 26 | 26 | 110 |
| fir_hp_loose_8k | 38 | 41 | 33 | 27 | 65 |
| fir_hp_tight_8k | 20 | 24 | 12 | 5 | 25 |
| fir_hp_loose_16k | 23 | 41 | 40 | 11 | 34 |
| fir_hp_tight_16k | 17 | 24 | 21 | 8 | 25 |
| fir_bp_loose_8k | 48 | 42 | 41 | 29 | 77 |
| fir_bp_tight_8k | 23 | 20 | 17 | 7 | 30 |
| fir_bp_loose_16k | 49 | 42 | 40 | 29 | 78 |
| fir_bp_tight_16k | 21 | 20 | 14 | 5 | 26 |
| fir_bs_loose_8k | 19 | 40 | 27 | None | None |
| fir_bs_tight_8k | 113 | 13 | 13 | 13 | 126 |
| fir_bs_loose_16k | 21 | 40 | 38 | None | None |
| fir_bs_tight_16k | 112 | 13 | 13 | 13 | 125 |
| iir_lp_loose_8k | 15 | 41 | 34 | 26 | 41 |
| iir_lp_tight_8k | 19 | 18 | 18 | 18 | 37 |
| iir_hp_loose_8k | 17 | 42 | 40 | 37 | 54 |
| iir_hp_tight_8k | 19 | 13 | 13 | 13 | 32 |
