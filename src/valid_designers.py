"""Library and random-valid designers.

Search objective is S_t(h)=1 only. Distance to the canonical reference
is measured after admission and is never a reject/accept criterion.
"""
from __future__ import annotations

from typing import Any

import numpy as np
from scipy import signal as sp_signal

from src.filter_geom import (
    cutoff_grid,
    default_cutoffs,
    estimate_fir_n,
    firls_desired,
    firwin2_spec,
    firwin_pass_zero,
    free_transitions,
    iir_btype,
    is_fir,
    pass_rp_db,
    remez_bands,
    remez_desired,
    response_type,
    stop_atten_db,
)
from src.spec_checker import check_specification

FIR_N_MAX = 401
IIR_ORDER_MAX = 12
RANDOM_FIR_N_MAX = 201
RANDOM_IIR_ORDER_MAX = 10


def _ok(task_id: str, impl) -> bool:
    try:
        return bool(check_specification(task_id, impl)["pass"])
    except Exception:
        return False


def _finite_h(h) -> bool:
    h = np.asarray(h, float)
    return bool(np.all(np.isfinite(h))) and h.size >= 3


def _finite_ba(ba) -> bool:
    b, a = ba
    b = np.asarray(b, float).reshape(-1)
    a = np.asarray(a, float).reshape(-1)
    return bool(np.all(np.isfinite(b)) and np.all(np.isfinite(a)) and len(b) >= 2 and len(a) >= 2)


def _odd_ns(lo: int, hi: int):
    if lo % 2 == 0:
        lo += 1
    return range(lo, hi + 1, 2)


def design_firwin(task: dict, n: int, cutoff, window="hamming"):
    fs = float(task["sampling_rate"])
    pz = firwin_pass_zero(task)
    return sp_signal.firwin(int(n), cutoff, window=window, fs=fs, pass_zero=pz)


def design_firwin2(task: dict, n: int):
    fs = float(task["sampling_rate"])
    freq, gain = firwin2_spec(task)
    return sp_signal.firwin2(int(n), freq, gain, fs=fs)


def design_remez(task: dict, n: int, weight=None):
    fs = float(task["sampling_rate"])
    bands = remez_bands(task)
    desired = remez_desired(task)
    if weight is None:
        weight = [1.0] * len(desired)
    return sp_signal.remez(int(n), bands, desired, weight=weight, fs=fs, maxiter=100)


def design_firls(task: dict, n: int):
    fs = float(task["sampling_rate"])
    freq, _g = firwin2_spec(task)
    desired = firls_desired(task)
    return sp_signal.firls(int(n), freq, desired, fs=fs)


def design_iir(task: dict, method: str, order: int, fc, rp=None, rs=None):
    fs = float(task["sampling_rate"])
    btype = iir_btype(task)
    if method == "butter":
        return sp_signal.butter(int(order), fc, btype=btype, fs=fs, output="ba")
    if method == "cheby1":
        return sp_signal.cheby1(int(order), float(rp), fc, btype=btype, fs=fs, output="ba")
    if method == "cheby2":
        return sp_signal.cheby2(int(order), float(rs), fc, btype=btype, fs=fs, output="ba")
    if method == "ellip":
        return sp_signal.ellip(int(order), float(rp), float(rs), fc, btype=btype, fs=fs, output="ba")
    raise KeyError(method)


def _try_fir(task, designer, n, **kwargs):
    try:
        h = designer(task, n, **kwargs)
    except Exception:
        return None
    if not _finite_h(h):
        return None
    h = np.asarray(h, float).reshape(-1)
    if _ok(task["task_id"], h):
        return h
    return None


def _try_iir(task, method, order, fc, rp=None, rs=None):
    try:
        ba = design_iir(task, method, order, fc, rp=rp, rs=rs)
    except Exception:
        return None
    if not _finite_ba(ba):
        return None
    impl = {"b": np.asarray(ba[0], float), "a": np.asarray(ba[1], float)}
    if _ok(task["task_id"], impl):
        return impl
    return None


