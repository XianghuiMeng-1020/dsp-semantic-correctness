# PHASE 0 — Reproducibility 10/10 target (design only)

Target entry (not implemented):

```bash
python -m experiments.icassp_final.run_all
```

Today the intended command is already

```bash
python -m experiments.icassp_10of10.run_all
```

| Item | Status | Gap |
|---|---|---|
| Single entry point | **complete** (`icassp_10of10.run_all`) | rename/alias only |
| Frozen seed | **complete** (`20260826`) | |
| Registry | **complete** | |
| Coefficients / invalids | **complete** (`data/valid`, `data/invalid`) | |
| Verifier | **complete** | |
| Result JSON | **complete** | `run_all` overwrites in place |
| Table generation | **partial** | reports Markdown, not LaTeX tables |
| Figure generation | **partial** | TikZ is in the paper, not generated from JSON |
| SHA manifest | **partial** | `environment.json` hashes registries; no lockfile of all artifacts |
| Environment lock | **missing** | `requirements.txt` is lower bounds only (clean clone used numpy 2.5 / scipy 1.18) |
| CI workflow | **missing** | no GitHub Actions |
| Default-branch release | **missing** | `main` is the old package |
| Release tag | **partial** | `icassp-spec-final-10of10` on research branch only |

## Gap verdict

```text
MODERATE
```

Scientific reconstruction from this **branch** works (and has been
clean-cloned). A 10/10 public reproduction story fails because
`main` + unpinned SciPy + no CI + paper tables are hand-copied.

Phase 1 should not invent `experiments.icassp_final` unless the PI
wants an alias. Pin `numpy`/`scipy`, add a SHA check that
`run_all` matches `summary.json` headlines, and point `main` at
the current paper. Do not implement that here.
