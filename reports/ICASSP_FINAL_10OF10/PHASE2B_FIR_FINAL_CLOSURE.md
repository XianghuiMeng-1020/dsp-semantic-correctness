# PHASE 2B — FIR final-two closure

Method: exact rational P(x); primitive-integer Sturm sequence; sign on root-free intervals

This route does not call the Phase-2A Bernstein engine and does not increase
the Bernstein node budget. It uses a primitive-integer Sturm sequence of the
exact squared-magnitude polynomial.

- previously UNDECIDED: 2
- CERTIFIED_VALID: 2
- CERTIFIED_INVALID: 0
- STILL_UNDECIDED: 0
- validity contradiction: NO

## Occupants

- `data/valid/first_principles/fir_bs_tight_8k__frequency_sampling__shortest.npy` n_taps=267 Phase-2A=UNDECIDED Phase-2B=`CERTIFIED_VALID` reason=`all_bands_sturm_sign`
- `data/valid/first_principles/fir_bs_tight_16k__frequency_sampling__shortest.npy` n_taps=267 Phase-2A=UNDECIDED Phase-2B=`CERTIFIED_VALID` reason=`all_bands_sturm_sign`

## Constructed FIR valid corpus after Phase 2B

- CERTIFIED_VALID: 336 / 336
- CERTIFIED_INVALID: 0
- UNDECIDED: 0
- coverage: 1.0

Phase-2A already certified the other 334 constructed FIR valids by Bernstein.
Together the two independent continuous routes cover the 336-occupant FIR valid corpus.
