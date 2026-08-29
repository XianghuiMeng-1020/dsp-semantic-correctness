# PHASE 3B — Observed-valid reference catalog complexity

Primary quantity: \(K_{t,\mathrm{obs}}^{\star}\), the minimum number of observed valid realizations such that the existing min-distance / common-threshold oracle exactly recovers frozen membership. Set-cover is used only as a computational reduction.

| task | metric | n_valid | n_invalid | K=1 | K=3 | K=5 | all-library | K*_obs | K*/n_valid |
| ---- | ------ | ------: | --------: | --- | --- | --- | ----------- | -----: | ---------: |
| fir_lp_loose_8k | coeff | 89 | 15 | 0 | 0 | 0 | 0 | 42 | 0.47191 |
| fir_lp_tight_8k | coeff | 104 | 15 | 0 | 0 | 0 | 0 | 84 | 0.807692 |
| fir_lp_loose_16k | coeff | 89 | 15 | 0 | 0 | 0 | 0 | 41 | 0.460674 |
| fir_lp_tight_16k | coeff | 104 | 15 | 0 | 0 | 0 | 0 | 84 | 0.807692 |
| fir_hp_loose_8k | coeff | 90 | 15 | 0 | 0 | 0 | 0 | 38 | 0.422222 |
| fir_hp_tight_8k | coeff | 104 | 15 | 0 | 0 | 0 | 0 | 20 | 0.192308 |
| fir_hp_loose_16k | coeff | 90 | 15 | 0 | 0 | 0 | 0 | 23 | 0.255556 |
| fir_hp_tight_16k | coeff | 104 | 15 | 0 | 0 | 0 | 0 | 17 | 0.163462 |
| fir_bp_loose_8k | coeff | 87 | 15 | 0 | 0 | 0 | 0 | 48 | 0.551724 |
| fir_bp_tight_8k | coeff | 111 | 15 | 0 | 0 | 0 | 0 | 23 | 0.207207 |
| fir_bp_loose_16k | coeff | 87 | 15 | 0 | 0 | 0 | 0 | 49 | 0.563218 |
| fir_bp_tight_16k | coeff | 111 | 15 | 0 | 0 | 0 | 0 | 21 | 0.189189 |
| fir_bs_loose_8k | coeff | 90 | 15 | 0 | 0 | 0 | 0 | 19 | 0.211111 |
| fir_bs_tight_8k | coeff | 123 | 15 | 0 | 0 | 0 | 0 | 113 | 0.918699 |
| fir_bs_loose_16k | coeff | 90 | 15 | 0 | 0 | 0 | 0 | 21 | 0.233333 |
| fir_bs_tight_16k | coeff | 123 | 15 | 0 | 0 | 0 | 0 | 112 | 0.910569 |
| iir_lp_loose_8k | coeff | 19 | 16 | 0 | 0 | 0 | 0 | 15 | 0.789474 |
| iir_lp_tight_8k | coeff | 19 | 16 | 0 | 0 | 0 | 0 | 19 | 1 |
| iir_hp_loose_8k | coeff | 19 | 16 | 0 | 0 | 0 | 0 | 17 | 0.894737 |
| iir_hp_tight_8k | coeff | 19 | 16 | 0 | 0 | 0 | 0 | 19 | 1 |

## Response

| fir_lp_loose_8k | resp | 89 | 15 | 0 | 0 | 0 | 0 | 25 | 0.280899 |
| fir_lp_tight_8k | resp | 104 | 15 | 0 | 0 | 0 | 0 | 2 | 0.0192308 |
| fir_lp_loose_16k | resp | 89 | 15 | 0 | 0 | 0 | 0 | 25 | 0.280899 |
| fir_lp_tight_16k | resp | 104 | 15 | 0 | 0 | 0 | 0 | 2 | 0.0192308 |
| fir_hp_loose_8k | resp | 90 | 15 | 0 | 0 | 0 | 0 | 17 | 0.188889 |
| fir_hp_tight_8k | resp | 104 | 15 | 0 | 0 | 0 | 0 | 48 | 0.461538 |
| fir_hp_loose_16k | resp | 90 | 15 | 0 | 0 | 0 | 0 | 17 | 0.188889 |
| fir_hp_tight_16k | resp | 104 | 15 | 0 | 0 | 0 | 0 | 49 | 0.471154 |
| fir_bp_loose_8k | resp | 87 | 15 | 0 | 0 | 0 | 0 | 18 | 0.206897 |
| fir_bp_tight_8k | resp | 111 | 15 | 0 | 0 | 0 | 0 | 81 | 0.72973 |
| fir_bp_loose_16k | resp | 87 | 15 | 0 | 0 | 0 | 0 | 18 | 0.206897 |
| fir_bp_tight_16k | resp | 111 | 15 | 0 | 0 | 0 | 0 | 83 | 0.747748 |
| fir_bs_loose_8k | resp | 90 | 15 | 0 | 0 | 0 | 0 | 26 | 0.288889 |
| fir_bs_tight_8k | resp | 123 | 15 | 0 | 0 | 0 | 0 | 4 | 0.0325203 |
| fir_bs_loose_16k | resp | 90 | 15 | 0 | 0 | 0 | 0 | 26 | 0.288889 |
| fir_bs_tight_16k | resp | 123 | 15 | 0 | 0 | 0 | 0 | 4 | 0.0325203 |
| iir_lp_loose_8k | resp | 19 | 16 | 0 | 0 | 0 | 0 | 4 | 0.210526 |
| iir_lp_tight_8k | resp | 19 | 16 | 0 | 0 | 0 | 0 | 1 | 0.0526316 |
| iir_hp_loose_8k | resp | 19 | 16 | 0 | 0 | 0 | 0 | 2 | 0.105263 |
| iir_hp_tight_8k | resp | 19 | 16 | 1 | 0 | 0 | 0 | 1 | 0.0526316 |