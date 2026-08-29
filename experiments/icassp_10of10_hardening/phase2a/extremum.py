"""Secondary stationary-point cross-check. Not a primary certificate."""
from __future__ import annotations

import math

import numpy as np

from src.continuous_certification.fir_power_polynomial import (
    _as_fir_taps,
    _eff_bounds,
    _load_task,
    f64_frac,
    power_polynomial,
)


def _c_k(h: np.ndarray) -> np.ndarray:
    n = len(h)
    c = np.zeros(n, dtype=np.float64)
    for k in range(n):
        c[k] = float(np.dot(h[: n - k], h[k:]))
    return c


def stationary_omegas(h: np.ndarray, w0: float, w1: float, n_grid: int = 4001) -> list[float]:
    """Zero crossings of dP/dω ≈ -2 Σ k c_k sin(kω) on a dense grid (audit only)."""
    c = _c_k(h)
    ks = np.arange(1, len(c))
    w = np.linspace(w0, w1, n_grid)
    dP = np.zeros_like(w)
    for k, ck in zip(ks, c[1:]):
        dP -= 2.0 * k * ck * np.sin(k * w)
    roots = []
    for i in range(len(w) - 1):
        if dP[i] == 0.0:
            roots.append(float(w[i]))
        elif dP[i] * dP[i + 1] < 0:
            # linear interpolate
            t = dP[i] / (dP[i] - dP[i + 1])
            roots.append(float(w[i] + t * (w[i + 1] - w[i])))
    return roots


def mag_sq(h: np.ndarray, omega: float) -> float:
    n = np.arange(len(h), dtype=np.float64)
    H = np.dot(h, np.exp(-1j * omega * n))
    return float(np.abs(H) ** 2)


def audit_occupant(task_id: str, impl) -> dict:
    task = _load_task(task_id)
    h = _as_fir_taps(impl)
    fs = float(task["sampling_rate"])
    floor = float(task["residual_floor"])
    two_pi = 2.0 * math.pi
    rows = []
    worst = None
    for band in list(task["pass_band"]) + list(task["stop_band"]):
        f0, f1 = float(band["f0"]), float(band["f1"])
        lo, hi = float(band["lo"]), float(band["hi"])
        L, U = _eff_bounds(lo, hi, floor)
        w0, w1 = two_pi * f0 / fs, two_pi * f1 / fs
        pts = [w0, w1] + stationary_omegas(h, w0, w1)
        for w in pts:
            p = mag_sq(h, w)
            mag = math.sqrt(max(p, 0.0))
            Lf, Uf = float(L), float(U)
            viol = (L > 0 and mag < Lf) or mag > Uf
            rec = {"omega": w, "f_hz": w * fs / two_pi, "mag": mag, "L": Lf, "U": Uf, "viol": viol}
            rows.append(rec)
            if viol and (worst is None or mag > Uf):
                worst = rec
    return {
        "task_id": task_id,
        "n_taps": int(len(h)),
        "n_checked_points": len(rows),
        "n_violating_grid_or_stat": sum(1 for r in rows if r["viol"]),
        "worst": worst,
        "note": "numerical stationary-point audit; not a continuous certificate",
    }
