"""Phase-2A FIR certifier: squared-magnitude polynomial sign.

Does not import spec_checker, search_checker, independent_spec_verifier,
or fir_adaptive. Reads registry JSON and raw taps only.
"""
from __future__ import annotations

import json
import math
import time
from fractions import Fraction
from pathlib import Path

import numpy as np
from mpmath import mp

ROOT = Path(__file__).resolve().parents[2]
MP_DPS = 80
COS_BITS = 72
MAX_BERNSTEIN_NODES = 2500
MAX_DEPTH = 36
MAX_SECONDS_PER_SIGN = 25.0
WITNESS_N = 1021  # prime; not 4096 or 131072 or 10007


def _load_task(task_id: str) -> dict:
    for name in ("suite_n.json", "suite_s.json"):
        payload = json.loads((ROOT / "registry" / name).read_text(encoding="utf-8"))
        for t in payload["tasks"]:
            if t["task_id"] == task_id:
                return t
    raise KeyError(task_id)


def _as_fir_taps(impl) -> np.ndarray:
    if isinstance(impl, dict):
        if impl.get("a") is not None and np.asarray(impl["a"]).size > 1:
            raise ValueError("IIR not supported")
        return np.asarray(impl.get("b", impl.get("h")), dtype=np.float64).reshape(-1)
    return np.asarray(impl, dtype=np.float64).reshape(-1)


def f64_frac(x: float) -> Fraction:
    return Fraction(*float(x).as_integer_ratio())


def _chebyshev_monomials(max_k: int) -> list[list[Fraction]]:
    """T_k as monomial lists, low degree first."""
    T: list[list[Fraction]] = []
    T.append([Fraction(1)])
    if max_k >= 1:
        T.append([Fraction(0), Fraction(1)])
    for k in range(2, max_k + 1):
        # T_k = 2x T_{k-1} - T_{k-2}
        prev = T[k - 1]
        twice = [Fraction(0)] + [2 * c for c in prev]
        older = T[k - 2] + [Fraction(0)] * (len(twice) - len(T[k - 2]))
        twice.extend([Fraction(0)] * (len(older) - len(twice)))
        T.append([a - b for a, b in zip(twice, older)])
    return T


def power_polynomial(h: np.ndarray) -> list[Fraction]:
    """Monomial coefficients of P(x)=|H|^2, x=cos ω, exact from binary64 taps."""
    hf = [f64_frac(float(v)) for v in h]
    n = len(hf)
    c = []
    for k in range(n):
        s = Fraction(0)
        for i in range(n - k):
            s += hf[i] * hf[i + k]
        c.append(s)
    T = _chebyshev_monomials(n - 1)
    deg = n - 1
    mono = [Fraction(0)] * (deg + 1)
    for j, coeff in enumerate(T[0]):
        mono[j] += c[0] * coeff
    for k in range(1, n):
        for j, coeff in enumerate(T[k]):
            mono[j] += 2 * c[k] * coeff
    return mono


def _poly_eval(mono: list[Fraction], x: Fraction) -> Fraction:
    acc = Fraction(0)
    for c in reversed(mono):
        acc = acc * x + c
    return acc


def _compose_affine(mono: list[Fraction], a: Fraction, width: Fraction) -> list[Fraction]:
    """Q(a + width * t) as monomials in t."""
    # Horner accumulation of powers of (a + w t)
    out = [Fraction(0)] * len(mono)
    # out = ... ((c_n) * (a+wt) + c_{n-1}) * (a+wt) + ...
    acc = [Fraction(0)]
    for c in reversed(mono):
        # acc = acc * (a + w t) + c
        new = [Fraction(0)] * (len(acc) + 1)
        for i, v in enumerate(acc):
            new[i] += v * a
            new[i + 1] += v * width
        new[0] += c
        acc = new
    return acc


def _binom(n: int, k: int) -> int:
    return math.comb(n, k)


def monomial_to_bernstein(a: list[Fraction]) -> list[Fraction]:
    n = len(a) - 1
    beta = []
    for j in range(n + 1):
        s = Fraction(0)
        cj = _binom(n, j)
        if cj == 0:
            beta.append(s)
            continue
        for k in range(j + 1):
            s += Fraction(_binom(j, k), _binom(n, k)) * a[k]
        beta.append(s)
    return beta


