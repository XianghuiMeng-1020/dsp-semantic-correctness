"""Frozen sampling/resampling semantic contracts.

Thresholds and identities were fixed before any generation in this family.
"""

from __future__ import annotations

import numpy as np
from scipy import signal as sp_signal

EPS = 1e-18
SEED = 20270824

# Theory / numerical floors. May be raised only from valid-control envelopes
# before freeze. Never from LLM residuals.
FLOOR = {
    "decimation_alias_frequency": 1e-8,
    "digital_frequency_rescale": 1e-8,
    "zero_insertion_spectral_images": 1e-8,
    "rational_resample_dc_preservation": 1e-6,
}

# Filled by freeze_oracle() from valid controls, then written into SEMANTIC_CONTRACTS.json
THRESHOLDS = dict(FLOOR)


def _as_float(y):
    return float(np.asarray(y, dtype=float).reshape(()))


def fold_alias_hz(f, fs_out):
    """One-sided aliased physical frequency in [0, fs_out/2]."""
    f = float(f)
    nyq = float(fs_out) / 2.0
    if nyq <= 0:
        raise ValueError("fs_out must be positive")
    period = float(fs_out)
    f_mod = np.mod(f + nyq, period) - nyq
    return float(abs(f_mod))


def image_freqs_rad(omega0, L):
    """L unique image frequencies in [0, pi] after L-fold zero insertion (real cosine)."""
    omega0 = float(omega0)
    L = int(L)
    vals = []
    for k in range(L):
        for s in (omega0, -omega0):
            w = np.mod((s + 2.0 * np.pi * k) / L, 2.0 * np.pi)
            if w > np.pi:
                w = 2.0 * np.pi - w
            vals.append(w)
    uniq = np.unique(np.round(np.asarray(vals, dtype=float), decimals=12))
    return np.sort(uniq.astype(float))


def task_decimation_alias_frequency():
    prompt = (
        "Write a Python function `aliased_frequency_hz(f, fs, M)` that returns the "
        "one-sided physical frequency in Hz of a real cosine tone originally at "
        "`f` Hz when the sequence is downsampled by integer `M` with NO anti-alias "
        "filter. The original sampling rate is `fs` Hz. The result must lie in "
        "[0, fs/(2*M)]. Use the standard folding identity: alias into the new "
        "sampling rate fs/M. Return a single finite float. Only output the function "
        "in a python code block."
    )

    def unit_test(fn):
        y = fn(350.0, 1000.0, 4)
        v = _as_float(y)
        return np.isfinite(v) and 0.0 <= v <= 125.0 + 1e-6

    def input_gen():
        return (350.0, 1000.0, 4)

    def reference_fn(f, fs, M):
        return fold_alias_hz(f, float(fs) / int(M))

    def residual(fn, args):
        f, fs, M = args
        y = _as_float(fn(f, fs, M))
        yref = reference_fn(f, fs, M)
        return abs(y - yref) / max(abs(yref), float(fs) / (2.0 * M), EPS)

    return dict(
        id="decimation_alias_frequency",
        family="sampling_resampling",
        mechanism_group="alias_frequency_mapping",
        func_name="aliased_frequency_hz",
        prompt=prompt,
        unit_test=unit_test,
        input_gen=input_gen,
        reference_fn=reference_fn,
        residual=residual,
        threshold=THRESHOLDS["decimation_alias_frequency"],
        identity="f_alias = |mod(f + fs_out/2, fs_out) - fs_out/2|, fs_out=fs/M, one-sided",
        shape="scalar",
    )


