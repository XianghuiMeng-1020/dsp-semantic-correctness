"""Post-admission distances. Never used as a search objective."""
from __future__ import annotations

import numpy as np
from scipy import signal as sp_signal

EPS = 1e-18
FREQZ_N = 4096
TAU_R = 0.05


def unpack(impl):
    if isinstance(impl, dict) and "b" in impl:
        b = np.asarray(impl["b"], float).reshape(-1)
        a = impl.get("a")
        a = None if a is None else np.asarray(a, float).reshape(-1)
        return b, a
    return np.asarray(impl, float).reshape(-1), None


def d_coeff(h, href) -> float:
    """Min-length relative L2. Same definition as paper R."""
    b, a = unpack(h)
    rb, ra = unpack(href)
    if a is None and ra is None:
        n = min(len(b), len(rb))
        if n == 0:
            return 1.0
        return float(np.linalg.norm(b[:n] - rb[:n]) / max(np.linalg.norm(rb[:n]), EPS))
    v1 = np.concatenate([b, np.ones(1) if a is None else a])
    v2 = np.concatenate([rb, np.ones(1) if ra is None else ra])
    n = min(len(v1), len(v2))
    return float(np.linalg.norm(v1[:n] - v2[:n]) / max(np.linalg.norm(v2[:n]), EPS))


def _freqz(h, fs: float):
    b, a = unpack(h)
    if a is None:
        w, H = sp_signal.freqz(b, worN=FREQZ_N, fs=fs)
    else:
        w, H = sp_signal.freqz(b, a, worN=FREQZ_N, fs=fs)
    return w, np.abs(H)


def mag_rmse(h, href, fs: float, bands=None) -> float:
    w, mag = _freqz(h, fs)
    _, mag_r = _freqz(href, fs)
    d = mag - mag_r
    if bands:
        mask = np.zeros_like(w, dtype=bool)
        for b in bands:
            mask |= (w >= b["f0"]) & (w <= b["f1"])
        if not np.any(mask):
            return 1.0
        d = d[mask]
    return float(np.sqrt(np.mean(d**2)))


def same_order(h, href) -> bool:
    b, a = unpack(h)
    rb, ra = unpack(href)
    if a is None and ra is None:
        return len(b) == len(rb)
    if a is None or ra is None:
        return False
    return len(b) == len(rb) and len(a) == len(ra)


def distance_to_reference(h, href, task: dict) -> dict:
    fs = float(task["sampling_rate"])
    bands = list(task["pass_band"]) + list(task["stop_band"])
    return {
        "d_coeff": d_coeff(h, href),
        "mag_rmse_band": mag_rmse(h, href, fs, bands),
        "mag_rmse_full": mag_rmse(h, href, fs, None),
        "same_order": bool(same_order(h, href)),
    }


def is_near_duplicate(h, href, fs: float) -> bool:
    return d_coeff(h, href) <= 0.01 and mag_rmse(h, href, fs, None) <= 1e-3


def is_type1_linear_phase(h, atol: float = 1e-8) -> bool:
    """Odd-length symmetric FIR (Type I). IIR is False."""
    b, a = unpack(h)
    if a is not None:
        a = np.asarray(a, float).reshape(-1)
        if len(a) > 1 or abs(float(a[0]) - 1.0) > atol:
            return False
    b = np.asarray(b, float).reshape(-1)
    if len(b) < 3 or len(b) % 2 == 0:
        return False
    return bool(np.allclose(b, b[::-1], atol=atol))
