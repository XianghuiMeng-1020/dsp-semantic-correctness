# PHASE 0 — Paper ↔ public repository consistency

Compared three surfaces. Nothing was edited.

| Surface | Commit | What it says |
|---|---|---|
| Current manuscript / this branch README | `41c8e69` | 412 / 144 / 0.900 / [0.871,0.925] / 20/20 / independent verifier / `python -m experiments.icassp_10of10.run_all` |
| `origin/research/icassp-spec-oracle-10of10` | `41c8e69` | Same as current manuscript |
| **GitHub default `origin/main`** | `a776d3c` | **Old package** |

## Public default (`main`) — material discrepancies

The manuscript abstract points to
`https://github.com/XianghuiMeng-1020/dsp-semantic-correctness`.
Unqualified GitHub landing is **`main`**, not the research branch.

`origin/main` README still states:

* RQ1 / Arm N: 48 planned generations, 20 execute, 14 eligible, 9 valid, 4/4 tasks
* RQ2 / P2A, RQ3 / P2C, RQ4 / Oracles A, B, C
* Reproduction: `python scripts/reproduce_*.py`
* Expected `ALL_PUBLISHED_COUNTS_MATCH`

`origin/main` `manuscript/w4/paper.tex` still reports **374/416**, Oracle A/B/C, RQ1–RQ3.
It does **not** contain 412, task-macro 0.900, or Proposition 1.

`origin/main` does **not** contain `src/verification/independent_spec_verifier.py`
or `experiments/icassp_10of10/`.

| Item | Manuscript (this branch) | Public default `main` |
|---|---|---|
| Title | same string | same string |
| Abstract headlines | 20/20 gap; independent verifier | 374/416; Oracle A–C |
| Valid/invalid | 412 / 144 | 416 constructed (paper); README Arm N 9/14 |
| Reproduction | `experiments.icassp_10of10.run_all` | `scripts/reproduce_*.py` |
| Verifier | independent 131072 + refine | `src/spec_checker.py` 4096 |
| Paper location | `manuscript/w4/` current rewrite | `manuscript/w4/` **old** rewrite |

## This branch (research) vs manuscript

Synced: title, headlines, verifier path, registry, `run_all`, archived Phase-2 banners.
Historical `scripts/reproduce_*.py` remain but are labeled non-authoritative.

## Release / tag

* Default branch: `main` @ `a776d3c` (stale science + stale paper)
* Research branch + tag `icassp-spec-final-10of10`: current science
* A visitor who does not know the branch name gets the **wrong paper**.

## Classification

```text
MATERIAL_MISMATCH
```

Reason: the public default repository state contradicts the current
manuscript on every headline a reviewer would check first.
This is a submission blocker if the GitHub URL is printed.
It is **not** a defect of the research-branch working tree.

No repair in Phase 0.
