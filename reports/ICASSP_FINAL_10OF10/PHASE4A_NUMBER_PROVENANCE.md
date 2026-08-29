# PHASE 4A — Number provenance

Every headline number in `manuscript/final/paper.tex` was read from a frozen artifact.
No value was invented or re-estimated.

| manuscript location | number/claim | frozen phase | artifact | verified |
|---|---|---|---|---|
| Title / abstract / Sec.~3 | 20 magnitude-mask tasks | Phase 1 / 3D-A | `results/icassp_10of10_hardening/phase1/headline.json` `summary_coeff.n_tasks=20` | YES |
| Abstract / Sec.~3 | 16 FIR / 4 IIR | Phase 1 suite lock | task IDs in transfer rows (16 `fir_*`, 4 `iir_*`) | YES |
| Abstract / Sec.~3 | 412 constructed valids | Phase 2B | 336 FIR + 76 IIR (`PHASE2B_FIR_FINAL_CLOSURE.md`, `PHASE2B_IIR_CERTIFICATION.md`) | YES |
| Abstract / Sec.~3 | 412/412 continuously certified | Phase 2A/2B | same reports; 0 valid→invalid contradictions | YES |
| Abstract / Table I / Sec.~4.1 | coeff. canonical non-sep. 20/20 | Phase 1 | `phase1/headline.json` `summary_coeff.canonical_nonseparable=20` | YES |
| Abstract / Table I / Sec.~4.1 | coeff. best-obs. non-sep. 20/20 | Phase 1 | `summary_coeff.best_observed_nonseparable=20` | YES |
| Table I / Sec.~4.1 | resp. canonical non-sep. 19/20 | Phase 1 | `summary_resp.canonical_nonseparable=19` | YES |
| Table I / Sec.~4.1 | resp. best-obs. non-sep. 18/20 | Phase 1 | `summary_resp.best_observed_nonseparable=18` | YES |
| Abstract / Table I | median coeff. \(K^\star=23\) | Phase 3B | `phase3b/headline.json` `coeff_med_k=23.0` | YES |
| Sec.~4.1 | \(K^\star>10\) on 20/20; range 15–113 | Phase 3B | `coeff_kgt10=20`, `coeff_min_k=15`, `coeff_max_k=113` | YES |
| Sec.~4.1 | median \(K^\star/\|V\|=0.512\) | Phase 3B | `coeff_med_rho=0.511817…` (reported 0.512) | YES |
| Table I | library exact 0/20 coeff and resp | Phase 3B | `lib_yes=0`; RCC `existing.all_library=0` on 20/20 both spaces | YES |
| Table I / Sec.~4.1 | resp. median \(K^\star=17.5\); \(K^\star=1\) on 2 tasks | Phase 3B | `resp_med_k=17.5`, `resp_k1=2` | YES |
| Sec.~4.1 | ambient 19/20 coeff, 20/20 resp | Phase 3A | `phase3a/headline.json` `coeff_ambient_separable=19`, `resp_ambient_separable=20` | YES |
| Sec.~4.1 | only `iir_lp_loose_8k` has no coeff. ambient center | Phase 3A | same headline / phase3a reports | YES |
| Abstract / protocol | 960 scheduled attempts | Phase 3D-A | `phase3d_a/seed_manifest.json` `n_attempts=960` | YES |
| Abstract / Fig.~1 / Table II | 614 prospective valids | Phase 3D-A/B | `phase3d_a/adequacy.json` `n_valid=614`; `transfer_coeff.json` `H_VALID=614` | YES |
| Sec.~3 | 500 FIR / 114 IIR; min 13/task; 20/20 tasks | Phase 3D-A | `adequacy.json` `n_valid_fir=500`, `n_valid_iir=114`, `min_valid=13`, `tasks_ge10_valid=20` | YES |
| Abstract / Table II | coeff. accept 66/614 (10.7%) | Phase 3D-B | `accepted=66`, `pooled_transfer=0.107491…` | YES |
| Abstract / Table II | coeff. task-macro median 4.8% | Phase 3D-B | `task_macro_median=0.047619…` | YES |
| Sec.~4.2 | coeff. macro mean 10.6%; range 0–50% | Phase 3D-B | `task_macro_mean=0.105569…`, min 0, max 0.5 | YES |
| Table II / Sec.~4.2 | coeff. 0/20 ≥95%; 20/20 <75% | Phase 3D-B | `tasks_ge95=0`, `tasks_lt75=20` | YES |
| Sec.~4.2 | FIR/IIR coeff. macros 11.8% / 5.5% | Phase 3D-B | `fir_macro=0.118315`, `iir_macro=0.054588` | YES |
| Abstract / Table II | resp. accept 585/614 (95.3%) | Phase 3D-B | `accepted=585`, `pooled_transfer=0.952769…` | YES |
| Abstract / Table II | resp. task-macro median 100% | Phase 3D-B | `task_macro_median=1.0` | YES |
| Sec.~4.2 | resp. macro mean 94.6% | Phase 3D-B | `task_macro_mean=0.946169…` | YES |
| Table II | resp. 15/20 ≥95%; 1/20 <75% | Phase 3D-B | `tasks_ge95=15`, `tasks_lt75=1` | YES |
| Sec.~4.2 | one tight FIR BP task at 70% | Phase 3D-B | `transfer_resp.json` row `fir_bp_tight_8k=0.7` | YES |
| Sec.~4.2 | generator family transfers | Phase 3D-B | `generator_structure_transfer.json` | YES |
| Sec.~4.2 | hierarchy: canon/K3/K5/lib coeff. 0; best-obs 7.5%; \(K^\star\) 10.7%; resp. canon 38.9% | Phase 3D-B | `hierarchy_transfer.json` | YES |
| Sec.~4.3 | median \(K^\star\) 23→55; relative growth 52.5% | Phase 3D-B | `maintenance.json` `coeff_suite.expanded_median_K=55`, `median_relative_growth=0.524845…` | YES |
| Sec.~4.3 | \(M^\star>0\) on 20/20; median 15.5; max 37 | Phase 3D-B | `tasks_M_pos=20`, `median_M=15.5`, `max_M=37` | YES |
| Sec.~4.3 | resp. median \(\Delta K=0\); \(M^\star>0\) on 9/20 | Phase 3D-B | `resp_suite` | YES |
| Limitations | H_INVALID 310; 12/20 tasks; FA 38/310 and 96/310 | Phase 3D-B | `invalid_secondary.json` / headline | YES |
| Sec.~3 | FIR \(P(x)=\|H\|^2\); IIR Schur + \(P_B-CP_A\) | Phase 2 | Phase-2A/2B reports | YES |

Rounding used in the paper (not new science):

- 0.107492 → 10.7%
- 0.047619 → 4.8%
- 0.952769 → 95.3%
- 0.511817 → 0.512
- 0.524845 → 52.5%
- 0.105569 → 10.6%
- 0.118315 → 11.8%
- 0.054588 → 5.5%
- 0.074919 → 7.5%
- 0.389251 → 38.9%
