# When Does Reference Matching Transfer? Specification-Certified Audits of FIR/IIR Realizations

ICASSP 2027 regular paper (single-anonymous review).

A magnitude-mask filter specification defines a feasible set of FIR/IIR
realizations, not a unique coefficient vector. Reference-based scoring
treats proximity to selected realizations as a proxy for specification
compliance. This repository audits whether that proxy transfers to later
specification-valid designs.

**Authors.** Xianghui Meng (The University of Hong Kong) and
Jionghao Lin (The University of Hong Kong / Carnegie Mellon University,
corresponding).

**Manuscript.** `manuscript/final/paper.tex`  
**PDF.** `manuscript/final/paper.pdf`

## Headline results (frozen)

| Quantity | Value |
|---|---|
| Tasks | 20 magnitude-mask specifications (16 FIR, 4 IIR) |
| Base constructed valids | 412 (336 FIR, 76 IIR) |
| Continuous certification | 412/412 |
| Coefficient single-reference exact recovery | 0/20 (non-separable 20/20) |
| Coefficient observed-valid catalog complexity, median \(K^\star\) | 23 (\(K^\star>10\) on 20/20) |
| Prospective catalog-blind certified valids | 614 (500 FIR, 114 IIR; eight standard designer families) |
| Frozen coefficient catalogs accept | **66/614** (task-macro median 0.047619) |
| Frozen magnitude-response catalogs accept | **585/614** (task-macro median 1.0) |
| Expanded coefficient median \(K^\star\) | 23 → 55; every task requires newly admitted references (20/20) |

These are finite-universe results on magnitude-mask tasks. They are not
a claim that no reference can exist, that reference matching is
impossible in general, or that magnitude-response matching is a
universally exact oracle. \(K^\star\) is an adequacy diagnostic; computing
it uses standard set-cover / prototype selection and is not claimed as
a new algorithm. The prospective challenge uses eight ordinary
design families (Remez, FIRLS, frequency sampling, window; Butterworth,
Chebyshev I/II, elliptic), not all possible implementations.

## Reproduce the published headlines

Requires Python 3.10+ (tested on CPython 3.12). The headline command
reads frozen JSON artifacts and needs **no** compiled extensions:

```bash
python -m experiments.icassp_final.run_all
```

Expected terminal (numbers must match exactly):

```text
ICASSP FINAL REPRODUCTION

BASE_TASKS = 20
BASE_VALID = 412
BASE_CONTINUOUSLY_CERTIFIED = 412/412

COEFF_SINGLE_REFERENCE_NONSEPARABLE = 20/20
COEFF_RCC_MEDIAN = 23

PROSPECTIVE_VALID = 614
COEFF_PROSPECTIVE_ACCEPT = 66/614
COEFF_TASK_MACRO_MEDIAN = 0.047619

RESPONSE_PROSPECTIVE_ACCEPT = 585/614
RESPONSE_TASK_MACRO_MEDIAN = 1.000000

COEFF_EXPANDED_RCC_MEDIAN = 55
COEFF_TASKS_REQUIRING_NEW_REFERENCES = 20/20

ALL_PUBLISHED_RESULTS_MATCH = YES
```

To compile the manuscript:

```bash
cd manuscript/final
pdflatex paper
bibtex paper
pdflatex paper
pdflatex paper
```

## Environment

- Headline reproduction: stdlib only (`json`, `pathlib`).
- Optional scientific stack used elsewhere in the repository:
  see `requirements.txt` (NumPy / SciPy) and pinned
  `requirements-lock.txt` (tested: CPython 3.12.10, NumPy 2.3.5,
  SciPy 1.15.3).
CI runs the headline command and fails on any mismatch. That is a
deterministic validation of frozen artifacts, not a re-derivation of
catalogs or the prospective challenge.

## What this repository is not

- Not a new FIR/IIR design method
- Not a new set-cover or prototype-selection algorithm
- Not a generic software test-oracle theory paper
- Not an LLM / generated-code leaderboard
- Not an infinite-universe impossibility theorem

## Historical / development artifacts

Earlier suites, independent-verifier strengthening, and internal
hardening/audit reports are preserved in the git history of this
repository (see the `icassp-10of10-*` tags) rather than in the current
working tree, which contains only the material needed to read and
reproduce this paper. They are **not** the user-facing result of this
paper. Do not treat construction-era headlines (including 374/416,
14-eligible / 9-valid generated-code witnesses, or Oracle A/B/C) as the
current science.

## Citation

Xianghui Meng and Jionghao Lin, “When Does Reference Matching Transfer?
Specification-Certified Audits of FIR/IIR Realizations,” submitted to
ICASSP 2027.

## License

MIT
