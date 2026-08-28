"""Write Phase-3A result-dependent reports. Static prior-art/metric/dual files are not overwritten."""
from __future__ import annotations

import json

from experiments.icassp_10of10_hardening.phase3a.config import OUT_DIR, REPORT_DIR


def _f(x, n=8):
    if x is None:
        return "n/a"
    if x == "+INF":
        return "+INF"
    return f"{float(x):.{n}g}"


def _load():
    return {name: json.loads((OUT_DIR / f"{name}.json").read_text(encoding="utf-8")) for name in (
        "headline",
        "metric_geometry",
        "coefficient_ambient",
        "response_ambient",
        "hierarchy",
        "validation",
        "novelty",
    )}


def write_validation(data: dict) -> None:
    v = data["validation"]
    syn = v["synthetic"]
    lines = [
        "# PHASE 3A — Ambient validation",
        "",
        f"Verdict: `{v['verdict']}`",
        "",
        "## Synthetic",
        "",
        f"- A (separated clusters): {syn['A_separable_clusters']['kind']} pass={syn['A_separable_clusters']['pass']}",
        f"- B (nested square): {syn['B_nested_square']['kind']} pass={syn['B_nested_square']['pass']}",
        f"- C (canonical fails, ambient succeeds): {syn['C_canonical_fails_ambient_succeeds']['kind']} pass={syn['C_canonical_fails_ambient_succeeds']['pass']}",
        "",
        "## Check D",
        "",
        "If a frozen canonical Euclidean gap is already positive, the ambient solver must not report `NO_AMBIENT_CENTER`.",
        "",
        f"- coefficient check D: `{v['check_D_coeff']}`",
        f"- response check D: `{v['check_D_resp']}`",
        "",
        "## Check E — second optimizer / independent dual",
        "",
    ]
    for tid, rec in (v.get("independent_checks") or {}).items():
        lines.append(f"- `{tid}`: kind_agree={rec.get('kind_agree')} gamma_close={rec.get('gamma_close')} strong_duality={rec.get('strong_duality_numeric')} pass={rec.get('pass')}")
    lines += ["", "## Engine", "", "The optimizer is `scipy.optimize.linprog` on the ambient primal/dual. It does not call Phase-1 `gap_for_reference`.", ""]
    (REPORT_DIR / "PHASE3A_AMBIENT_VALIDATION.md").write_text("\n".join(lines), encoding="utf-8")


def write_hierarchy(data: dict) -> None:
    h = data["hierarchy"]
    c = data["coefficient_ambient"]
    lines = [
        "# PHASE 3A — Reference hierarchy",
        "",
        "Level 1 = frozen canonical \(G_r\). Level 2 = Phase-1 `best_observed_valid_reference` \(G_{\\mathrm{obs}}^\\star\). Level 3 = ambient-center margin \(\\Gamma^{\\mathrm{amb}}\).",
        "",
        "## Coefficient",
        "",
        f"- Type A (canonical fail → observed fail → ambient fail): {h['coeff']['counts']['A']}",
        f"- Type B (canonical fail → observed fail → ambient succeeds): {h['coeff']['counts']['B']}",
        f"- Type C (canonical fail → observed succeeds): {h['coeff']['counts']['C']}",
        f"- Type D (canonical succeeds): {h['coeff']['counts']['D']}",
        "",
        "| task | canonical G | best-observed G* | ambient status | ambient margin | exact single-center exists | type | certificate |",
        "| ---- | ----------: | ---------------: | -------------- | -------------: | -------------------------- | ---- | ----------- |",
    ]
    by = {r["task"]: r for r in c["tasks"]}
    for row in h["coeff"]["rows"]:
        t = by[row["task"]]
        lines.append(
            f"| {row['task']} | {_f(row['canonical_G'])} | {_f(row['best_observed_valid_reference'])} | "
            f"{row['ambient_status']} | {_f(row['ambient_margin'])} | {t['exact_single_center_exists']} | "
            f"{row['type']} | {t['certificate_strength']} |"
        )
    if h.get("resp"):
        r = data["response_ambient"]
        rb = {x["task"]: x for x in r["tasks"]}
        lines += [
            "",
            "## Response (secondary)",
            "",
            f"- Type A: {h['resp']['counts']['A']}",
            f"- Type B: {h['resp']['counts']['B']}",
            f"- Type C: {h['resp']['counts']['C']}",
            f"- Type D: {h['resp']['counts']['D']}",
            "",
            "| task | canonical G | best-observed G* | ambient status | ambient margin | type | precision |",
            "| ---- | ----------: | ---------------: | -------------- | -------------: | ---- | --------- |",
        ]
        for row in h["resp"]["rows"]:
            t = rb[row["task"]]
            lines.append(
                f"| {row['task']} | {_f(row['canonical_G'])} | {_f(row['best_observed_valid_reference'])} | "
                f"{row['ambient_status']} | {_f(row['ambient_margin'])} | {row['type']} | {t['precision_stability']} |"
            )
    lines += [
        "",
        "## Claim guardrail",
        "",
        "Even if every coefficient task is Type A, the supported statement is only:",
        "",
        "> No single Euclidean-distance threshold center in the evaluated coefficient representation can recover specification membership over the frozen finite universe.",
        "",
    ]
    (REPORT_DIR / "PHASE3A_REFERENCE_HIERARCHY.md").write_text("\n".join(lines), encoding="utf-8")


