"""Deterministic geometry of a Suite N magnitude mask.

Cutoffs are midpoints of free transitions. Nothing here maximizes
distance from a reference.
"""
from __future__ import annotations


def response_type(task: dict) -> str:
    return str(task["type"]).split("_", 1)[1]


def is_fir(task: dict) -> bool:
    return str(task["type"]).startswith("fir_")


def nyquist(task: dict) -> float:
    return float(task["sampling_rate"]) / 2.0


def _kind(band: dict) -> str:
    return "pass" if float(band["lo"]) >= 0.5 else "stop"


def constrained_intervals(task: dict) -> list[tuple[float, float, str]]:
    ivals = []
    for b in list(task["pass_band"]) + list(task["stop_band"]):
        ivals.append((float(b["f0"]), float(b["f1"]), _kind(b)))
    ivals.sort(key=lambda x: x[0])
    return ivals


def free_transitions(task: dict) -> list[tuple[float, float]]:
    nyq = nyquist(task)
    gaps = []
    prev = 0.0
    for f0, f1, _k in constrained_intervals(task):
        if f0 > prev + 1e-12:
            gaps.append((prev, f0))
        prev = f1
    if prev < nyq - 1e-12:
        gaps.append((prev, nyq))
    return [(a, b) for a, b in gaps if b - a > 1e-12]


def default_cutoffs(task: dict) -> list[float]:
    """Midpoint of each free transition (mechanical, not tuned)."""
    return [0.5 * (a + b) for a, b in free_transitions(task)]


def cutoff_grid(task: dict, n_pts: int = 5) -> list[list[float]]:
    """Small linspace in each free transition, midpoint first."""
    gaps = free_transitions(task)
    if not gaps:
        return []
    per = []
    for a, b in gaps:
        xs = [0.5 * (a + b)]
        if n_pts > 1:
            span = b - a
            lo, hi = a + 0.15 * span, b - 0.15 * span
            if hi > lo:
                step = (hi - lo) / float(n_pts - 1)
                for i in range(n_pts):
                    x = lo + i * step
                    if all(abs(x - y) > 1e-9 for y in xs):
                        xs.append(x)
        per.append(xs)
    if len(per) == 1:
        return [[x] for x in per[0]]
    out = []
    for x in per[0]:
        for y in per[1]:
            if y > x + 1e-9:
                out.append([x, y])
    return out


def firwin_pass_zero(task: dict):
    r = response_type(task)
    if r in {"lp", "bs"}:
        return True
    if r in {"hp", "bp"}:
        return False
    raise KeyError(r)


def iir_btype(task: dict) -> str:
    r = response_type(task)
    if r == "lp":
        return "low"
    if r == "hp":
        return "high"
    raise KeyError(f"no IIR btype for {r}")


def remez_desired(task: dict) -> list[float]:
    r = response_type(task)
    return {"lp": [1, 0], "hp": [0, 1], "bp": [0, 1, 0], "bs": [1, 0, 1]}[r]


def firwin2_spec(task: dict) -> tuple[list[float], list[float]]:
    nyq = nyquist(task)
    r = response_type(task)
    passes = sorted(task["pass_band"], key=lambda b: b["f0"])
    stops = sorted(task["stop_band"], key=lambda b: b["f0"])
    if r == "lp":
        freq = [0.0, float(passes[0]["f1"]), float(stops[0]["f0"]), nyq]
        gain = [1.0, 1.0, 0.0, 0.0]
    elif r == "hp":
        freq = [0.0, float(stops[0]["f1"]), float(passes[0]["f0"]), nyq]
        gain = [0.0, 0.0, 1.0, 1.0]
    elif r == "bp":
        freq = [
            0.0,
            float(stops[0]["f1"]),
            float(passes[0]["f0"]),
            float(passes[0]["f1"]),
            float(stops[1]["f0"]),
            nyq,
        ]
        gain = [0.0, 0.0, 1.0, 1.0, 0.0, 0.0]
    elif r == "bs":
        freq = [
            0.0,
            float(passes[0]["f1"]),
            float(stops[0]["f0"]),
            float(stops[0]["f1"]),
            float(passes[1]["f0"]),
            nyq,
        ]
        gain = [1.0, 1.0, 0.0, 0.0, 1.0, 1.0]
    else:
        raise KeyError(r)
    cleaned_f, cleaned_g = [freq[0]], [gain[0]]
    for f, g in zip(freq[1:], gain[1:]):
        if f <= cleaned_f[-1] + 1e-9:
            continue
        cleaned_f.append(f)
        cleaned_g.append(g)
    return cleaned_f, cleaned_g


def remez_bands(task: dict) -> list[float]:
    freq, _g = firwin2_spec(task)
    return freq


def firls_desired(task: dict) -> list[float]:
    _freq, gain = firwin2_spec(task)
    return gain


def stop_atten_db(task: dict) -> float:
    hi = min(float(b["hi"]) for b in task["stop_band"])
    return float(max(20.0, -20.0 * __import__("math").log10(max(hi, 1e-9))))


def pass_rp_db(task: dict) -> float:
    """Textbook ripple that can still meet the pass mask."""
    hi = min(float(b["hi"]) for b in task["pass_band"])
    if hi >= 1.049:
        return 0.5
    return 0.1


def estimate_fir_n(task: dict) -> int:
    fs = float(task["sampling_rate"])
    gaps = free_transitions(task)
    df = min(b - a for a, b in gaps) if gaps else fs / 10.0
    atten = stop_atten_db(task)
    n = int(__import__("math").ceil(atten / max(22.0 * df / fs, 1e-6)))
    if n % 2 == 0:
        n += 1
    return max(21, min(n, 401))
