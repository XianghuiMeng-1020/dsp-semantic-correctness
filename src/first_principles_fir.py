"""First-principles FIR design. Numpy only. No SciPy design APIs.

Implements:
  A) windowed-sinc (Hamming), including BP/BS via complementary lowpass
  B) frequency-sampling (IDFT of a conjugate-symmetric linear-phase mask)

Design search is over length and cutoff/transition placement only.
"""
from __future__ import annotations

import ast
from pathlib import Path

import numpy as np

_FORBIDDEN = {
    "firwin",
    "firwin2",
    "firls",
    "remez",
    "firgr",
    "kaiserord",
    "kaiser_beta",
    "butter",
    "cheby1",
    "cheby2",
    "ellip",
    "bessel",
    "iirdesign",
    "iirfilter",
    "sosfilt",
}


def assert_no_scipy_design_in(path: Path) -> None:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module and "scipy" in node.module:
                raise AssertionError(f"scipy import in design module: {node.module}")
            names.update(a.name for a in node.names)
        if isinstance(node, ast.Attribute):
            names.add(node.attr)
        if isinstance(node, ast.Name):
            names.add(node.id)
    hit = names & _FORBIDDEN
    if hit:
        raise AssertionError(f"forbidden design symbols in {path.name}: {hit}")


def hamming(n_taps: int) -> np.ndarray:
    n = np.arange(n_taps, dtype=float)
    return 0.54 - 0.46 * np.cos(2.0 * np.pi * n / (n_taps - 1))


def windowed_sinc_lowpass(n_taps: int, fc_hz: float, fs: float) -> np.ndarray:
    """Type-I linear-phase lowpass: 2 fc sinc(2 fc (n-M)) * Hamming, DC-normalized."""
    if n_taps % 2 == 0:
        raise ValueError("windowed-sinc uses odd length (Type I)")
    m = (n_taps - 1) / 2.0
    n = np.arange(n_taps, dtype=float)
    fc = fc_hz / fs
    h = (2.0 * fc) * np.sinc(2.0 * fc * (n - m))
    h = h * hamming(n_taps)
    s = float(np.sum(h))
    if abs(s) < 1e-18:
        raise ValueError("windowed-sinc DC is zero")
    return h / s


def dtft_gain(h: np.ndarray, f_hz: float, fs: float) -> float:
    n = np.arange(len(h), dtype=float)
    H = np.dot(h, np.exp(-1j * 2.0 * np.pi * f_hz * n / fs))
    return float(np.abs(H))


def windowed_sinc_bandpass(n_taps: int, f1_hz: float, f2_hz: float, fs: float, f_norm_hz: float) -> np.ndarray:
    h = windowed_sinc_lowpass(n_taps, f2_hz, fs) - windowed_sinc_lowpass(n_taps, f1_hz, fs)
    g = dtft_gain(h, f_norm_hz, fs)
    if g < 1e-12:
        raise ValueError("bandpass gain at probe is zero")
    return h / g


def windowed_sinc_bandstop(n_taps: int, f1_hz: float, f2_hz: float, fs: float) -> np.ndarray:
    m = (n_taps - 1) // 2
    delta = np.zeros(n_taps, dtype=float)
    delta[m] = 1.0
    h_bp = windowed_sinc_lowpass(n_taps, f2_hz, fs) - windowed_sinc_lowpass(n_taps, f1_hz, fs)
    g = dtft_gain(h_bp, 0.5 * (f1_hz + f2_hz), fs)
    if g < 1e-12:
        raise ValueError("bandstop complementary gain is zero")
    h_bp = h_bp / g
    return delta - h_bp


def _linear_phase(H_mag: np.ndarray) -> np.ndarray:
    n = len(H_mag)
    k = np.arange(n, dtype=float)
    return H_mag.astype(complex) * np.exp(-1j * np.pi * (n - 1) * k / n)


def frequency_sampling(n_taps: int, mag_of_hz, fs: float) -> np.ndarray:
    """IDFT of a conjugate-symmetric linear-phase desired magnitude."""
    k = np.arange(n_taps, dtype=float)
    f_hz = k * fs / n_taps
    f_folded = np.minimum(f_hz, fs - f_hz)
    mag = np.array([mag_of_hz(float(f)) for f in f_folded], dtype=float)
    mag = np.clip(mag, 0.0, 1.0)
    H = _linear_phase(mag)
    h = np.real(np.fft.ifft(H))
    return np.asarray(h, float)


def windowed_sinc_highpass(n_taps: int, fc_hz: float, fs: float) -> np.ndarray:
    """Type-I highpass via complementary lowpass, Nyquist-normalized."""
    m = (n_taps - 1) // 2
    delta = np.zeros(n_taps, dtype=float)
    delta[m] = 1.0
    h = delta - windowed_sinc_lowpass(n_taps, fc_hz, fs)
    g = dtft_gain(h, 0.5 * fs, fs)
    if g < 1e-12:
        raise ValueError("highpass gain at Nyquist is zero")
    return h / g


def mag_lowpass(f, f_pass, f_stop):
    if f <= f_pass:
        return 1.0
    if f >= f_stop:
        return 0.0
    return float((f_stop - f) / (f_stop - f_pass))


def mag_highpass(f, f_stop, f_pass):
    return 1.0 - mag_lowpass(f, f_stop, f_pass)


def mag_bandpass(f, f_s1, f_p1, f_p2, f_s2):
    if f <= f_s1 or f >= f_s2:
        return 0.0
    if f_p1 <= f <= f_p2:
        return 1.0
    if f_s1 < f < f_p1:
        return float((f - f_s1) / (f_p1 - f_s1))
    return float((f_s2 - f) / (f_s2 - f_p2))


def mag_bandstop(f, f_p1, f_s1, f_s2, f_p2):
    return 1.0 - mag_bandpass(f, f_p1, f_s1, f_s2, f_p2)