def _mpf_to_outer_frac(y) -> tuple[Fraction, Fraction]:
    scale = Fraction(1, 1 << COS_BITS)
    yf = Fraction(int(mp.nint(y * (1 << COS_BITS))), 1 << COS_BITS)
    return yf - 4 * scale, yf + 4 * scale


def enclose_cos_omega(f: float, fs: float) -> tuple[Fraction, Fraction]:
    """Outward Fraction enclosure of cos(2π f / fs)."""
    fr, fsr = f64_frac(f), f64_frac(fs)
    if fr == 0:
        return Fraction(1), Fraction(1)
    if 2 * fr == fsr:
        return Fraction(-1), Fraction(-1)
    mp.dps = MP_DPS
    w = 2 * mp.pi * mp.mpf(fr.numerator) / mp.mpf(fr.denominator)
    w /= mp.mpf(fsr.numerator) / mp.mpf(fsr.denominator)
    # enlarge ω by a few ulps of the computed value
    w_lo, w_hi = w * (1 - mp.mpf(2) ** (-70)), w * (1 + mp.mpf(2) ** (-70))
    if w < 0:
        w_lo, w_hi = w_hi, w_lo
    c1 = mp.cos(w_lo)
    c2 = mp.cos(w_hi)
    lo1, hi1 = _mpf_to_outer_frac(c1)
    lo2, hi2 = _mpf_to_outer_frac(c2)
    return min(lo1, lo2), max(hi1, hi2)


def band_x_enclosures(f0: float, f1: float, fs: float) -> dict:
    """x=cos ω on ω=2πf/fs for f in [f0,f1] ⊆ [0, Nyquist]. cos decreasing on [0,π]."""
    a0, b0 = enclose_cos_omega(f0, fs)
    a1, b1 = enclose_cos_omega(f1, fs)
    # image of [ω0,ω1] under decreasing cos: [cos ω1, cos ω0]
    outer_lo, outer_hi = a1, b0
    inner_lo, inner_hi = b1, a0
    if outer_lo > outer_hi:
        outer_lo, outer_hi = outer_hi, outer_lo
    if inner_lo > inner_hi:
        inner_lo, inner_hi = inner_hi, inner_lo
    # keep inner inside outer
    inner_lo = max(inner_lo, outer_lo)
    inner_hi = min(inner_hi, outer_hi)
    return {
        "outer": (outer_lo, outer_hi),
        "inner": (inner_lo, inner_hi),
        "usable_inner": inner_lo < inner_hi,
    }


def _bernstein_sign(beta: list[Fraction]) -> str:
    pos = any(b > 0 for b in beta)
    neg = any(b < 0 for b in beta)
    if pos and not neg:
        return "nonneg"
    if neg and not pos:
        return "nonpos"
    if not pos and not neg:
        return "zero"
    return "mixed"


def certify_q_nonpositive(mono: list[Fraction], a: Fraction, b: Fraction) -> dict:
    """CERTIFIED Q<=0 / Q>=0 / mixed / undecided on [a,b] via Bernstein subdivision."""
    return _certify_sign(mono, a, b, want="nonpos")


def certify_q_nonnegative(mono: list[Fraction], a: Fraction, b: Fraction) -> dict:
    return _certify_sign(mono, a, b, want="nonneg")


