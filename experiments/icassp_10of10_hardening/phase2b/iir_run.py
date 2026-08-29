"""Run Phase-2B IIR stability + magnitude certification over the frozen corpus."""
from __future__ import annotations

from experiments.icassp_10of10_hardening.phase2b.occupants import all_iir
from src.continuous_certification.iir_schur import certify_stability, highprec_pole_radius
from src.continuous_certification.mask_sign import certify_iir_magnitude, load_task
from src.verification.io_utils import load_impl


def _combine(old_label: str, stab: dict, mag: dict) -> str:
    if old_label == "VALID":
        if stab["status"] == "CERTIFIED_UNSTABLE" or mag["status"] == "CERTIFIED_INVALID":
            return "CERTIFIED_INVALID"
        if stab["status"] == "CERTIFIED_STABLE" and mag["status"] == "CERTIFIED_VALID":
            return "CERTIFIED_VALID"
        return "UNDECIDED"
    # frozen invalid: one certified violation suffices
    if stab["status"] == "CERTIFIED_UNSTABLE" or mag["status"] == "CERTIFIED_INVALID":
        return "CERTIFIED_INVALID"
    if stab["status"] == "CERTIFIED_STABLE" and mag["status"] == "CERTIFIED_VALID":
        return "CERTIFIED_VALID"
    return "UNDECIDED"


def certify_one(occ: dict) -> dict:
    impl = load_impl(occ["cid"])
    task = load_task(occ["task_id"])
    pole_max = (task.get("constraints") or {}).get("pole_radius_max")
    a = impl["a"] if isinstance(impl, dict) else None
    b = impl["b"] if isinstance(impl, dict) else impl
    stab = certify_stability(a, float(pole_max) if pole_max is not None else None)
    hp = highprec_pole_radius(a)
    # Magnitude certificate requires A ≠ 0 on the circle. If unit-disk Schur failed
    # as unstable, magnitude may still be run for diagnostics but is not required.
    if stab.get("unit_circle", {}).get("status") == "CERTIFIED_STABLE" or stab["status"] == "CERTIFIED_STABLE":
        mag = certify_iir_magnitude(occ["task_id"], b, a)
    elif stab["status"] == "CERTIFIED_UNSTABLE":
        mag = {"status": "NOT_RUN", "reason": "already_certified_unstable"}
    else:
        mag = certify_iir_magnitude(occ["task_id"], b, a)
    final = _combine(occ["old_label"], stab, mag if mag.get("status") != "NOT_RUN" else {"status": "UNDECIDED"})
    if occ["old_label"] == "INVALID" and stab["status"] == "CERTIFIED_UNSTABLE":
        final = "CERTIFIED_INVALID"
    crit = None
    if mag.get("status") == "CERTIFIED_INVALID":
        crit = mag.get("reason")
    elif stab["status"] == "CERTIFIED_UNSTABLE":
        crit = stab.get("reason")
    return {
        "occupant": occ["cid"],
        "task": occ["task_id"],
        "old_label": occ["old_label"],
        "role": occ.get("role"),
        "stability": stab["status"],
        "stability_reason": stab.get("reason"),
        "hp_max_pole_radius": hp.get("max_radius"),
        "hp_min_dist_to_unit": hp.get("min_dist_to_unit"),
        "magnitude": mag.get("status"),
        "magnitude_reason": mag.get("reason"),
        "final": final,
        "critical": crit,
        "n_a": int(len(a)) if a is not None else None,
        "n_b": int(len(b)),
    }


def run_all_iir() -> dict:
    packs = all_iir()
    rows = []
    for role, items in packs.items():
        print(f"[phase2b] IIR certify {role} n={len(items)}", flush=True)
        for occ in items:
            occ = dict(occ)
            occ["role"] = role
            rec = certify_one(occ)
            rec["role"] = role
            rows.append(rec)
            print(
                f"    {rec['occupant'][-55:]} {rec['old_label']} stab={rec['stability']} "
                f"mag={rec['magnitude']} final={rec['final']}",
                flush=True,
            )

    def cohort(role: str) -> dict:
        sub = [r for r in rows if r["role"] == role]
        return {
            "total": len(sub),
            "CERTIFIED_VALID": sum(1 for r in sub if r["final"] == "CERTIFIED_VALID"),
            "CERTIFIED_INVALID": sum(1 for r in sub if r["final"] == "CERTIFIED_INVALID"),
            "UNDECIDED": sum(1 for r in sub if r["final"] == "UNDECIDED"),
            "CERTIFIED_STABLE": sum(1 for r in sub if r["stability"] == "CERTIFIED_STABLE"),
            "CERTIFIED_UNSTABLE": sum(1 for r in sub if r["stability"] == "CERTIFIED_UNSTABLE"),
            "STABILITY_UNDECIDED": sum(1 for r in sub if r["stability"] == "STABILITY_UNDECIDED"),
        }

    valid = [r for r in rows if r["role"] == "valid"]
    contradictions = [
        r
        for r in valid
        if r["final"] == "CERTIFIED_INVALID"
        or r["stability"] == "CERTIFIED_UNSTABLE"
        or r["magnitude"] == "CERTIFIED_INVALID"
    ]
    return {
        "method_stability": "exact rational Schur-Cohn on stored binary64 denominator; frozen disk |p|<0.999",
        "method_magnitude": "Q(x)=P_B(x)-C P_A(x); primitive-integer Sturm sign on outward x=cos ω interval",
        "certificate_type": "RIGOROUS_POLYNOMIAL_SIGN",
        "valid": cohort("valid"),
        "mechanism_invalid": cohort("mechanism_invalid"),
        "boundary_invalid": cohort("boundary_invalid"),
        "contradictions_valid_to_invalid": contradictions,
        "blocker": len(contradictions) > 0,
        "rows": rows,
    }
