"""Frozen filter-specification semantic contracts (Arm N, primary arm).

Tasks, thresholds, valid controls, and mutants were frozen before any
natural generation in this arm. Correctness is a frequency-response /
stability specification, never coefficient equality to one reference filter.
"""

from __future__ import annotations

import numpy as np
from scipy import signal as sp_signal

FS = 8000.0
EPS = 1e-18

# FIR: binary in-band satisfaction is residual 0. Theory floor 1e-6.
# IIR: operational floor 1e-3 chosen a priori from classical IIR ripple at
# modest order (not from LLM residuals).
THRESHOLDS = {
    "fir_lowpass_spec": 1e-6,
    "fir_bandpass_spec": 1e-6,
    "fir_bandstop_spec": 1e-6,
    "iir_lowpass_stable_spec": 1e-3,
}

POLE_RADIUS_MAX = 0.999


def _freqz_mag(b, a=None, fs=FS, n=4096):
    if a is None:
        w, H = sp_signal.freqz(b, worN=n, fs=fs)
    else:
        w, H = sp_signal.freqz(b, a, worN=n, fs=fs)
    return w, np.abs(H)


def spec_residual(b, bands, a=None, fs=FS):
    w, mag = _freqz_mag(b, a=a, fs=fs)
    worst = 0.0
    for band in bands:
        mask = (w >= band["f0"]) & (w <= band["f1"])
        if not np.any(mask):
            return 1.0
        m = mag[mask]
        lo, hi = band["lo"], band["hi"]
        below = np.maximum(0.0, lo - m)
        above = np.maximum(0.0, m - hi)
        span = max(hi - lo, 1e-6)
        worst = max(worst, float(np.max(below) / span), float(np.max(above) / span))
    if not np.all(np.isfinite(np.atleast_1d(b))):
        return 1.0
    if a is not None and not np.all(np.isfinite(np.atleast_1d(a))):
        return 1.0
    return worst


def iir_stability_residual(b, a, pole_max=POLE_RADIUS_MAX):
    _z, p, _k = sp_signal.tf2zpk(b, a)
    if np.any(np.abs(p) >= pole_max):
        return 1.0
    return 0.0


def _as_taps(y):
    h = np.asarray(y, dtype=float).reshape(-1)
    return h


def _unit_fir(fn, bands, n_taps_min=3):
    h = _as_taps(fn())
    return (
        h.ndim == 1
        and len(h) >= n_taps_min
        and np.all(np.isfinite(h))
        and np.isrealobj(h)
    )


FIR_LOWPASS_BANDS = [
    {"f0": 0.0, "f1": 800.0, "lo": 0.95, "hi": 1.05},
    {"f0": 2000.0, "f1": 4000.0, "lo": 0.0, "hi": 0.05},
]
FIR_BANDPASS_BANDS = [
    {"f0": 0.0, "f1": 500.0, "lo": 0.0, "hi": 0.06},
    {"f0": 1500.0, "f1": 2200.0, "lo": 0.95, "hi": 1.05},
    {"f0": 3200.0, "f1": 4000.0, "lo": 0.0, "hi": 0.06},
]
FIR_BANDSTOP_BANDS = [
    {"f0": 0.0, "f1": 600.0, "lo": 0.95, "hi": 1.05},
    {"f0": 1400.0, "f1": 2200.0, "lo": 0.0, "hi": 0.06},
    {"f0": 3000.0, "f1": 4000.0, "lo": 0.95, "hi": 1.05},
]
IIR_LOWPASS_BANDS = [
    {"f0": 0.0, "f1": 600.0, "lo": 0.90, "hi": 1.10},
    {"f0": 2400.0, "f1": 4000.0, "lo": 0.0, "hi": 0.10},
]


def task_fir_lowpass_spec():
    prompt = (
        "Write a Python function `design_fir_lowpass()` that returns a real 1-D "
        "FIR coefficient vector for sampling rate fs=8000 Hz. The filter must "
        "satisfy: |H(f)| in [0.95, 1.05] for all f in [0, 800] Hz, and |H(f)| "
        "<= 0.05 for all f in [2000, 4000] Hz. Linear phase is not required. "
        "Any design method is acceptable. Return only the coefficient vector. "
        "Only output the function in a python code block."
    )

    def unit_test(fn):
        return _unit_fir(fn, FIR_LOWPASS_BANDS)

    def residual(fn, _args=None):
        return spec_residual(_as_taps(fn()), FIR_LOWPASS_BANDS)

    return dict(
        id="fir_lowpass_spec",
        family="filter_specification",
        mechanism_group="fir_amplitude_spec",
        func_name="design_fir_lowpass",
        prompt=prompt,
        unit_test=unit_test,
        input_gen=lambda: tuple(),
        residual=residual,
        threshold=THRESHOLDS["fir_lowpass_spec"],
        identity="FIR lowpass amplitude specification at fs=8000 Hz",
        shape="array",
    )


