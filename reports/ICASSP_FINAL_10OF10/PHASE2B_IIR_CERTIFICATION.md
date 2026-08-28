# PHASE 2B — IIR continuous certification

Stability: exact rational Schur-Cohn on stored binary64 denominator; frozen disk |p|<0.999

Magnitude: Q(x)=P_B(x)-C P_A(x); primitive-integer Sturm sign on outward x=cos ω interval

Certificate type: `RIGOROUS_POLYNOMIAL_SIGN`

## Valid IIR

- total: 76
- CERTIFIED_VALID: 76
- CERTIFIED_INVALID: 0
- UNDECIDED: 0
- CERTIFIED_STABLE: 76
- CERTIFIED_UNSTABLE: 0
- STABILITY_UNDECIDED: 0

## Mechanism-invalid IIR

- total: 32
- CERTIFIED_INVALID: 32
- CERTIFIED_VALID: 0
- UNDECIDED: 0

## Boundary-invalid IIR

- total: 32
- CERTIFIED_INVALID: 32
- CERTIFIED_VALID: 0
- UNDECIDED: 0

VALID→INVALID contradictions: 0

## Implementation table

| task | id | frozen label | stability | magnitude | final certification | critical constraint/root |
| ---- | -- | ------------ | --------- | --------- | ------------------- | ------------------------ |
| iir_lp_loose_8k | `data/valid/library/iir_lp_loose_8k__butter.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_lp_loose_8k | `data/valid/library/iir_lp_loose_8k__cheby1.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_lp_loose_8k | `data/valid/library/iir_lp_loose_8k__cheby2.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_lp_loose_8k | `data/valid/library/iir_lp_loose_8k__ellip.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_lp_loose_8k | `data/valid/random/iir_lp_loose_8k__r005.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_lp_loose_8k | `data/valid/random/iir_lp_loose_8k__r006.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_lp_loose_8k | `data/valid/random/iir_lp_loose_8k__r007.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_lp_loose_8k | `data/valid/random/iir_lp_loose_8k__r008.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_lp_loose_8k | `data/valid/random/iir_lp_loose_8k__r009.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_lp_loose_8k | `data/valid/random/iir_lp_loose_8k__r010.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_lp_loose_8k | `data/valid/random/iir_lp_loose_8k__r011.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_lp_loose_8k | `data/valid/random/iir_lp_loose_8k__r012.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_lp_loose_8k | `data/valid/random/iir_lp_loose_8k__r013.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_lp_loose_8k | `data/valid/random/iir_lp_loose_8k__r014.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_lp_loose_8k | `data/valid/random/iir_lp_loose_8k__r015.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_lp_loose_8k | `data/valid/random/iir_lp_loose_8k__r016.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_lp_loose_8k | `data/valid/random/iir_lp_loose_8k__r017.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_lp_loose_8k | `data/valid/random/iir_lp_loose_8k__r018.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_lp_loose_8k | `data/valid/random/iir_lp_loose_8k__r019.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_lp_tight_8k | `data/valid/library/iir_lp_tight_8k__butter.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_lp_tight_8k | `data/valid/library/iir_lp_tight_8k__cheby1.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_lp_tight_8k | `data/valid/library/iir_lp_tight_8k__cheby2.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_lp_tight_8k | `data/valid/library/iir_lp_tight_8k__ellip.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_lp_tight_8k | `data/valid/random/iir_lp_tight_8k__r005.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_lp_tight_8k | `data/valid/random/iir_lp_tight_8k__r006.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_lp_tight_8k | `data/valid/random/iir_lp_tight_8k__r007.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_lp_tight_8k | `data/valid/random/iir_lp_tight_8k__r008.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_lp_tight_8k | `data/valid/random/iir_lp_tight_8k__r009.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_lp_tight_8k | `data/valid/random/iir_lp_tight_8k__r010.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_lp_tight_8k | `data/valid/random/iir_lp_tight_8k__r011.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_lp_tight_8k | `data/valid/random/iir_lp_tight_8k__r012.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_lp_tight_8k | `data/valid/random/iir_lp_tight_8k__r013.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_lp_tight_8k | `data/valid/random/iir_lp_tight_8k__r014.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_lp_tight_8k | `data/valid/random/iir_lp_tight_8k__r015.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_lp_tight_8k | `data/valid/random/iir_lp_tight_8k__r016.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_lp_tight_8k | `data/valid/random/iir_lp_tight_8k__r017.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_lp_tight_8k | `data/valid/random/iir_lp_tight_8k__r018.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_lp_tight_8k | `data/valid/random/iir_lp_tight_8k__r019.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_hp_loose_8k | `data/valid/library/iir_hp_loose_8k__butter.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_hp_loose_8k | `data/valid/library/iir_hp_loose_8k__cheby1.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_hp_loose_8k | `data/valid/library/iir_hp_loose_8k__cheby2.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_hp_loose_8k | `data/valid/library/iir_hp_loose_8k__ellip.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_hp_loose_8k | `data/valid/random/iir_hp_loose_8k__r005.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_hp_loose_8k | `data/valid/random/iir_hp_loose_8k__r006.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_hp_loose_8k | `data/valid/random/iir_hp_loose_8k__r007.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_hp_loose_8k | `data/valid/random/iir_hp_loose_8k__r008.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_hp_loose_8k | `data/valid/random/iir_hp_loose_8k__r009.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_hp_loose_8k | `data/valid/random/iir_hp_loose_8k__r010.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_hp_loose_8k | `data/valid/random/iir_hp_loose_8k__r011.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_hp_loose_8k | `data/valid/random/iir_hp_loose_8k__r012.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_hp_loose_8k | `data/valid/random/iir_hp_loose_8k__r013.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_hp_loose_8k | `data/valid/random/iir_hp_loose_8k__r014.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_hp_loose_8k | `data/valid/random/iir_hp_loose_8k__r015.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_hp_loose_8k | `data/valid/random/iir_hp_loose_8k__r016.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_hp_loose_8k | `data/valid/random/iir_hp_loose_8k__r017.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_hp_loose_8k | `data/valid/random/iir_hp_loose_8k__r018.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_hp_loose_8k | `data/valid/random/iir_hp_loose_8k__r019.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_hp_tight_8k | `data/valid/library/iir_hp_tight_8k__butter.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_hp_tight_8k | `data/valid/library/iir_hp_tight_8k__cheby1.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_hp_tight_8k | `data/valid/library/iir_hp_tight_8k__cheby2.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_hp_tight_8k | `data/valid/library/iir_hp_tight_8k__ellip.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_hp_tight_8k | `data/valid/random/iir_hp_tight_8k__r005.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_hp_tight_8k | `data/valid/random/iir_hp_tight_8k__r006.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_hp_tight_8k | `data/valid/random/iir_hp_tight_8k__r007.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_hp_tight_8k | `data/valid/random/iir_hp_tight_8k__r008.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_hp_tight_8k | `data/valid/random/iir_hp_tight_8k__r009.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_hp_tight_8k | `data/valid/random/iir_hp_tight_8k__r010.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_hp_tight_8k | `data/valid/random/iir_hp_tight_8k__r011.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_hp_tight_8k | `data/valid/random/iir_hp_tight_8k__r012.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_hp_tight_8k | `data/valid/random/iir_hp_tight_8k__r013.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_hp_tight_8k | `data/valid/random/iir_hp_tight_8k__r014.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_hp_tight_8k | `data/valid/random/iir_hp_tight_8k__r015.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_hp_tight_8k | `data/valid/random/iir_hp_tight_8k__r016.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_hp_tight_8k | `data/valid/random/iir_hp_tight_8k__r017.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_hp_tight_8k | `data/valid/random/iir_hp_tight_8k__r018.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_hp_tight_8k | `data/valid/random/iir_hp_tight_8k__r019.npz` | VALID | CERTIFIED_STABLE | CERTIFIED_VALID | CERTIFIED_VALID |  |
| iir_lp_loose_8k | `data/invalid/iir_lp_loose_8k/iir_lp_loose_8k__M1.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_lp_loose_8k | `data/invalid/iir_lp_loose_8k/iir_lp_loose_8k__M2.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_lp_loose_8k | `data/invalid/iir_lp_loose_8k/iir_lp_loose_8k__M3.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_lp_loose_8k | `data/invalid/iir_lp_loose_8k/iir_lp_loose_8k__M4.npz` | INVALID | CERTIFIED_UNSTABLE | NOT_RUN | CERTIFIED_INVALID | schur_reflection_gt_one |
| iir_lp_loose_8k | `data/invalid/iir_lp_loose_8k/iir_lp_loose_8k__M5.npz` | INVALID | CERTIFIED_UNSTABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_lp_loose_8k | `data/invalid/iir_lp_loose_8k/iir_lp_loose_8k__M6.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_lp_loose_8k | `data/invalid/iir_lp_loose_8k/iir_lp_loose_8k__M7.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_lp_loose_8k | `data/invalid/iir_lp_loose_8k/iir_lp_loose_8k__M8.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_lp_tight_8k | `data/invalid/iir_lp_tight_8k/iir_lp_tight_8k__M1.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_lp_tight_8k | `data/invalid/iir_lp_tight_8k/iir_lp_tight_8k__M2.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_lp_tight_8k | `data/invalid/iir_lp_tight_8k/iir_lp_tight_8k__M3.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_lp_tight_8k | `data/invalid/iir_lp_tight_8k/iir_lp_tight_8k__M4.npz` | INVALID | CERTIFIED_UNSTABLE | NOT_RUN | CERTIFIED_INVALID | schur_reflection_gt_one |
| iir_lp_tight_8k | `data/invalid/iir_lp_tight_8k/iir_lp_tight_8k__M5.npz` | INVALID | CERTIFIED_UNSTABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_lp_tight_8k | `data/invalid/iir_lp_tight_8k/iir_lp_tight_8k__M6.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_lp_tight_8k | `data/invalid/iir_lp_tight_8k/iir_lp_tight_8k__M7.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_lp_tight_8k | `data/invalid/iir_lp_tight_8k/iir_lp_tight_8k__M8.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_hp_loose_8k | `data/invalid/iir_hp_loose_8k/iir_hp_loose_8k__M1.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_hp_loose_8k | `data/invalid/iir_hp_loose_8k/iir_hp_loose_8k__M2.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_hp_loose_8k | `data/invalid/iir_hp_loose_8k/iir_hp_loose_8k__M3.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_hp_loose_8k | `data/invalid/iir_hp_loose_8k/iir_hp_loose_8k__M4.npz` | INVALID | CERTIFIED_UNSTABLE | NOT_RUN | CERTIFIED_INVALID | schur_reflection_gt_one |
| iir_hp_loose_8k | `data/invalid/iir_hp_loose_8k/iir_hp_loose_8k__M5.npz` | INVALID | CERTIFIED_UNSTABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_hp_loose_8k | `data/invalid/iir_hp_loose_8k/iir_hp_loose_8k__M6.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_hp_loose_8k | `data/invalid/iir_hp_loose_8k/iir_hp_loose_8k__M7.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_hp_loose_8k | `data/invalid/iir_hp_loose_8k/iir_hp_loose_8k__M8.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_hp_tight_8k | `data/invalid/iir_hp_tight_8k/iir_hp_tight_8k__M1.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_hp_tight_8k | `data/invalid/iir_hp_tight_8k/iir_hp_tight_8k__M2.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_hp_tight_8k | `data/invalid/iir_hp_tight_8k/iir_hp_tight_8k__M3.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_hp_tight_8k | `data/invalid/iir_hp_tight_8k/iir_hp_tight_8k__M4.npz` | INVALID | CERTIFIED_UNSTABLE | NOT_RUN | CERTIFIED_INVALID | schur_reflection_gt_one |
| iir_hp_tight_8k | `data/invalid/iir_hp_tight_8k/iir_hp_tight_8k__M5.npz` | INVALID | CERTIFIED_UNSTABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_hp_tight_8k | `data/invalid/iir_hp_tight_8k/iir_hp_tight_8k__M6.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_hp_tight_8k | `data/invalid/iir_hp_tight_8k/iir_hp_tight_8k__M7.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_hp_tight_8k | `data/invalid/iir_hp_tight_8k/iir_hp_tight_8k__M8.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_lp_loose_8k | `data/icassp_10of10/boundary_invalids/iir_lp_loose_8k__PASS_DROP__e0.002.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_lp_loose_8k | `data/icassp_10of10/boundary_invalids/iir_lp_loose_8k__STOP_LIFT__e0.002.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_lp_loose_8k | `data/icassp_10of10/boundary_invalids/iir_lp_loose_8k__PASS_DROP__e0.005.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_lp_loose_8k | `data/icassp_10of10/boundary_invalids/iir_lp_loose_8k__STOP_LIFT__e0.005.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_lp_loose_8k | `data/icassp_10of10/boundary_invalids/iir_lp_loose_8k__PASS_DROP__e0.01.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_lp_loose_8k | `data/icassp_10of10/boundary_invalids/iir_lp_loose_8k__STOP_LIFT__e0.01.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_lp_loose_8k | `data/icassp_10of10/boundary_invalids/iir_lp_loose_8k__PASS_DROP__e0.02.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_lp_loose_8k | `data/icassp_10of10/boundary_invalids/iir_lp_loose_8k__STOP_LIFT__e0.02.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_lp_tight_8k | `data/icassp_10of10/boundary_invalids/iir_lp_tight_8k__PASS_DROP__e0.002.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_lp_tight_8k | `data/icassp_10of10/boundary_invalids/iir_lp_tight_8k__STOP_LIFT__e0.002.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_lp_tight_8k | `data/icassp_10of10/boundary_invalids/iir_lp_tight_8k__PASS_DROP__e0.005.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_lp_tight_8k | `data/icassp_10of10/boundary_invalids/iir_lp_tight_8k__STOP_LIFT__e0.005.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_lp_tight_8k | `data/icassp_10of10/boundary_invalids/iir_lp_tight_8k__PASS_DROP__e0.01.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_lp_tight_8k | `data/icassp_10of10/boundary_invalids/iir_lp_tight_8k__STOP_LIFT__e0.01.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_lp_tight_8k | `data/icassp_10of10/boundary_invalids/iir_lp_tight_8k__PASS_DROP__e0.02.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_lp_tight_8k | `data/icassp_10of10/boundary_invalids/iir_lp_tight_8k__STOP_LIFT__e0.02.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_hp_loose_8k | `data/icassp_10of10/boundary_invalids/iir_hp_loose_8k__PASS_DROP__e0.002.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_hp_loose_8k | `data/icassp_10of10/boundary_invalids/iir_hp_loose_8k__STOP_LIFT__e0.002.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_hp_loose_8k | `data/icassp_10of10/boundary_invalids/iir_hp_loose_8k__PASS_DROP__e0.005.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_hp_loose_8k | `data/icassp_10of10/boundary_invalids/iir_hp_loose_8k__STOP_LIFT__e0.005.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_hp_loose_8k | `data/icassp_10of10/boundary_invalids/iir_hp_loose_8k__PASS_DROP__e0.01.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_hp_loose_8k | `data/icassp_10of10/boundary_invalids/iir_hp_loose_8k__STOP_LIFT__e0.01.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_hp_loose_8k | `data/icassp_10of10/boundary_invalids/iir_hp_loose_8k__PASS_DROP__e0.02.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_hp_loose_8k | `data/icassp_10of10/boundary_invalids/iir_hp_loose_8k__STOP_LIFT__e0.02.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_hp_tight_8k | `data/icassp_10of10/boundary_invalids/iir_hp_tight_8k__PASS_DROP__e0.002.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_hp_tight_8k | `data/icassp_10of10/boundary_invalids/iir_hp_tight_8k__STOP_LIFT__e0.002.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_hp_tight_8k | `data/icassp_10of10/boundary_invalids/iir_hp_tight_8k__PASS_DROP__e0.005.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_hp_tight_8k | `data/icassp_10of10/boundary_invalids/iir_hp_tight_8k__STOP_LIFT__e0.005.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_hp_tight_8k | `data/icassp_10of10/boundary_invalids/iir_hp_tight_8k__PASS_DROP__e0.01.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_hp_tight_8k | `data/icassp_10of10/boundary_invalids/iir_hp_tight_8k__STOP_LIFT__e0.01.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_hp_tight_8k | `data/icassp_10of10/boundary_invalids/iir_hp_tight_8k__PASS_DROP__e0.02.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |
| iir_hp_tight_8k | `data/icassp_10of10/boundary_invalids/iir_hp_tight_8k__STOP_LIFT__e0.02.npz` | INVALID | CERTIFIED_STABLE | CERTIFIED_INVALID | CERTIFIED_INVALID | sturm_sign_crossing |

