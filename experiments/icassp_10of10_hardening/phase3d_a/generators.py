"""Catalog-blind DSP generators. Depend only on S_t and the locked schedule."""
from __future__ import annotations

import numpy as np

from experiments.icassp_10of10_hardening.phase3d_a.config import (
    F3_EDGE_ALPHA,
    FIR_N_GRID,
    IIR_FC_FRAC,
    IIR_ORDER_GRID,
    IIR_RP_FRAC,
    IIR_RS_FRAC,
    REMEZ_W2,
    REMEZ_W3,
)
from src.filter_geom import (
    default_cutoffs,
    free_transitions,
    pass_rp_db,
    response_type,
    stop_atten_db,
)
from src.first_principles_fir import (
    frequency_sampling,
    mag_bandpass,
    mag_bandstop,
    mag_highpass,
    mag_lowpass,
)
from src.valid_designers import design_firls, design_firwin2, design_iir, design_remez
from src.valid_first_principles import _norm_at, _norm_dc, _norm_nyq, windowed_at


def _finite_h(h) -> bool:
    h = np.asarray(h, float).reshape(-1)
    return bool(h.size >= 3 and np.all(np.isfinite(h)))


def _finite_ba(ba) -> bool:
    b, a = ba
    b = np.asarray(b, float).reshape(-1)
    a = np.asarray(a, float).reshape(-1)
    return bool(np.all(np.isfinite(b)) and np.all(np.isfinite(a)) and len(b) >= 2 and len(a) >= 2)


def _edges(task):
    p = sorted(task["pass_band"], key=lambda b: b["f0"])
    s = sorted(task["stop_band"], key=lambda b: b["f0"])
    return p, s


def _inset(lo: float, hi: float, alpha: float) -> tuple[float, float]:
    width = hi - lo
    if width <= 1e-12:
        return lo, hi
    d = alpha * width / 2.0
    a, b = lo + d, hi - d
    if b <= a + 1e-12:
        return lo, hi
    return a, b


def _freqsamp_designed(task: dict, n: int, alpha: float):
    fs = float(task["sampling_rate"])
    r = response_type(task)
    p, s = _edges(task)
    if r == "lp":
        fp, fst = _inset(float(p[0]["f1"]), float(s[0]["f0"]), alpha)
        h = frequency_sampling(n, lambda f, a=fp, b=fst: mag_lowpass(f, a, b), fs)
        return _norm_dc(h)
    if r == "hp":
        fst, fp = _inset(float(s[0]["f1"]), float(p[0]["f0"]), alpha)
        h = frequency_sampling(n, lambda f, a=fst, b=fp: mag_highpass(f, a, b), fs)
        return _norm_nyq(h, fs)
    if r == "bp":
        s1, p1 = _inset(float(s[0]["f1"]), float(p[0]["f0"]), alpha)
        p2, s2 = _inset(float(p[0]["f1"]), float(s[1]["f0"]), alpha)
        h = frequency_sampling(n, lambda f: mag_bandpass(f, s1, p1, p2, s2), fs)
        return _norm_at(h, 0.5 * (p1 + p2), fs)
    if r == "bs":
        p1, s1 = _inset(float(p[0]["f1"]), float(s[0]["f0"]), alpha)
        s2, p2 = _inset(float(s[0]["f1"]), float(p[1]["f0"]), alpha)
        h = frequency_sampling(n, lambda f: mag_bandstop(f, p1, s1, s2, p2), fs)
        return _norm_dc(h)
    raise KeyError(r)


def generate_fir(task: dict, generator_id: str, attempt_index: int) -> dict:
    a = int(attempt_index)
    n = int(FIR_N_GRID[a])
    r = response_type(task)
    params = {"n": n, "generator_id": generator_id, "attempt_index": a}
    try:
        if generator_id == "F1_remez":
            w = list(REMEZ_W2[a] if r in {"lp", "hp"} else REMEZ_W3[a])
            params["weight"] = w
            h = design_remez(task, n, weight=w)
        elif generator_id == "F2_firls":
            h = design_firls(task, n)
        elif generator_id == "F3_freqsamp":
            alpha = float(F3_EDGE_ALPHA[a])
            params["edge_alpha"] = alpha
            h = _freqsamp_designed(task, n, alpha)
        elif generator_id == "F4_window":
            if a % 2 == 0:
                params["window_route"] = "firwin2"
                h = design_firwin2(task, n)
            else:
                params["window_route"] = "windowed_sinc"
                cut = default_cutoffs(task)
                params["cutoff"] = [float(x) for x in cut]
                h = windowed_at(task, n, cut)
        else:
            return {"ok": False, "reason": "unknown_generator", "params": params}
    except Exception as exc:
        return {"ok": False, "reason": f"generation_error:{type(exc).__name__}", "params": params}
    h = np.asarray(h, float).reshape(-1)
    if not _finite_h(h):
        return {"ok": False, "reason": "nonfinite", "params": params}
    return {"ok": True, "family": "fir", "impl": h, "params": params}


def _iir_fc(task: dict, a: int):
    gaps = free_transitions(task)
    if not gaps:
        cut = default_cutoffs(task)
        return cut[0] if cut else None
    lo, hi = gaps[0]
    return float(lo + IIR_FC_FRAC[a] * (hi - lo))


def generate_iir(task: dict, generator_id: str, attempt_index: int) -> dict:
    a = int(attempt_index)
    order = int(IIR_ORDER_GRID[a])
    fc = _iir_fc(task, a)
    rp = float(IIR_RP_FRAC[a] * pass_rp_db(task))
    rs = float(IIR_RS_FRAC[a] * stop_atten_db(task))
    method = {
        "I1_butter": "butter",
        "I2_cheby1": "cheby1",
        "I3_cheby2": "cheby2",
        "I4_ellip": "ellip",
    }.get(generator_id)
    params = {
        "order": order,
        "fc": fc,
        "rp": rp,
        "rs": rs,
        "method": method,
        "generator_id": generator_id,
        "attempt_index": a,
    }
    if method is None or fc is None:
        return {"ok": False, "reason": "unknown_generator", "params": params}
    try:
        ba = design_iir(task, method, order, fc, rp=rp, rs=rs)
    except Exception as exc:
        return {"ok": False, "reason": f"generation_error:{type(exc).__name__}", "params": params}
    if not _finite_ba(ba):
        return {"ok": False, "reason": "nonfinite", "params": params}
    impl = {"b": np.asarray(ba[0], float).reshape(-1), "a": np.asarray(ba[1], float).reshape(-1)}
    return {"ok": True, "family": "iir", "impl": impl, "params": params}


def generate_one(task: dict, generator_id: str, attempt_index: int) -> dict:
    if str(task["type"]).startswith("fir_"):
        return generate_fir(task, generator_id, attempt_index)
    return generate_iir(task, generator_id, attempt_index)
