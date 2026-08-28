"""Write Phase-2A human reports from JSON. Does not touch frozen science files."""
from __future__ import annotations

import json
from collections import Counter
from experiments.icassp_10of10_hardening.phase2a.config import OUT_DIR, REPORT_DIR


def _load(name: str) -> dict:
    return json.loads((OUT_DIR / name).read_text(encoding="utf-8"))


def write_numeric_semantics() -> None:
    text = """# PHASE 2A — Numeric semantics

## Stored FIR coefficients

Each tap is an IEEE-754 binary64 value on disk. Phase 2A treats that bit pattern as
the **exact rational** `float.as_integer_ratio()`. Taps are never rounded to a
shorter decimal before the autocorrelation / Chebyshev expansion.

## Specification constants

`registry/suite_n.json` is parsed by `json.loads`. Numbers become Python `float`
(binary64). Phase 2A treats those binary64 values as the frozen specification,
matching the existing pipeline. They are **not** re-interpreted as exact decimal
rationals (so `1e-6` is the binary64 nearest to \(10^{-6}\), not \(10^{-6}\) itself).

Floor expansion copies the old verifier:

`span = max(hi - lo, 1e-6)`, `L = lo - floor*span`, `U = hi + floor*span`.

If `L <= 0`, the lower magnitude constraint is vacuous (`|H| >= L` holds for all
real \(H\)). Phase 2A does **not** impose \(P \\ge L^2\) in that case.

## Frequency endpoints

\\(\\omega = 2\\pi f / f_s\\). If \(f=0\\) then \(\\cos\\omega=1\\) exactly. If
\\(2f=f_s\\) exactly as binary64 rationals, then \(\\cos\\omega=-1\\) exactly.
Otherwise \(\\cos\\omega\\) is enclosed by an outward `mpmath` bound converted to
`Fraction`. The inner \(x\\)-interval is certified first; leftover endpoint slivers
must also certify or the occupant is `UNDECIDED` (`endpoint_enclosure_limitation`).

## Equality

Frozen \(S_t\\) permits equality (`|H|` on the expanded wall). Bernstein
`nonpos` / `nonneg` includes zeros. Tangential contact is valid. Unresolved
proximity is `UNDECIDED`, not a fabricated positive margin.
"""
    (REPORT_DIR / "PHASE2A_NUMERIC_SEMANTICS.md").write_text(text, encoding="utf-8")


def write_guardrails() -> None:
    text = """# PHASE 2A — Claim guardrails (manuscript not edited)

Phase 1 best-observed-valid-reference:

* Coefficient distance: 20/20 tasks remain non-separable.
* Response distance: 18/20 remain non-separable (one additional IIR task rescued;
  `iir_hp_tight_8k` was already separable under the canonical response gap).

Allowed future wording:

> No observed valid realization restores coefficient-distance separability on any
> of the 20 tasks; under response distance, 18/20 remain non-separable.

Forbidden wording:

* all metrics are reference-invariant;
* no possible reference can work;
* no ambient-space center can work;
* 20/20 remain non-separable under every representation.

\\(G_{\\mathrm{obs}}^\\star\\) is finite-universe and observed-valid only.
"""
    (REPORT_DIR / "PHASE2A_CLAIM_GUARDRAILS.md").write_text(text, encoding="utf-8")


