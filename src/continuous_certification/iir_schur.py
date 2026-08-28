"""Exact rational Schur-Cohn strict disk-stability test.

Does not import numpy.roots / scipy as the certificate.
Stored binary64 denominator coefficients are exact rationals.

Convention (scipy tf / stored files):
    A(z) = a[0] + a[1] z^{-1} + ... + a[n] z^{-n}
    poles = roots of  a[0] z^n + a[1] z^{n-1} + ... + a[n].
"""
from __future__ import annotations

from fractions import Fraction

import numpy as np
from mpmath import mp

from src.continuous_certification.poly_trig import f64_frac


def _trim_leading(desc: list[Fraction]) -> list[Fraction]:
    q = list(desc)
    while len(q) > 1 and q[0] == 0:
        q.pop(0)
    return q


def _trim_trailing(desc: list[Fraction]) -> list[Fraction]:
    q = list(desc)
    while len(q) > 1 and q[-1] == 0:
        q.pop()
    return q


def schur_strict(desc: list[Fraction]) -> dict:
    """All roots of desc[0] z^n + ... + desc[n] satisfy |z|<1.

    desc is leading-first. Returns CERTIFIED_STABLE / CERTIFIED_UNSTABLE / STABILITY_UNDECIDED.
    """
    p = _trim_trailing(_trim_leading([Fraction(c) for c in desc]))
    if not p or all(c == 0 for c in p):
        return {"status": "STABILITY_UNDECIDED", "reason": "zero_polynomial", "degree": 0}
    if p[0] == 0:
        return {"status": "STABILITY_UNDECIDED", "reason": "vanishing_leading", "degree": len(p) - 1}
    steps = 0
    while len(p) > 1:
        leading, constant = p[0], p[-1]
        if abs(constant) > abs(leading):
            return {
                "status": "CERTIFIED_UNSTABLE",
                "reason": "schur_reflection_gt_one",
                "degree": len(p) - 1,
                "steps": steps,
            }
        if abs(constant) == abs(leading):
            return {
                "status": "CERTIFIED_UNSTABLE",
                "reason": "schur_root_on_or_reciprocal_circle",
                "degree": len(p) - 1,
                "steps": steps,
            }
        n = len(p) - 1
        nxt = [leading * p[k] - constant * p[n - k] for k in range(n)]
        nxt = _trim_trailing(_trim_leading(nxt))
        if not nxt or all(c == 0 for c in nxt):
            return {"status": "STABILITY_UNDECIDED", "reason": "schur_transform_vanished", "steps": steps}
        p = nxt
        steps += 1
        if steps > 64:
            return {"status": "STABILITY_UNDECIDED", "reason": "schur_step_cap", "steps": steps}
    if p[0] == 0:
        return {"status": "STABILITY_UNDECIDED", "reason": "final_zero", "steps": steps}
    return {"status": "CERTIFIED_STABLE", "reason": "schur_cohn_strict", "steps": steps, "degree": steps}


def scale_for_radius(desc: list[Fraction], radius: Fraction) -> list[Fraction]:
    """P_r(w) = P(radius * w): roots |z|<radius iff P_r is Schur."""
    p = list(desc)
    n = len(p) - 1
    # P(z)=d0 z^n + d1 z^{n-1} + ... + dn
    # P(r w)= d0 r^n w^n + d1 r^{n-1} w^{n-1} + ... + dn
    out = []
    rk = Fraction(1)
    # build from constant term upward then reverse
    pows = [Fraction(1)]
    for _ in range(n):
        pows.append(pows[-1] * radius)
    for k, ck in enumerate(p):
        # ck is coeff of z^{n-k}, multiply by r^{n-k}
        out.append(ck * pows[n - k])
    return out


def stored_denominator(a) -> list[Fraction]:
    return [f64_frac(float(v)) for v in np.asarray(a, dtype=np.float64).reshape(-1)]


def certify_stability(a, pole_radius_max: float | None) -> dict:
    """Primary certificate: exact Schur on the frozen disk.

    Frozen IIR S_t uses pole_radius_max=0.999 (binary64). That disk is a subset
    of |z|<1, so it also implies A(e^{jω}) ≠ 0.
    """
    desc = stored_denominator(a)
    unit = schur_strict(desc)
    out = {
        "unit_circle": unit,
        "method": "exact_rational_schur_cohn",
        "pole_radius_max": pole_radius_max,
    }
    if pole_radius_max is None:
        out["status"] = unit["status"]
        out["reason"] = unit.get("reason")
        return out
    r = f64_frac(float(pole_radius_max))
    if r <= 0 or r >= 1:
        out["status"] = "STABILITY_UNDECIDED"
        out["reason"] = "pole_radius_max_not_in_(0,1)"
        return out
    scaled = schur_strict(scale_for_radius(desc, r))
    out["frozen_disk"] = scaled
    # Frozen validity requires |p| < pole_radius_max.
    if scaled["status"] == "CERTIFIED_UNSTABLE" or unit["status"] == "CERTIFIED_UNSTABLE":
        out["status"] = "CERTIFIED_UNSTABLE"
        out["reason"] = scaled.get("reason") if scaled["status"] == "CERTIFIED_UNSTABLE" else unit.get("reason")
        return out
    if scaled["status"] == "CERTIFIED_STABLE" and unit["status"] == "CERTIFIED_STABLE":
        out["status"] = "CERTIFIED_STABLE"
        out["reason"] = "schur_on_frozen_disk_and_unit_disk"
        return out
    out["status"] = "STABILITY_UNDECIDED"
    out["reason"] = scaled.get("reason") or unit.get("reason")
    return out


def highprec_pole_radius(a, dps: int = 80) -> dict:
    """Secondary cross-check only. Not the certificate."""
    mp.dps = dps
    coeffs = [mp.mpf(float(v)) for v in np.asarray(a, dtype=np.float64).reshape(-1)]
    if len(coeffs) <= 1:
        return {"max_radius": 0.0, "min_dist_to_unit": 1.0, "n_poles": 0}
    # mpmath.polyroots wants highest-degree first — same as scipy tf `a`.
    try:
        roots = mp.polyroots(coeffs, maxsteps=200, extraprec=40)
    except Exception as exc:  # noqa: BLE001
        return {"error": type(exc).__name__, "max_radius": None}
    radii = [float(abs(z)) for z in roots]
    mx = max(radii) if radii else 0.0
    return {
        "max_radius": mx,
        "min_dist_to_unit": min((1.0 - r) for r in radii) if radii else 1.0,
        "n_poles": len(radii),
        "dps": dps,
    }
