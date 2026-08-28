"""Continuous magnitude-mask certification via Sturm sign (FIR or IIR-Q).

Does not import fir_adaptive, fir_power_polynomial decision routines,
spec_checker, or independent_spec_verifier.
"""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import numpy as np

from src.continuous_certification.poly_sturm import certify_sign_on_interval, poly_eval_frac
from src.continuous_certification.poly_trig import (
    band_x_outer,
    f64_frac,
    poly_sub_const,
    poly_sub_scaled,
    power_from_taps,
)

ROOT = Path(__file__).resolve().parents[2]


def load_task(task_id: str) -> dict:
    for name in ("suite_n.json", "suite_s.json"):
        payload = json.loads((ROOT / "registry" / name).read_text(encoding="utf-8"))
        for t in payload["tasks"]:
            if t["task_id"] == task_id:
                return t
    raise KeyError(task_id)


def eff_bounds(lo: float, hi: float, floor: float) -> tuple[Fraction, Fraction]:
    span = max(hi - lo, 1e-6)
    L = lo - floor * span
    U = hi + floor * span
    return f64_frac(L), f64_frac(U)


def certify_q_on_band(q: list[Fraction], f0: float, f1: float, fs: float, want: str) -> dict:
    a, b = band_x_outer(f0, f1, fs)
    rec = certify_sign_on_interval(q, a, b, want)
    rec["x_interval"] = [str(a), str(b)]
    rec["f0"] = f0
    rec["f1"] = f1
    return rec


def certify_fir_sturm(task_id: str, impl) -> dict:
    task = load_task(task_id)
    h = np.asarray(impl if not isinstance(impl, dict) else impl.get("b", impl.get("h")), dtype=np.float64).reshape(-1)
    if not np.all(np.isfinite(h)):
        return {"status": "CERTIFIED_INVALID", "reason": "nonfinite", "task_id": task_id, "method": "sturm_sign"}
    fs = float(task["sampling_rate"])
    floor = float(task["residual_floor"])
    p = power_from_taps(h)
    details = []
    for band in list(task["pass_band"]) + list(task["stop_band"]):
        L, U = eff_bounds(float(band["lo"]), float(band["hi"]), floor)
        U2 = U * U
        q_u = poly_sub_const(p, U2)
        up = certify_q_on_band(q_u, float(band["f0"]), float(band["f1"]), fs, "nonpos")
        if L > 0:
            q_l = poly_sub_const(p, L * L)
            low = certify_q_on_band(q_l, float(band["f0"]), float(band["f1"]), fs, "nonneg")
        else:
            low = {"status": "CERTIFIED", "reason": "lower_vacuous_L_nonpositive"}
        details.append({"upper": up, "lower": low, "L": str(L), "U": str(U)})
        if up["status"] == "REFUTED" or low.get("status") == "REFUTED":
            return {
                "status": "CERTIFIED_INVALID",
                "reason": "sturm_sign_crossing",
                "task_id": task_id,
                "n_taps": int(len(h)),
                "bands": details,
                "method": "sturm_sign",
            }
        if up["status"] != "CERTIFIED" or low.get("status") != "CERTIFIED":
            reason = up.get("reason") if up["status"] != "CERTIFIED" else low.get("reason")
            return {
                "status": "UNDECIDED",
                "reason": reason or "sturm_unresolved",
                "task_id": task_id,
                "n_taps": int(len(h)),
                "bands": details,
                "method": "sturm_sign",
            }
    return {
        "status": "CERTIFIED_VALID",
        "reason": "all_bands_sturm_sign",
        "task_id": task_id,
        "n_taps": int(len(h)),
        "degree": len(p) - 1,
        "bands": details,
        "method": "sturm_sign",
    }


def certify_iir_magnitude(task_id: str, b, a) -> dict:
    task = load_task(task_id)
    bb = np.asarray(b, dtype=np.float64).reshape(-1)
    aa = np.asarray(a, dtype=np.float64).reshape(-1)
    if not (np.all(np.isfinite(bb)) and np.all(np.isfinite(aa))):
        return {"status": "CERTIFIED_INVALID", "reason": "nonfinite", "method": "sturm_PB_minus_C_PA"}
    fs = float(task["sampling_rate"])
    floor = float(task["residual_floor"])
    pb = power_from_taps(bb)
    pa = power_from_taps(aa)
    details = []
    for band in list(task["pass_band"]) + list(task["stop_band"]):
        L, U = eff_bounds(float(band["lo"]), float(band["hi"]), floor)
        q_u = poly_sub_scaled(pb, U * U, pa)
        up = certify_q_on_band(q_u, float(band["f0"]), float(band["f1"]), fs, "nonpos")
        if L > 0:
            q_l = poly_sub_scaled(pb, L * L, pa)
            low = certify_q_on_band(q_l, float(band["f0"]), float(band["f1"]), fs, "nonneg")
        else:
            low = {"status": "CERTIFIED", "reason": "lower_vacuous_L_nonpositive"}
        details.append({"upper": up, "lower": low, "L": str(L), "U": str(U)})
        if up["status"] == "REFUTED" or low.get("status") == "REFUTED":
            return {
                "status": "CERTIFIED_INVALID",
                "reason": "sturm_sign_crossing",
                "bands": details,
                "method": "sturm_PB_minus_C_PA",
            }
        if up["status"] != "CERTIFIED" or low.get("status") != "CERTIFIED":
            reason = up.get("reason") if up["status"] != "CERTIFIED" else low.get("reason")
            return {
                "status": "UNDECIDED",
                "reason": reason or "sturm_unresolved",
                "bands": details,
                "method": "sturm_PB_minus_C_PA",
            }
    return {
        "status": "CERTIFIED_VALID",
        "reason": "all_bands_sturm_PB_minus_C_PA",
        "degree_B": len(pb) - 1,
        "degree_A": len(pa) - 1,
        "bands": details,
        "method": "sturm_PB_minus_C_PA",
    }


def exact_sample_violation(q: list[Fraction], x: Fraction, want: str) -> bool:
    v = poly_eval_frac(q, x)
    if want == "nonpos":
        return v > 0
    return v < 0
