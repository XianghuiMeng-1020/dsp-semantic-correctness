"""Mechanical Suite N mask derivation.

Tightness and 16 kHz scaling are arithmetic rules, not hand-tuned masks.
Do not edit derived numbers after seeing checker outcomes.
"""
from __future__ import annotations

from copy import deepcopy


def _scale_bands(bands: list[dict], factor: float) -> list[dict]:
    out = []
    for b in bands:
        d = dict(b)
        d["f0"] = float(b["f0"]) * factor
        d["f1"] = float(b["f1"]) * factor
        out.append(d)
    return out


def tighten_pass(band: dict) -> dict:
    """Pass ripple x 1/5 about unity gain."""
    lo, hi = float(band["lo"]), float(band["hi"])
    return {
        "f0": float(band["f0"]),
        "f1": float(band["f1"]),
        "lo": 1.0 - (1.0 - lo) / 5.0,
        "hi": 1.0 + (hi - 1.0) / 5.0,
    }


def tighten_stop(band: dict) -> dict:
    """Stop ceiling x 1/5. Floor stays 0."""
    return {
        "f0": float(band["f0"]),
        "f1": float(band["f1"]),
        "lo": 0.0,
        "hi": float(band["hi"]) / 5.0,
    }


def _facing_pass_edge(stop: dict, passes: list[dict]) -> tuple[str, float]:
    """Which stop edge faces the nearest pass, and that pass edge frequency."""
    s0, s1 = float(stop["f0"]), float(stop["f1"])
    best = None
    for p in passes:
        p0, p1 = float(p["f0"]), float(p["f1"])
        gap_right = p0 - s1
        if gap_right > 0:
            cand = ("f1", p0, gap_right)
            if best is None or cand[2] < best[2]:
                best = cand
        gap_left = s0 - p1
        if gap_left > 0:
            cand = ("f0", p1, gap_left)
            if best is None or cand[2] < best[2]:
                best = cand
    if best is None:
        raise ValueError(f"no free transition facing pass for stop {stop}")
    return best[0], best[1]


def shrink_stop_transitions(stops: list[dict], passes: list[dict]) -> list[dict]:
    """Move each stop edge halfway toward the facing pass edge."""
    out = []
    for stop in stops:
        d = dict(stop)
        # A stop between two passes (band-stop) has two facing edges.
        s0, s1 = float(stop["f0"]), float(stop["f1"])
        moved = {"f0": False, "f1": False}
        for p in passes:
            p0, p1 = float(p["f0"]), float(p["f1"])
            if p1 < s0:
                d["f0"] = s0 - 0.5 * (s0 - p1)
                moved["f0"] = True
            if p0 > s1:
                d["f1"] = s1 + 0.5 * (p0 - s1)
                moved["f1"] = True
        if not moved["f0"] and not moved["f1"]:
            edge, pass_f = _facing_pass_edge(stop, passes)
            if edge == "f0":
                d["f0"] = s0 - 0.5 * (s0 - pass_f)
            else:
                d["f1"] = s1 + 0.5 * (pass_f - s1)
        out.append(d)
    return out


def tighten_mask(pass_bands: list[dict], stop_bands: list[dict]) -> tuple[list[dict], list[dict]]:
    new_pass = [tighten_pass(b) for b in pass_bands]
    new_stop = [tighten_stop(b) for b in stop_bands]
    new_stop = shrink_stop_transitions(new_stop, new_pass)
    return new_pass, new_stop


def scale_mask(pass_bands: list[dict], stop_bands: list[dict], factor: float):
    return _scale_bands(pass_bands, factor), _scale_bands(stop_bands, factor)


def bands_for_checker(pass_bands: list[dict], stop_bands: list[dict]) -> list[dict]:
    return [deepcopy(b) for b in pass_bands + stop_bands]


# Frozen loose 8 kHz prototypes (Arm N LP/BP/BS/IIR LP plus HP complements).
LOOSE_8K = {
    "fir_lp": {
        "pass": [{"f0": 0.0, "f1": 800.0, "lo": 0.95, "hi": 1.05}],
        "stop": [{"f0": 2000.0, "f1": 4000.0, "lo": 0.0, "hi": 0.05}],
    },
    "fir_hp": {
        "pass": [{"f0": 2000.0, "f1": 4000.0, "lo": 0.95, "hi": 1.05}],
        "stop": [{"f0": 0.0, "f1": 800.0, "lo": 0.0, "hi": 0.05}],
    },
    "fir_bp": {
        "pass": [{"f0": 1500.0, "f1": 2200.0, "lo": 0.95, "hi": 1.05}],
        "stop": [
            {"f0": 0.0, "f1": 500.0, "lo": 0.0, "hi": 0.06},
            {"f0": 3200.0, "f1": 4000.0, "lo": 0.0, "hi": 0.06},
        ],
    },
    "fir_bs": {
        "pass": [
            {"f0": 0.0, "f1": 600.0, "lo": 0.95, "hi": 1.05},
            {"f0": 3000.0, "f1": 4000.0, "lo": 0.95, "hi": 1.05},
        ],
        "stop": [{"f0": 1400.0, "f1": 2200.0, "lo": 0.0, "hi": 0.06}],
    },
    "iir_lp": {
        "pass": [{"f0": 0.0, "f1": 600.0, "lo": 0.90, "hi": 1.10}],
        "stop": [{"f0": 2400.0, "f1": 4000.0, "lo": 0.0, "hi": 0.10}],
    },
    "iir_hp": {
        "pass": [{"f0": 2400.0, "f1": 4000.0, "lo": 0.90, "hi": 1.10}],
        "stop": [{"f0": 0.0, "f1": 600.0, "lo": 0.0, "hi": 0.10}],
    },
}

LEGACY_ARM_N = {
    "fir_lp_loose_8k": "fir_lowpass_spec",
    "fir_bp_loose_8k": "fir_bandpass_spec",
    "fir_bs_loose_8k": "fir_bandstop_spec",
    "iir_lp_loose_8k": "iir_lowpass_stable_spec",
}

CANONICAL = {
    "fir": "firwin_hamming",
    "iir": "butter",
}