def design_canonical(task: dict) -> dict[str, Any]:
    """Shortest Hamming firwin / lowest-order butter that meets S_t."""
    tid = task["task_id"]
    if is_fir(task):
        n0 = estimate_fir_n(task)
        grids = cutoff_grid(task, n_pts=5)
        mid = default_cutoffs(task)

        def at_n(n):
            for cut in [mid] + [g for g in grids if g != mid]:
                h = _try_fir(task, lambda t, nn, c=cut: design_firwin(t, nn, c if len(c) > 1 else c[0]), n)
                if h is not None:
                    return h, {"n": int(n), "cutoff": [float(x) for x in cut], "window": "hamming"}
            return None, None

        found = None
        for n in _odd_ns(n0, FIR_N_MAX):
            h, p = at_n(n)
            if h is not None:
                found = (n, h, p)
                break
        if found is None:
            for n in _odd_ns(21, n0 - 2):
                h, p = at_n(n)
                if h is not None:
                    found = (n, h, p)
                    break
        if found is None:
            return {"ok": False, "reason": "canonical_firwin_infeasible"}
        n_hit, h, params = found
        for n in range(n_hit - 2, 20, -2):
            h2, p2 = at_n(n)
            if h2 is None:
                break
            h, params = h2, p2
        return {
            "ok": True,
            "impl": h,
            "method": "firwin_hamming",
            "parameters": params,
        }

    mid = default_cutoffs(task)
    fc = mid[0] if len(mid) == 1 else mid
    grids = cutoff_grid(task, n_pts=5)
    for order in range(2, IIR_ORDER_MAX + 1):
        for cut in [mid] + [g for g in grids if g != mid]:
            fc_try = cut[0] if len(cut) == 1 else cut
            impl = _try_iir(task, "butter", order, fc_try)
            if impl is not None:
                return {
                    "ok": True,
                    "impl": impl,
                    "method": "butter",
                    "parameters": {"order": int(order), "cutoff": [float(x) for x in np.atleast_1d(fc_try)]},
                }
    return {"ok": False, "reason": "canonical_butter_infeasible", "task_id": tid}


def _library_fir_one(task, method: str):
    n0 = estimate_fir_n(task)
    grids = cutoff_grid(task, n_pts=5)
    mid = default_cutoffs(task)
    order_ns = list(_odd_ns(n0, FIR_N_MAX)) + list(_odd_ns(21, n0 - 2))

    def accept(n, kwargs, extra):
        designers = {
            "firwin": lambda t, nn: design_firwin(t, nn, (mid if len(mid) > 1 else mid[0])),
            "firwin2": design_firwin2,
            "remez": design_remez,
            "firls": design_firls,
        }
        if method == "firwin":
            for cut in [mid] + [g for g in grids if g != mid]:
                h = _try_fir(
                    task,
                    lambda t, nn, c=cut: design_firwin(t, nn, c if len(c) > 1 else c[0]),
                    n,
                )
                if h is not None:
                    return h, {"n": int(n), "cutoff": [float(x) for x in cut], "window": "hamming"}
            return None, None
        if method == "kaiser_firwin":
            try:
                width = min(b - a for a, b in free_transitions(task))
                width_n = 2.0 * width / float(task["sampling_rate"])
                atten = stop_atten_db(task)
                n_k, beta = sp_signal.kaiserord(atten, max(width_n, 1e-4))
            except Exception:
                n_k, beta = n, 8.6
            if n_k % 2 == 0:
                n_k += 1
            n_use = max(n, n_k)
            for cut in [mid] + [g for g in grids if g != mid]:
                h = _try_fir(
                    task,
                    lambda t, nn, c=cut, be=beta: design_firwin(
                        t, nn, c if len(c) > 1 else c[0], window=("kaiser", float(be))
                    ),
                    n_use,
                )
                if h is not None:
                    return h, {
                        "n": int(n_use),
                        "cutoff": [float(x) for x in cut],
                        "window": "kaiser",
                        "beta": float(beta),
                    }
            return None, None
        h = _try_fir(task, designers[method], n)
        if h is None:
            return None, None
        return h, {"n": int(n)}

    if method == "kaiser_firwin":
        h, p = accept(n0, {}, {})
        if h is not None:
            return h, p
        for n in order_ns:
            h, p = accept(n, {}, {})
            if h is not None:
                return h, p
        return None, None

    for n in order_ns:
        h, p = accept(n, {}, {})
        if h is not None:
            return h, p
    return None, None


def _library_iir_one(task, method: str):
    mid = default_cutoffs(task)
    grids = cutoff_grid(task, n_pts=5)
    rp = pass_rp_db(task)
    rs = max(stop_atten_db(task), 20.0)
    cuts = [mid] + [g for g in grids if g != mid]
    for order in range(2, IIR_ORDER_MAX + 1):
        for cut in cuts:
            fc = cut[0] if len(cut) == 1 else cut
            impl = _try_iir(task, method, order, fc, rp=rp, rs=rs)
            if impl is not None:
                return impl, {
                    "order": int(order),
                    "cutoff": [float(x) for x in np.atleast_1d(fc)],
                    "rp_db": float(rp) if method in {"cheby1", "ellip"} else None,
                    "rs_db": float(rs) if method in {"cheby2", "ellip"} else None,
                }
    return None, None


