#!/usr/bin/env python3
"""Reproduce RQ3 (P2C): tighter low-pass mask, same-order N=57 occupants.

Frozen reconstruction only. No new models or generations.
Design parameters are those that produced the published N=57 pair.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from scipy import signal as sp_signal

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.contracts_arm_n import FS, spec_residual  # noqa: E402
from src.first_principles_fir import (  # noqa: E402
    assert_no_scipy_design_in,
    frequency_sampling,
    mag_lowpass,
    windowed_sinc_lowpass,
)

assert_no_scipy_design_in(ROOT / "src" / "first_principles_fir.py")

TIGHT_BANDS = [
    {"f0": 0.0, "f1": 800.0, "lo": 0.99, "hi": 1.01},
    {"f0": 1400.0, "f1": 4000.0, "lo": 0.0, "hi": 0.01},
]
CONSTRAINED_TONES = [50.0, 400.0, 800.0, 1400.0, 2000.0, 3000.0, 3900.0]
N_TONE = 8192
DROP = 1024
TAU_R = 0.05
N_COMMON = 57
WORN = 4096


def rel_l2(a, b):
    a = np.asarray(a, float).reshape(-1)
    b = np.asarray(b, float).reshape(-1)
    n = min(len(a), len(b))
    return float(np.linalg.norm(a[:n] - b[:n]) / max(np.linalg.norm(b[:n]), 1e-18))


def mag_rmse(h, href, bands):
    w, H = sp_signal.freqz(h, worN=WORN, fs=FS)
    _, Hr = sp_signal.freqz(href, worN=WORN, fs=FS)
    d = np.abs(H) - np.abs(Hr)
    mask = np.zeros_like(w, dtype=bool)
    for band in bands:
        mask |= (w >= band["f0"]) & (w <= band["f1"])
    return float(np.sqrt(np.mean(d**2))), float(np.sqrt(np.mean(d[mask] ** 2)))


def group_delay_pass(h):
    w, H = sp_signal.freqz(h, worN=WORN, fs=FS)
    ok = (w <= 800.0) & (np.abs(H) >= 0.3)
    _w_gd, gd = sp_signal.group_delay((h, [1.0]), w=2 * np.pi * w / FS)
    gd = np.asarray(gd, float)
    vals = gd[ok]
    vals = vals[np.isfinite(vals)]
    return float(np.mean(vals))


def tone_gain(h, f0):
    t = np.arange(N_TONE) / FS
    x = np.cos(2 * np.pi * f0 * t)
    y = sp_signal.lfilter(h, [1.0], x)
    ax = float(np.mean(np.abs(sp_signal.hilbert(x[DROP:]))))
    ay = float(np.mean(np.abs(sp_signal.hilbert(y[DROP:]))))
    return ay / max(ax, 1e-18)


def tones_in_mask(h, bands):
    n_ok = n_con = 0
    for f0 in CONSTRAINED_TONES:
        for band in bands:
            if band["f0"] <= f0 <= band["f1"]:
                g = tone_gain(h, f0)
                n_con += 1
                n_ok += int(band["lo"] <= g <= band["hi"])
                break
    return n_ok, n_con


def design_ws(n, fc):
    return windowed_sinc_lowpass(n, fc, FS)


def design_fs(n, f_pass, f_stop):
    h = frequency_sampling(n, lambda f, a=f_pass, b=f_stop: mag_lowpass(f, a, b), FS)
    s = float(np.sum(h))
    if abs(s) > 1e-18:
        h = h / s
    return h


def check(cond, label, failures):
    print(f"  {'PASS' if cond else 'FAIL'}  {label}")
    if not cond:
        failures.append(label)


def main() -> int:
    failures: list[str] = []
    print("RQ3 / P2C — tight low-pass, frozen N=57 reconstruction")

    h_fw = sp_signal.firwin(N_COMMON, 1025.0, window="hamming", fs=FS, pass_zero=True)
    h_ws = design_ws(N_COMMON, 1025.0)
    h_fs = design_fs(N_COMMON, 820.0, 1350.0)

    rows = {"firwin": h_fw, "windowed_sinc": h_ws, "frequency_sampling": h_fs}
    for name, h in rows.items():
        resid = float(spec_residual(h, TIGHT_BANDS))
        n_ok, n_con = tones_in_mask(h, TIGHT_BANDS)
        gd = group_delay_pass(h)
        print(
            f"  {name}: n={len(h)} S={resid <= 1e-6} residual={resid:.3e} "
            f"tones={n_ok}/{n_con} GD={gd:.1f}"
        )
        check(len(h) == N_COMMON, f"{name} length {N_COMMON}", failures)
        check(resid <= 1e-6, f"{name} tight S_t", failures)
        check(n_ok == n_con == 7, f"{name} tones 7/7", failures)
        check(abs(gd - 28.0) < 0.05, f"{name} GD 28", failures)

    l2_ident = rel_l2(h_fw, h_ws)
    l2 = rel_l2(h_ws, h_fs)
    full_rmse, band_rmse = mag_rmse(h_ws, h_fs, TIGHT_BANDS)
    print(f"  firwin vs windowed-sinc l2={l2_ident:.3e} (same method)")
    print(
        f"  windowed-sinc vs frequency-sampling: "
        f"l2={l2:.4f} band_RMSE={band_rmse:.4f} full_RMSE={full_rmse:.4f}"
    )
    check(l2_ident < 1e-12, "firwin ≡ windowed-sinc", failures)
    check(abs(l2 - 0.115) < 0.002, "coeff l2 ≈ 0.115", failures)
    check(abs(band_rmse - 0.0014) < 0.0002, "spec-band |H| RMSE ≈ 0.0014", failures)
    check(abs(full_rmse - 0.057) < 0.002, "full-grid |H| RMSE ≈ 0.057", failures)
    check(l2 > TAU_R, "distinct pair exceeds tau_R", failures)

    h_fw43 = sp_signal.firwin(43, 1100.0, window="hamming", fs=FS, pass_zero=True)
    h_ws43 = design_ws(43, 1100.0)
    check(float(spec_residual(h_fw43, TIGHT_BANDS)) <= 1e-6, "firwin min-N=43 S_t", failures)
    check(float(spec_residual(h_ws43, TIGHT_BANDS)) <= 1e-6, "windowed-sinc min-N=43 S_t", failures)
    check(rel_l2(h_fw43, h_ws43) < 1e-12, "min-N firwin ≡ windowed-sinc", failures)

    if failures:
        print(f"P2C_PUBLISHED_COUNTS_MATCH: NO ({len(failures)} failed checks)")
        return 1
    print("P2C_PUBLISHED_COUNTS_MATCH: YES")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
