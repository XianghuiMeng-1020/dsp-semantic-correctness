"""Continuous certification wrappers. No reference-oracle I/O."""
from __future__ import annotations

from src.continuous_certification.fir_power_polynomial import certify_fir
from src.continuous_certification.iir_schur import certify_stability
from src.continuous_certification.mask_sign import certify_fir_sturm, certify_iir_magnitude, load_task
from src.spec_checker import check_specification
from src.verification.canonicalize import unpack


def _strip(rec: dict) -> dict:
    keep = (
        "status",
        "reason",
        "task_id",
        "n_taps",
        "degree",
        "method",
        "arithmetic",
        "max_pole_radius",
        "pole_radius_max",
    )
    return {k: rec[k] for k in keep if k in rec}


def grid_screen(task_id: str, impl) -> dict:
    try:
        rec = check_specification(task_id, impl)
    except Exception as exc:
        return {"pass": False, "reason": f"grid_error:{type(exc).__name__}"}
    return {"pass": bool(rec.get("pass")), "residuals": rec.get("residuals")}


def certify_fir_chain(task_id: str, impl) -> dict:
    bern = certify_fir(task_id, impl)
    status = bern.get("status")
    out = {"bernstein": _strip(bern), "sturm": None, "status": status}
    if status == "UNDECIDED":
        st = certify_fir_sturm(task_id, impl)
        out["sturm"] = _strip(st)
        out["status"] = st.get("status", "UNDECIDED")
    return out


def certify_iir_chain(task_id: str, impl) -> dict:
    task = load_task(task_id)
    _b, a = unpack(impl)
    pole_max = float(task["constraints"]["pole_radius_max"])
    stab = certify_stability(impl["a"] if isinstance(impl, dict) else a, pole_max)
    stab_s = stab.get("status")
    out = {"stability": _strip(stab), "magnitude": None, "status": None}
    if stab_s == "CERTIFIED_UNSTABLE":
        out["status"] = "CERTIFIED_INVALID"
        out["reason"] = "unstable"
        return out
    if stab_s != "CERTIFIED_STABLE":
        out["status"] = "UNDECIDED"
        out["reason"] = stab_s
        return out
    mag = certify_iir_magnitude(task_id, impl["b"], impl["a"])
    out["magnitude"] = _strip(mag)
    out["status"] = mag.get("status")
    return out


def certify_candidate(task: dict, impl) -> dict:
    tid = task["task_id"]
    if str(task["type"]).startswith("fir_"):
        return certify_fir_chain(tid, impl)
    return certify_iir_chain(tid, impl)
