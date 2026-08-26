# Code and manuscript repository for the ICASSP 2027 paper

*Beyond Reference Matching: Specification-Based Correctness Evaluation for DSP Implementations*

**Question.** When can a reference-distance evaluation oracle be a correct oracle for a specification-defined DSP task?

Final labels come from the **independent specification verifier**
(`src/verification/independent_spec_verifier.py`; \(N_f=131072\) plus
local extremum refinement), **not** from the 4096-point construction /
search checker (`src/spec_checker.py` / `src/verification/search_checker.py`).

Authoritative manuscript: `manuscript/w4/paper.tex`  
Authoritative PDF: `manuscript/w4/paper.pdf`  
Submission bundle: `manuscript/w4/submission/`

## Final scientific results (independently verified)

| Quantity | Value |
|---|---|
| Independent valid count | **412** |
| Invalid count (mechanism) | **144** |
| Independent-verifier label flips | **4** |
| Pooled descriptive FRR (\(\tau_R=0.05\), secondary) | **370/412 = 0.898** |
| Task-macro FRR | **0.900** |
| 95% task-cluster bootstrap CI | **[0.871, 0.925]** |
| Same-order valid / reference-discordant | **20/20** |
| Coefficient-distance non-separable | **20/20** |
| Response-distance non-separable | **19/20** |
| Boundary inversion witnesses | **20/20** |
| Reference-choice exact recovery | **0/20** |
| Multi-reference exact recovery (\(K=1,3,5,\mathrm{all}\)) | **0/20** |
| Singleton-control exact separation | **8/8** |
| Generated-code \(S=1,R=0\) witnesses | **9** (4/4 original masks) |

These numbers replace the earlier construction-checker headlines
(including 374/416). Occupant-pooled FRR is descriptive only. The
primary unit is the specification/task. \(\tau_R=0.05\) is an
illustrative operating point; the scientific claim is the sign of the
reference-separability gap \(G_r=D_I-D_V\).

## Authoritative reproduction

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Unix:    source .venv/bin/activate
pip install -r requirements.txt
python -m experiments.icassp_10of10.run_all
```

This regenerates independently verified labels, same-order probes,
boundary invalids, separability diagnostics, reference-choice and
multi-reference tables, task-level statistics, and
`reports/ICASSP_10OF10/` summaries under `data/icassp_10of10/`.

Frozen seed: `20260826`.

## Manuscript compile

```bash
cd manuscript/w4
pdflatex paper
bibtex paper
pdflatex paper
pdflatex paper
```

## What this repository is not

- Not an LLM / generated-code leaderboard
- Not a new FIR/IIR design algorithm
- Not a global impossibility theorem over all filters
- Historical Arm N scripts under `scripts/reproduce_*.py` reproduce an
  earlier generated-code witness package. They are **not** the
  authoritative ICASSP 2027 experiment.
- Phase 2 construction reports are archived under
  `reports/archive/phase2/` and are not current results.

## Scientific package

```text
registry/suite_s.json, suite_n.json     specifications
src/verification/independent_spec_verifier.py   final labels
src/verification/search_checker.py     construction checker only
src/verification/feasible_set_probe.py Type-I feasible-set probe
src/verification/canonicalize.py       representation equivalence
experiments/icassp_10of10/run_all.py   authoritative entry point
data/valid/, data/invalid/             constructed occupants
data/icassp_10of10/                    verified artifacts
reports/ICASSP_10OF10/                 scientific strengthening reports
manuscript/w4/                         current paper
```

## Citation

Xianghui Meng and Jionghao Lin, “Beyond Reference Matching:
Specification-Based Correctness Evaluation for DSP Implementations,”
ICASSP 2027.

## License

MIT
