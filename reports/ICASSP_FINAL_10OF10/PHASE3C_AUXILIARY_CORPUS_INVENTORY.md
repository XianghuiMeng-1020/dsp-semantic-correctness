# PHASE 3C — Auxiliary corpus inventory

Every listed corpus existed before Phase 3C. Eligibility requires catalog-exclusion from Phase-3B fitting, frozen task membership, independent certification, and non-duplicate coefficients.

| corpus | existed pre-Phase3C | in base 412? | tasks mapped | independently certified? | used in Phase3B catalog selection? | eligible external holdout? |
| ------ | ------------------- | ------------ | ------------ | ------------------------ | ---------------------------------- | -------------------------- |
| manuscript_constructed_valids_412 | 1 | 1 | 20 tasks | 1 | 1 | 0 |
| type_i_feasible_probes_1260 | 1 | 0 | 16 tasks | 1 | 1 | 0 |
| first_principles_occupants | 1 | 1 | 16 tasks | 1 | 1 | 0 |
| library_occupants_in_412 | 1 | 1 | 20 tasks | 1 | 1 | 0 |
| random_occupants_in_412 | 1 | 1 | 20 tasks | 1 | 1 | 0 |
| generated_code_witness_records | 1 | 0 | 4 tasks | 0 | 0 | 0 |
| failed_or_non_genuine_type_i_probe_rows | 1 | 0 | none | 0 | 0 | 0 |
| mechanism_invalids | 1 | 0 | 20 tasks | 1 | 1 | 0 |
| boundary_invalids | 1 | 0 | frozen_boundary_invalids.json | 1 | 1 | 0 |
| independent_invalid_label_flips | 1 | 0 | 4 tasks | 1 | 0 | 0 |
| disk_valid_npy_not_in_recertify_412 | 1 | 0 | none | 0 | 0 | 0 |

## Type-I probe provenance

- Unique certified probes: 1260 (unique paths 1260)
- Tasks covered: 16 FIR tasks (no IIR probes)
- CID overlap with constructed 412: 0
- Per-task counts: `{'fir_bp_loose_16k': 66, 'fir_bp_loose_8k': 66, 'fir_bp_tight_16k': 90, 'fir_bp_tight_8k': 90, 'fir_bs_loose_16k': 68, 'fir_bs_loose_8k': 68, 'fir_bs_tight_16k': 102, 'fir_bs_tight_8k': 102, 'fir_hp_loose_16k': 68, 'fir_hp_loose_8k': 68, 'fir_hp_tight_16k': 84, 'fir_hp_tight_8k': 84, 'fir_lp_loose_16k': 68, 'fir_lp_loose_8k': 68, 'fir_lp_tight_16k': 84, 'fir_lp_tight_8k': 84}`
- Construction: `data/icassp_10of10/feasible_probe.json` rows with `genuine_same_order`, a stored `path`, and `independent_ok`.
- These probes were **not** members of the manuscript 412 constructed valids.
- They **were** members of Phase-3B $V_t$ via `load_frozen_universe()`.

## Phase-3B catalog membership of probes

- Coefficient catalog members that are probe paths: 467 / 825
- Tasks whose optimal coefficient catalog contains at least one probe: 16 / 16 FIR

| task | Phase-3B n_valid | K* | probe IDs in catalog |
| ---- | ---------------: | -: | -------------------: |
| fir_lp_loose_8k | 89 | 42 | 23 |
| fir_lp_tight_8k | 104 | 84 | 64 |
| fir_lp_loose_16k | 89 | 41 | 23 |
| fir_lp_tight_16k | 104 | 84 | 64 |
| fir_hp_loose_8k | 90 | 38 | 20 |
| fir_hp_tight_8k | 104 | 20 | 2 |
| fir_hp_loose_16k | 90 | 23 | 7 |
| fir_hp_tight_16k | 104 | 17 | 2 |
| fir_bp_loose_8k | 87 | 48 | 30 |
| fir_bp_tight_8k | 111 | 23 | 4 |
| fir_bp_loose_16k | 87 | 49 | 30 |
| fir_bp_tight_16k | 111 | 21 | 4 |
| fir_bs_loose_8k | 90 | 19 | 4 |
| fir_bs_tight_8k | 123 | 113 | 93 |
| fir_bs_loose_16k | 90 | 21 | 4 |
| fir_bs_tight_16k | 123 | 112 | 93 |
| iir_lp_loose_8k | 19 | 15 | 0 |
| iir_lp_tight_8k | 19 | 19 | 0 |
| iir_hp_loose_8k | 19 | 17 | 0 |
| iir_hp_tight_8k | 19 | 19 | 0 |

## Eligibility conclusion

- Primary holdout designation: none
- Blocker: `PHASE3C_HOLDOUT_LEAKAGE_BLOCKER`
- Reason: The 1260 Type-I probes existed before Phase 3C and are continuously certified, but they were members of Phase-3B V_t and candidate/selected references. They are not an independent external holdout.
- Eligible secondary corpora: NONE
- Extra disk npy after excluding the 412: 4 (the independent-INVALID firwin2 flips)
- Optional catalog-excluded invalids: 4 eligible=1
- Generated-witness records: 48 (9 independent_ok); stored implementations: 0

Language: the Type-I probes are previously frozen auxiliary Type-I valid realizations that were **included** in the primary catalog-fitting universe. They are not temporally prospective and not a catalog-excluded dataset.
