# PHASE 3D-A — Blinding audit

Written after the protocol-lock tag and before candidate generation. This audit maps catalog-bearing artifacts. Generation must not open them.

## Catalog-bearing artifacts (do not open during generation)

| Path | Why forbidden |
|---|---|
| `results/icassp_10of10_hardening/phase3b/reference_catalog_complexity.json` | Phase-3B \(K^\star\) catalogs, IDs, \(D_V\), \(D_I\) |
| `results/icassp_10of10_hardening/phase3b/headline.json` | Phase-3B summary |
| `results/icassp_10of10_hardening/phase3a/coefficient_ambient.json` | Ambient centers |
| `results/icassp_10of10_hardening/phase3a/response_ambient.json` | Ambient centers |
| `results/icassp_10of10_hardening/phase3a/hierarchy.json` | Reference-hierarchy identities |
| `results/icassp_10of10_hardening/phase1/best_observed_reference.json` | Best-observed reference identities |

## Source modules that know those paths (must not be imported by generation)

| Module | Role |
|---|---|
| `experiments/icassp_10of10_hardening/phase3b/*` | RCC / set-cover |
| `experiments/icassp_10of10_hardening/phase3a/*` | Ambient LP |
| `experiments/icassp_10of10_hardening/phase3c/freeze.py` | Frozen catalog copy |
| `experiments/icassp_10of10_hardening/phase1/best_observed.py` | Best-observed search (distance code exists; generation does not call it) |

## Generation entry point may import

- `registry` via `src.verification.registry_io`
- `src.valid_designers` design functions (not `_try_fir` admission-by-S_t-only is OK; we call `design_*` directly)
- `src.first_principles_fir` / `src.valid_first_principles.windowed_at`
- `src.continuous_certification.*`
- `src.spec_checker` for grid **reject** only
- `data/icassp_10of10/recertify.json` and `feasible_probe.json` **IDs and coefficient files** for exact-duplicate identity only

## Guard

`experiments/icassp_10of10_hardening/phase3d_a/blinding.py` wraps `builtins.open` and raises `PHASE3D_A_BLINDING_VIOLATION` if a forbidden path is opened during generate/certify/mutate.

Reporting modules after the challenge freeze may mention those files exist. They must not compute transfer.
