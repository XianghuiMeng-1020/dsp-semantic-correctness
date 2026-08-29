# PHASE 4B — Clean-room reproduction

Date: 2026-08-29

1. `git clone --local` of `F:/ICASSP/project_a_public_release` into `%TEMP%\icassp4b_cr`
2. Checkout `3935587`
3. Fresh `python -m venv .venv` (CPython 3.12)
4. `pip install -r requirements.txt` (resolved NumPy 2.5.2 / SciPy 1.18.1; not required for headlines)
5. `python -m experiments.icassp_final.run_all`

Output: `ALL_PUBLISHED_RESULTS_MATCH = YES` with every locked headline exact.

No `F:/` runtime paths. `pathlib.Path` only.

CI: `.github/workflows/repro-headlines.yml` runs the same command on `ubuntu-latest` (smoke/full headline validation; does not re-fit catalogs).

**Verdict: `PASS_EXACT`**
