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
    # Frozen P2A same-order placements (length locked to firwin).
    if kind == "lp":
        h = windowed_sinc_lowpass(n, 1400.0, FS)
        return float(spec_residual(h, FIR_LOWPASS_BANDS)), h
    if kind == "bp":
        h = windowed_sinc_bandpass(n, 1000.0, 2700.0, FS, 1850.0)
        return float(spec_residual(h, FIR_BANDPASS_BANDS)), h
    h = windowed_sinc_bandstop(n, 1000.0, 2600.0, FS)
    return float(spec_residual(h, FIR_BANDSTOP_BANDS)), h


def best_freq(kind, n):
    # Frozen P2A same-order frequency-sampling grids.
    if kind == "lp":
        h = frequency_sampling(n, lambda f: mag_lowpass(f, 800.0, 2000.0), FS)
        s = float(np.sum(h))
        if abs(s) > 1e-18:
            h = h / s
        return float(spec_residual(h, FIR_LOWPASS_BANDS)), h
    if kind == "bp":
        h = frequency_sampling(n, lambda f: mag_bandpass(f, 500.0, 1500.0, 2200.0, 3200.0), FS)
        g = float(np.abs(np.dot(h, np.exp(-1j * 2.0 * np.pi * 1850.0 * np.arange(len(h)) / FS))))
        if g > 1e-12:
            h = h / g
        return float(spec_residual(h, FIR_BANDPASS_BANDS)), h
    h = frequency_sampling(n, lambda f: mag_bandstop(f, 600.0, 1400.0, 2200.0, 3000.0), FS)
    s = float(np.sum(h))
    if abs(s) > 1e-18:
        h = h / s
    return float(spec_residual(h, FIR_BANDSTOP_BANDS)), h


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
    if n_s != 6 or n_disc != 5:
        raise SystemExit("FIRST_PRINCIPLES_SAMEORDER: FAIL")
    print("FIRST_PRINCIPLES_SAMEORDER: PASS")


if __name__ == "__main__":
    main()
