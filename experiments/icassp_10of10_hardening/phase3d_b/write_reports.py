"""Write remaining Phase-3D-B reports from frozen JSON. Protocol lock is not overwritten."""
from __future__ import annotations

import json

from experiments.icassp_10of10_hardening.phase3d_b.config import OUT_DIR, REPORT_DIR


def _f(x, nd=6):
    if x is None:
        return "—"
    return f"{float(x):.{nd}g}"


def write_remaining_reports() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    hier = json.loads((OUT_DIR / "hierarchy_transfer.json").read_text(encoding="utf-8"))
    inv = json.loads((OUT_DIR / "invalid_secondary.json").read_text(encoding="utf-8"))
    gen = json.loads((OUT_DIR / "generator_structure_transfer.json").read_text(encoding="utf-8"))
    maint = json.loads((OUT_DIR / "maintenance.json").read_text(encoding="utf-8")) if (OUT_DIR / "maintenance.json").exists() else None

    lines = [
        "# PHASE 3D-B — Reference hierarchy transfer",
        "",
        "Same base-only maximal-safe threshold. H_VALID was not used to choose oracles.",
        "",
        "| oracle | coeff base exact? | coeff H_VALID transfer | response base exact? | response H_VALID transfer |",
        "| ------ | ----------------- | ---------------------: | -------------------- | ------------------------: |",
    ]
    for o in hier["oracles"]:
        lines.append(
            f"| {o['oracle']} | {o['coeff_base_exact_tasks']}/20 | {_f(o['coeff_transfer'])} | "
            f"{o['resp_base_exact_tasks']}/20 | {_f(o['resp_transfer'])} |"
        )
    lines += [
        "",
        "Increasing catalog size on the finite base universe does not automatically improve",
        "prospective coefficient transfer. Response transfer rises sharply only at Phase-3B K*_obs.",
        "",
    ]
    (REPORT_DIR / "PHASE3D_B_HIERARCHY.md").write_text("\n".join(lines), encoding="utf-8")

    glines = [
        "# PHASE 3D-B — Generator-family and DSP-structural transfer",
        "",
        "Generator groups were frozen in Phase 3D-A. They were not inferred from rejection.",
        "",
        "| generator | n | coeff transfer | response transfer |",
        "| --------- | -: | -------------: | ----------------: |",
    ]
    for r in gen["generators"]:
        glines.append(f"| {r['generator']} | {r['n']} | {_f(r['coeff_transfer'])} | {_f(r['resp_transfer'])} |")
    glines += [
        "",
        f"Generator-effect verdict: `{gen['generator_effect_verdict']}`",
        "",
        f"Order-bin definition: {gen['order_bin_definition']}",
        "",
        f"Structure (coeff): {gen['structure']['coeff']}",
        "",
        f"Structure (resp): {gen['structure']['resp']}",
        "",
    ]
    (REPORT_DIR / "PHASE3D_B_GENERATOR_STRUCTURE.md").write_text("\n".join(glines), encoding="utf-8")

    ilines = [
        "# PHASE 3D-B — Secondary H_INVALID",
        "",
        "> H_INVALID does not provide balanced prospective invalid coverage across all 20 tasks.",
        "",
        f"- Total: {inv['H_INVALID_total']}",
        f"- Tasks represented: {inv['tasks_represented']}",
        f"- Coefficient false accept: {inv['metrics']['coeff']['false_accept']} / {inv['metrics']['coeff']['n']} ({_f(inv['metrics']['coeff']['false_accept_rate'])})",
        f"- Response false accept: {inv['metrics']['resp']['false_accept']} / {inv['metrics']['resp']['n']} ({_f(inv['metrics']['resp']['false_accept_rate'])})",
        "",
        "No 20-task macro FAR is computed.",
        "",
    ]
    (REPORT_DIR / "PHASE3D_B_INVALID.md").write_text("\n".join(ilines), encoding="utf-8")

    if maint:
        cs = maint["coeff_suite"]
        mlines = [
            "# PHASE 3D-B — Catalog maintenance (not a new algorithm)",
            "",
            "Phase-3B K* is unaltered. V+ = V_base union H_VALID. Invalids remain the frozen base set.",
            "",
            f"- Coeff tasks exact / bounded: {cs['tasks_exact']} / {cs['tasks_bounded']}",
            f"- Expanded median K* coeff: {_f(cs['expanded_median_K'])}",
            f"- Median ΔK / relative growth: {_f(cs['median_delta_K'])} / {_f(cs['median_relative_growth'])}",
            f"- LOW / MODERATE / HIGH: {cs['low']} / {cs['moderate']} / {cs['high']}",
            f"- Tasks with M*>0: {cs['tasks_M_pos']}; median M*={_f(cs['median_M'])}; max M*={cs['max_M']}",
            f"- Median / max J*: {_f(cs['median_J'])} / {cs['max_J']}",
            f"- Verdict: `{cs['verdict']}`",
            "",
            "| task | K*_base | H_VALID n | K*_expanded | ΔK | relative growth | rho_base | rho_expanded |",
            "| ---- | ------: | --------: | ----------: | -: | --------------: | -------: | -----------: |",
        ]
        for r in maint["coeff"]["tasks"]:
            mlines.append(
                f"| {r['task']} | {r['K_star_base']} | {r['H_VALID_n']} | {r['K_star_expanded']} | "
                f"{r['delta_K']} | {_f(r['relative_growth'])} | {_f(r['rho_base'])} | {_f(r['rho_expanded'])} |"
            )
        mlines += [
            "",
            "| task | original K* | prospective valid n | transfer rejected | J* added references | final catalog size |",
            "| ---- | ----------: | ------------------: | ----------------: | ------------------: | -----------------: |",
        ]
        for r in maint["coeff"]["tasks"]:
            mlines.append(
                f"| {r['task']} | {r['original_K']} | {r['H_VALID_n']} | {r['transfer_rejected']} | "
                f"{r['J_star']} | {r['final_catalog_size']} |"
            )
        mlines.append("")
        (REPORT_DIR / "PHASE3D_B_MAINTENANCE.md").write_text("\n".join(mlines), encoding="utf-8")


if __name__ == "__main__":
    write_remaining_reports()
