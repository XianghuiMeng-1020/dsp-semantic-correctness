# PHASE 4B — Final reproduction provenance

`python -m experiments.icassp_final.run_all` reads frozen JSON. It does not regenerate filters, catalogs, or distances.

| final output | frozen source |
|---|---|
| BASE_TASKS = 20 | `results/icassp_10of10_hardening/phase1/headline.json` `summary_coeff.n_tasks` |
| BASE_VALID = 412 | Phase-2B constructed corpus 336 FIR + 76 IIR (`PHASE2B_FIR_FINAL_CLOSURE.md`, IIR certification) |
| BASE_CONTINUOUSLY_CERTIFIED = 412/412 | same Phase-2 closure; wrapper checks the locked equality |
| COEFF_SINGLE_REFERENCE_NONSEPARABLE = 20/20 | `phase1/headline.json` `canonical_nonseparable` |
| COEFF_RCC_MEDIAN = 23 | `phase3b/headline.json` `coeff_med_k` |
| PROSPECTIVE_VALID = 614 | `phase3d_b/transfer_coeff.json` `H_VALID` (also `phase3d_a/adequacy.json`) |
| COEFF_PROSPECTIVE_ACCEPT = 66/614 | `transfer_coeff.json` `accepted` / `H_VALID` |
| COEFF_TASK_MACRO_MEDIAN = 0.047619 | `transfer_coeff.json` `task_macro_median` rounded to 6 decimals |
| RESPONSE_PROSPECTIVE_ACCEPT = 585/614 | `transfer_resp.json` `accepted` / `H_VALID` |
| RESPONSE_TASK_MACRO_MEDIAN = 1.000000 | `transfer_resp.json` `task_macro_median` |
| COEFF_EXPANDED_RCC_MEDIAN = 55 | `phase3d_b/maintenance.json` `coeff_suite.expanded_median_K` |
| COEFF_TASKS_REQUIRING_NEW_REFERENCES = 20/20 | `maintenance.json` `coeff_suite.tasks_M_pos` |

No silent redefinition of \(S_t\), \(K^\star\), or \(\tau\).
