#!/usr/bin/env python3
"""Reproduce RQ2: same-order first-principles FIR occupants of frozen Arm N masks."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from scipy import signal as sp_signal

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.contracts_arm_n import (  # noqa: E402
    FIR_BANDPASS_BANDS,
    FIR_BANDSTOP_BANDS,
    FIR_LOWPASS_BANDS,
    FS,
    spec_residual,
)
from src.first_principles_fir import (  # noqa: E402
    assert_no_scipy_design_in,
    frequency_sampling,
    mag_bandpass,
    mag_bandstop,
    mag_lowpass,
    windowed_sinc_bandpass,
    windowed_sinc_bandstop,
    windowed_sinc_lowpass,
)

assert_no_scipy_design_in(ROOT / "src" / "first_principles_fir.py")
TAU_R = 0.05


def rel_l2(a, b):
    a = np.asarray(a, float).reshape(-1)
    b = np.asarray(b, float).reshape(-1)
    n = min(len(a), len(b))
    return float(np.linalg.norm(a[:n] - b[:n]) / max(np.linalg.norm(b[:n]), 1e-18))


def best_windowed(kind, n):
    best = None
    if kind == "lp":
        for fc in np.linspace(900.0, 1400.0, 21):
            h = windowed_sinc_lowpass(n, float(fc), FS)
            r = float(spec_residual(h, FIR_LOWPASS_BANDS))
            if best is None or r < best[0]:
                best = (r, h)
    elif kind == "bp":
        for f1, f2 in ((1100, 2700), (1200, 2600), (1000, 2800)):
            h = windowed_sinc_bandpass(n, f1, f2, FS, 1850.0)
            r = float(spec_residual(h, FIR_BANDPASS_BANDS))
            if best is None or r < best[0]:
                best = (r, h)
    else:
        for f1, f2 in ((900, 2700), (1000, 2600), (1100, 2500)):
            h = windowed_sinc_bandstop(n, f1, f2, FS)
            r = float(spec_residual(h, FIR_BANDSTOP_BANDS))
            if best is None or r < best[0]:
                best = (r, h)
    return best


def best_freq(kind, n):
    best = None
    if kind == "lp":
        grids = ((800.0, 2000.0), (800.0, 1800.0), (750.0, 2000.0))
        for a, b in grids:
            h = frequency_sampling(n, lambda f, x=a, y=b: mag_lowpass(f, x, y), FS)
            s = float(np.sum(h))
            if abs(s) > 1e-18:
                h = h / s
            r = float(spec_residual(h, FIR_LOWPASS_BANDS))
            if best is None or r < best[0]:
                best = (r, h)
    elif kind == "bp":
        grids = ((500, 1500, 2200, 3200), (400, 1500, 2200, 3300))
        for g in grids:
            h = frequency_sampling(n, lambda f, gg=g: mag_bandpass(f, *gg), FS)
            r = float(spec_residual(h, FIR_BANDPASS_BANDS))
            if best is None or r < best[0]:
                best = (r, h)
    else:
        grids = ((600, 1400, 2200, 3000), (600, 1300, 2300, 3000))
        for g in grids:
            h = frequency_sampling(n, lambda f, gg=g: mag_bandstop(f, *gg), FS)
            r = float(spec_residual(h, FIR_BANDSTOP_BANDS))
            if best is None or r < best[0]:
                best = (r, h)
    return best


def main():
    gold = {
        "lp": (81, FIR_LOWPASS_BANDS, sp_signal.firwin(81, 1100.0, window="hamming", fs=FS, pass_zero=True)),
        "bp": (101, FIR_BANDPASS_BANDS, sp_signal.firwin(101, [1200.0, 2600.0], window="hamming", fs=FS, pass_zero=False)),
        "bs": (101, FIR_BANDSTOP_BANDS, sp_signal.firwin(101, [1000.0, 2600.0], window="hamming", fs=FS, pass_zero=True)),
    }
    n_s = 0
    n_disc = 0
    for kind, (n, _bands, href) in gold.items():
        for method, fn in (("ws", best_windowed), ("fs", best_freq)):
            resid, h = fn(kind, n)
            ok = resid <= 1e-6
            d = rel_l2(h, href)
            n_s += int(ok)
            n_disc += int(d > TAU_R)
            print(f"  {method} {kind} n={n}: S={ok} residual={resid:.3e} l2={d:.4f}")
    print(f"same-order in V_t: {n_s}/6")
    print(f"same-order coeff-discordant: {n_disc}/6")
    if n_s != 6:
        raise SystemExit("FIRST_PRINCIPLES_SAMEORDER: FAIL")
    print("FIRST_PRINCIPLES_SAMEORDER: PASS")


if __name__ == "__main__":
    main()