def task_fir_bandpass_spec():
    prompt = (
        "Write a Python function `design_fir_bandpass()` that returns a real 1-D "
        "FIR coefficient vector for sampling rate fs=8000 Hz. The filter must "
        "satisfy: |H(f)| <= 0.06 on [0, 500] Hz; |H(f)| in [0.95, 1.05] on "
        "[1500, 2200] Hz; |H(f)| <= 0.06 on [3200, 4000] Hz. Linear phase is "
        "not required. Any design method is acceptable. Return only the "
        "coefficient vector. Only output the function in a python code block."
    )

    def unit_test(fn):
        return _unit_fir(fn, FIR_BANDPASS_BANDS)

    def residual(fn, _args=None):
        return spec_residual(_as_taps(fn()), FIR_BANDPASS_BANDS)

    return dict(
        id="fir_bandpass_spec",
        family="filter_specification",
        mechanism_group="fir_amplitude_spec",
        func_name="design_fir_bandpass",
        prompt=prompt,
        unit_test=unit_test,
        input_gen=lambda: tuple(),
        residual=residual,
        threshold=THRESHOLDS["fir_bandpass_spec"],
        identity="FIR bandpass amplitude specification at fs=8000 Hz",
        shape="array",
    )


def task_fir_bandstop_spec():
    prompt = (
        "Write a Python function `design_fir_bandstop()` that returns a real 1-D "
        "FIR coefficient vector for sampling rate fs=8000 Hz. The filter must "
        "satisfy: |H(f)| in [0.95, 1.05] on [0, 600] Hz; |H(f)| <= 0.06 on "
        "[1400, 2200] Hz; |H(f)| in [0.95, 1.05] on [3000, 4000] Hz. Linear "
        "phase is not required. Any design method is acceptable. Return only "
        "the coefficient vector. Only output the function in a python code block."
    )

    def unit_test(fn):
        return _unit_fir(fn, FIR_BANDSTOP_BANDS)

    def residual(fn, _args=None):
        return spec_residual(_as_taps(fn()), FIR_BANDSTOP_BANDS)

    return dict(
        id="fir_bandstop_spec",
        family="filter_specification",
        mechanism_group="fir_amplitude_spec",
        func_name="design_fir_bandstop",
        prompt=prompt,
        unit_test=unit_test,
        input_gen=lambda: tuple(),
        residual=residual,
        threshold=THRESHOLDS["fir_bandstop_spec"],
        identity="FIR bandstop amplitude specification at fs=8000 Hz",
        shape="array",
    )


def task_iir_lowpass_stable_spec():
    prompt = (
        "Write a Python function `design_iir_lowpass()` that returns a pair "
        "(b, a) of real IIR numerator and denominator coefficient vectors for "
        "sampling rate fs=8000 Hz. The filter must be BIBO stable (all poles "
        "strictly inside the unit circle) and satisfy: |H(f)| in [0.90, 1.10] "
        "on [0, 600] Hz and |H(f)| <= 0.10 on [2400, 4000] Hz. Any classical "
        "or numerical design is acceptable. Only output the function in a "
        "python code block."
    )

    def unit_test(fn):
        out = fn()
        if not (isinstance(out, (tuple, list)) and len(out) == 2):
            return False
        b, a = np.asarray(out[0], float).reshape(-1), np.asarray(out[1], float).reshape(-1)
        return (
            len(b) >= 2
            and len(a) >= 2
            and np.all(np.isfinite(b))
            and np.all(np.isfinite(a))
        )

    def residual(fn, _args=None):
        b, a = fn()
        b = np.asarray(b, float).reshape(-1)
        a = np.asarray(a, float).reshape(-1)
        return max(spec_residual(b, IIR_LOWPASS_BANDS, a=a), iir_stability_residual(b, a))

    return dict(
        id="iir_lowpass_stable_spec",
        family="filter_specification",
        mechanism_group="iir_spec_stability",
        func_name="design_iir_lowpass",
        prompt=prompt,
        unit_test=unit_test,
        input_gen=lambda: tuple(),
        residual=residual,
        threshold=THRESHOLDS["iir_lowpass_stable_spec"],
        identity="IIR lowpass magnitude specification plus pole-radius stability",
        shape="ba",
    )


TASK_FACTORIES = [
    task_fir_lowpass_spec,
    task_fir_bandpass_spec,
    task_fir_bandstop_spec,
    task_iir_lowpass_stable_spec,
]
