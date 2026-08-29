# PHASE 4B — Author-mode audit

Official review mode (2026-08-29): **single-anonymous**.
Reviewers know authors; authors do not know reviewers.

## Authoritative local metadata (not invented)

Sources (consistent across history):

- `manuscript/final/paper.tex` / `manuscript/w4/paper.tex`
- `manuscript/w4/submission/README.txt`
- `manuscript/w4/paper_pre4a.tex`
- `reports/archive/w4_phase3/PHASE_3D_FINAL_SUBMISSION_AUDIT.md`

| Order | Name | Affiliation | Role |
|---|---|---|---|
| 1 | Xianghui Meng | The University of Hong Kong | first author; `margretmeng1020@gmail.com` |
| 2 | Jionghao Lin | The University of Hong Kong and Carnegie Mellon University | corresponding; `jionghao@hku.hk` |

No “Anonymous Author”, no omitted affiliations, no blinded repository wording in the final PDF.

PDF `/Author` and `/Title` metadata are set via `\hypersetup` to the same names and title as the typeset block.

**Verdict: `SINGLE_ANONYMOUS_COMPLIANT`**

Author order vs CMT/submission-system entry: **USER_ACTION_REQUIRED** (no local export of the submission form).
