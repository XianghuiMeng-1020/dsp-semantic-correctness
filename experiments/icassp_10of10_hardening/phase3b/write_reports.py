"""Write Phase-3B result-dependent reports. Static protocol/audit/prior-art files are not overwritten."""
from __future__ import annotations

import json

from experiments.icassp_10of10_hardening.phase3b.config import OUT_DIR, REPORT_DIR


def _f(x, n=6):
    if x is None:
        return "n/a"
    if isinstance(x, bool):
        return "1" if x else "0"
    return f"{float(x):.{n}g}"


def _load():
    names = (
        "headline",
        "reference_catalog_complexity",
        "validation",
        "ambient_vs_catalog",
        "novelty",
        "coeff_summary",
        "resp_summary",
    )
    return {n: json.loads((OUT_DIR / f"{n}.json").read_text(encoding="utf-8")) for n in names}


def write_validation(d: dict) -> None:
    v = d["validation"]
    lines = ["# PHASE 3B — K* validation", "", f"Verdict: `{v['verdict']}`", "", "| task | K* | gap ok | gap match | K*-1 feasible | lower bound | pass |", "| --- | ---: | --- | --- | --- | --- | --- |"]
    for c in v["checks"]:
        lines.append(
            f"| {c['task']} | {c['k']} | {c['gap_ok']} | {c['gap_match']} | {c['k_minus_feasible']} | {c['lower_bound_ok']} | {c['pass']} |"
        )
    lines += ["", f"Unexpected coefficient K*=1: {v['unexpected_k1']}", ""]
    (REPORT_DIR / "PHASE3B_KSTAR_VALIDATION.md").write_text("\n".join(lines), encoding="utf-8")


def write_hierarchy_table(d: dict) -> None:
    rcc = d["reference_catalog_complexity"]
    lines = [
        "# PHASE 3B — Observed-valid reference catalog complexity",
        "",
        r"Primary quantity: \(K_{t,\mathrm{obs}}^{\star}\), the minimum number of observed valid realizations such that the existing min-distance / common-threshold oracle exactly recovers frozen membership. Set-cover is used only as a computational reduction.",
        "",
        "| task | metric | n_valid | n_invalid | K=1 | K=3 | K=5 | all-library | K*_obs | K*/n_valid |",
        "| ---- | ------ | ------: | --------: | --- | --- | --- | ----------- | -----: | ---------: |",
    ]
    for t in rcc["coeff"]["tasks"]:
        e = t["existing"]
        lines.append(
            f"| {t['task']} | coeff | {t['n_valid']} | {t['n_invalid']} | "
            f"{int(bool(e.get('K1')))} | {int(bool(e.get('K3')))} | {int(bool(e.get('K5')))} | "
            f"{int(bool(e.get('all_library')))} | {t['K_obs_star']} | {_f(t['rho'])} |"
        )
    if rcc.get("resp"):
        lines += ["", "## Response", ""]
        for t in rcc["resp"]["tasks"]:
            e = t["existing"]
            lines.append(
                f"| {t['task']} | resp | {t['n_valid']} | {t['n_invalid']} | "
                f"{int(bool(e.get('K1')))} | {int(bool(e.get('K3')))} | {int(bool(e.get('K5')))} | "
                f"{int(bool(e.get('all_library')))} | {t['K_obs_star']} | {_f(t['rho'])} |"
            )
    (REPORT_DIR / "PHASE3B_REFERENCE_CATALOG_COMPLEXITY.md").write_text("\n".join(lines), encoding="utf-8")


