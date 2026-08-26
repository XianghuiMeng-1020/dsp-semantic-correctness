# 04 — Same-order feasible-set probe

Directions were frozen before observing disagreement (`PROBE_SEED=20260826`):
basis, frozen-seed random, tap combinations, and predetermined same-order library differences.

Positive-amplitude Type-I linear program on 512 constraint frequencies per band.
Every kept candidate passed the independent verifier.

## Task-level coverage (FIR)

| Quantity | Value |
|---|---:|
| FIR specifications probed | 16 |
| Specs with a same-order genuine alternative | 16 / 16 |
| Specs with a same-order valid **reference-discordant** alternative | 16 / 16 |
| Tight-mask discordant | 8 |
| Loose-mask discordant | 8 |

Candidates: `data/icassp_10of10/probe_candidates/`.

IIR confirmatory same-order alternatives are independently verified library occupants of the same \((b,a)\) length (no LP). All 4/4 IIR tasks have at least one such reference-discordant alternative.

Combined same-order / same-structure coverage: **20/20** specifications (16/16 FIR Type-I probes + 4/4 IIR library same-order).
Ideal 20/20 was a target, not a manufactured outcome.
