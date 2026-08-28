# PHASE 2A — FIR power-polynomial certification

Method: squared-magnitude polynomial \(P(x)=c_0+2\sum c_k T_k(x)\), \(x=\cos\omega\);
Bernstein sign certificates on floor-expanded \(S_t\).

Arithmetic: `exact IEEE-754 binary64 rationals for taps; JSON spec as binary64; Bernstein over Fraction`

Certificate type: `RIGOROUS_POLYNOMIAL_SIGN`

Frequency endpoints use an outward cosine enclosure. Probe occupants with n_taps>80 use witness-only (resource). Manuscript unique FIR valids are the 336 constructed FIR files.

## Existing-valid FIR (manuscript constructed; unique occupant files)

- unique occupants: 336
- CERTIFIED_VALID: 334
- CERTIFIED_INVALID: 0
- UNDECIDED: 2
- coverage: 0.9940476190476191

## Confirmatory probe valids (NOT in the 412 headline; reported separately)

- unique occupants: 1260
- CERTIFIED_VALID: 1260
- CERTIFIED_INVALID: 0
- UNDECIDED: 0

## Mechanism-invalid FIR

- unique occupants: 112
- CERTIFIED_INVALID: 112
- CERTIFIED_VALID: 0
- UNDECIDED: 0

## Boundary-invalid FIR

- unique occupants: 128
- CERTIFIED_INVALID: 128
- CERTIFIED_VALID: 0
- UNDECIDED: 0

VALID→INVALID contradictions (constructed+probe): 0

## Phase-1 vs Phase-2A (constructed FIR valids only)

| Phase-1 status | Phase-2A valid | Phase-2A invalid | Phase-2A undecided |
| -------------- | -------------: | ---------------: | -----------------: |
| CERTIFIED_VALID | 68 | 0 | 0 |
| UNDECIDED | 266 | 0 | 2 |

## Per-task constructed-valid coverage

| task | frozen valid count | certified valid | contradicted | undecided | coverage |
| ---- | -----------------: | --------------: | -----------: | --------: | -------: |
| fir_bp_loose_16k | 21 | 21 | 0 | 0 | 1.000 |
| fir_bp_loose_8k | 21 | 21 | 0 | 0 | 1.000 |
| fir_bp_tight_16k | 21 | 21 | 0 | 0 | 1.000 |
| fir_bp_tight_8k | 21 | 21 | 0 | 0 | 1.000 |
| fir_bs_loose_16k | 22 | 22 | 0 | 0 | 1.000 |
| fir_bs_loose_8k | 22 | 22 | 0 | 0 | 1.000 |
| fir_bs_tight_16k | 21 | 20 | 0 | 1 | 0.952 |
| fir_bs_tight_8k | 21 | 20 | 0 | 1 | 0.952 |
| fir_hp_loose_16k | 22 | 22 | 0 | 0 | 1.000 |
| fir_hp_loose_8k | 22 | 22 | 0 | 0 | 1.000 |
| fir_hp_tight_16k | 20 | 20 | 0 | 0 | 1.000 |
| fir_hp_tight_8k | 20 | 20 | 0 | 0 | 1.000 |
| fir_lp_loose_16k | 21 | 21 | 0 | 0 | 1.000 |
| fir_lp_loose_8k | 21 | 21 | 0 | 0 | 1.000 |
| fir_lp_tight_16k | 20 | 20 | 0 | 0 | 1.000 |
| fir_lp_tight_8k | 20 | 20 | 0 | 0 | 1.000 |

Tasks with 100% constructed-valid certification: 14/16
Tasks with ≥95%: 16/16

This does **not** replace the frozen universe by the certified subset.

