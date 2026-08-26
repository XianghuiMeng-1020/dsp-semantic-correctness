# 06 — README / code / paper stale-number search

Searched the repository for `374`, `416`, `89.9`, `374/416`,
`48 planned generations`, `RQ1`, `RQ2`, `RQ3`, `Oracle C`, `4096`.

## Current surfaces (must be final science only)

| Surface | Result |
|---|---|
| Root `README.md` | Final table is 412 / 144 / 0.900 / [0.871, 0.925] / 20/20 / 19/20 / 0/20 / 4 flips. Mentions `374/416` only as the **replaced** construction-checker headline. States independent verifier, not 4096-point checker. Exposes `python -m experiments.icassp_10of10.run_all`. |
| `manuscript/w4/paper.tex` / `paper.pdf` | No RQ1–RQ3, no Oracle C, no 374/416 headline. `416` appears only as the superseded construction-checker count that the four flips replaced. `4096` appears only as the construction checker that is **not** the final labeler. |
| `manuscript/w4/submission/` | Copied from the current w4 sources; same headlines. |
| `experiments/icassp_10of10/run_all.py` | Authoritative entry; no stale headlines. |
| `experiments/icassp_10of10/pipeline.py` | Records `headline_374_of_416_survives` as a **negative** diagnostic (value 0). Not a current user-facing claim. |
| `scripts/reproduce_*.py` | Banner: historical; not the ICASSP 2027 experiment. |

## Archived / historical (left in place)

`reports/ICASSP_10OF10/00_BASELINE_AUDIT.md` and related strengthening reports document the pre-verifier baseline (374/416, Oracle C circularity). That is the scientific audit trail.

`reports/archive/phase2/` and `reports/archive/w4_phase3/` hold Phase 2/3 records, each marked **ARCHIVED**.

arXiv:2107.03374 in `refs.bib` is a citation key, not a result count.

## Verdict

Current user-facing surfaces tell the same scientific story as the final manuscript.