def task_digital_frequency_rescale():
    prompt = (
        "Write a Python function `digital_freq_after_rate_change(f_hat, fs_in, fs_out)` "
        "where `f_hat` is a digital frequency in cycles/sample at sampling rate "
        "`fs_in` (so 0 <= f_hat < 0.5). After ideal resampling to `fs_out` without "
        "aliasing, return the digital frequency in cycles/sample at the new rate "
        "of the SAME physical tone. Assume the physical frequency f_hat*fs_in lies "
        "strictly below the new Nyquist fs_out/2. Return a single finite float in "
        "[0, 0.5]. Only output the function in a python code block."
    )

    def unit_test(fn):
        y = fn(0.125, 8000.0, 16000.0)
        v = _as_float(y)
        return np.isfinite(v) and 0.0 <= v <= 0.5 + 1e-12

    def input_gen():
        return (0.125, 8000.0, 16000.0)

    def reference_fn(f_hat, fs_in, fs_out):
        return float(f_hat) * float(fs_in) / float(fs_out)

    def residual(fn, args):
        f_hat, fs_in, fs_out = args
        y = _as_float(fn(f_hat, fs_in, fs_out))
        yref = reference_fn(f_hat, fs_in, fs_out)
        return abs(y - yref) / max(abs(yref), 0.5, EPS)

    return dict(
        id="digital_frequency_rescale",
        family="sampling_resampling",
        mechanism_group="alias_frequency_mapping",
        func_name="digital_freq_after_rate_change",
        prompt=prompt,
        unit_test=unit_test,
        input_gen=input_gen,
        reference_fn=reference_fn,
        residual=residual,
        threshold=THRESHOLDS["digital_frequency_rescale"],
        identity="f_hat_out = f_hat_in * fs_in / fs_out  (physical Hz invariant; no alias)",
        shape="scalar",
    )


def task_zero_insertion_spectral_images():
    prompt = (
        "Write a Python function `zero_insert_image_freqs(omega0, L)` for a real "
        "cosine whose original digital frequency is `omega0` radians/sample "
        "(0 < omega0 < pi). After the expander that inserts L-1 zeros between "
        "samples (x_e[n] = x[n/L] if n is a multiple of L, else 0), return the L "
        "distinct image frequencies of the expanded real cosine, in radians/sample, "
        "as a 1-D numpy array of length L, sorted, each in [0, pi]. Only output "
        "the function in a python code block."
    )

    def unit_test(fn):
        y = np.asarray(fn(0.7, 4), dtype=float)
        return (
            isinstance(y, np.ndarray)
            and y.ndim == 1
            and y.size == 4
            and np.all(np.isfinite(y))
            and np.all(y >= -1e-9)
            and np.all(y <= np.pi + 1e-9)
        )

    def input_gen():
        return (0.7, 4)

    def reference_fn(omega0, L):
        return image_freqs_rad(omega0, L)

    def residual(fn, args):
        omega0, L = args
        y = np.sort(np.asarray(fn(omega0, L), dtype=float).reshape(-1))
        yref = reference_fn(omega0, L)
        if y.size != yref.size:
            return 1.0
        return float(np.max(np.abs(y - yref))) / max(np.pi, EPS)

    return dict(
        id="zero_insertion_spectral_images",
        family="sampling_resampling",
        mechanism_group="interpolation_resampling_consistency",
        func_name="zero_insert_image_freqs",
        prompt=prompt,
        unit_test=unit_test,
        input_gen=input_gen,
        reference_fn=reference_fn,
        residual=residual,
        threshold=THRESHOLDS["zero_insertion_spectral_images"],
        identity="images of a real cosine after L-expander: fold((+/- omega0 + 2 pi k)/L) into [0, pi], L unique values",
        shape="array",
    )


