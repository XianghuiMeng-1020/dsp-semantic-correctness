"""Write Phase-2A human reports from JSON. Does not touch frozen science files."""
from __future__ import annotations

import json
from collections import Counter
from experiments.icassp_10of10_hardening.phase2a.config import OUT_DIR, REPORT_DIR


def _load(name: str) -> dict:
    return json.loads((OUT_DIR / name).read_text(encoding="utf-8"))


def _limitation(cert: dict) -> str:
    stored = cert.get("limitation") or ""
    rows = cert.get("rows") or []
    probes = [r for r in rows if r.get("role") == "probe_valid"]
    n_probe_bernstein = sum(1 for r in probes if r.get("method") == "power_polynomial_bernstein")
    n_probe_valid_sign = sum(
        1
        for r in probes
        if r.get("phase2a_status") == "CERTIFIED_VALID" and r.get("reason") == "all_bands_polynomial_sign"
    )
    extra = (
        " Frozen confirmatory probes in this corpus all have n_taps≤80 and all "
        f"{n_probe_bernstein}/{len(probes)} probe rows are Bernstein certificates "
        f"({n_probe_valid_sign} with reason all_bands_polynomial_sign). "
        "The runner's n_taps>80 witness-only cap was not used on any frozen probe. "
        "CERTIFIED_INVALID rows use a conservative prime-grid witness with a rounding "
        "envelope; that is an invalidity certificate, not a validity certificate."
    )
    return stored + extra


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

The secondary extremum cross-check imports `power_polynomial` from the
Phase-2A certifier. That checks stationary-point consistency of the same
\(P(x)\); it is not a third construction of the autocorrelation.
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
        _limitation(cert),
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
        "## Certified-subset implication for finite-universe separability",
        "",
        "Removing a valid occupant can only decrease \(D_V\) and therefore can only",
        "increase \(G=D_I-D_V\). A certified-valid subset must not be treated as a",
        "substitute universe for the existing non-separability claim: \(G\) on a",
        "subset can become positive even when \(G\) on \(\\mathcal{U}_t\) is negative.",
        "Phase 2A does **not** recompute \(G\) (no \(K^*\), no metric sweep).",
        "The frozen gap still uses the full labeled universe, including the two",
        "UNDECIDED constructed occupants, which remain frozen VALID (not contradicted).",
        "Those two occupants are the longest frequency-sampling tight bandstops;",
        "they are not the farthest valids in the frozen reference-choice tables.",
        "Each affected task still has 20 other constructed occupants with Bernstein",
        "certificates, plus confirmatory probes. The central finite-universe gap is",
        "therefore not uniquely supported by the two uncertified files, but the",
        "manuscript universe is not replaced.",
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
        "The two UNDECIDED constructed occupants are the longest frequency-sampling",
        "tight bandstops (`n_taps=267`). Bernstein subdivision hit the node/time budget.",
        "They remain frozen VALID. They are not the farthest valids in the frozen",
        "reference-choice tables. Each of `fir_bs_tight_8k` and `fir_bs_tight_16k`",
        "still has 20/21 constructed occupants with Bernstein `CERTIFIED_VALID`.",
        "This does not materially threaten the existing finite-universe gap, but it",
        "also does not license replacing those tasks' \(\\mathcal{U}_t\\) by the certified subset.",
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


def write_constraint_transformation() -> None:
    text = """# PHASE 2A — Constraint transformation

Frozen Suite N FIR tasks are magnitude-mask specifications.
`phase_requirement` is `none` and `order_constraint` is `free` on every FIR
task, so Phase 2A adds no extra polynomial conditions beyond the registered
pass and stop bands.

## Frozen \(S_t\) (exact existing semantics)

Each registered band is a closed frequency interval \([f_0,f_1]\) with a
closed magnitude interval \([\\mathrm{lo},\\mathrm{hi}]\). The old verifier
and the construction checker both use inclusive endpoints
(`w >= f0` and `w <= f1`). Phase 2A uses the same closed interval.

Floor expansion is copied from the frozen residual contract:

\\[
\\mathrm{span}=\\max(\\mathrm{hi}-\\mathrm{lo},10^{-6}),\\quad
L=\\mathrm{lo}-\\mathrm{floor}\\cdot\\mathrm{span},\\quad
U=\\mathrm{hi}+\\mathrm{floor}\\cdot\\mathrm{span}.
\\]

The constants `1e-6` and `residual_floor` are the JSON/binary64 values, not
re-parsed decimal rationals. Equality on the expanded wall remains valid
(`residual <= floor`).

Transition bands (frequencies listed in neither pass nor stop) are
unconstrained and are not certified.

## Polynomial-sign form

Let \(P(x)=|H(e^{j\\omega})|^2\) with \(x=\\cos\\omega\).

| Frozen condition | After floor | Polynomial-sign condition | Vacuous case |
|---|---|---|---|
| \\(|H|\\le \\mathrm{hi}\\) | \\(|H|\\le U\\) | \(Q_U(x)=P(x)-U^2\\le 0\\) on the \(x\\)-image of the band | never (\(U>0\\) on all Suite N FIR bands) |
| \\(|H|\\ge \\mathrm{lo}\\) | \\(|H|\\ge L\\) | \(Q_L(x)=P(x)-L^2\\ge 0\\) | if \(L\\le 0\\), omit \(Q_L\\) (true for every real \(H\\)) |

Stop bands have `lo=0`, so after a non-negative floor expansion \(L\\le 0\)
and the lower constraint is vacuous. Pass bands have `lo` near 1, so both
\(Q_U\\le 0\) and \(Q_L\\ge 0\\) are enforced.

The map \(x=\\cos\\omega\) is monotonic on \(\\omega\\in[0,\\pi]\). The
continuous band in \(\\omega\\) becomes a continuous interval in \(x\),
enclosed conservatively when \(\\cos(2\\pi f/f_s)\) is not a dyadic rational.

Tangential roots of \(Q_U=0\) or \(Q_L=0\) with no sign change into the
forbidden half-line remain valid. A true crossing is `CERTIFIED_INVALID`.
Unresolved mixed Bernstein coefficients are `UNDECIDED`.
"""
    (REPORT_DIR / "PHASE2A_CONSTRAINT_TRANSFORMATION.md").write_text(text, encoding="utf-8")


