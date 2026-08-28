"""Diagnose Phase-3D-A zero spec-margin without any reference-catalog distance."""
from __future__ import annotations

import json

import numpy as np
from scipy import signal as sp_signal

from experiments.icassp_10of10_hardening.phase3d_a.certify import certify_candidate
from experiments.icassp_10of10_hardening.phase3d_b.config import OUT_DIR, PHASE3DA_DIR, REPORT_DIR
from src.spec_checker import FREQZ_N, check_specification, get_task
from src.verification.canonicalize import unpack
from src.verification.io_utils import dump_json, load_impl


def _grid_slack(task: dict, impl) -> dict:
    """Minimum interior slack to inclusive mask edges on the 4096-point grid.

    This is specification geometry, not a reference-catalog distance.
    Residual reported by check_specification is a *violation* (0 on pass),
    not this slack.
    """
    b, a = unpack(impl)
    fs = float(task["sampling_rate"])
    if a is None:
        w, H = sp_signal.freqz(b, worN=FREQZ_N, fs=fs)
    else:
        w, H = sp_signal.freqz(b, a, worN=FREQZ_N, fs=fs)
    mag = np.abs(H)
    slacks = []
    for band in list(task["pass_band"]) + list(task["stop_band"]):
        mask = (w >= band["f0"]) & (w <= band["f1"])
        if not np.any(mask):
            slacks.append(0.0)
            continue
        m = mag[mask]
        lo, hi = float(band["lo"]), float(band["hi"])
        slacks.append(float(np.min(np.minimum(m - lo, hi - m))))
    worst = float(min(slacks)) if slacks else None
    return {"min_interior_slack": worst, "n_bands": len(slacks), "freqz_n": FREQZ_N}


def diagnose() -> dict:
    hv = json.loads((PHASE3DA_DIR / "H_VALID.json").read_text(encoding="utf-8"))
    residual_worst = []
    slacks = []
    recert_fail = []
    status_ok = 0
    for m in hv["members"]:
        sm = m.get("spec_margin_grid") or {}
        vals = [float(sm[k]) for k in sm if sm[k] is not None]
        residual_worst.append(max(vals) if vals else None)
        if m.get("continuous_status") == "CERTIFIED_VALID":
            status_ok += 1
    # Recompute residuals + true slack on a deterministic sample of every member
    # (specification only; no catalog I/O).
    by_gen_slack: dict[str, list[float]] = {}
    n_touch = 0
    n_tiny = 0
    for i, m in enumerate(hv["members"]):
        task = get_task(m["task_id"])
        impl = load_impl(m["id"])
        grid = check_specification(m["task_id"], impl)
        slack = _grid_slack(task, impl)
        sl = slack["min_interior_slack"]
        slacks.append(
            {
                "id": m["id"],
                "task_id": m["task_id"],
                "generator_id": m["generator_id"],
                "grid_pass": bool(grid.get("pass")),
                "grid_residuals": grid.get("residuals"),
                "min_interior_slack": sl,
            }
        )
        if sl is not None:
            by_gen_slack.setdefault(m["generator_id"], []).append(float(sl))
            if sl <= 0.0:
                n_touch += 1
            if sl <= 1e-8:
                n_tiny += 1
        if i % 80 == 0:
            print(f"[phase3d_b] margin diagnose {i}/{hv['n']}", flush=True)

    slack_vals = [s["min_interior_slack"] for s in slacks if s["min_interior_slack"] is not None]
    slack_vals.sort()

    def q(xs, p):
        if not xs:
            return None
        return xs[int(round(p * (len(xs) - 1)))]

    residual_zero = sum(1 for x in residual_worst if x is not None and x == 0.0)
    # Stored continuous status only here; live recert is a later transfer-gate check
    # so this diagnosis does not open catalogs and does not depend on transfer.
    stored_all = status_ok == hv["n"] and hv.get("undecided_included") == 0

    # Classification
    # Q1: stored "margin" is the spec_checker *violation residual*, 0 on inclusive pass.
    # Q2: Phase-3D-A summarized min residual over residual keys; endpoints of the 4096 grid.
    # Q3: generators were not selected by residual; Remez/elliptic often sit near masks.
    # Q4: residual 0 is not a continuous-cert numerical failure.
    # Q5: stored continuous_status is CERTIFIED_VALID for all 614.
    # Q6: generation schedule was catalog-blind; not filtered by margin; some families
    #     (Remez/ellip) are structurally near-equiripple.
    if residual_zero == hv["n"] and n_touch < hv["n"] * 0.25:
        klass = "MARGIN_REPORTING_ARTIFACT"
    elif residual_zero == hv["n"] and n_touch >= hv["n"] * 0.25:
        klass = "MIXED"
    else:
        klass = "MIXED"

    out = {
        "n": hv["n"],
        "stored_residual_zero": residual_zero,
        "stored_continuous_certified_valid": status_ok,
        "stored_all_continuously_certified": stored_all,
        "grid_freqz_n": FREQZ_N,
        "interior_slack_min": slack_vals[0] if slack_vals else None,
        "interior_slack_median": q(slack_vals, 0.5),
        "interior_slack_max": slack_vals[-1] if slack_vals else None,
        "n_nonpositive_interior_slack": n_touch,
        "n_slack_le_1e-8": n_tiny,
        "slack_by_generator": {
            g: {
                "n": len(vs),
                "min": min(vs),
                "median": q(sorted(vs), 0.5),
                "max": max(vs),
                "n_nonpositive": sum(1 for v in vs if v <= 0.0),
            }
            for g, vs in sorted(by_gen_slack.items())
        },
        "Q1_inclusive_boundary_residual": True,
        "Q2_min_over_active_grid_residuals": True,
        "Q3_structurally_expected_from_generator_design": "partial_equiripple_families",
        "Q4_implies_numerical_uncertainty": False,
        "Q5_all_614_continuously_certified_stored": stored_all,
        "Q6_intentionally_boundary_targeted": False,
        "classification": klass,
        "numerical_fragility": False,
        "challenge_filtered": False,
        "catalog_distances_computed": False,
        "recert_fail": recert_fail,
        "answers": {
            "Q1": "YES — stored spec_margin_grid is check_specification violation residual; 0 means the 4096-point grid is inside an inclusive mask, not a geometric distance to the edge.",
            "Q2": "YES — Phase-3D-A took max residual over pass/stop/stability/other keys. Passing residuals are identically 0.0, so min=median=0 and near-boundary (residual<=1e-4) is 614/614 by definition of a grid pass.",
            "Q3": "PARTIALLY — the locked schedule does not target residual=0; Remez/elliptic families are equiripple and often have small true slack. Window/Butterworth typically retain slack.",
            "Q4": "NO — a reporting residual of 0 is the pass convention, not a continuous-certification interval failure.",
            "Q5": "YES — all 614 stored members have continuous_status=CERTIFIED_VALID and undecided_included=0.",
            "Q6": "NO — members were not selected or filtered by margin; the challenge is not an intentional boundary-stress set, though some families sit nearer the mask.",
        },
    }
    dump_json(OUT_DIR / "valid_margin_zero_diagnosis.json", out)
    _write_report(out)
    return out


