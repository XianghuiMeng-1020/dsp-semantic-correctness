# Specification-Based Evaluation of Generated DSP Implementations

Code for *Beyond Reference Matching: Specification-Based Evaluation of
Generated DSP Implementations* (ICASSP 2027).

On specification-defined filter-design tasks that admit more than one
valid realization, a reference filter is one occupant of
\(\mathcal{V}_t=\{h:S_t(h)=1\}\), not a definition of the solution set.
This repository freezes the magnitude-mask and stability contracts, the
extracted generated implementations, and the first-principles FIR
designers used to reproduce every published count.

Coefficient agreement with `firwin` / `butter` is a realization
diagnostic.

## Quick start

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Unix:    source .venv/bin/activate
pip install -r requirements.txt
python scripts/reproduce_all.py
python scripts/reproduce_first_principles.py
python scripts/reproduce_p2c.py
python scripts/reproduce_oracles.py
```

Expected terminal tokens:

```text
ALL_PUBLISHED_COUNTS_MATCH: YES
FIRST_PRINCIPLES_SAMEORDER: PASS
P2C_PUBLISHED_COUNTS_MATCH: YES
ORACLE_TABLE_MATCH: YES
```

## What is reproduced

- **RQ1 / Arm N.** 48 planned generations, 20 execute, 14 eligible, 9
  specification-valid and coefficient-discordant with the canonical
  reference (4/4 tasks, 6/12 cells). Pre-generation: 12/12 valid
  controls pass \(S_t\); 12/12 mutants fail.
- **RQ2 / P2A.** Hamming windowed-sinc and frequency-sampling FIR
  designs (`src/first_principles_fir.py`, numpy only) occupy the same
  frozen masks at the canonical lengths (same-order \(6/6\) in
  \(\mathcal{V}_t\), \(5/6\) coefficient-discordant).
- **RQ3 / P2C.** Tight low-pass mask
  (\(\lvert H\rvert\in[0.99,1.01]\) on \([0,800]\,\mathrm{Hz}\),
  \(\lvert H\rvert\le 0.01\) on \([1400,4000]\,\mathrm{Hz}\)).
  At common length \(N=57\), windowed-sinc and frequency sampling both
  satisfy \(S_t\), pass \(7/7\) constrained tones, share group delay
  \(28\), and differ by coefficient \(\ell_2=0.115\), spec-band
  \(\lvert H\rvert\) RMSE \(0.0014\), and full-grid RMSE \(0.057\).
- **RQ4 / Oracles A, B, C.** Table III on the 14 eligible
  implementations:
  - **A** — coefficient concordance with the canonical occupant
    (\(\tau_R=0.05\)). Distances are the frozen values in
    `data/arm_n_oracle_a_frozen.json` (one same-order `remez` row sits
    on the \(\tau_R\) boundary; live SciPy taps can move at \(10^{-4}\)).
  - **B** — spec-band \(\lvert H\rvert\) RMSE versus that occupant,
    no larger than the same-order control-pair maximum.
  - **C** — specification membership \(S_t\).
  - **T** — constrained real cosines of length \(8192\), `lfilter`,
    steady-state Hilbert envelopes compared with the same mask.

**T is a consistency probe of the same mask as \(S_t\), not an
independent gold or correctness oracle.** Oracle C and T agree because
they are two readings of one specification.

Supporting arms H/P/B remain in `data/` so the original identity-suite
counts still re-score; they are not the paper's primary claim.

Model generation is not shipped. Every number is computed from the
extracted implementations in `data/` and from deterministic FIR designs.

## Repository structure

```text
src/contracts_arm_n.py              FIR/IIR specification contracts
src/first_principles_fir.py         windowed-sinc and frequency sampling
src/runtime.py                      restricted-namespace exec
scripts/reproduce_all.py            Arm N / H / P / B published counts
scripts/reproduce_first_principles.py   RQ2 same-order occupants
scripts/reproduce_p2c.py            RQ3 tight-mask N=57 pair
scripts/reproduce_oracles.py        Table III, Oracles A/B/C vs T
data/arm_n_generations.json         48 scored generations
data/arm_n_valid_controls/          12 pre-generation controls
data/arm_n_mutants/                 12 mechanism mutants
manuscript/                         ICASSP LaTeX sources (final wording)
```

## Citation

Xianghui Meng and Jionghao Lin, “Beyond Reference Matching:
Specification-Based Evaluation of Generated DSP Implementations,”
ICASSP 2027.

## License

MIT
