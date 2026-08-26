"""Canonical and historical distances.

Confirmatory analysis uses canonical / response distances.
Historical min-length truncation is retained only as a baseline metric.
"""
from __future__ import annotations

import numpy as np
from scipy import signal as sp_signal

from src.verification.canonicalize import (
    TRIM_ABS,
    canonicalize_fir,
    canonicalize_iir,
    unpack,
)
from src.verification.independent_spec_verifier import FREQZ_N
from src.verification.registry_io import is_fir

EPS = 1e-18
RESP_N = FREQZ_N


def d_coeff_historical(h, href) -> float:
    """Min-length relative L2. Frozen Phase 2 definition. Not confirmatory."""
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


def _pad_eq(a: np.ndarray, b: np.ndarray):
    n = max(len(a), len(b))
    aa = np.zeros(n, float)
    bb = np.zeros(n, float)
    aa[: len(a)] = a
    bb[: len(b)] = b
    return aa, bb


def d_coeff_canonical_fir(h, href, magnitude_equiv: bool = False) -> dict:
    c = canonicalize_fir(h)
    r = canonicalize_fir(href)
    v, vr = _pad_eq(c.h, r.h)
    den = max(float(np.linalg.norm(vr)), EPS)
    d_signed = float(np.linalg.norm(v - vr) / den)
    d_flip = float(np.linalg.norm(-v - vr) / den)
    d_mag = min(d_signed, d_flip)
    same_len = c.n_taps == r.n_taps
    zero_pad_only = (c.n_taps != r.n_taps) and (
        np.allclose(v, vr, atol=TRIM_ABS) or np.allclose(-v, vr, atol=TRIM_ABS)
    )
    return {
        "d_coeff_canonical": d_mag if magnitude_equiv else d_signed,
        "d_coeff_signed": d_signed,
        "d_coeff_mag_equiv": d_mag,
        "same_length_after_trim": same_len,
        "zero_pad_artifact": bool(zero_pad_only),
        "sign_flip_only": bool(d_signed > 1e-12 and d_mag <= 1e-12),
        "n_taps": c.n_taps,
        "n_taps_ref": r.n_taps,
        "type1": c.type1,
        "type1_ref": r.type1,
    }


def d_coeff_canonical_iir(h, href) -> dict:
    c = canonicalize_iir(h)
    r = canonicalize_iir(href)
    b, br = _pad_eq(c.b, r.b)
    a, ar = _pad_eq(c.a, r.a)
    v = np.concatenate([b, a])
    vr = np.concatenate([br, ar])
    d = float(np.linalg.norm(v - vr) / max(float(np.linalg.norm(vr)), EPS))
    return {
        "d_coeff_canonical": d,
        "d_coeff_signed": d,
        "d_coeff_mag_equiv": d,
        "same_length_after_trim": len(c.b) == len(r.b) and len(c.a) == len(r.a),
        "zero_pad_artifact": bool(
            np.allclose(b, br, atol=TRIM_ABS) and np.allclose(a, ar, atol=TRIM_ABS)
        ),
        "sign_flip_only": False,
        "n_b": int(len(c.b)),
        "n_a": int(len(c.a)),
        "n_b_ref": int(len(r.b)),
        "n_a_ref": int(len(r.a)),
        "a0_scaled": "scaled_a0_to_1" in c.notes or "scaled_a0_to_1" in r.notes,
    }


def d_coeff_canonical(h, href, task: dict | None = None) -> dict:
    if task is not None and is_fir(task):
        return d_coeff_canonical_fir(h, href, magnitude_equiv=True)
    b, a = unpack(h)
    rb, ra = unpack(href)
    if a is None and ra is None:
        return d_coeff_canonical_fir(h, href, magnitude_equiv=True)
    return d_coeff_canonical_iir(h, href)


def _mag_pair(h, href, fs: float, n: int = RESP_N):
    b, a = unpack(h)
    rb, ra = unpack(href)
    if a is None:
        w, H = sp_signal.freqz(b, worN=n, fs=fs)
    else:
        try:
            sos = sp_signal.tf2sos(b, a)
            w, H = sp_signal.sosfreqz(sos, worN=n, fs=fs)
        except Exception:
            w, H = sp_signal.freqz(b, a, worN=n, fs=fs)
    if ra is None:
        _, Hr = sp_signal.freqz(rb, worN=n, fs=fs)
    else:
        try:
            sosr = sp_signal.tf2sos(rb, ra)
            _, Hr = sp_signal.sosfreqz(sosr, worN=n, fs=fs)
        except Exception:
            _, Hr = sp_signal.freqz(rb, ra, worN=n, fs=fs)
    return w, np.abs(H), np.abs(Hr)


def d_resp(h, href, fs: float, bands=None, n: int = RESP_N) -> float:
    w, mag, mag_r = _mag_pair(h, href, fs, n=n)
    d = mag - mag_r
    if bands:
        mask = np.zeros_like(w, dtype=bool)
        for b in bands:
            mask |= (w >= float(b["f0"])) & (w <= float(b["f1"]))
        if not np.any(mask):
            return 1.0
        d = d[mask]
    return float(np.sqrt(np.mean(d**2)))


def same_order_canonical(h, href, task: dict | None = None) -> bool:
    if task is not None and is_fir(task):
        return canonicalize_fir(h).n_taps == canonicalize_fir(href).n_taps
    b, a = unpack(h)
    rb, ra = unpack(href)
    if a is None and ra is None:
        return canonicalize_fir(h).n_taps == canonicalize_fir(href).n_taps
    c = canonicalize_iir(h)
    r = canonicalize_iir(href)
    return len(c.b) == len(r.b) and len(c.a) == len(r.a)


def distance_bundle(h, href, task: dict) -> dict:
    fs = float(task["sampling_rate"])
    bands = list(task["pass_band"]) + list(task["stop_band"])
    can = d_coeff_canonical(h, href, task)
    return {
        **can,
        "d_coeff_historical": d_coeff_historical(h, href),
        "d_resp_band": d_resp(h, href, fs, bands),
        "d_resp_full": d_resp(h, href, fs, None),
        "same_order_canonical": bool(same_order_canonical(h, href, task)),
    }
