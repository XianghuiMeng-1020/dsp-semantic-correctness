"""Stage B — independent specification verifier.

Does not import ``src.spec_checker`` or ``search_checker``.
Does not compute coefficient distance or consult a canonical designer.

Numerical certificate: dense-grid |H| plus local extremum refinement.
This is not a continuous-frequency proof.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy import optimize as sp_opt
from scipy import signal as sp_signal

from src.verification import VERIFIER_VERSION
from src.verification.canonicalize import canonicalize_fir, canonicalize_iir, unpack
from src.verification.registry_io import get_task, is_fir

FREQZ_N = 131072
NEAR_ABS = 1e-5
HIGHPREC_N = 16
EPS = 1e-18


@dataclass
class BandWorst:
    name: str
    f0: float
    f1: float
    lo: float
    hi: float
    worst_below: float
    worst_above: float
    f_min: float
    f_max: float
    n_grid: int


@dataclass
class VerifierResult:
    ok: bool
    family: str
    verifier: str = VERIFIER_VERSION
    freqz_n: int = FREQZ_N
    refined: bool = False
    high_precision: bool = False
    passband_error: float = 0.0
    stopband_error: float = 0.0
    stability_error: float = 0.0
    other_error: float = 0.0
    worst_pass_abs: float = 0.0
    worst_stop_abs: float = 0.0
    f_worst_pass: float | None = None
    f_worst_stop: float | None = None
    max_pole_radius: float | None = None
    stability_margin: float | None = None
    finite: bool = True
    numerical_failure: str | None = None
    near_boundary: bool = False
    normalization: dict = field(default_factory=dict)
    bands: list = field(default_factory=list)
    notes: list = field(default_factory=list)

    def as_dict(self) -> dict:
        return {
            "ok": bool(self.ok),
            "family": self.family,
            "verifier": self.verifier,
            "freqz_n": int(self.freqz_n),
            "refined": bool(self.refined),
            "high_precision": bool(self.high_precision),
            "passband_error": float(self.passband_error),
            "stopband_error": float(self.stopband_error),
            "stability_error": float(self.stability_error),
            "other_error": float(self.other_error),
            "worst_pass_abs": float(self.worst_pass_abs),
            "worst_stop_abs": float(self.worst_stop_abs),
            "f_worst_pass": self.f_worst_pass,
            "f_worst_stop": self.f_worst_stop,
            "max_pole_radius": self.max_pole_radius,
            "stability_margin": self.stability_margin,
            "finite": bool(self.finite),
            "numerical_failure": self.numerical_failure,
            "near_boundary": bool(self.near_boundary),
            "normalization": dict(self.normalization),
            "bands": list(self.bands),
            "notes": list(self.notes),
        }


def _empty_fail(family: str, reason: str) -> VerifierResult:
    r = VerifierResult(ok=False, family=family, numerical_failure=reason)
    r.passband_error = 1.0
    r.stopband_error = 1.0
    r.other_error = 1.0
    return r


def _mag_fir(b: np.ndarray, f_hz: np.ndarray, fs: float) -> np.ndarray:
    n = np.arange(len(b), dtype=float)
    phase = np.exp(-1j * 2.0 * np.pi * np.outer(f_hz, n) / fs)
    return np.abs(phase @ b)


def _mag_fir_scalar(b: np.ndarray, f_hz: float, fs: float) -> float:
    n = np.arange(len(b), dtype=float)
    H = np.dot(b, np.exp(-1j * 2.0 * np.pi * float(f_hz) * n / fs))
    return float(np.abs(H))


def _sos_mag_scalar(sos: np.ndarray, f_hz: float, fs: float) -> float:
    z = np.exp(1j * 2.0 * np.pi * float(f_hz) / fs)
    H = 1.0 + 0.0j
    for row in sos:
        b0, b1, b2, a0, a1, a2 = (float(x) for x in row)
        num = b0 * z * z + b1 * z + b2
        den = a0 * z * z + a1 * z + a2
        if abs(den) < EPS:
            return float("inf")
        H *= num / den
    return float(np.abs(H))


def _dense_mag(b, a, fs: float, n: int):
    if a is None:
        w, H = sp_signal.freqz(b, worN=n, fs=fs)
        return w, np.abs(H), None
    try:
        sos = sp_signal.tf2sos(b, a)
        w, H = sp_signal.sosfreqz(sos, worN=n, fs=fs)
        return w, np.abs(H), sos
    except Exception:
        w, H = sp_signal.freqz(b, a, worN=n, fs=fs)
        return w, np.abs(H), None


def _refine_extrema(mag_fn, f0, f1, f_grid, mag_grid):
    """Bracket grid min/max and refine with scalar search."""
    if len(f_grid) == 0:
        return None
    i_min = int(np.argmin(mag_grid))
    i_max = int(np.argmax(mag_grid))
    out = {}
    for kind, idx in (("min", i_min), ("max", i_max)):
        lo = float(f_grid[max(0, idx - 1)])
        hi = float(f_grid[min(len(f_grid) - 1, idx + 1)])
        lo = max(float(f0), lo)
        hi = min(float(f1), hi)
        f_star = float(f_grid[idx])
        m_star = float(mag_grid[idx])
        if hi > lo + 1e-15:
            def obj(f, sign=1.0 if kind == "min" else -1.0):
                return sign * mag_fn(float(f))

            try:
                res = sp_opt.minimize_scalar(obj, bounds=(lo, hi), method="bounded", options={"xatol": 1e-12})
                if res.success:
                    f_star = float(res.x)
                    m_star = float(mag_fn(f_star))
            except Exception:
                pass
        out[kind] = (f_star, m_star)
    return out


def _normalized_err(below: float, above: float, lo: float, hi: float) -> float:
    span = max(hi - lo, 1e-6)
    return float(max(below, above) / span)


def _verify_filter(task: dict, implementation, grid_n: int | None = None) -> VerifierResult:
    r = VerifierResult(ok=False, family="filter_specification")
    grid_n = int(grid_n or FREQZ_N)
    r.freqz_n = grid_n
    b, a = unpack(implementation)
    fs = float(task["sampling_rate"])
    floor = float(task["residual_floor"])
    pole_max = (task.get("constraints") or {}).get("pole_radius_max")

    if not np.all(np.isfinite(b)) or (a is not None and not np.all(np.isfinite(a))):
        r.finite = False
        r.passband_error = 1.0
        r.stopband_error = 1.0
        r.notes.append("nonfinite_coefficients")
        return r

    if is_fir(task) or a is None:
        cf = canonicalize_fir(b)
        r.normalization = {
            "kind": "fir",
            "n_taps": cf.n_taps,
            "type1": cf.type1,
            "dc_gain": cf.dc_gain,
            "order_constraint": task.get("order_constraint"),
            "phase_requirement": task.get("phase_requirement"),
            "trimmed_trailing": cf.trimmed_trailing,
        }
        b_use, a_use = cf.h, None
    else:
        ci = canonicalize_iir({"b": b, "a": a})
        r.normalization = {
            "kind": "iir",
            "n_b": int(len(ci.b)),
            "n_a": int(len(ci.a)),
            "a0_before": ci.a0_before,
            "max_pole_radius_canon": ci.max_pole_radius,
            "order_constraint": task.get("order_constraint"),
        }
        b_use, a_use = ci.b, ci.a
        if ci.max_pole_radius is not None:
            r.max_pole_radius = ci.max_pole_radius
            if pole_max is not None:
                r.stability_margin = float(float(pole_max) - ci.max_pole_radius)

    if pole_max is not None and a_use is not None:
        try:
            _z, p, _k = sp_signal.tf2zpk(b_use, a_use)
            rp = float(np.max(np.abs(p))) if len(p) else 0.0
            r.max_pole_radius = rp
            r.stability_margin = float(float(pole_max) - rp)
            if rp >= float(pole_max):
                r.stability_error = 1.0
        except Exception as exc:  # noqa: BLE001
            r.numerical_failure = f"stability:{type(exc).__name__}"
            r.stability_error = 1.0

    try:
        w, mag, sos = _dense_mag(b_use, a_use, fs, grid_n)
    except Exception as exc:  # noqa: BLE001
        r.numerical_failure = f"freqz:{type(exc).__name__}"
        r.passband_error = 1.0
        r.stopband_error = 1.0
        return r

    if a_use is None:
        mag_fn = lambda f: _mag_fir_scalar(b_use, f, fs)
    elif sos is not None:
        mag_fn = lambda f: _sos_mag_scalar(sos, f, fs)
    else:
        def mag_fn(f, _b=b_use, _a=a_use, _fs=fs):
            ww, HH = sp_signal.freqz(_b, _a, worN=np.array([2.0 * np.pi * f / _fs]))
            return float(np.abs(HH[0]))

    pass_err = 0.0
    stop_err = 0.0
    worst_pass_abs = 0.0
    worst_stop_abs = 0.0
    f_worst_pass = None
    f_worst_stop = None
    near = False
    refined = False

    bands = list(task["pass_band"]) + list(task["stop_band"])
    for band in bands:
        f0, f1 = float(band["f0"]), float(band["f1"])
        lo, hi = float(band["lo"]), float(band["hi"])
        mask = (w >= f0) & (w <= f1)
        if not np.any(mask):
            r.notes.append(f"empty_grid_band:{f0}-{f1}")
            pass_err = max(pass_err, 1.0)
            stop_err = max(stop_err, 1.0)
            continue
        fw, mw = w[mask], mag[mask]
        below = float(np.maximum(0.0, lo - mw).max())
        above = float(np.maximum(0.0, mw - hi).max())
        f_min = float(fw[int(np.argmin(mw))])
        f_max = float(fw[int(np.argmax(mw))])

        ext = _refine_extrema(mag_fn, f0, f1, fw, mw)
        if ext:
            refined = True
            fmin, mmin = ext["min"]
            fmax, mmax = ext["max"]
            below = max(below, max(0.0, lo - mmin))
            above = max(above, max(0.0, mmax - hi))
            f_min, f_max = fmin, fmax

        slack = max(hi - lo, 1e-6) * floor
        if below <= max(10.0 * slack, NEAR_ABS) or above <= max(10.0 * slack, NEAR_ABS):
            if below > 0.0 or above > 0.0 or min(np.min(mw) - lo, hi - np.max(mw)) < max(10.0 * slack, NEAR_ABS):
                near = True
                r.high_precision = True
                # denser local samples around current extrema
                for f_c in (f_min, f_max):
                    loc = np.linspace(max(f0, f_c - (f1 - f0) / grid_n * 8), min(f1, f_c + (f1 - f0) / grid_n * 8), HIGHPREC_N)
                    for f in loc:
                        m = mag_fn(float(f))
                        below = max(below, max(0.0, lo - m))
                        above = max(above, max(0.0, m - hi))

        nerr = _normalized_err(below, above, lo, hi)
        rec = {
            "f0": f0,
            "f1": f1,
            "lo": lo,
            "hi": hi,
            "worst_below": below,
            "worst_above": above,
            "f_min": f_min,
            "f_max": f_max,
            "n_grid": int(np.count_nonzero(mask)),
            "normalized_error": nerr,
            "role": "pass" if lo >= 0.5 else "stop",
        }
        r.bands.append(rec)
        if lo >= 0.5:
            pass_err = max(pass_err, nerr)
            if below + above >= worst_pass_abs:
                worst_pass_abs = below + above
                f_worst_pass = f_min if below >= above else f_max
        else:
            stop_err = max(stop_err, nerr)
            if below + above >= worst_stop_abs:
                worst_stop_abs = below + above
                f_worst_stop = f_min if below >= above else f_max

    r.passband_error = float(pass_err)
    r.stopband_error = float(stop_err)
    r.worst_pass_abs = float(worst_pass_abs)
    r.worst_stop_abs = float(worst_stop_abs)
    r.f_worst_pass = f_worst_pass
    r.f_worst_stop = f_worst_stop
    r.refined = refined
    r.near_boundary = near
    r.ok = (
        r.finite
        and pass_err <= floor
        and stop_err <= floor
        and r.stability_error <= 0.0
        and r.numerical_failure is None
    )
    return r


def _rel(y, ytrue, scale):
    return float(np.linalg.norm(np.asarray(y, float) - np.asarray(ytrue, float))) / max(
        float(np.linalg.norm(np.asarray(ytrue, float))), scale, EPS
    )


def _fold_alias_hz(f, fs_out):
    nyq = float(fs_out) / 2.0
    period = float(fs_out)
    f_mod = np.mod(float(f) + nyq, period) - nyq
    return float(abs(f_mod))


def _as_fn(implementation):
    if callable(implementation):
        return implementation
    if isinstance(implementation, dict) and callable(implementation.get("fn")):
        return implementation["fn"]
    if isinstance(implementation, dict) and "value" in implementation:
        return lambda *a, **k: implementation["value"]
    if isinstance(implementation, dict) and "h" in implementation:
        return lambda: np.asarray(implementation["h"], float)
    raise TypeError("implementation must be a callable or {fn|value|h}")


def _verify_singleton(task: dict, implementation) -> VerifierResult:
    """Independent reimplementation of Suite S identities. Not a wrap of spec_checker."""
    r = VerifierResult(ok=False, family="singleton_identity", freqz_n=0)
    tid = task["task_id"]
    floor = float(task["residual_floor"])
    tv = task["constraints"]["test_vector"]
    fn = _as_fn(implementation)
    err = 1.0
    try:
        if tid == "crosscorrelation_integer_delay":
            rng = np.random.default_rng(tv["seed"])
            x = rng.standard_normal(int(tv["N"]))
            L = int(tv["L"])
            y = np.roll(x, L)
            lhat = int(np.rint(float(fn(x, y))))
            err = 0.0 if ((lhat - L) % len(x) == 0) else 1.0
        elif tid == "circular_convolution_theorem":
            rng = np.random.default_rng(tv["seed"])
            x = rng.standard_normal(int(tv["N"]))
            h = rng.standard_normal(int(tv["N"]))
            y = np.asarray(fn(x, h), float)
            y_id = np.fft.ifft(np.fft.fft(x) * np.fft.fft(h)).real
            err = 1.0 if y.shape != y_id.shape else _rel(y, y_id, 1.0)
        elif tid == "linear_convolution_zero_padded_dft":
            rng = np.random.default_rng(tv["seed"])
            x = rng.standard_normal(int(tv["Nx"]))
            h = rng.standard_normal(int(tv["Nh"]))
            y = np.asarray(fn(x, h), float)
            y_id = np.convolve(x, h)
            err = 1.0 if y.shape != y_id.shape else _rel(y, y_id, 1.0)
        elif tid == "autocorrelation_lag0_energy":
            rng = np.random.default_rng(tv["seed"])
            x = rng.standard_normal(int(tv["N"])) + 0.5 * np.sin(
                2.0 * np.pi * 3 * np.arange(int(tv["N"])) / int(tv["N"])
            )
            rr = np.asarray(fn(x), float)
            mid = len(x) - 1
            if rr.ndim != 1 or len(rr) != 2 * len(x) - 1:
                err = 1.0
            else:
                et = float(np.sum(np.asarray(x, float) ** 2))
                err = abs(float(rr[mid]) - et) / max(abs(et), EPS)
        elif tid == "decimation_alias_frequency":
            f, fs, m = float(tv["f"]), float(tv["fs"]), int(tv["M"])
            y = float(np.asarray(fn(f, fs, m)).reshape(()))
            y_id = _fold_alias_hz(f, fs / m)
            err = abs(y - y_id) / max(abs(y_id), fs / (2.0 * m), EPS)
        elif tid == "digital_frequency_rescale":
            fh, fsi, fso = float(tv["f_hat"]), float(tv["fs_in"]), float(tv["fs_out"])
            y = float(np.asarray(fn(fh, fsi, fso)).reshape(()))
            y_id = fh * fsi / fso
            err = abs(y - y_id) / max(abs(y_id), 0.5, EPS)
        elif tid == "nyquist_hz":
            fs = float(tv["fs"])
            y = float(np.asarray(fn(fs)).reshape(()))
            err = 0.0 if abs(y - fs / 2.0) <= 1e-15 else 1.0
        elif tid == "integer_delay_impulse":
            n, d = int(tv["N"]), int(tv["D"])
            h = np.asarray(fn(), float).reshape(-1)
            h_id = np.zeros(n)
            h_id[d] = 1.0
            err = 0.0 if h.shape == h_id.shape and np.array_equal(h, h_id) else 1.0
        else:
            r.numerical_failure = f"unknown_singleton:{tid}"
            r.other_error = 1.0
            return r
    except Exception as exc:  # noqa: BLE001
        r.numerical_failure = f"singleton:{type(exc).__name__}"
        r.other_error = 1.0
        return r
    r.other_error = float(err)
    r.ok = err <= floor and r.numerical_failure is None
    r.normalization = {"kind": "singleton", "task_id": tid}
    return r


def verify_specification(task_id: str, implementation, grid_n: int | None = None) -> VerifierResult:
    task = get_task(task_id)
    if task["family"] == "filter_specification":
        return _verify_filter(task, implementation, grid_n=grid_n)
    if task["family"] == "singleton_identity":
        return _verify_singleton(task, implementation)
    return _empty_fail("unknown", f"unsupported family {task.get('family')}")


def verify_ok(task_id: str, implementation, grid_n: int | None = None) -> bool:
    return bool(verify_specification(task_id, implementation, grid_n=grid_n).ok)
