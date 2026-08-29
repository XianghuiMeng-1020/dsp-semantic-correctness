# PHASE 1 — Best-observed-valid-reference

Phase 1 is confirmatory with respect to the frozen Phase-0 scientific corpus. No occupant, task, specification, distance metric, or original label was changed.

## Quantity

Finite-universe, observed-valid-reference gap

$$G_{\mathrm{obs},t}^{\star} = \max_{r \in V_t \cap U_t} \bigl( D_I(r) - D_V(r) \bigr)$$

with the paper's existing $d_{\mathrm{coeff,mag\text{-}equiv}}$ and $d_{\mathrm{resp,band}}$.

**Limitation (every use):** this is *not* unrestricted $G^*$. It maximises only over frozen valid occupants in $\mathcal{U}_t$. It does not rule out an unobserved valid realisation or an arbitrary ambient-space centre.

## Primary universe (manuscript confirmatory $\mathcal{U}_t$)

manuscript confirmatory U_t: constructed+probe valids; mechanism+boundary invalids

- constructed valids: 412
- probe valids: 1260
- mechanism invalids: 144
- boundary invalids: 160

Secondary mechanism-only / boundary-only decompositions are in `results/icassp_10of10_hardening/phase1/best_observed_reference_decomposition.json` and **must not replace** this primary table.

## Coefficient-distance oracle

- Tasks evaluated: 20
- $G_{\mathrm{obs}}^\star > 0$: 0
- $G_{\mathrm{obs}}^\star = 0$: 0
- $G_{\mathrm{obs}}^\star < 0$: 20
- median / min / max: -0.41198469 / -0.65725324 / -0.042232562
- Canonical non-separable: 20
- Best-observed non-separable: 20
- Separability status changes: 0
- Largest improvement (not necessarily a rescue): {'task_id': 'iir_lp_loose_8k', 'improvement': 66.49102531173565, 'canonical_G': -66.53325787349704, 'Gobs_star': -0.04223256176137824}

| task | metric | n_valid | n_invalid | canonical_G | best_reference_id | best_DV | best_DI | Gobs_star | exact_separable |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fir_lp_loose_8k | coeff | 89 | 15 | -1.5079817 | data/icassp_10of10/probe_candidates/fir_lp_loose_8k__alternating__max.npy | 1.1657133 | 0.66462505 | -0.50108825 | 0 |
| fir_lp_tight_8k | coeff | 104 | 15 | -1.4603262 | data/valid/random/fir_lp_tight_8k__r017.npy | 1.4423656 | 1.0174136 | -0.42495196 | 0 |
| fir_lp_loose_16k | coeff | 89 | 15 | -1.484841 | data/icassp_10of10/probe_candidates/fir_lp_loose_16k__alternating__max.npy | 1.1568436 | 0.66462505 | -0.49221851 | 0 |
| fir_lp_tight_16k | coeff | 104 | 15 | -1.4805876 | data/valid/random/fir_lp_tight_16k__r008.npy | 1.4226536 | 1.0165637 | -0.4060899 | 0 |
| fir_hp_loose_8k | coeff | 90 | 15 | -1.475535 | data/icassp_10of10/probe_candidates/fir_hp_loose_8k__alternating__max.npy | 1.2319326 | 0.58557905 | -0.6463535 | 0 |
| fir_hp_tight_8k | coeff | 104 | 15 | -1.4469103 | data/valid/random/fir_hp_tight_8k__r014.npy | 1.4283508 | 1.0180249 | -0.41032588 | 0 |
| fir_hp_loose_16k | coeff | 90 | 15 | -1.4959156 | data/icassp_10of10/probe_candidates/fir_hp_loose_16k__alternating__max.npy | 1.2428323 | 0.58557905 | -0.65725324 | 0 |
| fir_hp_tight_16k | coeff | 104 | 15 | -1.4465031 | data/valid/random/fir_hp_tight_16k__r021.npy | 1.4305423 | 1.0180936 | -0.41244872 | 0 |
| fir_bp_loose_8k | coeff | 87 | 15 | -1.5973294 | data/valid/random/fir_bp_loose_8k__r018.npy | 1.5963139 | 1.0141213 | -0.58219259 | 0 |
| fir_bp_tight_8k | coeff | 111 | 15 | -1.4950833 | data/valid/random/fir_bp_tight_8k__r008.npy | 1.427475 | 1.0159543 | -0.41152066 | 0 |
| fir_bp_loose_16k | coeff | 87 | 15 | -1.6120386 | data/valid/random/fir_bp_loose_16k__r019.npy | 1.5813484 | 1.0136666 | -0.56768188 | 0 |
| fir_bp_tight_16k | coeff | 111 | 15 | -1.5147614 | data/valid/random/fir_bp_tight_16k__r018.npy | 1.4138426 | 1.0152617 | -0.39858089 | 0 |
| fir_bs_loose_8k | coeff | 90 | 15 | -1.4786604 | data/valid/random/fir_bs_loose_8k__r016.npy | 1.5213491 | 1.0163433 | -0.50500578 | 0 |
| fir_bs_tight_8k | coeff | 123 | 15 | -1.4208344 | data/valid/random/fir_bs_tight_8k__r012.npy | 1.4158234 | 1.0169319 | -0.39889151 | 0 |
| fir_bs_loose_16k | coeff | 90 | 15 | -1.534753 | data/valid/random/fir_bs_loose_16k__r014.npy | 1.4796942 | 1.0154283 | -0.46426589 | 0 |
| fir_bs_tight_16k | coeff | 123 | 15 | -1.4478007 | data/valid/random/fir_bs_tight_16k__r017.npy | 1.4170739 | 1.0175473 | -0.39952662 | 0 |
| iir_lp_loose_8k | coeff | 19 | 16 | -66.533258 | data/valid/random/iir_lp_loose_8k__r017.npz | 0.99875713 | 0.95652457 | -0.042232562 | 0 |
| iir_lp_tight_8k | coeff | 19 | 16 | -11.304934 | data/valid/random/iir_lp_tight_8k__r013.npz | 0.9937622 | 0.94744794 | -0.046314258 | 0 |
| iir_hp_loose_8k | coeff | 19 | 16 | -22.035263 | data/valid/random/iir_hp_loose_8k__r006.npz | 1.0103687 | 0.83856412 | -0.17180463 | 0 |
| iir_hp_tight_8k | coeff | 19 | 16 | -11.876136 | data/valid/random/iir_hp_tight_8k__r007.npz | 1.1385186 | 0.85757993 | -0.28093865 | 0 |

