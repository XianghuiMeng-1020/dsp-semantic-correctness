# PHASE 3A — Reference hierarchy

Level 1 = frozen canonical \(G_r\). Level 2 = Phase-1 `best_observed_valid_reference` \(G_{\mathrm{obs}}^{\star}\). Level 3 = ambient-center margin \(\Gamma^{\mathrm{amb}}\).

## Coefficient

- Type A (canonical fail → observed fail → ambient fail): 1
- Type B (canonical fail → observed fail → ambient succeeds): 19
- Type C (canonical fail → observed succeeds): 0
- Type D (canonical succeeds): 0

| task | canonical G | best-observed G* | ambient status | ambient margin | exact single-center exists | type | certificate |
| ---- | ----------: | ---------------: | -------------- | -------------: | -------------------------- | ---- | ----------- |
| fir_lp_loose_8k | -1.5079817 | -0.50108825 | AMBIENT_SEPARABLE | +INF | 1 | B | HIGH_PRECISION_DUAL_CERTIFICATE |
| fir_lp_tight_8k | -1.4603262 | -0.42495196 | AMBIENT_SEPARABLE | +INF | 1 | B | HIGH_PRECISION_DUAL_CERTIFICATE |
| fir_lp_loose_16k | -1.484841 | -0.49221851 | AMBIENT_SEPARABLE | +INF | 1 | B | HIGH_PRECISION_DUAL_CERTIFICATE |
| fir_lp_tight_16k | -1.4805876 | -0.4060899 | AMBIENT_SEPARABLE | +INF | 1 | B | HIGH_PRECISION_DUAL_CERTIFICATE |
| fir_hp_loose_8k | -1.475535 | -0.6463535 | AMBIENT_SEPARABLE | +INF | 1 | B | HIGH_PRECISION_DUAL_CERTIFICATE |
| fir_hp_tight_8k | -1.4469103 | -0.41032588 | AMBIENT_SEPARABLE | +INF | 1 | B | HIGH_PRECISION_DUAL_CERTIFICATE |
| fir_hp_loose_16k | -1.4959156 | -0.65725324 | AMBIENT_SEPARABLE | +INF | 1 | B | HIGH_PRECISION_DUAL_CERTIFICATE |
| fir_hp_tight_16k | -1.4465031 | -0.41244872 | AMBIENT_SEPARABLE | +INF | 1 | B | HIGH_PRECISION_DUAL_CERTIFICATE |
| fir_bp_loose_8k | -1.5973294 | -0.58219259 | AMBIENT_SEPARABLE | +INF | 1 | B | HIGH_PRECISION_DUAL_CERTIFICATE |
| fir_bp_tight_8k | -1.4950833 | -0.41152066 | AMBIENT_SEPARABLE | +INF | 1 | B | HIGH_PRECISION_DUAL_CERTIFICATE |
| fir_bp_loose_16k | -1.6120386 | -0.56768188 | AMBIENT_SEPARABLE | +INF | 1 | B | HIGH_PRECISION_DUAL_CERTIFICATE |
| fir_bp_tight_16k | -1.5147614 | -0.39858089 | AMBIENT_SEPARABLE | +INF | 1 | B | HIGH_PRECISION_DUAL_CERTIFICATE |
| fir_bs_loose_8k | -1.4786604 | -0.50500578 | AMBIENT_SEPARABLE | +INF | 1 | B | HIGH_PRECISION_DUAL_CERTIFICATE |
| fir_bs_tight_8k | -1.4208344 | -0.39889151 | AMBIENT_SEPARABLE | +INF | 1 | B | HIGH_PRECISION_DUAL_CERTIFICATE |
| fir_bs_loose_16k | -1.534753 | -0.46426589 | AMBIENT_SEPARABLE | +INF | 1 | B | HIGH_PRECISION_DUAL_CERTIFICATE |
| fir_bs_tight_16k | -1.4478007 | -0.39952662 | AMBIENT_SEPARABLE | +INF | 1 | B | HIGH_PRECISION_DUAL_CERTIFICATE |
| iir_lp_loose_8k | -66.533258 | -0.042232562 | NO_AMBIENT_CENTER | -0.02740973 | 0 | A | HIGH_PRECISION_DUAL_CERTIFICATE |
| iir_lp_tight_8k | -11.304934 | -0.046314258 | AMBIENT_SEPARABLE | 1.0589776e-06 | 1 | B | EXACT_RATIONAL_CERTIFICATE |
| iir_hp_loose_8k | -22.035263 | -0.17180463 | AMBIENT_SEPARABLE | 0.0077007476 | 1 | B | EXACT_RATIONAL_CERTIFICATE |
| iir_hp_tight_8k | -11.876136 | -0.28093865 | AMBIENT_SEPARABLE | 0.0068906651 | 1 | B | EXACT_RATIONAL_CERTIFICATE |