def _certify_sign(mono: list[Fraction], a: Fraction, b: Fraction, want: str) -> dict:
    if b < a:
        a, b = b, a
    if a == b:
        v = _poly_eval(mono, a)
        if want == "nonpos" and v <= 0:
            return {"status": "CERTIFIED", "reason": "point_ok", "nodes": 1}
        if want == "nonneg" and v >= 0:
            return {"status": "CERTIFIED", "reason": "point_ok", "nodes": 1}
        if (want == "nonpos" and v > 0) or (want == "nonneg" and v < 0):
            return {"status": "REFUTED", "reason": "point_violation", "x": str(a), "nodes": 1}
        return {"status": "UNDECIDED", "reason": "point_ambiguous", "nodes": 1}

    stack = [(a, b, 0)]
    nodes = 0
    t0 = time.time()
    while stack:
        lo, hi, depth = stack.pop()
        nodes += 1
        if nodes > MAX_BERNSTEIN_NODES or (time.time() - t0) > MAX_SECONDS_PER_SIGN:
            return {"status": "UNDECIDED", "reason": "polynomial_arithmetic_resource_limit", "nodes": nodes}
        width = hi - lo
        aff = _compose_affine(mono, lo, width)
        beta = monomial_to_bernstein(aff)
        sg = _bernstein_sign(beta)
        if sg == "zero":
            continue
        if want == "nonpos" and sg == "nonpos":
            continue
        if want == "nonneg" and sg == "nonneg":
            continue
        if want == "nonpos" and sg == "nonneg" and all(v > 0 for v in beta):
            return {"status": "REFUTED", "reason": "bernstein_strict_positive", "nodes": nodes, "interval": [str(lo), str(hi)]}
        if want == "nonneg" and sg == "nonpos" and all(v < 0 for v in beta):
            return {"status": "REFUTED", "reason": "bernstein_strict_negative", "nodes": nodes, "interval": [str(lo), str(hi)]}
        if depth >= MAX_DEPTH:
            return {"status": "UNDECIDED", "reason": "root_isolation_or_depth_limit", "nodes": nodes}
        mid = (lo + hi) / 2
        stack.append((lo, mid, depth + 1))
        stack.append((mid, hi, depth + 1))
    return {"status": "CERTIFIED", "reason": "bernstein_sign", "nodes": nodes}


def _witness_invalid(h: np.ndarray, f0: float, f1: float, fs: float, L: Fraction, U: Fraction) -> dict | None:
    """Independent prime-grid witness on |H| vs [L,U]. Conservative (needs clear violation)."""
    freqs = np.linspace(f0, f1, WITNESS_N)
    n = np.arange(len(h), dtype=np.float64)
    omegas = 2.0 * math.pi * freqs / fs
    H = np.exp(-1j * np.outer(omegas, n)) @ h
    mag = np.abs(H)
    s = float(np.sum(np.abs(h)))
    err_h = 8.0 * (len(h) + 1) * float(np.finfo(np.float64).eps) * (s + 1.0)
    Lf, Uf = float(L), float(U)
    below = (L > 0) and (mag + err_h < Lf)
    above = mag - err_h > Uf
    hit = np.where(below | above)[0]
    if hit.size == 0:
        return None
    k = int(hit[0])
    return {
        "f_hz": float(freqs[k]),
        "mag": float(mag[k]),
        "L": Lf,
        "U": Uf,
        "grid": "independent_prime_1021",
    }


def _eff_bounds(lo: float, hi: float, floor: float) -> tuple[Fraction, Fraction]:
    span = max(hi - lo, 1e-6)
    L = lo - floor * span
    U = hi + floor * span
    return f64_frac(L), f64_frac(U)


