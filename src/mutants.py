"""Suite N invalid-by-construction mutants M1–M8.

Admission is S_t(h)=0 only. Coefficient distance, Oracle B, and T
are not consulted.
"""
from __future__ import annotations

import numpy as np
from scipy import signal as sp_signal

from src.filter_geom import (
    default_cutoffs,
    estimate_fir_n,
    is_fir,
    nyquist,
    response_type,
)
from src.spec_checker import check_specification
from src.valid_metrics import unpack

FIR_N_TYPICAL = 51
IIR_ORDER_TYPICAL = 4


def _chk(task, impl):
    return check_specification(task["task_id"], impl)


def _failing(task, impl):
    if impl is None:
        return None
    try:
        out = _chk(task, impl)
    except Exception:
        return None
    if out["pass"]:
        return None
    return out


def _fir(n, cutoff, fs, pass_zero, window="hamming"):
    try:
        h = sp_signal.firwin(int(n), cutoff, window=window, fs=float(fs), pass_zero=pass_zero)
    except Exception:
        return None
    h = np.asarray(h, float).reshape(-1)
    if not np.all(np.isfinite(h)):
        return None
    return h


def _iir(order, fc, fs, btype):
    try:
        b, a = sp_signal.butter(int(order), fc, btype=btype, fs=float(fs), output="ba")
    except Exception:
        return None
    b, a = np.asarray(b, float), np.asarray(a, float)
    if not (np.all(np.isfinite(b)) and np.all(np.isfinite(a))):
        return None
    return {"b": b, "a": a}


def _correct_pz(task):
    r = response_type(task)
    return True if r in {"lp", "bs"} else False


def _correct_btype(task):
    return "low" if response_type(task) == "lp" else "high"


def _n_fir(task):
    return max(int(estimate_fir_n(task)), FIR_N_TYPICAL)


def _cut(task):
    c = default_cutoffs(task)
    return c if len(c) > 1 else c[0]


def _into_constrained(task, which="stop"):
    bands = task["stop_band"] if which == "stop" else task["pass_band"]
    bands = sorted(bands, key=lambda b: b["f0"])
    return [0.5 * (float(b["f0"]) + float(b["f1"])) for b in bands]


def _scale_pass_gain(impl, task, target=0.2):
    b, a = unpack(impl)
    fs = float(task["sampling_rate"])
    p = sorted(task["pass_band"], key=lambda x: x["f0"])[0]
    f0 = 0.5 * (float(p["f0"]) + float(p["f1"]))
    if a is None:
        w, H = sp_signal.freqz(b, worN=4096, fs=fs)
    else:
        w, H = sp_signal.freqz(b, a, worN=4096, fs=fs)
    idx = int(np.argmin(np.abs(w - f0)))
    g = float(np.abs(H[idx]))
    if g < 1e-12:
        return None
    scale = target / g
    if a is None:
        return b * scale
    return {"b": b * scale, "a": a}


def _m1(task):
    fs = float(task["sampling_rate"])
    r = response_type(task)
    cut = _cut(task)
    if is_fir(task):
        n = _n_fir(task)
        swap = {"lp": False, "hp": True, "bp": True, "bs": False}[r]
        return _fir(n, cut, fs, swap), {"pass_zero": swap, "cutoff": np.atleast_1d(cut).tolist(), "n": n}
    order = IIR_ORDER_TYPICAL
    btype = "high" if r == "lp" else "low"
    fc = float(np.atleast_1d(cut)[0])
    return _iir(order, fc, fs, btype), {"btype": btype, "order": order, "cutoff": fc}


def _m2(task):
    fs = float(task["sampling_rate"])
    into = _into_constrained(task, "stop")
    r = response_type(task)
    if r in {"lp", "hp"}:
        cut = into[0]
    else:
        if len(into) < 2:
            into = into + _into_constrained(task, "pass")
        cut = [into[0], into[-1]]
        if cut[1] <= cut[0]:
            nyq = nyquist(task)
            cut = [0.15 * nyq, 0.85 * nyq]
    if is_fir(task):
        n = _n_fir(task)
        h = _fir(n, cut, fs, _correct_pz(task))
        return h, {"cutoff": np.atleast_1d(cut).tolist(), "n": n, "into": "stop"}
    fc = cut if isinstance(cut, list) else cut
    if response_type(task) in {"lp", "hp"}:
        fc = float(np.atleast_1d(cut)[0])
    return _iir(IIR_ORDER_TYPICAL, fc, fs, _correct_btype(task)), {
        "cutoff": np.atleast_1d(fc).tolist(),
        "order": IIR_ORDER_TYPICAL,
        "into": "stop",
    }


def _m3(task):
    fs = float(task["sampling_rate"])
    cut = _cut(task)
    if is_fir(task):
        h = _fir(7, cut, fs, _correct_pz(task))
        return h, {"n": 7, "cutoff": np.atleast_1d(cut).tolist()}
    fc = float(np.atleast_1d(cut)[0])
    return _iir(1, fc, fs, _correct_btype(task)), {"order": 1, "cutoff": fc}


def _m4(task):
    if is_fir(task):
        return None, {"applicable": False}
    fs = float(task["sampling_rate"])
    fc = float(np.atleast_1d(_cut(task))[0])
    ba = _iir(2, fc, fs, _correct_btype(task))
    if ba is None:
        return None, {"failed": "butter"}
    z, p, k = sp_signal.tf2zpk(ba["b"], ba["a"])
    p = np.asarray(p, complex)
    if p.size == 0:
        p = np.array([1.02 + 0.0j])
    else:
        scale = 1.02 / max(float(np.max(np.abs(p))), 1e-18)
        p = p * scale
    b, a = sp_signal.zpk2tf(z, p, k)
    b = np.real(np.real_if_close(b, tol=1e6))
    a = np.real(np.real_if_close(a, tol=1e6))
    return {"b": np.asarray(b, float), "a": np.asarray(a, float)}, {
        "pole_radius": 1.02,
        "order": 2,
        "cutoff": fc,
    }


