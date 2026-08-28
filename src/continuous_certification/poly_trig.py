"""Squared-magnitude cosine polynomial from stored real taps.

Independent of fir_power_polynomial.py. Same mathematical object P(x)=|H|^2,
own implementation. Taps are exact binary64 rationals.
"""
from __future__ import annotations

import math
from fractions import Fraction

import numpy as np
from mpmath import mp

MP_DPS = 80
COS_BITS = 80


def f64_frac(x: float) -> Fraction:
    return Fraction(*float(x).as_integer_ratio())


def chebyshev_monomials_int(max_k: int) -> list[list[int]]:
    """T_k have integer monomial coefficients."""
    T: list[list[int]] = [[1]]
    if max_k >= 1:
        T.append([0, 1])
    for _k in range(2, max_k + 1):
        prev = T[-1]
        twice = [0] + [2 * c for c in prev]
        older = T[-2] + [0] * (len(twice) - len(T[-2]))
        twice.extend([0] * (len(older) - len(twice)))
        T.append([a - b for a, b in zip(twice, older)])
    return T


def _lcm_int(a: int, b: int) -> int:
    return a * b // math.gcd(a, b) if a and b else 0


def power_from_taps(h) -> list[Fraction]:
    """P(x)=c0 + 2 sum_k ck T_k(x), ck = sum_n h_n h_{n+k}."""
    hf = [f64_frac(float(v)) for v in np.asarray(h, dtype=np.float64).reshape(-1)]
    n = len(hf)
    c = []
    for k in range(n):
        s = Fraction(0)
        for i in range(n - k):
            s += hf[i] * hf[i + k]
        c.append(s)
    T = chebyshev_monomials_int(n - 1)
    den = 1
    for ck in c:
        den = _lcm_int(den, ck.denominator)
    mono_int = [0] * n
    for j, coeff in enumerate(T[0]):
        mono_int[j] += (c[0].numerator * (den // c[0].denominator)) * coeff
    for k in range(1, n):
        ck_int = c[k].numerator * (den // c[k].denominator)
        for j, coeff in enumerate(T[k]):
            mono_int[j] += 2 * ck_int * coeff
    return [Fraction(v, den) for v in mono_int]


def _mpf_to_outer_frac(y) -> tuple[Fraction, Fraction]:
    scale = Fraction(1, 1 << COS_BITS)
    yf = Fraction(int(mp.nint(y * (1 << COS_BITS))), 1 << COS_BITS)
    return yf - 8 * scale, yf + 8 * scale


def enclose_cos_omega(f: float, fs: float) -> tuple[Fraction, Fraction]:
    fr, fsr = f64_frac(f), f64_frac(fs)
    if fr == 0:
        return Fraction(1), Fraction(1)
    if 2 * fr == fsr:
        return Fraction(-1), Fraction(-1)
    mp.dps = MP_DPS
    w = 2 * mp.pi * mp.mpf(fr.numerator) / mp.mpf(fr.denominator)
    w /= mp.mpf(fsr.numerator) / mp.mpf(fsr.denominator)
    w_lo, w_hi = w * (1 - mp.mpf(2) ** (-72)), w * (1 + mp.mpf(2) ** (-72))
    if w < 0:
        w_lo, w_hi = w_hi, w_lo
    c1, c2 = mp.cos(w_lo), mp.cos(w_hi)
    lo1, hi1 = _mpf_to_outer_frac(c1)
    lo2, hi2 = _mpf_to_outer_frac(c2)
    return min(lo1, lo2), max(hi1, hi2)


def band_x_outer(f0: float, f1: float, fs: float) -> tuple[Fraction, Fraction]:
    """Outward x=cos ω enclosure of the closed frequency band. cos decreasing on [0,π]."""
    a0, b0 = enclose_cos_omega(f0, fs)
    a1, b1 = enclose_cos_omega(f1, fs)
    lo, hi = a1, b0
    if lo > hi:
        lo, hi = hi, lo
    return lo, hi


def poly_sub_const(p: list[Fraction], c: Fraction) -> list[Fraction]:
    q = list(p)
    q[0] = q[0] - c
    return q


def poly_sub_scaled(p: list[Fraction], s: Fraction, q: list[Fraction]) -> list[Fraction]:
    n = max(len(p), len(q))
    out = [Fraction(0)] * n
    for i, a in enumerate(p):
        out[i] += a
    for i, b in enumerate(q):
        out[i] -= s * b
    return out