## Response (secondary)

- Type A: 0
- Type B: 18
- Type C: 1
- Type D: 1

| task | canonical G | best-observed G* | ambient status | ambient margin | type | precision |
| ---- | ----------: | ---------------: | -------------- | -------------: | ---- | --------- |
| fir_lp_loose_8k | -0.031194893 | -0.0081107117 | AMBIENT_SEPARABLE | +INF | B | undecided |
| fir_lp_tight_8k | -0.0069606196 | -2.2224504e-05 | AMBIENT_SEPARABLE | +INF | B | undecided |
| fir_lp_loose_16k | -0.031194893 | -0.0081107117 | AMBIENT_SEPARABLE | +INF | B | undecided |
| fir_lp_tight_16k | -0.0069606196 | -2.2224504e-05 | AMBIENT_SEPARABLE | +INF | B | undecided |
| fir_hp_loose_8k | -0.032258594 | -0.021254659 | AMBIENT_SEPARABLE | +INF | B | undecided |
| fir_hp_tight_8k | -0.0067192885 | -0.0034941385 | AMBIENT_SEPARABLE | +INF | B | stable |
| fir_hp_loose_16k | -0.032258594 | -0.021254659 | AMBIENT_SEPARABLE | +INF | B | undecided |
| fir_hp_tight_16k | -0.0067192885 | -0.0034941385 | AMBIENT_SEPARABLE | +INF | B | undecided |
| fir_bp_loose_8k | -0.036220986 | -0.0034585059 | AMBIENT_SEPARABLE | +INF | B | undecided |
| fir_bp_tight_8k | -0.0077477501 | -0.00040234824 | AMBIENT_SEPARABLE | +INF | B | undecided |
| fir_bp_loose_16k | -0.036220986 | -0.0034585059 | AMBIENT_SEPARABLE | +INF | B | undecided |
| fir_bp_tight_16k | -0.0077477501 | -0.00040234559 | AMBIENT_SEPARABLE | +INF | B | undecided |
| fir_bs_loose_8k | -0.038128933 | -0.015672925 | AMBIENT_SEPARABLE | +INF | B | undecided |
| fir_bs_tight_8k | -0.0082378695 | -0.0012599213 | AMBIENT_SEPARABLE | +INF | B | stable |
| fir_bs_loose_16k | -0.038128933 | -0.015672925 | AMBIENT_SEPARABLE | +INF | B | stable |
| fir_bs_tight_16k | -0.0082378695 | -0.0012599213 | AMBIENT_SEPARABLE | +INF | B | undecided |
| iir_lp_loose_8k | -0.057121309 | -0.0049969025 | AMBIENT_SEPARABLE | +INF | B | stable |
| iir_lp_tight_8k | -0.0034238405 | 0.0016863272 | AMBIENT_SEPARABLE | 202.60234 | C | stable |
| iir_hp_loose_8k | -0.018423317 | -0.0017348388 | AMBIENT_SEPARABLE | 579.12517 | B | stable |
| iir_hp_tight_8k | 3.8046047e-06 | 0.002817539 | AMBIENT_SEPARABLE | 603.97978 | D | stable |

## Claim guardrail

Even if every coefficient task is Type A, the supported statement is only:

> No single Euclidean-distance threshold center in the evaluated coefficient representation can recover specification membership over the frozen finite universe.
