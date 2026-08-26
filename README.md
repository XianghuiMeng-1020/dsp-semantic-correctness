# Code and manuscript repository for the ICASSP 2027 paper

*Beyond Reference Matching: Specification-Based Correctness Evaluation for DSP Implementations*

Final manuscript: `manuscript/w4/`  
Submission PDF: `manuscript/w4/submission/paper.pdf`

Frozen constructed-label package: `registry/suite_s.json`,
`registry/suite_n.json`, `src/spec_checker.py`, Phase 2B/2C scripts
under `scripts/`, and occupants under `data/valid/` and `data/invalid/`.

Historical Arm N / identity-suite reproduction scripts remain below.

Paper: specification-set membership \(\mathcal{V}_t=\{h:S_t(h)=1\}\)
on filter-design tasks that admit more than one valid realization.
Coefficient agreement with `firwin` / `butter` is a realization
diagnostic.

## Overview

- **RQ1 / Arm N.** 48 planned generations, 20 execute, 14 eligible, 9
  specification-valid and coefficient-discordant with the canonical
  reference (4/4 tasks, 6/12 cells). Pre-generation: 12/12 valid
  controls pass \(S_t\); 12/12 mutants fail.
- **RQ2 / P2A.** Hamming windowed-sinc and frequency-sampling FIR
  designs (`src/first_principles_fir.py`, numpy only) occupy the same
  frozen masks at the canonical lengths (same-order \(6/6\) in
  \(\mathcal{V}_t\), \(5/6\) coefficient-discordant).
- **RQ3 / P2C.** Tight low-pass mask at common length \(N=57\):
  windowed-sinc and frequency sampling both satisfy \(S_t\), pass
  \(7/7\) constrained tones, share group delay \(28\), and differ by
  coefficient \(\ell_2=0.115\).
- **RQ4 / Oracles A, B, C.** Table III on the 14 eligible
  implementations. \(T\) is a consistency probe of the same mask as
  \(S_t\), not an independent gold or correctness oracle.

Supporting arms H/P/B remain in `data/` so the original identity-suite
counts still re-score; they are not the paper's primary claim.

Model generation is not shipped. Every number is computed from the
extracted implementations in `data/` and from deterministic FIR designs.

## Environment setup

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Unix:    source .venv/bin/activate
pip install -r requirements.txt
```

Requires Python 3 with `numpy` and `scipy` (see `requirements.txt`).

## Reproduction commands

```bash
python scripts/reproduce_all.py
python scripts/reproduce_first_principles.py
python scripts/reproduce_p2c.py
python scripts/reproduce_oracles.py
```

## Expected outputs

```text
ALL_PUBLISHED_COUNTS_MATCH: YES
FIRST_PRINCIPLES_SAMEORDER: PASS
P2C_PUBLISHED_COUNTS_MATCH: YES
ORACLE_TABLE_MATCH: YES
```

Oracle A uses the frozen coefficient distances in
`data/arm_n_oracle_a_frozen.json` (one same-order `remez` row sits on
the \(\tau_R=0.05\) boundary; live SciPy taps can move at \(10^{-4}\)).
Oracles B and C and the tone check \(T\) are recomputed live.

## Repository structure

```text
src/contracts_arm_n.py                 FIR/IIR specification contracts
src/first_principles_fir.py            windowed-sinc and frequency sampling
src/runtime.py                         restricted-namespace exec
scripts/reproduce_all.py               Arm N / H / P / B published counts
scripts/reproduce_first_principles.py  RQ2 same-order occupants
scripts/reproduce_p2c.py               RQ3 tight-mask N=57 pair
scripts/reproduce_oracles.py           Table III, Oracles A/B/C vs T
data/arm_n_generations.json            48 scored generations
data/arm_n_valid_controls/             12 pre-generation controls
data/arm_n_mutants/                    12 mechanism mutants
data/arm_n_oracle_a_frozen.json        frozen Oracle A distances
```

## Citation

Xianghui Meng and Jionghao Lin, “Beyond Reference Matching:
Specification-Based Correctness Evaluation for DSP Implementations,”
ICASSP 2027.

## License

MIT