def task_rational_resample_dc_preservation():
    prompt = (
        "Write a Python function `rational_resample(x, L, M)` that resamples a real "
        "1-D array `x` by the rational factor L/M (output sampling rate is L/M times "
        "the input rate). `L` and `M` are positive integers. `len(x)` is a multiple "
        "of `M`. Return a 1-D numpy array of length len(x)*L//M. A constant input "
        "must remain that same constant (DC / interpolation gain preserved). Only "
        "output the function in a python code block."
    )

    def unit_test(fn):
        x = np.full(24, 2.5)
        y = fn(x, 2, 3)
        return (
            isinstance(y, np.ndarray)
            and y.ndim == 1
            and len(y) == 16
            and np.all(np.isfinite(y))
        )

    def input_gen():
        return (np.full(24, 2.5), 2, 3)

    def reference_fn(x, L, M):
        x = np.asarray(x, dtype=float)
        return np.full(len(x) * int(L) // int(M), float(x[0]))

    def residual(fn, args):
        x, L, M = args
        x = np.asarray(x, dtype=float)
        y = np.asarray(fn(x, L, M), dtype=float)
        n_out = len(x) * int(L) // int(M)
        if y.ndim != 1 or len(y) != n_out:
            return 1.0
        c = float(np.mean(x))
        return float(np.max(np.abs(y - c))) / max(abs(c), EPS)

    return dict(
        id="rational_resample_dc_preservation",
        family="sampling_resampling",
        mechanism_group="interpolation_resampling_consistency",
        func_name="rational_resample",
        prompt=prompt,
        unit_test=unit_test,
        input_gen=input_gen,
        reference_fn=reference_fn,
        residual=residual,
        threshold=THRESHOLDS["rational_resample_dc_preservation"],
        identity="if x[n]=C for all n, rational resample L/M yields y[k]=C (interpolation DC gain)",
        shape="array",
    )


TASK_FACTORIES = [
    task_decimation_alias_frequency,
    task_digital_frequency_rescale,
    task_zero_insertion_spectral_images,
    task_rational_resample_dc_preservation,
]


def fresh_tasks():
    return [fn() for fn in TASK_FACTORIES]


def battery_for(tid):
    rng = np.random.default_rng(SEED)
    if tid == "decimation_alias_frequency":
        return [
            ("canonical", (350.0, 1000.0, 4)),
            ("below_new_nyquist", (40.0, 1000.0, 4)),
            ("at_old_nyquist", (500.0, 1000.0, 5)),
            ("high_tone", (1750.0, 2000.0, 4)),
            ("even_fold", (300.0, 800.0, 2)),
        ]
    if tid == "digital_frequency_rescale":
        return [
            ("canonical", (0.125, 8000.0, 16000.0)),
            ("downsample_ok", (0.05, 48000.0, 16000.0)),
            ("upsample_3x", (0.2, 1000.0, 3000.0)),
            ("identity_rate", (0.3, 44100.0, 44100.0)),
        ]
    if tid == "zero_insertion_spectral_images":
        return [
            ("canonical", (0.7, 4)),
            ("L2", (np.pi / 2, 2)),
            ("L3", (0.4, 3)),
            ("L5", (1.1, 5)),
        ]
    if tid == "rational_resample_dc_preservation":
        items = [
            ("canonical", (np.full(24, 2.5), 2, 3)),
            ("upsample_2", (np.full(16, -1.0), 2, 1)),
            ("down_3", (np.full(30, 0.25), 1, 3)),
            ("L3M2", (np.full(20, 7.0), 3, 2)),
        ]
        x = rng.standard_normal(1)  # keep rng used; not a semantic input
        _ = x
        return items
    raise KeyError(tid)


def valid_implementations(tid):
    """Structurally different routes that preserve the frozen identity."""
    if tid == "decimation_alias_frequency":
        def via_mod(f, fs, M):
            return fold_alias_hz(f, float(fs) / int(M))

        def via_loop(f, fs, M):
            fs_out = float(fs) / int(M)
            nyq = fs_out / 2.0
            x = float(f)
            while x > nyq:
                x = abs(x - fs_out)
            while x < -nyq:
                x = abs(x + fs_out)
            return abs(float(x))

        def via_min_k(f, fs, M):
            fs_out = float(fs) / int(M)
            k = np.round(float(f) / fs_out)
            return abs(float(f) - k * fs_out)

        return [
            ("fold_mod", via_mod),
            ("fold_loop", via_loop),
            ("nearest_image", via_min_k),
        ]
    if tid == "digital_frequency_rescale":
        def via_ratio(f_hat, fs_in, fs_out):
            return float(f_hat) * float(fs_in) / float(fs_out)

        def via_physical(f_hat, fs_in, fs_out):
            f_hz = float(f_hat) * float(fs_in)
            return f_hz / float(fs_out)

        return [
            ("direct_ratio", via_ratio),
            ("via_physical_hz", via_physical),
        ]
    if tid == "zero_insertion_spectral_images":
        def via_pm(omega0, L):
            return image_freqs_rad(omega0, L)

        def via_unique_set(omega0, L):
            s = set()
            for k in range(int(L)):
                for sgn in (1.0, -1.0):
                    w = (sgn * float(omega0) + 2.0 * np.pi * k) / int(L)
                    w = w % (2.0 * np.pi)
                    w = min(w, 2.0 * np.pi - w)
                    s.add(round(w, 12))
            return np.sort(np.array(list(s), dtype=float))

        return [
            ("pm_fold", via_pm),
            ("set_fold", via_unique_set),
        ]
    if tid == "rational_resample_dc_preservation":
        def via_fft_resample(x, L, M):
            x = np.asarray(x, dtype=float)
            n_out = len(x) * int(L) // int(M)
            return sp_signal.resample(x, n_out)

        def via_constant(x, L, M):
            x = np.asarray(x, dtype=float)
            return np.full(len(x) * int(L) // int(M), float(np.mean(x)))

        def via_repeat_stride(x, L, M):
            # Sample-and-hold then keep every M-th sample. Identity-preserving only
            # because the contract battery is constant signals.
            y = np.repeat(np.asarray(x, dtype=float), int(L))
            return y[:: int(M)]

        return [
            ("fft_resample", via_fft_resample),
            ("constant_fill", via_constant),
            ("repeat_stride", via_repeat_stride),
        ]
    raise KeyError(tid)


def mutants_for(tid):
    """Interpretable single-identity mutants. Must execute; should pass unit tests."""
    if tid == "decimation_alias_frequency":
        def no_fold(f, fs, M):
            return float(f) / int(M)

        def clip_only(f, fs, M):
            return min(abs(float(f)), float(fs) / (2.0 * int(M)))

        return [
            ("scale_by_M_no_fold", no_fold),
            ("clip_to_new_nyquist", clip_only),
        ]
    if tid == "digital_frequency_rescale":
        def inverted(f_hat, fs_in, fs_out):
            return float(f_hat) * float(fs_out) / float(fs_in)

        def unchanged(f_hat, fs_in, fs_out):
            return float(f_hat)

        return [
            ("inverted_ratio", inverted),
            ("forget_rescale", unchanged),
        ]
    if tid == "zero_insertion_spectral_images":
        def only_compressed(omega0, L):
            return np.array([float(omega0) / int(L)] * int(L), dtype=float)

        def missing_divide(omega0, L):
            vals = [(float(omega0) + 2.0 * np.pi * k) for k in range(int(L))]
            w = np.mod(vals, 2.0 * np.pi)
            w = np.minimum(w, 2.0 * np.pi - w)
            return np.sort(w)

        return [
            ("only_omega_over_L", only_compressed),
            ("images_without_divide_L", missing_divide),
        ]
    if tid == "rational_resample_dc_preservation":
        def zero_insert_only(x, L, M):
            x = np.asarray(x, dtype=float)
            # expand by L then keep every M-th zero-inserted sample: DC becomes C/L
            exp = np.zeros(len(x) * int(L), dtype=float)
            exp[:: int(L)] = x
            return exp[:: int(M)]

        def scaled_poly(x, L, M):
            y = sp_signal.resample_poly(np.asarray(x, dtype=float), int(L), int(M))
            return y / float(L)

        return [
            ("zero_insert_decimate_no_gain", zero_insert_only),
            ("poly_divided_by_L", scaled_poly),
        ]
    raise KeyError(tid)


def differential_spec(tid):
    if tid in {
        "decimation_alias_frequency",
        "digital_frequency_rescale",
        "zero_insertion_spectral_images",
    }:
        return {
            "applicable": True,
            "metric": "same residual as the semantic contract (unique algebraic output)",
            "alignment": "none",
            "meaningful": True,
        }
    if tid == "rational_resample_dc_preservation":
        return {
            "applicable": True,
            "metric": "linf relative to constant C; interpolator shape is unidentified on non-constants",
            "alignment": "length must match N*L/M",
            "meaningful": True,
            "note": "only DC inputs are used for the semantic/differential identity",
        }
    raise KeyError(tid)


TASKS = [
    task_decimation_alias_frequency(),
    task_digital_frequency_rescale(),
    task_zero_insertion_spectral_images(),
    task_rational_resample_dc_preservation(),
]
