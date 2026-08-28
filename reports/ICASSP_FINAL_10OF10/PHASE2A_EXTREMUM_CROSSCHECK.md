# PHASE 2A — Extremum cross-check (secondary)

Stationary points of \(P(\omega)\) are found by dense sign-change of \(dP/d\omega\).
This is **not** the primary certificate.

Audited occupants: 13

- `shortest` `data/valid/library/fir_lp_loose_8k__firwin.npy` n_taps=21 P2A=CERTIFIED_VALID violating_points=0
- `longest` `data/valid/first_principles/fir_bs_tight_16k__frequency_sampling__shortest.npy` n_taps=267 P2A=UNDECIDED violating_points=0
- `tight_lp` `data/valid/library/fir_lp_tight_8k__firwin.npy` n_taps=43 P2A=CERTIFIED_VALID violating_points=0
- `hp` `data/valid/library/fir_hp_loose_8k__firwin.npy` n_taps=21 P2A=CERTIFIED_VALID violating_points=0
- `bp` `data/valid/library/fir_bp_loose_8k__firwin.npy` n_taps=21 P2A=CERTIFIED_VALID violating_points=0
- `bs` `data/valid/library/fir_bs_loose_8k__firwin.npy` n_taps=25 P2A=CERTIFIED_VALID violating_points=0
- `phase1_undecided` `data/valid/library/fir_lp_loose_8k__firwin2.npy` n_taps=39 P2A=CERTIFIED_VALID violating_points=0
- `phase1_undecided` `data/valid/random/fir_lp_loose_8k__r007.npy` n_taps=175 P2A=CERTIFIED_VALID violating_points=0
- `phase1_undecided` `data/valid/random/fir_lp_loose_8k__r008.npy` n_taps=173 P2A=CERTIFIED_VALID violating_points=0
- `phase1_undecided` `data/valid/random/fir_lp_loose_8k__r009.npy` n_taps=113 P2A=CERTIFIED_VALID violating_points=0
- `boundary_invalid` `data/icassp_10of10/boundary_invalids/fir_lp_loose_8k__PASS_DROP__e0.002.npy` n_taps=21 P2A=CERTIFIED_INVALID violating_points=1
- `boundary_invalid` `data/icassp_10of10/boundary_invalids/fir_lp_loose_8k__STOP_LIFT__e0.002.npy` n_taps=21 P2A=CERTIFIED_INVALID violating_points=1
- `boundary_invalid` `data/icassp_10of10/boundary_invalids/fir_lp_loose_8k__PASS_DROP__e0.005.npy` n_taps=21 P2A=CERTIFIED_INVALID violating_points=1

