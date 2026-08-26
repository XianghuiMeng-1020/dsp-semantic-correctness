"""Near-boundary invalid construction.

Severity levels and mechanisms are frozen a priori. They are not tuned
per candidate to force reference-oracle failure.

Every constructed invalid must fail the independent verifier.
A draw that remains valid is a failed construction, not an invalid label.
"""
from __future__ import annotations

import numpy as np
from scipy import signal as sp_signal

from src.verification.canonicalize import canonicalize_fir, unpack
from src.verification.independent_spec_verifier import FREQZ_N
from src.verification.registry_io import is_fir

# Absolute linear-magnitude overshoot/undershoot. Not task-tuned.
SEVERITIES = (0.002, 0.005, 0.010, 0.020)
MECHANISMS = ("PASS_DROP", "STOP_LIFT")


def _dense_mag(impl, fs: float):
    b, a = unpack(impl)
    if a is None:
        w, H = sp_signal.freqz(b, worN=FREQZ_N, fs=fs)
    else:
        try:
            sos = sp_signal.tf2sos(b, a)
            w, H = sp_signal.sosfreqz(sos, worN=FREQZ_N, fs=fs)
        except Exception:
            w, H = sp_signal.freqz(b, a, worN=FREQZ_N, fs=fs)
    return w, np.abs(H)


def _band_stats(impl, task: dict, role: str):
    fs = float(task["sampling_rate"])
    w, mag = _dense_mag(impl, fs)
    bands = task["pass_band"] if role == "pass" else task["stop_band"]
    min_m, max_m = np.inf, -np.inf
    f_min = f_max = None
    lo_used = hi_used = None
    for band in bands:
        mask = (w >= float(band["f0"])) & (w <= float(band["f1"]))
        if not np.any(mask):
            continue
        mw, fw = mag[mask], w[mask]
        i0 = int(np.argmin(mw))
        i1 = int(np.argmax(mw))
        if mw[i0] < min_m:
            min_m, f_min, lo_used = float(mw[i0]), float(fw[i0]), float(band["lo"])
        if mw[i1] > max_m:
            max_m, f_max, hi_used = float(mw[i1]), float(fw[i1]), float(band["hi"])
    return {
        "min": min_m,
        "max": max_m,
        "f_min": f_min,
        "f_max": f_max,
        "lo": lo_used,
        "hi": hi_used,
    }


def _scale_impl(impl, alpha: float):
    b, a = unpack(impl)
    if a is None:
        return b * float(alpha)
    return {"b": np.asarray(b, float) * float(alpha), "a": np.asarray(a, float).copy()}


def _add_type1_cosine(h: np.ndarray, f_hz: float, fs: float, beta: float) -> np.ndarray:
    h = np.asarray(h, float).reshape(-1)
    n = len(h)
    m = (n - 1) / 2.0
    k = np.arange(n, dtype=float)
    v = np.cos(2.0 * np.pi * f_hz * (k - m) / fs)
    v = 0.5 * (v + v[::-1])
    return h + float(beta) * v


def construct_pass_drop(href, task: dict, eps: float):
    st = _band_stats(href, task, "pass")
    if st["min"] is None or not np.isfinite(st["min"]) or st["min"] <= 0:
        return None, "pass_min_undefined"
    target = float(st["lo"]) - float(eps)
    if target <= 0:
        target = max(1e-6, float(st["lo"]) * 0.5)
    alpha = target / float(st["min"])
    return _scale_impl(href, alpha), {"alpha": alpha, "target_pass_min": target, "src_pass_min": st["min"]}


def construct_stop_lift(href, task: dict, eps: float):
    st = _band_stats(href, task, "stop")
    if st["max"] is None or not np.isfinite(st["max"]):
        return None, "stop_max_undefined"
    target = float(st["hi"]) + float(eps)
    fs = float(task["sampling_rate"])
    f_star = float(st["f_max"] if st["f_max"] is not None else 0.0)
    if is_fir(task):
        h = canonicalize_fir(href).h
        # binary search beta so max_stop ~= target
        lo, hi = 0.0, 4.0
        best = None
        for _ in range(40):
            mid = 0.5 * (lo + hi)
            cand = _add_type1_cosine(h, f_star, fs, mid)
            cur = _band_stats(cand, task, "stop")["max"]
            best = cand
            if cur < target:
                lo = mid
            else:
                hi = mid
        return best, {"beta": 0.5 * (lo + hi), "target_stop_max": target, "f_star": f_star}
    # IIR: scale numerator
    cur = float(st["max"])
    if cur <= 0:
        alpha = 1.0 + float(eps)
    else:
        alpha = target / cur
    return _scale_impl(href, alpha), {"alpha": alpha, "target_stop_max": target, "src_stop_max": cur}


def construct_boundary_invalids(href, task: dict) -> list[dict]:
    out = []
    for eps in SEVERITIES:
        for mech in MECHANISMS:
            if mech == "PASS_DROP":
                impl, meta = construct_pass_drop(href, task, eps)
            else:
                impl, meta = construct_stop_lift(href, task, eps)
            rec = {
                "mechanism": mech,
                "epsilon": float(eps),
                "impl": impl,
                "meta": meta if isinstance(meta, dict) else {"reason": meta},
                "construction_ok": impl is not None,
            }
            out.append(rec)
    return out
