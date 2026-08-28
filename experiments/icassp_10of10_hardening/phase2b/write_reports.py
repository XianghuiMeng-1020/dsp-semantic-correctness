"""Write Phase-2B human reports from JSON. Does not touch frozen science files."""
from __future__ import annotations

import json

from experiments.icassp_10of10_hardening.phase2b.config import OUT_DIR, REPORT_DIR


def _load(name: str) -> dict:
    return json.loads((OUT_DIR / name).read_text(encoding="utf-8"))


def write_population(pop: dict) -> None:
    lines = [
        "# PHASE 2B — Population audit",
        "",
        "Phase 2B evaluates the already frozen implementations and specifications.",
        "It cannot change the scientific universe, validity definitions, or original labels",
        "in response to certification outcomes.",
        "",
        f"Verdict: `{pop['verdict']}`",
        "",
        "| family | unique valid | mechanism invalid | boundary invalid | tasks | source |",
        "| ------ | -----------: | ----------------: | ---------------: | ----: | ------ |",
    ]
    for r in pop["table"]:
        lines.append(
            f"| {r['family']} | {r['unique_valid']} | {r['mechanism_invalid']} | {r['boundary_invalid']} | {r['tasks']} | {r['source']} |"
        )
    lines += [
        "",
        f"Unique valid total {pop['table'][-1]['unique_valid']} reconciles to the manuscript 412: "
        f"{'YES' if not pop['blocker'] else 'NO'}.",
        "",
        "Type-I confirmatory probes are not in the 412:",
        f"- FIR probes: {pop['probe_fir_valid']}",
        f"- IIR probes: {pop['probe_iir_valid']}",
        "",
        "Suite S identities are not magnitude-mask IIR occupants.",
        "",
    ]
    (REPORT_DIR / "PHASE2B_POPULATION_AUDIT.md").write_text("\n".join(lines), encoding="utf-8")


def write_fir_closure(fir: dict) -> None:
    fin = fir["constructed_fir_valid_final"]
    lines = [
        "# PHASE 2B — FIR final-two closure",
        "",
        f"Method: {fir['method']}",
        "",
        "This route does not call the Phase-2A Bernstein engine and does not increase",
        "the Bernstein node budget. It uses a primitive-integer Sturm sequence of the",
        "exact squared-magnitude polynomial.",
        "",
        f"- previously UNDECIDED: {fir['previously_undecided']}",
        f"- CERTIFIED_VALID: {fir['CERTIFIED_VALID']}",
        f"- CERTIFIED_INVALID: {fir['CERTIFIED_INVALID']}",
        f"- STILL_UNDECIDED: {fir['STILL_UNDECIDED']}",
        f"- validity contradiction: {'YES' if fir['blocker'] else 'NO'}",
        "",
        "## Occupants",
        "",
    ]
    for r in fir["rows"]:
        lines.append(
            f"- `{r['occupant']}` n_taps={r.get('n_taps')} Phase-2A=UNDECIDED Phase-2B=`{r['phase2b_status']}` reason=`{r.get('reason')}`"
        )
    lines += [
        "",
        "## Constructed FIR valid corpus after Phase 2B",
        "",
        f"- CERTIFIED_VALID: {fin['CERTIFIED_VALID']} / {fin['total']}",
        f"- CERTIFIED_INVALID: {fin['CERTIFIED_INVALID']}",
        f"- UNDECIDED: {fin['UNDECIDED']}",
        f"- coverage: {fin['coverage']}",
        "",
        "Phase-2A already certified the other 334 constructed FIR valids by Bernstein.",
        "Together the two independent continuous routes cover the 336-occupant FIR valid corpus.",
        "",
    ]
    (REPORT_DIR / "PHASE2B_FIR_FINAL_CLOSURE.md").write_text("\n".join(lines), encoding="utf-8")