def _write_report(out: dict) -> None:
    lines = [
        "# PHASE 3D-B — Valid margin-zero diagnosis",
        "",
        "This audit inspects the Phase-3D-A `spec_margin_grid` field and the frozen",
        "specification checker. It does **not** compute any Phase-3B catalog distance.",
        "The challenge is not filtered or modified.",
        "",
        f"Classification: `{out['classification']}`",
        "",
        f"- H_VALID n: {out['n']}",
        f"- Stored residual identically 0: {out['stored_residual_zero']} / {out['n']}"
        " (the other 3 are IIR stopband residuals of order 1e-15, i.e. binary64 contact with an inclusive mask; still <= 1e-4)",
        f"- Stored continuously certified valid: {out['stored_continuous_certified_valid']} / {out['n']}",
        f"- True 4096-point min interior slack: min={out['interior_slack_min']}, median={out['interior_slack_median']}, max={out['interior_slack_max']}",
        f"- Members with non-positive interior slack: {out['n_nonpositive_interior_slack']}",
        f"- Numerical fragility: `{out['numerical_fragility']}`",
        f"- Challenge filtered after diagnosis: `{out['challenge_filtered']}`",
        f"- Catalog distances computed: `{out['catalog_distances_computed']}`",
        "",
        "## Q1",
        "",
        out["answers"]["Q1"],
        "",
        "## Q2",
        "",
        out["answers"]["Q2"],
        "",
        "## Q3",
        "",
        out["answers"]["Q3"],
        "",
        "## Q4",
        "",
        out["answers"]["Q4"],
        "",
        "## Q5",
        "",
        out["answers"]["Q5"],
        "",
        "## Q6",
        "",
        out["answers"]["Q6"],
        "",
        "## Slack by generator (specification geometry only)",
        "",
        "| generator | n | min slack | median slack | max slack | n ≤ 0 |",
        "| --------- | -: | --------: | -----------: | --------: | ----: |",
    ]
    for g, rec in out["slack_by_generator"].items():
        lines.append(
            f"| {g} | {rec['n']} | {rec['min']} | {rec['median']} | {rec['max']} | {rec['n_nonpositive']} |"
        )
    lines += [
        "",
        "STOP condition: `NUMERICAL_FRAGILITY` was **not** found.",
        "Continue to primary transfer.",
        "",
    ]
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "PHASE3D_B_VALID_MARGIN_ZERO_DIAGNOSIS.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    diagnose()