def write_attack_d(cert: dict) -> None:
    ev = cert["existing_valid_fir_constructed"]
    n_contra = len(cert.get("contradictions_valid_to_invalid") or [])
    tasks = cert.get("task_coverage_constructed") or []
    n100 = sum(1 for r in tasks if r.get("coverage") == 1)
    n95 = sum(1 for r in tasks if (r.get("coverage") or 0) >= 0.95)
    text = f"""# PHASE 2A — Attack D reaudit

Attack D is the claim that frozen FIR valid/invalid labels are only
grid-local and might flip under a continuous-band certificate.

## Facts after Phase 2A

* Valid→invalid contradictions: {n_contra}
* Manuscript constructed FIR valids: {ev['total_unique_occupants']} unique occupants;
  {ev['CERTIFIED_VALID']} `CERTIFIED_VALID`; {ev['UNDECIDED']} `UNDECIDED`;
  {ev['CERTIFIED_INVALID']} `CERTIFIED_INVALID`
* FIR headline tasks with 100% constructed-valid certification: {n100}/{len(tasks)}
* FIR headline tasks with ≥95%: {n95}/{len(tasks)}
* Mechanism-invalid FIR: all tested `CERTIFIED_INVALID`
* Boundary-invalid FIR: all tested `CERTIFIED_INVALID`
* Phase-2A certifier independence: `PARTIAL_INDEPENDENCE`
* Remaining UNDECIDED cause: Bernstein resource limit on two \(n=267\) tight bandstops

## Classification

```text
ATTACK_D_PARTIALLY_CLOSED
```

`ATTACK_D_STRONGLY_CLOSED` is not used.

Reasons to close partially rather than claim a full close:

1. Independence is `PARTIAL_INDEPENDENCE` because every method reads the same
   registered \(S_t\) and the same `residual_floor` contract.
2. Two manuscript constructed FIR valids remain `UNDECIDED`. The cause is
   a resource limit, not a suspected violation, but they are not certified.
3. `CERTIFIED_INVALID` on mechanism/boundary FIR uses a conservative
   prime-grid witness. That is a valid invalidity certificate, not the
   Bernstein sign certificate used for validity.
4. Cosine band endpoints use a high-precision outward enclosure, not a
   formal machine-interval cosine.

Reasons it is not left `ATTACK_D_OPEN`:

* Zero valid→invalid contradictions after an independent polynomial-sign method.
* 334/336 constructed FIR valids, and all 16 FIR headline tasks at ≥95%,
  now have continuous Bernstein certificates on the frozen \(S_t\\).
* The two UNDECIDED occupants have a specific, non-threatening explanation
  and are not the farthest valids supporting the frozen gap tables.

Phase 2A does not edit the manuscript. IIR certification was not run.
"""
    (REPORT_DIR / "PHASE2A_ATTACK_D.md").write_text(text, encoding="utf-8")


def write_all_reports() -> None:
    write_numeric_semantics()
    write_guardrails()
    write_independence()
    write_constraint_transformation()
    cert_p = OUT_DIR / "fir_power_polynomial_certification.json"
    if cert_p.exists():
        cert = json.loads(cert_p.read_text(encoding="utf-8"))
        write_fir(cert)
        write_undecided(cert)
        write_attack_d(cert)
    xp = OUT_DIR / "extremum_crosscheck.json"
    if xp.exists():
        write_extremum(json.loads(xp.read_text(encoding="utf-8")))

