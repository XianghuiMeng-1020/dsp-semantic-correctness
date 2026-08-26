"""Explicit representation-equivalence rules.

These rules remove trivial encodings before confirmatory coefficient
distance. They do not change specification membership.

Rules (all explicit):

FIR
  R1. Finite real coefficients; drop a trivial FIR denominator ``a=[1]``.
  R2. Trim accidental trailing numerical zeros (|c| < TRIM_ABS).
      Leading zeros are *not* stripped: they are a delay, recorded as a flag.
  R3. Length after R2 is the recorded FIR length. Zero-padding an already
      trimmed vector is a representation artifact (same polynomial).
  R4. Coefficient orientation is left-to-right, index 0 = first tap.
  R5. Global scale is semantically relevant for Suite N magnitude masks
      (pass/stop bounds are absolute). Scale is *detected* as a flag,
      never removed for confirmatory distance.
  R6. Sign flip leaves |H| unchanged. For magnitude-only tasks, a pure
      sign flip is an equivalence class, not a distinct realization.
  R7. Type-I symmetry is detected; breaking it is a structural change.

IIR
  R8. Require a[0] != 0 and divide (b,a) by a[0] so a0=1.
      Therefore (b,a) and (c b, c a) compare equal.
  R9. Trim trailing numerical zeros on b and on a (after a0=1), never
      dropping a[0].
  R10. Unequal-order truncation is NOT a confirmatory distance. Extra
       true-zero coefficients are padding; extra nonzero coefficients
       are a different polynomial.

Historical min-length truncation remains available only as
``d_coeff_historical`` in ``distances.py``.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

TRIM_ABS = 1e-14
EPS = 1e-18


def _as_1d(x) -> np.ndarray:
    return np.asarray(x, float).reshape(-1)


def unpack(impl):
    if isinstance(impl, dict) and "b" in impl:
        b = _as_1d(impl["b"])
        a = impl.get("a")
        a = None if a is None else _as_1d(a)
        return b, a
    if isinstance(impl, (tuple, list)) and len(impl) == 2:
        b = _as_1d(impl[0])
        a = _as_1d(impl[1])
        if a.size == 1 and abs(float(a[0]) - 1.0) <= 1e-12:
            return b, None
        return b, a
    return _as_1d(impl), None


def _trim_trailing(v: np.ndarray, keep_min: int = 1) -> np.ndarray:
    v = _as_1d(v)
    last = len(v) - 1
    while last >= keep_min and abs(float(v[last])) < TRIM_ABS:
        last -= 1
    return v[: last + 1].copy()


def _n_leading_zeros(v: np.ndarray) -> int:
    n = 0
    for x in v:
        if abs(float(x)) < TRIM_ABS:
            n += 1
        else:
            break
    return n


@dataclass
class CanonicalFIR:
    h: np.ndarray
    n_taps: int
    n_leading_zeros: int
    trimmed_trailing: int
    type1: bool
    first_nonzero_sign: float
    dc_gain: float
    notes: list[str] = field(default_factory=list)


@dataclass
class CanonicalIIR:
    b: np.ndarray
    a: np.ndarray
    a0_before: float
    max_pole_radius: float | None
    notes: list[str] = field(default_factory=list)


def is_type1(h: np.ndarray, atol: float = 1e-8) -> bool:
    h = _as_1d(h)
    if len(h) < 3 or len(h) % 2 == 0:
        return False
    return bool(np.allclose(h, h[::-1], atol=atol))


def canonicalize_fir(impl) -> CanonicalFIR:
    b, a = unpack(impl)
    notes = []
    if a is not None:
        if len(a) == 1 and abs(float(a[0]) - 1.0) <= 1e-12:
            notes.append("dropped_trivial_a")
        else:
            notes.append("nontrivial_a_on_fir_treated_as_numerator_only")
    raw_len = len(b)
    h = _as_1d(b).copy()
    # Do not strip a single trailing tap from an odd-length symmetric FIR:
    # that destroys Type I. Unpaired trailing zeros (asymmetric padding)
    # are still removed.
    if len(h) >= 3 and len(h) % 2 == 1 and np.allclose(h, h[::-1], atol=1e-8):
        notes.append("type1_endpoints_preserved")
    else:
        h = _trim_trailing(h, keep_min=1)
    n_lead = _n_leading_zeros(h)
    if n_lead:
        notes.append("leading_zeros_retained_as_delay")
    nz = h[np.abs(h) >= TRIM_ABS]
    sign = float(np.sign(nz[0])) if len(nz) else 0.0
    return CanonicalFIR(
        h=h,
        n_taps=int(len(h)),
        n_leading_zeros=int(n_lead),
        trimmed_trailing=int(raw_len - len(h)),
        type1=is_type1(h),
        first_nonzero_sign=sign,
        dc_gain=float(np.sum(h)),
        notes=notes,
    )


def canonicalize_iir(impl) -> CanonicalIIR:
    b, a = unpack(impl)
    notes = []
    if a is None:
        a = np.ones(1, float)
        notes.append("fir_promoted_to_iir_a0_1")
    b = _as_1d(b)
    a = _as_1d(a)
    if not np.all(np.isfinite(b)) or not np.all(np.isfinite(a)):
        notes.append("nonfinite")
        return CanonicalIIR(b=b, a=a, a0_before=float("nan"), max_pole_radius=None, notes=notes)
    a0 = float(a[0])
    if abs(a0) < EPS:
        notes.append("a0_near_zero")
        return CanonicalIIR(b=b, a=a, a0_before=a0, max_pole_radius=None, notes=notes)
    if abs(a0 - 1.0) > 1e-15:
        b = b / a0
        a = a / a0
        notes.append("scaled_a0_to_1")
    b = _trim_trailing(b, keep_min=1)
    a = _trim_trailing(a, keep_min=1)
    a[0] = 1.0
    max_p = None
    try:
        from scipy import signal as sp_signal

        _z, p, _k = sp_signal.tf2zpk(b, a)
        max_p = float(np.max(np.abs(p))) if len(p) else 0.0
    except Exception as exc:  # noqa: BLE001
        notes.append(f"pole_radius_failed:{type(exc).__name__}")
    return CanonicalIIR(b=b, a=a, a0_before=a0, max_pole_radius=max_p, notes=notes)


def fir_same_polynomial(h1: np.ndarray, h2: np.ndarray, atol: float = 1e-12) -> bool:
    """True if trimmed FIR polynomials are identical (no sign/scale)."""
    a = _trim_trailing(_as_1d(h1))
    b = _trim_trailing(_as_1d(h2))
    n = max(len(a), len(b))
    aa = np.zeros(n)
    bb = np.zeros(n)
    aa[: len(a)] = a
    bb[: len(b)] = b
    return bool(np.allclose(aa, bb, atol=atol, rtol=0.0))


def fir_sign_equivalent(h1: np.ndarray, h2: np.ndarray, atol: float = 1e-12) -> bool:
    return fir_same_polynomial(h1, h2, atol=atol) or fir_same_polynomial(h1, -np.asarray(h2, float), atol=atol)


def iir_same_tf(b1, a1, b2, a2, atol: float = 1e-12) -> bool:
    c1 = canonicalize_iir({"b": b1, "a": a1})
    c2 = canonicalize_iir({"b": b2, "a": a2})
    nb = max(len(c1.b), len(c2.b))
    na = max(len(c1.a), len(c2.a))
    B1, B2 = np.zeros(nb), np.zeros(nb)
    A1, A2 = np.zeros(na), np.zeros(na)
    B1[: len(c1.b)] = c1.b
    B2[: len(c2.b)] = c2.b
    A1[: len(c1.a)] = c1.a
    A2[: len(c2.a)] = c2.a
    return bool(np.allclose(B1, B2, atol=atol) and np.allclose(A1, A2, atol=atol))


def metadata_fir(c: CanonicalFIR) -> dict:
    return {
        "n_taps": c.n_taps,
        "n_leading_zeros": c.n_leading_zeros,
        "trimmed_trailing": c.trimmed_trailing,
        "type1": c.type1,
        "first_nonzero_sign": c.first_nonzero_sign,
        "dc_gain": c.dc_gain,
        "notes": list(c.notes),
    }


def metadata_iir(c: CanonicalIIR) -> dict:
    return {
        "n_b": int(len(c.b)),
        "n_a": int(len(c.a)),
        "a0_before": c.a0_before,
        "max_pole_radius": c.max_pole_radius,
        "notes": list(c.notes),
    }