## Response-distance oracle

- Tasks evaluated: 20
- $G_{\mathrm{obs}}^\star > 0$: 2
- $G_{\mathrm{obs}}^\star = 0$: 0
- $G_{\mathrm{obs}}^\star < 0$: 18
- median / min / max: -0.0034585059 / -0.021254659 / 0.002817539
- Canonical non-separable: 19
- Best-observed non-separable: 18
- Separability status changes: 1
- Largest improvement (not necessarily a rescue): {'task_id': 'iir_lp_loose_8k', 'improvement': 0.05212440674803251, 'canonical_G': -0.05712130926935302, 'Gobs_star': -0.004996902521320512}

Status-changing tasks (response):

- `iir_lp_tight_8k`: canonical $G=-0.0034238405$ → $G_{\mathrm{obs}}^\star=0.0016863272$ (best `data/valid/random/iir_lp_tight_8k__r019.npz`)

| task | metric | n_valid | n_invalid | canonical_G | best_reference_id | best_DV | best_DI | Gobs_star | exact_separable |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fir_lp_loose_8k | resp | 89 | 15 | -0.031194893 | data/icassp_10of10/probe_candidates/fir_lp_loose_8k__basis_6__max.npy | 0.042650805 | 0.034540094 | -0.0081107117 | 0 |
| fir_lp_tight_8k | resp | 104 | 15 | -0.0069606196 | data/icassp_10of10/probe_candidates/fir_lp_tight_8k__basis_21__min.npy | 0.0070699069 | 0.0070476824 | -2.2224504e-05 | 0 |
| fir_lp_loose_16k | resp | 89 | 15 | -0.031194893 | data/icassp_10of10/probe_candidates/fir_lp_loose_16k__basis_6__max.npy | 0.042650805 | 0.034540094 | -0.0081107117 | 0 |
| fir_lp_tight_16k | resp | 104 | 15 | -0.0069606196 | data/icassp_10of10/probe_candidates/fir_lp_tight_16k__basis_21__min.npy | 0.0070699069 | 0.0070476824 | -2.2224504e-05 | 0 |
| fir_hp_loose_8k | resp | 90 | 15 | -0.032258594 | data/icassp_10of10/probe_candidates/fir_hp_loose_8k__random_11__min.npy | 0.057738688 | 0.036484029 | -0.021254659 | 0 |
| fir_hp_tight_8k | resp | 104 | 15 | -0.0067192885 | data/valid/library/fir_hp_tight_8k__remez.npy | 0.009265297 | 0.0057711585 | -0.0034941385 | 0 |
| fir_hp_loose_16k | resp | 90 | 15 | -0.032258594 | data/icassp_10of10/probe_candidates/fir_hp_loose_16k__random_11__min.npy | 0.057738688 | 0.036484029 | -0.021254659 | 0 |
| fir_hp_tight_16k | resp | 104 | 15 | -0.0067192885 | data/valid/library/fir_hp_tight_16k__remez.npy | 0.009265297 | 0.0057711585 | -0.0034941385 | 0 |
| fir_bp_loose_8k | resp | 87 | 15 | -0.036220986 | data/icassp_10of10/probe_candidates/fir_bp_loose_8k__basis_6__max.npy | 0.041736434 | 0.038277928 | -0.0034585059 | 0 |
| fir_bp_tight_8k | resp | 111 | 15 | -0.0077477501 | data/icassp_10of10/probe_candidates/fir_bp_tight_8k__random_06__min.npy | 0.0080328409 | 0.0076304926 | -0.00040234824 | 0 |
| fir_bp_loose_16k | resp | 87 | 15 | -0.036220986 | data/icassp_10of10/probe_candidates/fir_bp_loose_16k__basis_6__max.npy | 0.041736434 | 0.038277928 | -0.0034585059 | 0 |
| fir_bp_tight_16k | resp | 111 | 15 | -0.0077477501 | data/icassp_10of10/probe_candidates/fir_bp_tight_16k__random_06__min.npy | 0.0080328382 | 0.0076304926 | -0.00040234559 | 0 |
| fir_bs_loose_8k | resp | 90 | 15 | -0.038128933 | data/icassp_10of10/probe_candidates/fir_bs_loose_8k__basis_7__min.npy | 0.055990873 | 0.040317948 | -0.015672925 | 0 |
| fir_bs_tight_8k | resp | 123 | 15 | -0.0082378695 | data/icassp_10of10/probe_candidates/fir_bs_tight_8k__basis_5__max.npy | 0.0088650251 | 0.0076051038 | -0.0012599213 | 0 |
| fir_bs_loose_16k | resp | 90 | 15 | -0.038128933 | data/icassp_10of10/probe_candidates/fir_bs_loose_16k__basis_7__min.npy | 0.055990873 | 0.040317948 | -0.015672925 | 0 |
| fir_bs_tight_16k | resp | 123 | 15 | -0.0082378695 | data/icassp_10of10/probe_candidates/fir_bs_tight_16k__basis_5__max.npy | 0.0088650251 | 0.0076051038 | -0.0012599213 | 0 |
| iir_lp_loose_8k | resp | 19 | 16 | -0.057121309 | data/valid/library/iir_lp_loose_8k__ellip.npz | 0.068374708 | 0.063377806 | -0.0049969025 | 0 |
| iir_lp_tight_8k | resp | 19 | 16 | -0.0034238405 | data/valid/random/iir_lp_tight_8k__r019.npz | 0.0091739612 | 0.010860288 | 0.0016863272 | 1 |
| iir_hp_loose_8k | resp | 19 | 16 | -0.018423317 | data/valid/random/iir_hp_loose_8k__r011.npz | 0.034448253 | 0.032713414 | -0.0017348388 | 0 |
| iir_hp_tight_8k | resp | 19 | 16 | 3.8046047e-06 | data/valid/random/iir_hp_tight_8k__r007.npz | 0.0088947815 | 0.01171232 | 0.002817539 | 1 |

## Tie handling

Deterministic: maximise $G$, then lexicographically smallest `ref_id`. All IDs with $|G-G^\star|\le 10^{-15}$ are listed in `tied_reference_ids` of the machine-readable artifact.

## Attack B

`ATTACK_B_STRONGLY_CLOSED`

Coefficient distance remains 20/20 non-separable even after the best observed valid centre. Response distance remains 18/20 non-separable; one previously non-separable IIR task becomes exactly separable and the already-separable `iir_hp_tight_8k` stays separable. Reference choice improves many gaps but does **not** restore a single-reference oracle on the confirmatory coefficient metric, and does not rescue the overwhelming majority of response tasks.

Wall time is printed to stdout as `elapsed_s` and is not a frozen scientific output.