def write_independence() -> None:
    text = """# PHASE 2A — Independence audit

| Pair | Shared correctness logic? | Shared assets |
|---|---|---|
| Construction vs old final verifier | No pass/fail import | registry JSON, residual_floor contract, numpy/scipy |
| Construction vs Phase-1 derivative | No | registry JSON, residual_floor, numpy |
| Construction vs Phase-2A polynomial | No | registry JSON, residual_floor, numpy |
| Old final vs Phase-1 | No | registry, residual formula, scipy freqz family |
| Old final vs Phase-2A | No | registry, residual_floor *contract* only |
| Phase-1 vs Phase-2A | No | registry, residual_floor contract, numpy (not the same H routine) |

Phase-2A (`fir_power_polynomial.py`) does not import `spec_checker`,
`search_checker`, `independent_spec_verifier`, or `fir_adaptive`.
It does not call their residual or grid functions.
It builds \(P(x)=|H|^2\\) from exact binary64 autocorrelations and certifies
polynomial sign by Bernstein subdivision.

Witness grid length is 1021 (prime), not 4096 / 131072 / 10007.

## Classification of the Phase-2A certifier

```text
PARTIAL_INDEPENDENCE
```

**Why not STRONG:** the target is still the registered \(S_t\\) (bands + `residual_floor`).
A corrupted registry would mislead every procedure.

**Why not WEAK:** decision procedure is a different mathematical object
(polynomial sign on \(x=\\cos\\omega\\)), different arithmetic (exact rationals),
and a different implementation file with no shared pass/fail function.
"""
    (REPORT_DIR / "PHASE2A_INDEPENDENCE_AUDIT.md").write_text(text, encoding="utf-8")


