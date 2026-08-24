"""Frozen convolution/correlation semantic contracts.

Thresholds and identities were fixed before any generation in this family.
"""

import numpy as np

EPS = 1e-18

# Pre-specified numerical/theory floors. Not taken from any LLM residual.
THRESHOLDS = {
    "circular_convolution_theorem": 1e-6,
    "autocorrelation_lag0_energy": 1e-4,
    "crosscorrelation_integer_delay": 0.0,  # exact integer lag required
    "linear_convolution_zero_padded_dft": 1e-6,
}


def task_circular_convolution_theorem():
    prompt = (
        "Write a Python function `circular_convolve(x, h)` that returns the circular "
        "convolution of two equal-length real 1-D arrays `x` and `h`, implementing the "
        "DFT convolution theorem: IFFT(FFT(x) * FFT(h)), real part. Return a 1-D numpy "
        "array of the same length. Only output the function in a python code block."
    )

    def unit_test(fn):
        y = fn(np.random.randn(64), np.random.randn(64))
        return isinstance(y, np.ndarray) and y.ndim == 1 and len(y) == 64 and np.all(np.isfinite(y))

    def input_gen():
        rng = np.random.default_rng(20270823)
        return (rng.standard_normal(128), rng.standard_normal(128))

    def reference_fn(x, h):
        return np.fft.ifft(np.fft.fft(x) * np.fft.fft(h)).real

    def residual(fn, args):
        x, h = args
        y = np.asarray(fn(x, h), dtype=float)
        yref = reference_fn(x, h)
        return float(np.linalg.norm(y - yref) / max(np.linalg.norm(yref), EPS))

    return dict(
        id="circular_convolution_theorem",
        family="convolution_correlation",
        func_name="circular_convolve",
        prompt=prompt,
        unit_test=unit_test,
        input_gen=input_gen,
        reference_fn=reference_fn,
        residual=residual,
        threshold=THRESHOLDS["circular_convolution_theorem"],
        identity="y = IFFT(FFT(x) FFT(h)) for circular convolution",
    )


def task_autocorrelation_lag0_energy():
    prompt = (
        "Write a Python function `raw_autocorrelation(x)` that returns the raw "
        "(unnormalized) aperiodic autocorrelation of real 1-D `x` as a 1-D array of "
        "lags from -(N-1) to +(N-1). The lag-0 coefficient MUST equal sum(x**2). "
        "Only output the function in a python code block."
    )

    def unit_test(fn):
        r = fn(np.random.randn(50))
        return isinstance(r, np.ndarray) and r.ndim == 1 and len(r) == 99 and np.all(np.isfinite(r))

    def input_gen():
        rng = np.random.default_rng(7)
        return (rng.standard_normal(64) + 0.5 * np.sin(2 * np.pi * 3 * np.arange(64) / 64),)

    def reference_fn(x):
        return np.correlate(x, x, mode="full")

    def residual(fn, args):
        (x,) = args
        r = np.asarray(fn(x), dtype=float)
        mid = len(x) - 1
        r0 = float(r[mid])
        et = float(np.sum(np.asarray(x, dtype=float) ** 2))
        return abs(r0 - et) / max(abs(et), EPS)

    return dict(
        id="autocorrelation_lag0_energy",
        family="convolution_correlation",
        func_name="raw_autocorrelation",
        prompt=prompt,
        unit_test=unit_test,
        input_gen=input_gen,
        reference_fn=reference_fn,
        residual=residual,
        threshold=THRESHOLDS["autocorrelation_lag0_energy"],
        identity="R_xx[0] = sum(x**2)",
    )


def task_crosscorrelation_integer_delay():
    prompt = (
        "Write a Python function `estimate_delay_samples(x, y)` that estimates the "
        "integer sample delay of `y` relative to `x`, where `y` is `x` circularly "
        "shifted by an unknown integer L (y[n] = x[n-L]). Return a single integer "
        "(or integer-valued numpy scalar) L in 0..N-1. Only output the function."
    )

    def unit_test(fn):
        x = np.random.randn(80)
        L = 5
        y = np.roll(x, L)
        out = fn(x, y)
        return np.isfinite(float(out))

    def input_gen():
        rng = np.random.default_rng(19)
        x = rng.standard_normal(128)
        L = 17
        return (x, np.roll(x, L), L)

    def reference_fn(x, y, L=None):
        c = np.fft.ifft(np.fft.fft(y) * np.conj(np.fft.fft(x))).real
        return int(np.argmax(c))

    def residual(fn, args):
        x, y, L = args
        Lhat = int(np.rint(float(fn(x, y))))
        return float(0.0 if ((Lhat - L) % len(x) == 0) else 1.0)

    return dict(
        id="crosscorrelation_integer_delay",
        family="convolution_correlation",
        func_name="estimate_delay_samples",
        prompt=prompt,
        unit_test=unit_test,
        input_gen=input_gen,
        reference_fn=reference_fn,
        residual=residual,
        threshold=THRESHOLDS["crosscorrelation_integer_delay"],
        identity="argmax of circular cross-correlation equals the circular delay",
    )


def task_linear_convolution_zero_padded_dft():
    prompt = (
        "Write a Python function `linear_convolve_dft(x, h)` that computes the LINEAR "
        "convolution of real 1-D `x` and `h` using zero-padded FFTs (not np.convolve). "
        "Return a 1-D array of length len(x)+len(h)-1. Only output the function."
    )

    def unit_test(fn):
        y = fn(np.random.randn(20), np.random.randn(7))
        return isinstance(y, np.ndarray) and y.ndim == 1 and len(y) == 26 and np.all(np.isfinite(y))

    def input_gen():
        rng = np.random.default_rng(3)
        return (rng.standard_normal(32), rng.standard_normal(9))

    def reference_fn(x, h):
        n = len(x) + len(h) - 1
        return np.fft.ifft(np.fft.fft(x, n=n) * np.fft.fft(h, n=n)).real

    def residual(fn, args):
        x, h = args
        y = np.asarray(fn(x, h), dtype=float)
        yref = np.convolve(x, h)
        if len(y) != len(yref):
            return 1.0
        return float(np.linalg.norm(y - yref) / max(np.linalg.norm(yref), EPS))

    return dict(
        id="linear_convolution_zero_padded_dft",
        family="convolution_correlation",
        func_name="linear_convolve_dft",
        prompt=prompt,
        unit_test=unit_test,
        input_gen=input_gen,
        reference_fn=reference_fn,
        residual=residual,
        threshold=THRESHOLDS["linear_convolution_zero_padded_dft"],
        identity="zero-padded circular convolution equals linear convolution",
    )


TASKS = [
    task_circular_convolution_theorem(),
    task_autocorrelation_lag0_energy(),
    task_crosscorrelation_integer_delay(),
    task_linear_convolution_zero_padded_dft(),
]
