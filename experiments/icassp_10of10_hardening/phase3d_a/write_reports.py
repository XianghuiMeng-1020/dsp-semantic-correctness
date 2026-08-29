"""Write Phase-3D-A result reports. Protocol lock is not overwritten."""
from __future__ import annotations

import json

from experiments.icassp_10of10_hardening.phase3d_a.config import OUT_DIR, REPORT_DIR


def _yn(v) -> str:
    return "YES" if v else "NO"


def write_attrition(attr: list[dict], inv: list[dict]) -> None:
    lines = [
        "# PHASE 3D-A — Generation attrition",
        "",
        "| task | generator | attempts | generation errors | grid-screen fail | continuous valid | continuous invalid | undecided | exact duplicates | H_VALID admitted |",
        "| ---- | --------- | -------: | ----------------: | ---------------: | ---------------: | -----------------: | --------: | ---------------: | ---------------: |",
    ]
    for r in attr:
        lines.append(
            f"| {r['task']} | {r['generator']} | {r['attempts']} | {r['generation_errors']} | {r['grid_screen_fail']} | "
            f"{r['continuous_valid']} | {r['continuous_invalid']} | {r['undecided']} | {r['exact_duplicates']} | {r['H_VALID_admitted']} |"
        )
    lines += [
        "",
        "## Invalid mutations",
        "",
        "| task | mutation | eligible progenitors | attempts | certified invalid | remained valid | undecided | duplicates | admitted |",
        "| ---- | -------- | -------------------: | -------: | ----------------: | -------------: | --------: | ---------: | -------: |",
    ]
    for r in inv:
        lines.append(
            f"| {r['task']} | {r['mutation']} | {r['eligible_progenitors']} | {r['attempts']} | {r['certified_invalid']} | "
            f"{r['remained_valid']} | {r['undecided']} | {r['duplicates']} | {r['admitted']} |"
        )
    lines.append("")
    (REPORT_DIR / "PHASE3D_A_ATTRITION.md").write_text("\n".join(lines), encoding="utf-8")


def write_diversity(div: dict, adeq: dict) -> None:
    lines = [
        "# PHASE 3D-A — Generator diversity",
        "",
        "No reference-catalog distances are reported.",
        "",
        f"- By generator: `{div['by_generator']}`",
        f"- By LP/HP/BP/BS: `{div['by_filter_type']}`",
        f"- By loose/tight: `{div['by_loose_tight']}`",
        f"- Order/taps range: {div['order_min']} … {div['order_max']}",
        f"- Tasks with ≥2 contributing families: {adeq['families_ge2_tasks']} / 20",
        "",
        "## Grid specification residuals (intrinsic, not reference distance)",
        "",
        f"- n: {div['n_with_margin']}",
        f"- min / Q1 / median / Q3 / max worst-band residual: "
        f"{div['margin_min']} / {div['margin_q1']} / {div['margin_median']} / {div['margin_q3']} / {div['margin_max']}",
        f"- near-boundary (worst residual ≤ 1e-4): {div['near_boundary_count']}",
        "",
        "Members were not selected or filtered by margin.",
        "",
    ]
    (REPORT_DIR / "PHASE3D_A_GENERATOR_DIVERSITY.md").write_text("\n".join(lines), encoding="utf-8")


def write_blinding_result(scan: dict) -> None:
    lines = [
        "# PHASE 3D-A — Post-generation no-transfer check",
        "",
        f"Verdict: `{scan['verdict']}`",
        "",
    ]
    if scan["hits"]:
        for h in scan["hits"]:
            lines.append(f"- `{h['path']}` contains `{h['token']}`")
    else:
        lines.append("No Phase-3D-A output contains newly computed transfer, FRR/FAR, catalog distance, or expanded K*.")
    lines.append("")
    (REPORT_DIR / "PHASE3D_A_NO_TRANSFER_CHECK.md").write_text("\n".join(lines), encoding="utf-8")


def write_all_reports() -> None:
    adeq = json.loads((OUT_DIR / "adequacy.json").read_text(encoding="utf-8"))
    div = json.loads((OUT_DIR / "diversity.json").read_text(encoding="utf-8"))
    attr = json.loads((OUT_DIR / "attrition.json").read_text(encoding="utf-8"))
    scan = json.loads((OUT_DIR / "no_transfer_scan.json").read_text(encoding="utf-8"))
    write_attrition(attr["valid"], attr["invalid"])
    write_diversity(div, adeq)
    write_blinding_result(scan)
