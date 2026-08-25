# Specification-Based Evaluation of Generated DSP Implementations

Code for *Beyond Reference Matching: Specification-Based Evaluation of
Generated DSP Implementations* (ICASSP 2027).

A reference filter is one valid occupant of a design specification, not
the definition of correctness. This repository freezes the magnitude-mask
and stability contracts, the extracted generated implementations, and the
first-principles FIR designers used to reproduce every published count.

Paper: specification-set membership \(\mathcal{V}_t=\{h:S_t(h)=1\}\).
Coefficient agreement with `firwin` / `butter` is a realization diagnostic.

## Quick start

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Unix:    source .venv/bin/activate
pip install -r requirements.txt
python scripts/reproduce_all.py
python scripts/reproduce_first_principles.py
```

`reproduce_all.py` should end with:

```text
ALL_PUBLISHED_COUNTS_MATCH: YES
```

## What is reproduced

- **RQ1.** Arm N: 48 planned generations, 20 execute, 14 eligible, 9
  specification-valid and coefficient-discordant with the canonical
  reference (4/4 tasks, 2/3 models, 6/12 cells). Pre-generation:
  12/12 valid controls pass \(S_t\); 12/12 mutants fail.
- **RQ2.** Hamming windowed-sinc and frequency-sampling FIR designs
  (`src/first_principles_fir.py`, numpy only) occupy the same frozen
  masks at the canonical lengths.
- Supporting arms H/P/B remain in `data/` so the original identity-suite
  counts still re-score; they are not the paper's primary claim.

Model generation is not shipped. Every number is computed from the
extracted implementations in `data/` and from deterministic FIR designs.

## Repository structure

```text
src/contracts_arm_n.py           FIR/IIR specification contracts
src/first_principles_fir.py      windowed-sinc and frequency sampling
src/runtime.py                   restricted-namespace exec
scripts/reproduce_all.py         Arm N / H / P / B published counts
scripts/reproduce_first_principles.py
data/arm_n_generations.json      48 scored generations
data/arm_n_valid_controls/       12 pre-generation controls
data/arm_n_mutants/              12 mechanism mutants
manuscript/                      ICASSP LaTeX sources
```

## Citation

Xianghui Meng and Jionghao Lin, “Beyond Reference Matching:
Specification-Based Evaluation of Generated DSP Implementations,”
ICASSP 2027.

## License

MIT
