"""Write reports 02–10 and 12 from frozen JSON artifacts."""
from __future__ import annotations

import json
from pathlib import Path

from experiments.icassp_10of10.config import OUT_DIR, REPORT_DIR, SEED, VERIFIER_VERSION


def _load(name: str):
    return json.loads((OUT_DIR / name).read_text(encoding="utf-8"))


def _md(path: str, text: str) -> None:
    p = REPORT_DIR / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text.replace("\r\n", "\n"), encoding="utf-8")


def write_reports(summary: dict | None = None) -> None:
    rec = _load("recertify.json")
    srec = rec["summary"]
    probe = _load("feasible_probe.json")
    tasks = _load("task_metrics.json")
    stats = _load("task_stats.json")
    refs = _load("reference_choice.json")
    multi = _load("multi_reference.json")
    bound = _load("boundary_invalids.json")
    single = _load("singleton.json")
    gen = _load("generated_witness.json")
    env = _load("environment.json")
    canon = _load("canonicalization.json")

    flips = srec.get("flips") or []
    flip_lines = "\n".join(
        f"- `{f['id']}` {f['previous_label']} → {f['independent_label']}: {f['flip_reason']}"
        for f in flips
    ) or "- none"

    _md(
        "02_INDEPENDENT_VERIFICATION.md",
        f"""# 02 — Independent verification

Verifier: `{VERIFIER_VERSION}`  
Grid: \(N_f=131072\) plus local extremum refinement.  
Construction labels come from `search_checker` (4096-point). Final labels come only from the independent verifier.

## Counts

| Quantity | Value |
|---|---:|
| Total constructed candidates | {srec['total_candidates']} |
| Previous VALID | {srec['previous_valid']} |
| Previous INVALID | {srec['previous_invalid']} |
| Independent VALID (from previous-valid set) | {srec['independent_valid']} |
| Independent INVALID (from previous-invalid set) | {srec['independent_invalid']} |
| Label flips | {srec['label_flips']} |
| Near-boundary flags | {srec['near_boundary']} |
| Numerical failures | {len(srec.get('numerical_failures') or [])} |
| Independent FIR valids | {srec['fir_valid_indep']} |
| Independent IIR valids | {srec['iir_valid_indep']} |

Headline 374/416 at \(\\tau_R=0.05\) (historical \(d\)) survives unchanged: **{srec.get('headline_374_of_416_survives')}**

Descriptive historical FRR on independently verified valids: {srec.get('descriptive_FRR_historical_indep')}

## Label flips

{flip_lines}

If flips occurred, corrected independent labels are authoritative. Old numbers are not preserved for narrative convenience.

Dense sampling plus refinement is a numerical certificate, not a continuous-frequency proof.
""",
    )

    n_trim = sum(1 for r in canon if r.get("trimmed_trailing"))
    n_a0 = sum(1 for r in canon if r.get("kind") == "iir" and "scaled_a0_to_1" in (r.get("notes") or []))
    n_sign = sum(1 for r in canon if (r.get("historical_vs_canonical") or {}).get("sign_flip_only"))
    _md(
        "03_CANONICALIZATION_AUDIT.md",
        f"""# 03 — Canonicalization audit

Rules are listed in `src/verification/canonicalize.py`. Confirmatory distances use those rules. Historical min-length truncation is retained only as `d_coeff_historical`.

## Observed artifacts on constructed occupants

| Artifact | Count |
|---|---:|
| Occupants inspected | {len(canon)} |
| FIR trailing-zero trims | {n_trim} |
| IIR \(a_0\\neq 1\) rescales | {n_a0} |
| Pure sign-flip vs canonical | {n_sign} |

Scale is **not** removed: Suite N masks constrain absolute \(\lvert H\\rvert\).

Unequal-order truncation is **not** used as a confirmatory metric.

Every confirmatory “distinct realization” excludes zero-padding artifacts, pure sign flips (magnitude-only), and pure global rescaling.
""",
    )

    ps = probe["summary"]
    _md(
        "04_SAME_ORDER_FEASIBLE_SET_PROBE.md",
        f"""# 04 — Same-order feasible-set probe

Directions were frozen before observing disagreement (`PROBE_SEED={SEED}`):
basis, frozen-seed random, tap combinations, and predetermined same-order library differences.

Positive-amplitude Type-I linear program on 512 constraint frequencies per band.
Every kept candidate passed the independent verifier.

## Task-level coverage (FIR)

| Quantity | Value |
|---|---:|
| FIR specifications probed | {ps['n_fir_tasks']} |
| Specs with a same-order genuine alternative | {ps['tasks_with_same_order_alt']} / {ps['n_fir_tasks']} |
| Specs with a same-order valid **reference-discordant** alternative | {ps['tasks_with_discordant_alt']} / {ps['n_fir_tasks']} |
| Tight-mask discordant | {ps['tight_discordant']} |
| Loose-mask discordant | {ps['loose_discordant']} |

Candidates: `data/icassp_10of10/probe_candidates/`.

IIR confirmatory same-order alternatives are library same-order occupants only (no LP).
Ideal 20/20 was a target, not a manufactured outcome.
""",
    )

    n_bound_ok = sum(1 for r in bound if r.get("independent_invalid"))
    n_bound = len(bound)
    inv_lines = []
    for t in tasks:
        c = t["coeff_with_boundary"]
        inv = c.get("inversion")
        inv_lines.append(
            f"| `{t['task_id']}` | {c.get('D_V')} | {c.get('D_I')} | {c.get('G_r')} | {c.get('exact_threshold_exists')} | {bool(inv)} |"
        )
    _md(
        "05_BOUNDARY_INVALID_AND_SEPARABILITY.md",
        f"""# 05 — Boundary invalids and reference-separability

Severity levels frozen: \(0.002, 0.005, 0.010, 0.020\).
Mechanisms frozen: `PASS_DROP`, `STOP_LIFT`. Not tuned per candidate.

Independently verified invalids: **{n_bound_ok}/{n_bound}** constructed boundary mutants.

A failed construction that remains VALID is not relabeled invalid.

## Per-task coefficient-space diagnostics (constructed valids + probe valids vs mechanism+boundary invalids)

| Task | \(D_V\) | \(D_I\) | \(G_r\) | exact \(\\tau\) exists | inversion |
|---|---:|---:|---:|---|---|
{chr(10).join(inv_lines)}

Tasks with empirical coefficient non-separability: **{stats['n_coeff_nonsep']}/{stats['n_tasks']}**  
Tasks with empirical response non-separability: **{stats['n_resp_nonsep']}/{stats['n_tasks']}**  
Coefficient inversion witnesses: **{stats['n_boundary_inversions']}**

\(\\tau_R=0.05\) is an illustrative operating point only. The scientific statement is the sign of \(G_r\).
""",
    )

    any_sep = sum(1 for r in refs if r.get("any_ref_separable_coeff"))
    all_non = sum(1 for r in refs if r.get("all_refs_nonseparable_coeff"))
    ref_lines = "\n".join(
        f"| `{r['task_id']}` | {r['n_refs']} | {r.get('G_coeff_min')} | {r.get('G_coeff_median')} | {r.get('G_coeff_max')} | {r.get('any_ref_separable_coeff')} |"
        for r in refs
    )
    _md(
        "06_REFERENCE_CHOICE_ROBUSTNESS.md",
        f"""# 06 — Reference-choice robustness

Every independently verified library realization is used as \(h_r\) in turn.
Selection is the library set, not a cherry-picked best reference.

| Task | n refs | \(G_r\) min | median | max | any ref exactly separable |
|---|---:|---:|---:|---:|---|
{ref_lines}

Tasks where **some** library reference restores exact coefficient separation: {any_sep}/{len(refs)}  
Tasks where **every** library reference remains non-separable: {all_non}/{len(refs)}

If every eligible reference still has \(G_r\\le 0\), changing the canonical designer does not eliminate the problem on that evaluated universe.
""",
    )

    k_ok = {1: 0, 3: 0, 5: 0, "all": 0}
    k_n = {1: 0, 3: 0, 5: 0, "all": 0}
    for row in multi:
        for ks in row.get("k_sweep") or []:
            k = ks.get("K")
            key = "all" if isinstance(k, str) and str(k).startswith("all") else k
            if key not in k_n:
                continue
            k_n[key] += 1
            coeff = ks.get("coeff") or {}
            if coeff.get("exact_threshold_exists"):
                k_ok[key] += 1
    _md(
        "07_MULTI_REFERENCE_ANALYSIS.md",
        f"""# 07 — Multi-reference analysis

\(d_K(h)=\\min_{{r\\in\\mathcal R_K}} d(h,h_r)\).  
Reference sets are deterministic library prefixes (`firwin`, `remez`, `firls`, … / `butter`, `cheby1`, …), not the best combination.

| K | Tasks with exact coeff. separation |
|---|---|
| 1 | {k_ok[1]}/{k_n[1]} |
| 3 | {k_ok[3]}/{k_n[3]} |
| 5 | {k_ok[5]}/{k_n[5]} |
| all library | {k_ok['all']}/{k_n['all']} |

The question is whether a finite library of realizations recovers the specification-defined evaluated feasible set, or whether the mismatch persists.
""",
    )

    macro = stats.get("macro") or {}
    _md(
        "08_TASK_LEVEL_STATISTICS.md",
        f"""# 08 — Task-level statistics

Primary unit: specification/task (\(n={stats['n_tasks']}\)). Occupant-pooled rates are secondary.

| Statistic | Value |
|---|---|
| Tasks with reference disagreement (descriptive \(\\tau=0.05\), canonical \(d\)) | {stats['tasks_with_reference_disagreement']}/{stats['n_tasks']} |
| Task-macro FRR | {macro.get('mean')} |
| Median task FRR | {macro.get('median')} |
| IQR | {macro.get('iqr')} |
| Min / max | {macro.get('min')} / {macro.get('max')} |
| Task-cluster bootstrap 95% CI | {macro.get('ci95')} |
| Bootstrap B / seed | {macro.get('B')} / {macro.get('seed')} |
| Pooled descriptive FRR | {stats.get('pooled_descriptive_FRR')} |

By generation source (independently verified valids, descriptive \(\\tau=0.05\)): `{stats.get('by_source')}`

The central conclusion must not depend on how many random-valid occupants were drawn.
""",
    )

    s_exact = sum(1 for m in single["metrics"] if (m.get("coeff") or {}).get("exact_threshold_exists"))
    _md(
        "09_SINGLETON_POSITIVE_CONTROL.md",
        f"""# 09 — Singleton positive control

Suite S identities were independently re-verified (separate code path, not a wrap of `search_checker`).

Tasks with exact scalar separation on the evaluated universe: **{s_exact}/{len(single['metrics'])}**

Language: these tasks are **effectively singleton over the evaluated representation/universe**.
This is not a proof of mathematical uniqueness among all functions.

When the specification identifies one realization in the evaluation representation, a reference-distance oracle can be exact on that universe (\(G_r>0\)).
""",
    )

    n_exec = sum(1 for r in gen if r.get("status") == "executed")
    n_s1 = sum(1 for r in gen if r.get("independent_ok"))
    n_wit = sum(1 for r in gen if r.get("S1_R0_witness"))
    tasks_w = sorted({r.get("task_id") for r in gen if r.get("S1_R0_witness")})
    _md(
        "10_GENERATED_WITNESS_REVALIDATION.md",
        f"""# 10 — Generated-code witness revalidation

Not an LLM benchmark. Existing frozen generations only (`data/arm_n_generations.json`).

| Quantity | Value |
|---|---:|
| Records | {len(gen)} |
| Executed | {n_exec} |
| Independently specification-valid | {n_s1} |
| Independently valid and reference-discordant (\(S=1,R=0\)) | {n_wit} |
| Tasks with such a witness | {len(tasks_w)} ({', '.join(tasks_w) if tasks_w else 'none'}) |

If \(n_{{wit}}=0\), the constructed-label study still stands; the external witness does not.
""",
    )

    _md(
        "12_REPRODUCIBILITY_AUDIT.md",
        f"""# 12 — Reproducibility audit

Entry point:

```text
python -m experiments.icassp_10of10.run_all
```

## Environment recorded at this run

- Python: {env.get('python')}
- Platform: {env.get('platform')}
- numpy: {env.get('numpy')}
- scipy: {env.get('scipy')}
- seed: {env.get('seed')}
- verifier: {env.get('verifier')}
- elapsed_s: {env.get('elapsed_s')}

## Dataset hashes

{json.dumps(env.get('hashes'), indent=2)}

## Regenerated artifacts

All under `data/icassp_10of10/`:
`recertify.json`, `canonicalization.json`, `feasible_probe.json`,
`boundary_invalids.json`, `task_metrics.json`, `reference_choice.json`,
`multi_reference.json`, `task_stats.json`, `singleton.json`,
`generated_witness.json`, `environment.json`, `summary.json`,
plus `probe_candidates/` and `boundary_invalids/`.

README is **not** rewritten in this scientific pass.
""",
    )
    print("reports 02-10 and 12 written")