def _m5(task):
    fs = float(task["sampling_rate"])
    nyq = nyquist(task)
    raw = np.asarray(default_cutoffs(task), float)
    cut = (raw / nyq).tolist()
    if len(cut) == 1:
        cut = cut[0]
    if is_fir(task):
        n = _n_fir(task)
        h = _fir(n, cut, fs, _correct_pz(task))
        return h, {"cutoff_hz_as_if_nyquist_1": np.atleast_1d(cut).tolist(), "n": n}
    fc = float(np.atleast_1d(cut)[0])
    return _iir(IIR_ORDER_TYPICAL, fc, fs, _correct_btype(task)), {
        "cutoff_hz_as_if_nyquist_1": fc,
        "order": IIR_ORDER_TYPICAL,
    }


def _m6(task):
    fs = float(task["sampling_rate"])
    cut = _cut(task)
    if is_fir(task):
        base = _fir(_n_fir(task), cut, fs, _correct_pz(task))
    else:
        fc = float(np.atleast_1d(cut)[0])
        base = _iir(IIR_ORDER_TYPICAL, fc, fs, _correct_btype(task))
    scaled = _scale_pass_gain(base, task, 0.2)
    return scaled, {"target_pass_gain": 0.2}


def _m7(task):
    cut = _cut(task)
    wrong_fs = 48000.0
    if is_fir(task):
        h = _fir(_n_fir(task), cut, wrong_fs, _correct_pz(task))
        return h, {"designed_fs": wrong_fs, "scored_fs": float(task["sampling_rate"]), "n": _n_fir(task)}
    fc = float(np.atleast_1d(cut)[0])
    return _iir(IIR_ORDER_TYPICAL, fc, wrong_fs, _correct_btype(task)), {
        "designed_fs": wrong_fs,
        "scored_fs": float(task["sampling_rate"]),
        "order": IIR_ORDER_TYPICAL,
    }


def _m8(task):
    fs = float(task["sampling_rate"])
    nyq = nyquist(task)
    r = response_type(task)
    if is_fir(task):
        n = _n_fir(task)
        mid = default_cutoffs(task)
        if r == "bp":
            h = _fir(n, mid, fs, True)
            return h, {"emitted": "bandstop", "n": n, "cutoff": mid}
        if r == "bs":
            h = _fir(n, mid, fs, False)
            return h, {"emitted": "bandpass", "n": n, "cutoff": mid}
        # LP/HP: emit a two-band type
        pair = [0.25 * nyq, 0.65 * nyq]
        if r == "lp":
            h = _fir(n, pair, fs, False)
            return h, {"emitted": "bandpass", "n": n, "cutoff": pair}
        h = _fir(n, pair, fs, True)
        return h, {"emitted": "bandstop", "n": n, "cutoff": pair}
    # IIR: bandpass at a mid-band, not the complementary one-pole-type swap
    pair = [0.25 * nyq, 0.55 * nyq]
    return _iir(IIR_ORDER_TYPICAL, pair, fs, "bandpass"), {
        "emitted": "bandpass",
        "order": IIR_ORDER_TYPICAL,
        "cutoff": pair,
    }


_BUILDERS = {
    "M1": _m1,
    "M2": _m2,
    "M3": _m3,
    "M4": _m4,
    "M5": _m5,
    "M6": _m6,
    "M7": _m7,
    "M8": _m8,
}


def applicable(task: dict, mid: str) -> bool:
    if mid == "M4":
        return not is_fir(task)
    return True


def generate_mutant(task: dict, mid: str):
    if not applicable(task, mid):
        return None
    impl, params = _BUILDERS[mid](task)
    out = _failing(task, impl)
    if out is not None:
        return {
            "task_id": task["task_id"],
            "mechanism": mid,
            "source_parameters": params,
            "impl": impl,
            "S_t": False,
            "residuals": out["residuals"],
            "label": "invalid-by-construction",
        }
    # M3 fallback: still "too short", N=3 / already order 1
    if mid == "M3" and is_fir(task):
        cut = _cut(task)
        impl = _fir(3, cut, float(task["sampling_rate"]), _correct_pz(task))
        out = _failing(task, impl)
        if out is not None:
            params = {"n": 3, "cutoff": np.atleast_1d(cut).tolist(), "fallback": "n=3"}
            return {
                "task_id": task["task_id"],
                "mechanism": mid,
                "source_parameters": params,
                "impl": impl,
                "S_t": False,
                "residuals": out["residuals"],
                "label": "invalid-by-construction",
            }
    # M7 fallback: fs=1
    if mid == "M7":
        cut = default_cutoffs(task)
        nyq = nyquist(task)
        cut_n = [c / nyq for c in cut]
        c7 = cut_n if len(cut_n) > 1 else cut_n[0]
        if is_fir(task):
            impl = _fir(_n_fir(task), c7, 1.0, _correct_pz(task))
        else:
            impl = _iir(IIR_ORDER_TYPICAL, float(np.atleast_1d(c7)[0]), 1.0, _correct_btype(task))
        out = _failing(task, impl)
        if out is not None:
            params = {"designed_fs": 1.0, "scored_fs": float(task["sampling_rate"]), "fallback": "fs=1"}
            return {
                "task_id": task["task_id"],
                "mechanism": mid,
                "source_parameters": params,
                "impl": impl,
                "S_t": False,
                "residuals": out["residuals"],
                "label": "invalid-by-construction",
            }
    return None