FIR_LIBRARY = ("firwin", "firwin2", "remez", "firls", "kaiser_firwin")
IIR_LIBRARY = ("butter", "cheby1", "cheby2", "ellip")


def generate_library(task: dict) -> tuple[list[dict], dict]:
    """One occupant per library method if S_t=1; else method-infeasible."""
    rows = []
    log = {"attempts": 0, "accepted": 0, "infeasible": []}
    methods = FIR_LIBRARY if is_fir(task) else IIR_LIBRARY
    for method in methods:
        log["attempts"] += 1
        if is_fir(task):
            impl, params = _library_fir_one(task, method)
        else:
            impl, params = _library_iir_one(task, method)
        if impl is None:
            log["infeasible"].append(method)
            continue
        log["accepted"] += 1
        rows.append(
            {
                "task_id": task["task_id"],
                "source": "library",
                "method": method,
                "parameters": params,
                "impl": impl,
                "label": "valid-by-construction",
            }
        )
    return rows, log


def _draw_cutoff(rng, task):
    out = []
    for a, b in free_transitions(task):
        out.append(float(rng.uniform(a, b)))
    if response_type(task) in {"bp", "bs"} and len(out) >= 2 and out[1] <= out[0]:
        out = sorted(out)
        if out[1] <= out[0]:
            return None
    return out


def random_attempt(rng, task: dict):
    """One unbiased draw. Returns (impl, params) or (None, params)."""
    if is_fir(task):
        odds = np.arange(21, RANDOM_FIR_N_MAX + 1, 2)
        n = int(rng.choice(odds))
        style = str(rng.choice(["windowed", "remez"]))
        cut = _draw_cutoff(rng, task)
        if cut is None:
            return None, {"failed": "cutoff"}
        if style == "windowed":
            window = str(rng.choice(["hamming", "hann", "blackman"]))
            try:
                h = design_firwin(task, n, cut if len(cut) > 1 else cut[0], window=window)
            except Exception:
                return None, {"n": n, "method": "windowed", "window": window}
            if _finite_h(h) and _ok(task["task_id"], h):
                return np.asarray(h, float), {
                    "n": n,
                    "method": "windowed",
                    "window": window,
                    "cutoff": [float(x) for x in cut],
                }
            return None, {"n": n, "method": "windowed", "window": window}
        ws = float(np.exp(rng.uniform(np.log(0.2), np.log(5.0))))
        desired = remez_desired(task)
        if desired == [1, 0]:
            weight = [1.0, ws]
        elif desired == [0, 1]:
            weight = [ws, 1.0]
        elif desired == [0, 1, 0]:
            weight = [ws, 1.0, ws]
        else:
            weight = [1.0, ws, 1.0]
        try:
            h = design_remez(task, n, weight=weight)
        except Exception:
            return None, {"n": n, "method": "remez", "weight": weight}
        if _finite_h(h) and _ok(task["task_id"], h):
            return np.asarray(h, float), {
                "n": n,
                "method": "remez",
                "weight": [float(x) for x in weight],
            }
        return None, {"n": n, "method": "remez"}

    order = int(rng.integers(2, RANDOM_IIR_ORDER_MAX + 1))
    method = str(rng.choice(["butter", "cheby1", "cheby2", "ellip"]))
    cut = _draw_cutoff(rng, task)
    if cut is None:
        return None, {"failed": "cutoff"}
    fc = cut[0] if len(cut) == 1 else cut
    tight = "tight" in task["task_id"]
    if tight:
        rp = float(rng.uniform(0.05, 0.17))
        rs = float(rng.uniform(34.0, 55.0))
    else:
        rp = float(rng.uniform(0.1, 0.8))
        rs = float(rng.uniform(20.0, 50.0))
    impl = _try_iir(task, method, order, fc, rp=rp, rs=rs)
    params = {
        "order": order,
        "method": method,
        "cutoff": [float(x) for x in np.atleast_1d(fc)],
        "rp_db": rp,
        "rs_db": rs,
    }
    if impl is None:
        return None, params
    return impl, params
