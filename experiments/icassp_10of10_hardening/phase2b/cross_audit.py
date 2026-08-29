"""Secondary numerical and cross-method audits. Not primary certificates."""
from __future__ import annotations

import math

import numpy as np

from experiments.icassp_10of10_hardening.phase2b.occupants import (
    boundary_invalids,
    constructed_valids,
    mechanism_invalids,
)
from src.continuous_certification.mask_sign import certify_fir_sturm, certify_iir_magnitude, load_task
from src.continuous_certification.poly_trig import f64_frac
from src.verification.io_utils import load_impl


def _eff(lo, hi, floor):
    span = max(hi - lo, 1e-6)
    return lo - floor * span, hi + floor * span


def numerical_iir_extrema(task_id: str, impl, n: int = 20001) -> dict:
    task = load_task(task_id)
    b = np.asarray(impl["b"], dtype=np.float64)
    a = np.asarray(impl["a"], dtype=np.float64)
    fs = float(task["sampling_rate"])
    floor = float(task["residual_floor"])
    hits = []
    for band in list(task["pass_band"]) + list(task["stop_band"]):
        f0, f1 = float(band["f0"]), float(band["f1"])
        L, U = _eff(float(band["lo"]), float(band["hi"]), floor)
        freqs = np.linspace(f0, f1, n)
        w = 2.0 * math.pi * freqs / fs
        k = np.arange(len(b))
        B = np.exp(-1j * np.outer(w, k)) @ b
        k = np.arange(len(a))
        A = np.exp(-1j * np.outer(w, k)) @ a
        mag = np.abs(B) / np.maximum(np.abs(A), 1e-300)
        below = (L > 0) and np.any(mag < L - 1e-12)
        above = np.any(mag > U + 1e-12)
        hits.append({"f0": f0, "f1": f1, "below": bool(below), "above": bool(above), "min": float(mag.min()), "max": float(mag.max()), "L": L, "U": U})
    return {"bands": hits, "any_violation": any(h["below"] or h["above"] for h in hits)}


def iir_numerical_subset(iir_cert: dict) -> dict:
    rows = iir_cert["rows"]
    picks = []
    by_task = {}
    for r in rows:
        by_task.setdefault(r["task"], []).append(r)
    for tid, rs in by_task.items():
        valids = [x for x in rs if x["old_label"] == "VALID"]
        invalids = [x for x in rs if x["old_label"] == "INVALID"]
        if valids:
            picks.append(valids[0])
            picks.append(max(valids, key=lambda x: x.get("n_a") or 0))
        if invalids:
            picks.append(invalids[0])
        picks.extend([x for x in rs if x["final"] == "UNDECIDED"])
    seen = set()
    audits = []
    agree = 0
    notes = 0
    for r in picks:
        if r["occupant"] in seen:
            continue
        seen.add(r["occupant"])
        impl = load_impl(r["occupant"])
        num = numerical_iir_extrema(r["task"], impl)
        # Compare: numerical violation should not appear on CERTIFIED_VALID
        if r["final"] == "CERTIFIED_VALID" and num["any_violation"]:
            ok = False
            notes += 1
        elif r["final"] == "CERTIFIED_INVALID" and not num["any_violation"] and r["stability"] != "CERTIFIED_UNSTABLE":
            ok = True  # numerical grid may miss; not a failure of the exact route
            notes += 1
        else:
            ok = True
            agree += 1
        audits.append(
            {
                "occupant": r["occupant"],
                "task": r["task"],
                "final": r["final"],
                "numerical_violation": num["any_violation"],
                "agree": ok,
            }
        )
    return {"audits": audits, "n": len(audits), "agree": agree, "notes": notes, "verdict": "PASS" if notes == 0 else "PASS_WITH_NOTES"}


def fir_cross_method() -> dict:
    """Sturm vs Phase-2A Bernstein on a stratified FIR sample. Does not reread Phase-2A decision code."""
    import json
    from experiments.icassp_10of10_hardening.phase2b.config import PHASE2A_DIR

    p2a = json.loads((PHASE2A_DIR / "fir_power_polynomial_certification.json").read_text(encoding="utf-8"))
    p2a_by = {r["occupant"]: r["phase2a_status"] for r in p2a["rows"]}
    picks = []
    valids = constructed_valids("fir")
    by_task: dict[str, list] = {}
    for v in valids:
        by_task.setdefault(v["task_id"], []).append(v)
    for tid, rs in sorted(by_task.items()):
        # skip the two longest FS tight bandstops here if we already resolved them separately
        short = [x for x in rs if "frequency_sampling__shortest" not in x["cid"] or "bs_tight" not in x["task_id"]]
        for item in short[:2]:
            picks.append(item)
    for item in mechanism_invalids("fir")[:6]:
        picks.append(item)
    for item in boundary_invalids("fir")[:6]:
        picks.append(item)
    rows = []
    disagree = []
    for occ in picks:
        rec = certify_fir_sturm(occ["task_id"], load_impl(occ["cid"]))
        p1 = p2a_by.get(occ["cid"])
        both_decided = rec["status"] in ("CERTIFIED_VALID", "CERTIFIED_INVALID") and p1 in (
            "CERTIFIED_VALID",
            "CERTIFIED_INVALID",
        )
        match = (not both_decided) or (rec["status"] == p1)
        rows.append(
            {
                "occupant": occ["cid"],
                "task": occ["task_id"],
                "old_label": occ["old_label"],
                "phase2a": p1,
                "phase2b_sturm": rec["status"],
                "match_when_both_decided": match,
            }
        )
        if both_decided and rec["status"] != p1:
            disagree.append(rows[-1])
        print(f"    cross {occ['cid'][-50:]} P2A={p1} Sturm={rec['status']}", flush=True)
    verdict = "FAIL" if disagree else "PASS"
    return {"rows": rows, "n": len(rows), "disagreements": disagree, "verdict": verdict}
