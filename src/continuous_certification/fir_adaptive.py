"""Adaptive derivative-bound FIR certification.

Arithmetic: CONTINUOUS_BOUND_HIGH_PRECISION_NOT_FORMAL_INTERVAL

H and H' are evaluated in float64 with a documented rounding envelope.
Derivative bounds M1 / M_local are analytic. This is not interval
arithmetic and is not imported from the construction or 131072-grid
verifiers.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]

MAX_INTERVALS_PER_BAND = 2500
INITIAL_SPLITS = 48
MAX_DEPTH = 20
WITNESS_GRID = 10007  # prime; not the construction 4096 or verifier 131072
EARLY_UNDECIDED_AFTER = 400
EPS64 = float(np.finfo(np.float64).eps)


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


def _H_Hp(h: np.ndarray, omega: float):
    n = np.arange(len(h), dtype=np.float64)
    e = np.exp(-1j * omega * n)
    H = np.dot(h, e)
    Hp = -1j * np.dot(h * n, e)
    return H, Hp


def _eval_error(h: np.ndarray) -> float:
    """Loose |H| / |H'| rounding envelope for the naive DFT sum."""
    s = float(np.sum(np.abs(h)))
    s1 = float(np.dot(np.arange(len(h), dtype=np.float64), np.abs(h)))
    # (n+1) ulps times the exact triangle bound, times 4 for complex ops
    return 4.0 * (len(h) + 1) * EPS64 * (s + 1.0), 4.0 * (len(h) + 1) * EPS64 * (s1 + 1.0)