def write_fir(cert: dict) -> None:
    ev = cert["existing_valid_fir_constructed"]
    pr = cert["existing_valid_fir_probe_confirmatory"]
    em = cert["mechanism_invalid_fir"]
    eb = cert["boundary_invalid_fir"]
    lines = [
        "# PHASE 2A — FIR power-polynomial certification",
        "",
        "Method: squared-magnitude polynomial \(P(x)=c_0+2\\sum c_k T_k(x)\), \(x=\\cos\\omega\);",
        "Bernstein sign certificates on floor-expanded \(S_t\\).",
        "",
        f"Arithmetic: `{cert.get('arithmetic')}`",
        "",
        f"Certificate type: `{cert.get('certificate_type')}`",
        "",
        cert.get("limitation", ""),
        "",
        "## Existing-valid FIR (manuscript constructed; unique occupant files)",
        "",
        f"- unique occupants: {ev['total_unique_occupants']}",
        f"- CERTIFIED_VALID: {ev['CERTIFIED_VALID']}",
        f"- CERTIFIED_INVALID: {ev['CERTIFIED_INVALID']}",
        f"- UNDECIDED: {ev['UNDECIDED']}",
        f"- coverage: {ev['coverage']}",
        "",
        "## Confirmatory probe valids (NOT in the 412 headline; reported separately)",
        "",
        f"- unique occupants: {pr['total_unique_occupants']}",
        f"- CERTIFIED_VALID: {pr['CERTIFIED_VALID']}",
        f"- CERTIFIED_INVALID: {pr['CERTIFIED_INVALID']}",
        f"- UNDECIDED: {pr['UNDECIDED']}",
        "",
        "## Mechanism-invalid FIR",
        "",
        f"- unique occupants: {em['total_unique_occupants']}",
        f"- CERTIFIED_INVALID: {em['CERTIFIED_INVALID']}",
        f"- CERTIFIED_VALID: {em['CERTIFIED_VALID']}",
        f"- UNDECIDED: {em['UNDECIDED']}",
        "",
        "## Boundary-invalid FIR",
        "",
        f"- unique occupants: {eb['total_unique_occupants']}",
        f"- CERTIFIED_INVALID: {eb['CERTIFIED_INVALID']}",
        f"- CERTIFIED_VALID: {eb['CERTIFIED_VALID']}",
        f"- UNDECIDED: {eb['UNDECIDED']}",
        "",
        f"VALID→INVALID contradictions (constructed+probe): {len(cert.get('contradictions_valid_to_invalid', []))}",
        "",
        "## Phase-1 vs Phase-2A (constructed FIR valids only)",
        "",
        "| Phase-1 status | Phase-2A valid | Phase-2A invalid | Phase-2A undecided |",
        "| -------------- | -------------: | ---------------: | -----------------: |",
    ]
    xtab = cert.get("phase1_vs_phase2a_constructed") or {}
    for p1, row in xtab.items():
        lines.append(
            f"| {p1} | {row.get('CERTIFIED_VALID', 0)} | {row.get('CERTIFIED_INVALID', 0)} | {row.get('UNDECIDED', 0)} |"
        )
    lines += [
        "",
        "## Per-task constructed-valid coverage",
        "",
        "| task | frozen valid count | certified valid | contradicted | undecided | coverage |",
        "| ---- | -----------------: | --------------: | -----------: | --------: | -------: |",
    ]
    for r in cert.get("task_coverage_constructed") or []:
        cov = "" if r.get("coverage") is None else f"{r['coverage']:.3f}"
        lines.append(
            f"| {r['task']} | {r['frozen_valid_count']} | {r['certified_valid']} | {r['contradicted']} | {r['undecided']} | {cov} |"
        )
    n100 = sum(1 for r in cert.get("task_coverage_constructed") or [] if r.get("coverage") == 1)
    n95 = sum(1 for r in cert.get("task_coverage_constructed") or [] if (r.get("coverage") or 0) >= 0.95)
    ntasks = len(cert.get("task_coverage_constructed") or [])
    lines += [
        "",
        f"Tasks with 100% constructed-valid certification: {n100}/{ntasks}",
        f"Tasks with ≥95%: {n95}/{ntasks}",
        "",
        "This does **not** replace the frozen universe by the certified subset.",
        "",
    ]
    (REPORT_DIR / "PHASE2A_FIR_CERTIFICATION.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_undecided(cert: dict) -> None:
    rows = [r for r in cert["rows"] if r["role"] == "constructed_valid" and r["phase2a_status"] == "UNDECIDED"]
    reasons = Counter(r.get("reason") for r in rows)
    lines = [
        "# PHASE 2A — UNDECIDED diagnosis (constructed FIR valids)",
        "",
        f"Total constructed FIR valids UNDECIDED: {len(rows)} / {cert['existing_valid_fir_constructed']['total_unique_occupants']}",
        "",
        "## Reason counts",
        "",
    ]
    for k, v in reasons.most_common():
        lines.append(f"- `{k}`: {v}")
        for r in rows:
            if r.get("reason") == k:
                lines.append(f"  - `{r['occupant']}` (n_taps={r.get('n_taps')})")
    if rows:
        lines += ["", "Occupants:", ""]
        for r in rows:
            lines.append(f"- `{r['occupant']}` n_taps={r.get('n_taps')} reason=`{r.get('reason')}`")
    lines += [
        "",
        "Categories:",
        "",
        "* `endpoint_enclosure_limitation`: cosine endpoint sliver not certified;",
        "* `polynomial_arithmetic_resource_limit`: Bernstein node/depth budget;",
        "* `root_isolation_or_depth_limit`: mixed Bernstein coefficients at max depth;",
        "* `exact_equality_ambiguity`: not used as a dump category in this run;",
        "* `implementation_bug`: none identified unless a VALID→INVALID appears.",
        "",
        "Implication for the finite-universe gap: Phase-2A does not relabel occupants.",
        "A certified-valid *subset* must not silently replace \(\\mathcal{U}_t\\).",
        "",
    ]
    (REPORT_DIR / "PHASE2A_UNDECIDED_DIAGNOSIS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_extremum(xcheck: dict) -> None:
    lines = [
        "# PHASE 2A — Extremum cross-check (secondary)",
        "",
        "Stationary points of \(P(\\omega)\\) are found by dense sign-change of \(dP/d\\omega\\).",
        "This is **not** the primary certificate.",
        "",
        f"Audited occupants: {xcheck.get('n')}",
        "",
    ]
    for a in xcheck.get("audits") or []:
        lines.append(
            f"- `{a.get('tag')}` `{a.get('occupant')}` n_taps={a.get('n_taps')} "
            f"P2A={a.get('phase2a_status')} violating_points={a.get('n_violating_grid_or_stat')}"
        )
    lines.append("")
    (REPORT_DIR / "PHASE2A_EXTREMUM_CROSSCHECK.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_all_reports() -> None:
    write_numeric_semantics()
    write_guardrails()
    write_independence()
    cert_p = OUT_DIR / "fir_power_polynomial_certification.json"
    if cert_p.exists():
        cert = json.loads(cert_p.read_text(encoding="utf-8"))
        write_fir(cert)
        write_undecided(cert)
    xp = OUT_DIR / "extremum_crosscheck.json"
    if xp.exists():
        write_extremum(json.loads(xp.read_text(encoding="utf-8")))
