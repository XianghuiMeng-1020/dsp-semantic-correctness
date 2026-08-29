# PHASE 1 — Public `main` sync inventory (not executed)

Phase 0 classified `origin/main` vs the current manuscript as `MATERIAL_MISMATCH`.
Phase 1 does **not** push or merge. The public default branch should move only
with the final scientifically hardened package.

## What must eventually change on public `main`

| Item | Action |
|---|---|
| `README.md` | Replace RQ1–RQ4 / Oracle A–C / 374/416 text with the locked 412/144/0.900/20/20 package and `python -m experiments.icassp_10of10.run_all` |
| `manuscript/w4/paper.tex` / `paper.pdf` | Replace the stale `main` manuscript with the authoritative w4 rewrite (plus later PI-approved wording only) |
| `manuscript/w4/submission/` | Refresh the CMS zip contents after any approved wording pass |
| Final reproduction path | Document `experiments.icassp_10of10.run_all` as authoritative; label historical `scripts/reproduce_*.py` non-authoritative |
| Result manifests | Publish `data/icassp_10of10/*.json` hashes / `summary.json` headlines from the baseline tag |
| Expected outputs | README expected-count block must match frozen headlines, not Arm-N 9/14 |
| Branch / tag / release | Point default `main` at the hardened science; keep `icassp-pre-10of10-hardening-baseline` and Phase tags immutable; cut a new release tag only after PI sign-off |
| Environment lock | Pin numpy/scipy (currently lower bounds only) if the PI wants a clean-clone guarantee |
| Phase-1 hardening tree | Optionally include `experiments/icassp_10of10_hardening/` and `src/continuous_certification/` as supplementary, not as a replacement for the frozen pipeline |

## What must not happen in an intermediate sync

Do not fast-forward `main` to this Phase-1 commit.
Do not move `icassp-pre-10of10-hardening-baseline` or `icassp-10of10-phase1-protocol-lock`.
