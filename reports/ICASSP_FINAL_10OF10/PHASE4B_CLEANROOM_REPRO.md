# PHASE 4B — Clean-room reproduction

Procedure:

1. Isolated copy of the repository (no developer `.venv`).
2. Fresh virtualenv.
3. `pip install -r requirements.txt` (optional for headlines; used to match the declared environment).
4. `python -m experiments.icassp_final.run_all`
5. Confirm all headline numbers.
6. Confirm `manuscript/final/paper.pdf` is 5 pages (compiled in the developer tree; the clean copy compiles if TeX is present).

Headline command uses only stdlib + frozen JSON under `results/icassp_10of10_hardening/`. No `F:/` paths, no undocumented environment variables.

Cross-platform: `pathlib.Path` throughout `experiments/icassp_final/run_all.py`. CI (`.github/workflows/repro-headlines.yml`) runs the same command on `ubuntu-latest`.

**Verdict:** filled after the isolated run in this phase.