def certify_fir(task_id: str, impl) -> dict:
    task = _load_task(task_id)
    if not str(task.get("type", "")).startswith("fir_"):
        return {
            "status": "UNDECIDED",
            "reason": "not_fir_mask",
            "task_id": task_id,
            "arithmetic": "CONTINUOUS_BOUND_HIGH_PRECISION_NOT_FORMAL_INTERVAL",
        }
    h = _as_fir_taps(impl)
    if not np.all(np.isfinite(h)):
        return {"status": "CERTIFIED_INVALID", "reason": "nonfinite", "task_id": task_id}

    fs = float(task["sampling_rate"])
    floor = float(task["residual_floor"])
    two_pi = 2.0 * math.pi
    n_idx = np.arange(len(h), dtype=np.float64)
    M1 = float(np.dot(n_idx, np.abs(h)))
    M2 = float(np.dot(n_idx**2, np.abs(h)))
    err_h, err_hp = _eval_error(h)

    bands = []
    for band in list(task["pass_band"]) + list(task["stop_band"]):
        lo, hi = float(band["lo"]), float(band["hi"])
        span = max(hi - lo, 1e-6)
        bands.append(
            {
                "f0": float(band["f0"]),
                "f1": float(band["f1"]),
                "L": lo - floor * span,
                "U": hi + floor * span,
            }
        )

    # Independent dense witness (not inherited from either existing grid).
    for band in bands:
        f0, f1 = band["f0"], band["f1"]
        if f1 <= f0:
            continue
        freqs = np.linspace(f0, f1, WITNESS_GRID)
        omegas = two_pi * freqs / fs
        n = np.arange(len(h), dtype=np.float64)
        # Vectorized Horner-equivalent DFT on the witness grid
        H = np.exp(-1j * np.outer(omegas, n)) @ h
        mag = np.abs(H)
        below = mag + err_h < band["L"]
        above = mag - err_h > band["U"]
        hit = np.where(below | above)[0]
        if hit.size:
            k = int(hit[0])
            return {
                "status": "CERTIFIED_INVALID",
                "reason": "witnessed_violation",
                "task_id": task_id,
                "n_taps": int(len(h)),
                "M1": M1,
                "witness": {
                    "omega": float(omegas[k]),
                    "f_hz": float(freqs[k]),
                    "mag": float(mag[k]),
                    "L": band["L"],
                    "U": band["U"],
                    "grid": "independent_prime_10007",
                },
                "min_certified_margin": None,
                "arithmetic": "CONTINUOUS_BOUND_HIGH_PRECISION_NOT_FORMAL_INTERVAL",
            }

    min_margin = math.inf
    critical = None
    undecided_intervals = 0
    certified_intervals = 0

    for band in bands:
        w0 = two_pi * band["f0"] / fs
        w1 = two_pi * band["f1"] / fs
        if w1 <= w0:
            continue
        queue = []
        for i in range(INITIAL_SPLITS):
            a = w0 + (w1 - w0) * i / INITIAL_SPLITS
            b = w0 + (w1 - w0) * (i + 1) / INITIAL_SPLITS
            queue.append((a, b, 0))
        n_seen = 0
        while queue:
            a, b, depth = queue.pop()
            n_seen += 1
            if n_seen > MAX_INTERVALS_PER_BAND or (
                n_seen > EARLY_UNDECIDED_AFTER and certified_intervals == 0
            ):
                undecided_intervals += 1 + len(queue)
                break
            c = 0.5 * (a + b)
            delta = 0.5 * (b - a)
            H, Hp = _H_Hp(h, c)
            mag = float(np.abs(H))
            hp_abs = float(np.abs(Hp))
            M_local = (hp_abs + err_hp) + M2 * delta
            M = min(M1, M_local)
            mag_hi = mag + err_h
            mag_lo = max(0.0, mag - err_h)

            if mag_lo > band["U"] or mag_hi < band["L"]:
                return {
                    "status": "CERTIFIED_INVALID",
                    "reason": "witnessed_violation",
                    "task_id": task_id,
                    "n_taps": int(len(h)),
                    "M1": M1,
                    "witness": {
                        "omega": c,
                        "f_hz": c * fs / two_pi,
                        "mag": mag,
                        "L": band["L"],
                        "U": band["U"],
                    },
                    "min_certified_margin": None,
                    "arithmetic": "CONTINUOUS_BOUND_HIGH_PRECISION_NOT_FORMAL_INTERVAL",
                }

            upper_ok = mag_hi + M * delta < band["U"]
            lower_ok = mag_lo - M * delta > band["L"]
            if upper_ok and lower_ok:
                certified_intervals += 1
                slack = min(band["U"] - (mag_hi + M * delta), (mag_lo - M * delta) - band["L"])
                if slack < min_margin:
                    min_margin = slack
                    critical = {"omega": c, "delta": delta, "M": M, "f_hz": c * fs / two_pi}
                continue
            if depth >= MAX_DEPTH or delta <= 0.0:
                undecided_intervals += 1
                if critical is None:
                    critical = {"omega": c, "delta": delta, "M": M, "undecided": True}
                continue
            queue.append((a, c, depth + 1))
            queue.append((c, b, depth + 1))

    if undecided_intervals > 0:
        return {
            "status": "UNDECIDED",
            "reason": "resource_or_loose_bound",
            "task_id": task_id,
            "n_taps": int(len(h)),
            "M1": M1,
            "certified_intervals": certified_intervals,
            "undecided_intervals": undecided_intervals,
            "min_certified_margin": None if not math.isfinite(min_margin) else min_margin,
            "critical_interval": critical,
            "arithmetic": "CONTINUOUS_BOUND_HIGH_PRECISION_NOT_FORMAL_INTERVAL",
        }
    return {
        "status": "CERTIFIED_VALID",
        "reason": "all_bands_certified",
        "task_id": task_id,
        "n_taps": int(len(h)),
        "M1": M1,
        "certified_intervals": certified_intervals,
        "undecided_intervals": 0,
        "min_certified_margin": None if not math.isfinite(min_margin) else min_margin,
        "critical_interval": critical,
        "arithmetic": "CONTINUOUS_BOUND_HIGH_PRECISION_NOT_FORMAL_INTERVAL",
    }
