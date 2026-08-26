"""Specification membership checker.

S_t(h) = 1 iff the implementation satisfies the registered specification.
Does not compute coefficient distance, does not load a canonical designer,
does not call Oracle A/B, and does not run the tone battery T.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy import signal as sp_signal

ROOT = Path(__file__).resolve().parents[1]
EPS = 1e-18
FREQZ_N = 4096
POLE_RADIUS_MAX = 0.999

_REG = None


def load_registries():
    global _REG
    if _REG is not None:
        return _REG
    tasks = {}
    for name in ("suite_s.json", "suite_n.json"):
        payload = json.loads((ROOT / "registry" / name).read_text(encoding="utf-8"))
        for t in payload["tasks"]:
            tasks[t["task_id"]] = t
            legacy = t.get("legacy_arm_n_id")
            if legacy:
                tasks[legacy] = t
    _REG = tasks
    return tasks


def get_task(task_id: str) -> dict:
    tasks = load_registries()
    if task_id not in tasks:
        raise KeyError(f"unknown task_id: {task_id}")
    return tasks[task_id]


def _empty_residuals():
    return {
        "passband_error": 0.0,
        "stopband_error": 0.0,
        "stability_error": 0.0,
        "other_constraints": 0.0,
    }


def _result(ok: bool, residuals: dict) -> dict:
    return {"pass": bool(ok), "residuals": residuals}


def _unpack_filter(implementation):
    if isinstance(implementation, dict) and "b" in implementation:
        b = np.asarray(implementation["b"], float).reshape(-1)
        a = implementation.get("a")
        a = None if a is None else np.asarray(a, float).reshape(-1)
        return b, a
    if isinstance(implementation, (tuple, list)) and len(implementation) == 2:
        return (
            np.asarray(implementation[0], float).reshape(-1),
            np.asarray(implementation[1], float).reshape(-1),
        )
    return np.asarray(implementation, float).reshape(-1), None


def _band_errors(b, a, bands, fs):
    if a is None:
        w, H = sp_signal.freqz(b, worN=FREQZ_N, fs=fs)
    else:
        w, H = sp_signal.freqz(b, a, worN=FREQZ_N, fs=fs)
    mag = np.abs(H)
    pass_err = 0.0
    stop_err = 0.0
    for band in bands:
        mask = (w >= band["f0"]) & (w <= band["f1"])
        if not np.any(mask):
            return 1.0, 1.0
        m = mag[mask]
        lo, hi = band["lo"], band["hi"]
        below = np.maximum(0.0, lo - m)
        above = np.maximum(0.0, m - hi)
        span = max(hi - lo, 1e-6)
        err = float(max(np.max(below) / span, np.max(above) / span))
        if lo >= 0.5:
            pass_err = max(pass_err, err)
        else:
            stop_err = max(stop_err, err)
    return pass_err, stop_err


def _stability_error(b, a, pole_max):
    if a is None:
        return 0.0
    _z, p, _k = sp_signal.tf2zpk(b, a)
    if np.any(np.abs(p) >= pole_max):
        return 1.0
    return 0.0


def _check_filter(task, implementation) -> dict:
    b, a = _unpack_filter(implementation)
    fs = float(task["sampling_rate"])
    floor = float(task["residual_floor"])
    pole_max = (task.get("constraints") or {}).get("pole_radius_max")
    pass_err, stop_err = _band_errors(b, a, task["pass_band"] + task["stop_band"], fs)
    stab = 0.0
    if pole_max is not None:
        stab = _stability_error(b, a, float(pole_max))
    if not np.all(np.isfinite(b)) or (a is not None and not np.all(np.isfinite(a))):
        pass_err = max(pass_err, 1.0)
        stop_err = max(stop_err, 1.0)
    residuals = _empty_residuals()
    residuals["passband_error"] = pass_err
    residuals["stopband_error"] = stop_err
    residuals["stability_error"] = stab
    ok = pass_err <= floor and stop_err <= floor and stab <= 0.0
    return _result(ok, residuals)


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


def _check_singleton(task, implementation) -> dict:
    tid = task["task_id"]
    floor = float(task["residual_floor"])
    tv = task["constraints"]["test_vector"]
    residuals = _empty_residuals()
    fn = _as_fn(implementation)

    if tid == "crosscorrelation_integer_delay":
        rng = np.random.default_rng(tv["seed"])
        x = rng.standard_normal(int(tv["N"]))
        L = int(tv["L"])
        y = np.roll(x, L)
        lhat = int(np.rint(float(fn(x, y))))
        err = 0.0 if ((lhat - L) % len(x) == 0) else 1.0
        residuals["other_constraints"] = err
        return _result(err <= floor, residuals)

    if tid == "circular_convolution_theorem":
        rng = np.random.default_rng(tv["seed"])
        x = rng.standard_normal(int(tv["N"]))
        h = rng.standard_normal(int(tv["N"]))
        y = np.asarray(fn(x, h), float)
        y_id = np.fft.ifft(np.fft.fft(x) * np.fft.fft(h)).real
        err = 1.0 if y.shape != y_id.shape else _rel(y, y_id, 1.0)
        residuals["other_constraints"] = err
        return _result(err <= floor, residuals)

    if tid == "linear_convolution_zero_padded_dft":
        rng = np.random.default_rng(tv["seed"])
        x = rng.standard_normal(int(tv["Nx"]))
        h = rng.standard_normal(int(tv["Nh"]))
        y = np.asarray(fn(x, h), float)
        y_id = np.convolve(x, h)
        err = 1.0 if y.shape != y_id.shape else _rel(y, y_id, 1.0)
        residuals["other_constraints"] = err
        return _result(err <= floor, residuals)

    if tid == "autocorrelation_lag0_energy":
        rng = np.random.default_rng(tv["seed"])
        x = rng.standard_normal(int(tv["N"])) + 0.5 * np.sin(
            2 * np.pi * 3 * np.arange(int(tv["N"])) / int(tv["N"])
        )
        r = np.asarray(fn(x), float)
        mid = len(x) - 1
        if r.ndim != 1 or len(r) != 2 * len(x) - 1:
            residuals["other_constraints"] = 1.0
            return _result(False, residuals)
        et = float(np.sum(np.asarray(x, float) ** 2))
        err = abs(float(r[mid]) - et) / max(abs(et), EPS)
        residuals["other_constraints"] = err
        return _result(err <= floor, residuals)

    if tid == "decimation_alias_frequency":
        f, fs, m = float(tv["f"]), float(tv["fs"]), int(tv["M"])
        y = float(np.asarray(fn(f, fs, m)).reshape(()))
        y_id = _fold_alias_hz(f, fs / m)
        err = abs(y - y_id) / max(abs(y_id), fs / (2.0 * m), EPS)
        residuals["other_constraints"] = err
        return _result(err <= floor, residuals)

    if tid == "digital_frequency_rescale":
        fh, fsi, fso = float(tv["f_hat"]), float(tv["fs_in"]), float(tv["fs_out"])
        y = float(np.asarray(fn(fh, fsi, fso)).reshape(()))
        y_id = fh * fsi / fso
        err = abs(y - y_id) / max(abs(y_id), 0.5, EPS)
        residuals["other_constraints"] = err
        return _result(err <= floor, residuals)

    if tid == "nyquist_hz":
        fs = float(tv["fs"])
        y = float(np.asarray(fn(fs)).reshape(()))
        err = 0.0 if abs(y - fs / 2.0) <= 1e-15 else 1.0
        residuals["other_constraints"] = err
        return _result(err <= floor, residuals)

    if tid == "integer_delay_impulse":
        n, d = int(tv["N"]), int(tv["D"])
        h = np.asarray(fn(), float).reshape(-1)
        h_id = np.zeros(n)
        h_id[d] = 1.0
        err = 0.0 if h.shape == h_id.shape and np.array_equal(h, h_id) else 1.0
        residuals["other_constraints"] = err
        return _result(err <= floor, residuals)

    raise KeyError(f"no singleton checker for {tid}")


def check_specification(task_id: str, implementation) -> dict:
    """Return {pass, residuals} for specification membership only."""
    task = get_task(task_id)
    if task["family"] == "filter_specification":
        return _check_filter(task, implementation)
    if task["family"] == "singleton_identity":
        return _check_singleton(task, implementation)
    raise ValueError(f"unsupported family {task['family']}")