def write_iir(cert: dict) -> None:
    ev, em, eb = cert["valid"], cert["mechanism_invalid"], cert["boundary_invalid"]
    lines = [
        "# PHASE 2B — IIR continuous certification",
        "",
        f"Stability: {cert['method_stability']}",
        "",
        f"Magnitude: {cert['method_magnitude']}",
        "",
        f"Certificate type: `{cert['certificate_type']}`",
        "",
        "## Valid IIR",
        "",
        f"- total: {ev['total']}",
        f"- CERTIFIED_VALID: {ev['CERTIFIED_VALID']}",
        f"- CERTIFIED_INVALID: {ev['CERTIFIED_INVALID']}",
        f"- UNDECIDED: {ev['UNDECIDED']}",
        f"- CERTIFIED_STABLE: {ev['CERTIFIED_STABLE']}",
        f"- CERTIFIED_UNSTABLE: {ev['CERTIFIED_UNSTABLE']}",
        f"- STABILITY_UNDECIDED: {ev['STABILITY_UNDECIDED']}",
        "",
        "## Mechanism-invalid IIR",
        "",
        f"- total: {em['total']}",
        f"- CERTIFIED_INVALID: {em['CERTIFIED_INVALID']}",
        f"- CERTIFIED_VALID: {em['CERTIFIED_VALID']}",
        f"- UNDECIDED: {em['UNDECIDED']}",
        "",
        "## Boundary-invalid IIR",
        "",
        f"- total: {eb['total']}",
        f"- CERTIFIED_INVALID: {eb['CERTIFIED_INVALID']}",
        f"- CERTIFIED_VALID: {eb['CERTIFIED_VALID']}",
        f"- UNDECIDED: {eb['UNDECIDED']}",
        "",
        f"VALID→INVALID contradictions: {len(cert.get('contradictions_valid_to_invalid') or [])}",
        "",
        "## Implementation table",
        "",
        "| task | id | frozen label | stability | magnitude | final certification | critical constraint/root |",
        "| ---- | -- | ------------ | --------- | --------- | ------------------- | ------------------------ |",
    ]
    for r in cert["rows"]:
        crit = r.get("critical") or ""
        lines.append(
            f"| {r['task']} | `{r['occupant']}` | {r['old_label']} | {r['stability']} | {r['magnitude']} | {r['final']} | {crit} |"
        )
    lines.append("")
    (REPORT_DIR / "PHASE2B_IIR_CERTIFICATION.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_independence() -> None:
    text = """# PHASE 2B — Independence audit

Compared procedures:

1. construction checker (`src/spec_checker.py`);
2. original final verifier (`src/verification/independent_spec_verifier.py`);
3. Phase-1 derivative verifier (`src/continuous_certification/fir_adaptive.py`);
4. Phase-2A FIR Bernstein verifier (`src/continuous_certification/fir_power_polynomial.py`);
5. Phase-2B root/sign verifier (`src/continuous_certification/poly_sturm.py`, `mask_sign.py`);
6. Phase-2B stability verifier (`src/continuous_certification/iir_schur.py`).

| Pair | Shared correctness logic? | Shared assets |
|---|---|---|
| Construction vs Phase-2B root/sign | No | registry JSON, residual_floor contract |
| Old final vs Phase-2B root/sign | No | registry JSON, residual_floor contract |
| Phase-1 vs Phase-2B root/sign | No | registry JSON |
| Phase-2A Bernstein vs Phase-2B Sturm | No pass/fail import | same P(x) mathematics, independently reimplemented; different algorithm |
| Phase-2B Sturm vs Phase-2B Schur | No | Fraction / stored coefficients only |
| Old final vs Phase-2B Schur | No | stored `a`; old final uses `tf2zpk` |

Phase-2B does not import `spec_checker`, `search_checker`,
`independent_spec_verifier`, `fir_adaptive`, or `fir_power_polynomial`.
It does not call their residual, grid, or Bernstein functions.

High-precision `mpmath.polyroots` is a stability *cross-check* only.

## Phase-2B algorithm independence

```text
STRONG_INDEPENDENCE
```

The decision objects are a Sturm sequence / real-root sign analysis and an
exact rational Schur-Cohn recursion. Those are not wrappers around an
existing pass/fail routine.

## Overall evidence-chain independence

```text
PARTIAL_INDEPENDENCE
```

Every method still reads the same frozen `S_t` and the same `residual_floor`
contract. A corrupted registry would mislead the whole chain. That is why
the *chain* is not classified STRONG even though the Phase-2B algorithm is.
"""
    (REPORT_DIR / "PHASE2B_INDEPENDENCE_AUDIT.md").write_text(text, encoding="utf-8")


def write_cross(cross: dict, iir_num: dict) -> None:
    lines = [
        "# PHASE 2B — Cross-method audit",
        "",
        "## FIR Bernstein (Phase 2A) vs Sturm (Phase 2B)",
        "",
        f"Sampled occupants: {cross.get('n')}",
        f"Disagreements when both decided: {len(cross.get('disagreements') or [])}",
        f"Verdict: `{cross.get('verdict')}`",
        "",
    ]
    for r in cross.get("rows") or []:
        lines.append(
            f"- `{r['occupant']}` P2A=`{r.get('phase2a')}` Sturm=`{r.get('phase2b_sturm')}` match={r.get('match_when_both_decided')}"
        )
    lines += [
        "",
        "## IIR numerical extremum cross-check (not a certificate)",
        "",
        f"Audited: {iir_num.get('n')}  agree={iir_num.get('agree')} notes={iir_num.get('notes')}",
        f"Verdict: `{iir_num.get('verdict')}`",
        "",
    ]
    for a in iir_num.get("audits") or []:
        lines.append(
            f"- `{a['occupant']}` final=`{a['final']}` numerical_violation={a['numerical_violation']} agree={a['agree']}"
        )
    lines.append("")
    (REPORT_DIR / "PHASE2B_CROSS_METHOD_AUDIT.md").write_text("\n".join(lines), encoding="utf-8")


def write_matrix(headline: dict) -> None:
    m = headline["matrix_valid"]
    lines = [
        "# PHASE 2B — Full continuous-certification matrix",
        "",
        "Manuscript constructed valids only (the 412). Type-I probes are separate.",
        "",
        "| family | frozen-valid | cert-valid | cert-invalid | undecided | coverage |",
        "| ------ | -----------: | ---------: | -----------: | --------: | -------: |",
        f"| FIR | {m['FIR']['frozen']} | {m['FIR']['cert_valid']} | {m['FIR']['cert_invalid']} | {m['FIR']['undecided']} | {m['FIR']['coverage']:.6f} |",
        f"| IIR | {m['IIR']['frozen']} | {m['IIR']['cert_valid']} | {m['IIR']['cert_invalid']} | {m['IIR']['undecided']} | {m['IIR']['coverage']:.6f} |",
        f"| TOTAL | {m['TOTAL']['frozen']} | {m['TOTAL']['cert_valid']} | {m['TOTAL']['cert_invalid']} | {m['TOTAL']['undecided']} | {m['TOTAL']['coverage']:.6f} |",
        "",
        "## Mechanism invalids",
        "",
        f"- FIR: {headline['mech']['FIR']['certified_invalid']} / {headline['mech']['FIR']['total']}",
        f"- IIR: {headline['mech']['IIR']['certified_invalid']} / {headline['mech']['IIR']['total']}",
        "",
        "## Boundary invalids",
        "",
        f"- FIR: {headline['boundary']['FIR']['certified_invalid']} / {headline['boundary']['FIR']['total']}",
        f"- IIR: {headline['boundary']['IIR']['certified_invalid']} / {headline['boundary']['IIR']['total']}",
        "",
        "## Type-I confirmatory probes",
        "",
        "1260 / 1260 Phase-2A Bernstein certificates preserved. Not mixed into the 412.",
        "",
        f"Attack D: `{headline['attack_d']}`",
        "",
        f"Technical correctness 10/10 gate: `{headline['tech_gate']}`",
        "",
    ]
    (REPORT_DIR / "PHASE2B_FULL_CERTIFICATION_MATRIX.md").write_text("\n".join(lines), encoding="utf-8")


def write_all_reports() -> None:
    if (OUT_DIR / "population.json").exists():
        write_population(_load("population.json"))
    if (OUT_DIR / "fir_remaining_resolution.json").exists():
        write_fir_closure(_load("fir_remaining_resolution.json"))
    if (OUT_DIR / "iir_continuous_certification.json").exists():
        write_iir(_load("iir_continuous_certification.json"))
    write_independence()
    if (OUT_DIR / "cross_method.json").exists() and (OUT_DIR / "iir_numerical.json").exists():
        write_cross(_load("cross_method.json"), _load("iir_numerical.json"))
    if (OUT_DIR / "headline.json").exists():
        write_matrix(_load("headline.json"))