def write_novelty(data: dict) -> None:
    n = data["novelty"]
    lines = [
        "# PHASE 3A — Novelty red-team",
        "",
        "Attacks assume a knowledgeable reviewer. Phase 3A does not make the sphere LP novel.",
        "",
    ]
    for key in ("N1", "N2", "N3", "N4", "N5", "N6"):
        a = n["attacks"][key]
        lines += [
            f"## {key}. {a['title']}",
            "",
            f"- Severity before Phase 3A: {a['severity_before']}",
            f"- Evidence after Phase 3A: {a['evidence_after']}",
            f"- Residual severity: {a['residual']}",
            f"- Manuscript-safe defense: {a['defense']}",
            f"- Additional science needed: {a['more_science']}",
            "",
        ]
    lines += [
        "## K* decision (not run)",
        "",
        f"`KSTAR_NEXT = {n['KSTAR_NEXT']}`",
        "",
        n["kstar_rationale"],
        "",
        "## Claim gates",
        "",
        f"- Q1 generic oracle novel? {n['Q1']}",
        f"- Q2 generic sphere LP novel? {n['Q2']}",
        f"- Q3 manuscript-specific: {n['Q3']}",
        f"- Q4 testing reviewer 'already known'? {n['Q4']}",
        f"- Q5 SP reviewer sees a DSP contribution? {n['Q5']}",
        "",
    ]
    (REPORT_DIR / "PHASE3A_NOVELTY_REDTEAM.md").write_text("\n".join(lines), encoding="utf-8")


def write_contribution(data: dict) -> None:
    c = data["novelty"]["contribution"]
    lines = [
        "# PHASE 3A — Contribution options",
        "",
        "Manuscript text is not edited. These are internal framings.",
        "",
    ]
    for name in ("A", "B", "C"):
        opt = c["options"][name]
        lines += [
            f"## Candidate {name} — {opt['name']}",
            "",
            opt["text"],
            "",
            f"- novelty: {opt['novelty']}",
            f"- ICASSP fit: {opt['icassp_fit']}",
            f"- mathematical defensibility: {opt['math']}",
            f"- page cost: {opt['page_cost']}",
            f"- reviewer attack resistance: {opt['resistance']}",
            "",
        ]
    lines += [f"## Selected: Candidate {c['best']}", "", c["why"], ""]
    (REPORT_DIR / "PHASE3A_CONTRIBUTION_OPTIONS.md").write_text("\n".join(lines), encoding="utf-8")


def write_all_reports() -> None:
    data = _load()
    write_validation(data)
    write_hierarchy(data)
    write_novelty(data)
    write_contribution(data)