def certify_fir(task_id: str, impl) -> dict:
    task = _load_task(task_id)
    if not str(task.get("type", "")).startswith("fir_"):
        return {
            "status": "UNDECIDED",
            "reason": "not_fir_mask",
            "task_id": task_id,
            "method": "power_polynomial_bernstein",
        }
    h = _as_fir_taps(impl)
    if not np.all(np.isfinite(h)):
        return {"status": "CERTIFIED_INVALID", "reason": "nonfinite", "task_id": task_id}
    fs = float(task["sampling_rate"])
    floor = float(task["residual_floor"])
    mono = power_polynomial(h)
    bands = list(task["pass_band"]) + list(task["stop_band"])
    details = []
    min_nodes = 0

    for band in bands:
        f0, f1 = float(band["f0"]), float(band["f1"])
        lo, hi = float(band["lo"]), float(band["hi"])
        L, U = _eff_bounds(lo, hi, floor)
        # Frozen spec: |H|>=L. If L<=0 the lower bound is vacuous (do NOT use P>=L^2).
        L2 = L * L if L > 0 else Fraction(0)
        U2 = U * U if U >= 0 else Fraction(0)
        wit = _witness_invalid(h, f0, f1, fs, L if L > 0 else Fraction(0), U)
        if wit is not None:
            return {
                "status": "CERTIFIED_INVALID",
                "reason": "witnessed_violation",
                "task_id": task_id,
                "n_taps": int(len(h)),
                "degree": len(mono) - 1,
                "witness": wit,
                "method": "power_polynomial_bernstein",
                "arithmetic": "exact_binary64_rationals_plus_witness_grid",
            }
        enc = band_x_enclosures(f0, f1, fs)
        q_upper = [c for c in mono]
        q_upper[0] = q_upper[0] - U2
        q_lower = [c for c in mono]
        q_lower[0] = q_lower[0] - L2
        outer_a, outer_b = enc["outer"]
        # VALID: Q_upper<=0 always; Q_lower>=0 only if L>0 (else vacuous).
        # Use the INNER x-interval as a subset certificate, then the two
        # endpoint slivers. A full-band valid certificate requires all pieces.
        inner_ok = enc["usable_inner"]
        ia, ib = enc["inner"] if inner_ok else (outer_a, outer_b)
        up = certify_q_nonpositive(q_upper, ia, ib)
        if L > 0:
            low = certify_q_nonnegative(q_lower, ia, ib)
        else:
            low = {"status": "CERTIFIED", "reason": "lower_vacuous_L_nonpositive", "nodes": 0}
        min_nodes += up.get("nodes", 0) + low.get("nodes", 0)
        details.append(
            {
                "f0": f0,
                "f1": f1,
                "L": str(L),
                "U": str(U),
                "upper": {k: up[k] for k in up if k != "interval"},
                "lower": {k: low[k] for k in low if k != "interval"},
            }
        )
        if up["status"] == "REFUTED" or low["status"] == "REFUTED":
            return {
                "status": "CERTIFIED_INVALID",
                "reason": "polynomial_sign_crossing_inner",
                "task_id": task_id,
                "n_taps": int(len(h)),
                "degree": len(mono) - 1,
                "band": details[-1],
                "method": "power_polynomial_bernstein",
                "arithmetic": "exact_binary64_rationals_bernstein",
            }
        if up["status"] != "CERTIFIED" or low["status"] != "CERTIFIED":
            reason = up.get("reason") if up["status"] != "CERTIFIED" else low.get("reason")
            return {
                "status": "UNDECIDED",
                "reason": reason or "sign_unresolved",
                "task_id": task_id,
                "n_taps": int(len(h)),
                "degree": len(mono) - 1,
                "bands": details,
                "method": "power_polynomial_bernstein",
                "arithmetic": "exact_binary64_rationals_bernstein",
            }
        # Endpoint slivers: outer\\inner. Must not be left uncertified.
        slivers = []
        if inner_ok:
            if outer_a < ia:
                slivers.append((outer_a, ia))
            if ib < outer_b:
                slivers.append((ib, outer_b))
        for sa, sb in slivers:
            su = certify_q_nonpositive(q_upper, sa, sb)
            sl = (
                certify_q_nonnegative(q_lower, sa, sb)
                if L > 0
                else {"status": "CERTIFIED", "reason": "lower_vacuous_L_nonpositive", "nodes": 0}
            )
            min_nodes += su.get("nodes", 0) + sl.get("nodes", 0)
            if su["status"] == "REFUTED" or sl["status"] == "REFUTED":
                return {
                    "status": "UNDECIDED",
                    "reason": "endpoint_enclosure_limitation",
                    "task_id": task_id,
                    "n_taps": int(len(h)),
                    "degree": len(mono) - 1,
                    "bands": details,
                    "method": "power_polynomial_bernstein",
                    "arithmetic": "exact_binary64_rationals_bernstein",
                }
            if su["status"] != "CERTIFIED" or sl["status"] != "CERTIFIED":
                return {
                    "status": "UNDECIDED",
                    "reason": "endpoint_enclosure_limitation",
                    "task_id": task_id,
                    "n_taps": int(len(h)),
                    "degree": len(mono) - 1,
                    "bands": details,
                    "method": "power_polynomial_bernstein",
                    "arithmetic": "exact_binary64_rationals_bernstein",
                }

    return {
        "status": "CERTIFIED_VALID",
        "reason": "all_bands_polynomial_sign",
        "task_id": task_id,
        "n_taps": int(len(h)),
        "degree": len(mono) - 1,
        "bernstein_nodes": min_nodes,
        "bands": details,
        "method": "power_polynomial_bernstein",
        "arithmetic": "exact_binary64_rationals_bernstein",
    }
