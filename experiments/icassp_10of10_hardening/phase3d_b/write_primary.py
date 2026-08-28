"""Write primary-transfer markdown tables. Protocol lock is not overwritten."""
from __future__ import annotations

import json

from experiments.icassp_10of10_hardening.phase3d_b.config import OUT_DIR, REPORT_DIR


def _f(x, nd=6):
    if x is None:
        return "—"
    return f"{float(x):.{nd}g}"


def _table(rows: list[dict]) -> list[str]:
    lines = [
        "| task | H_VALID n | K*_base | tau_maxsafe | accepted | rejected | transfer | external FRR |",
        "| ---- | --------: | ------: | ----------: | -------: | -------: | -------: | -----------: |",
    ]
    for r in rows:
        lines.append(
            f"| {r['task']} | {r['H_VALID_n']} | {r['K_star_base']} | {_f(r['tau'])} | "
            f"{r['accepted']} | {r['rejected']} | {_f(r['transfer'])} | {_f(r['external_FRR'])} |"
        )
    return lines


def write_primary_report() -> None:
    coeff = json.loads((OUT_DIR / "transfer_coeff.json").read_text(encoding="utf-8"))
    resp = json.loads((OUT_DIR / "transfer_resp.json").read_text(encoding="utf-8"))
    sens = json.loads((OUT_DIR / "threshold_sensitivity.json").read_text(encoding="utf-8"))
    lines = [
        "# PHASE 3D-B — Primary prospective valid-realization transfer",
        "",
        "Catalogs and thresholds were frozen before scoring. H_VALID was not used to select",
        "catalogs or tau. Coefficient and response are separate. Reference rejection is",
        "not evidence of invalidity.",
        "",
        "## Coefficient",
        "",
        f"- Pooled transfer: `{_f(coeff['pooled_transfer'])}` ({coeff['accepted']} / {coeff['H_VALID']})",
        f"- Task-macro mean / median: `{_f(coeff['task_macro_mean'])}` / `{_f(coeff['task_macro_median'])}`",
        f"- Min / max: `{_f(coeff['min_task_transfer'])}` / `{_f(coeff['max_task_transfer'])}`",
        f"- Tasks ≥95% / 75–95% / <75%: {coeff['tasks_ge95']} / {coeff['tasks_75_95']} / {coeff['tasks_lt75']}",
        f"- FIR / IIR macro: `{_f(coeff['fir_macro'])}` / `{_f(coeff['iir_macro'])}`",
        f"- Loose / tight: `{_f(coeff['loose_macro'])}` / `{_f(coeff['tight_macro'])}`",
        f"- LP / HP / BP / BS: `{_f(coeff['lp_macro'])}` / `{_f(coeff['hp_macro'])}` / `{_f(coeff['bp_macro'])}` / `{_f(coeff['bs_macro'])}`",
        f"- Verdict: `{coeff['verdict']}`",
        "",
        *_table(coeff["rows"]),
        "",
        "## Response",
        "",
        f"- Pooled transfer: `{_f(resp['pooled_transfer'])}` ({resp['accepted']} / {resp['H_VALID']})",
        f"- Task-macro mean / median: `{_f(resp['task_macro_mean'])}` / `{_f(resp['task_macro_median'])}`",
        f"- Tasks ≥95% / <75%: {resp['tasks_ge95']} / {resp['tasks_lt75']}",
        f"- FIR / IIR macro: `{_f(resp['fir_macro'])}` / `{_f(resp['iir_macro'])}`",
        f"- Verdict: `{resp['verdict']}`",
        "",
        *_table(resp["rows"]),
        "",
        "## Midpoint-threshold sensitivity",
        "",
        f"- Coefficient: `{sens['coeff']}`",
        f"- Response: `{sens['resp']}`",
        "",
        "Primary remains `tau_maxsafe`.",
        "",
    ]
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "PHASE3D_B_PRIMARY_TRANSFER.md").write_text("\n".join(lines), encoding="utf-8")