def write_ambient(d: dict) -> None:
    a = d["ambient_vs_catalog"]
    lines = [
        "# PHASE 3B — Ambient center vs realizable catalog",
        "",
        f"- R1 ambient exists + low K*: {a['counts']['R1']}",
        f"- R2 ambient exists + high/near-enumerative K*: {a['counts']['R2']}",
        f"- R3 no ambient center + high/near-enumerative K*: {a['counts']['R3']}",
        f"- R4 other/mixed: {a['counts']['R4']}",
        "",
        "| task | ambient | K*_obs | ρ | band | class |",
        "| ---- | ------- | -----: | -: | ---- | ----- |",
    ]
    for r in a["rows"]:
        lines.append(f"| {r['task']} | {r['ambient']} | {r['K_obs_star']} | {_f(r['rho'])} | {r['burden_band']} | {r['class']} |")
    (REPORT_DIR / "PHASE3B_AMBIENT_VS_CATALOG.md").write_text("\n".join(lines), encoding="utf-8")


def write_redteam(d: dict) -> None:
    n = d["novelty"]
    lines = [
        "# PHASE 3B — Novelty red-team",
        "",
        "## Attack K1. This is just set cover.",
        "",
        f"- Residual: {n['attacks']['K1']}. Honest response: the reduction is known. The manuscript-specific object is the DSP catalog-burden diagnostic, not the optimizer.",
        "",
        "## Attack K2. Of course more prototypes help.",
        "",
        f"- Residual: {n['attacks']['K2']}. The quantitative question is how many observed valids are required for exact recovery, not whether adding references can help.",
        "",
        "## Attack K3. The finite universe makes K* artificial.",
        "",
        f"- Residual: {n['attacks']['K3']}. Yes, this is a finite-universe diagnostic. It does not bound the infinite implementation set. That limitation is explicit.",
        "",
        "## Attack K4. Why not use the ambient center if it works?",
        "",
        f"- Residual: {n['attacks']['K4']}. Phase 3A centers need not be realizable filters. Phase 3B asks the realizable-catalog question the existing oracle actually uses.",
        "",
        "## Attack K5. Why insist references be real implementations?",
        "",
        f"- Residual: {n['attacks']['K5']}. Because the published oracle family scores distance to realizations, not to an abstract ambient point.",
        "",
        "## Attack K6. This is prototype classification, not signal processing.",
        "",
        f"- Residual: {n['attacks']['K6']}. The object is specification-defined filter membership vs realization catalogs. Prototype selection is the computational means.",
        "",
        f"NOVELTY_10OF10_GATE: `{n['NOVELTY_10OF10_GATE']}`",
        "",
        n["strongest_novelty"],
        "",
    ]
    (REPORT_DIR / "PHASE3B_NOVELTY_REDTEAM.md").write_text("\n".join(lines), encoding="utf-8")


def write_contribution(d: dict) -> None:
    n = d["novelty"]
    lines = [
        "# PHASE 3B — Contribution options",
        "",
        "## Candidate A — conservative",
        "",
        "Specification-defined correctness vs canonical reference matching.",
        "",
        "- novelty 6.2; DSP 8.0; defensibility 9.0; 4-page cost low; simplicity high; resistance medium.",
        "",
        "## Candidate B — reference adequacy hierarchy",
        "",
        "canonical → best observed valid → ambient center → realizable catalog complexity.",
        "",
        "- novelty 7.0; DSP 8.0; defensibility 8.0; 4-page cost medium; simplicity medium; resistance medium-high.",
        "",
        "## Candidate C — certified reference-oracle adequacy audit",
        "",
        "continuous certification + fixed-center gap + observed-center robustness + minimal catalog burden.",
        "",
        "- novelty 7.4; DSP 7.5; defensibility 7.5; 4-page cost high; simplicity lower; resistance high if all pieces stay.",
        "",
        f"## Selected: {n['best_framing']}",
        "",
        "Choose the simplest framing that the Type-B ambient result and the catalog-burden numbers can jointly support.",
        "",
    ]
    (REPORT_DIR / "PHASE3B_CONTRIBUTION_OPTIONS.md").write_text("\n".join(lines), encoding="utf-8")


def write_all_reports() -> None:
    d = _load()
    write_validation(d)
    write_hierarchy_table(d)
    write_ambient(d)
    write_redteam(d)
    write_contribution(d)
