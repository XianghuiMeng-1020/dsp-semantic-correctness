"""Canonical valids and predefined mutants for Suite S.

These are protocol fixtures for checker validation, not a generated dataset.
"""
from __future__ import annotations

import numpy as np


def fold_alias_hz(f, fs_out):
    nyq = float(fs_out) / 2.0
    f_mod = np.mod(float(f) + nyq, float(fs_out)) - nyq
    return float(abs(f_mod))


# --- canonicals ---

def s1_canonical(x, y):
    c = np.fft.ifft(np.fft.fft(y) * np.conj(np.fft.fft(x))).real
    return int(np.argmax(c))


def s1_alt_correlate(x, y):
    c = np.correlate(y, x, mode="full")
    # circular delay via roll search: unique L minimizing ||y - roll(x,L)||
    n = len(x)
    best_l, best = 0, np.inf
    for lag in range(n):
        e = np.linalg.norm(y - np.roll(x, lag))
        if e < best:
            best, best_l = e, lag
    return int(best_l)


def s2_canonical(x, h):
    return np.fft.ifft(np.fft.fft(x) * np.fft.fft(h)).real


def s2_alt_time_domain(x, h):
    x = np.asarray(x, float)
    h = np.asarray(h, float)
    n = len(x)
    y = np.zeros(n, float)
    for n0 in range(n):
        acc = 0.0
        for k in range(n):
            acc += x[k] * h[(n0 - k) % n]
        y[n0] = acc
    return y


def s3_canonical(x, h):
    n = len(x) + len(h) - 1
    return np.fft.ifft(np.fft.fft(x, n=n) * np.fft.fft(h, n=n)).real


def s3_alt_convolve(x, h):
    return np.convolve(x, h)


def s4_canonical(x):
    return np.correlate(x, x, mode="full")


def s5_canonical(f, fs, m):
    return fold_alias_hz(f, float(fs) / int(m))


def s6_canonical(f_hat, fs_in, fs_out):
    return float(f_hat) * float(fs_in) / float(fs_out)


def s7_canonical(fs):
    return float(fs) / 2.0


def s8_canonical():
    h = np.zeros(32)
    h[7] = 1.0
    return h


def s8_alt_roll():
    h = np.zeros(32)
    h[0] = 1.0
    return np.roll(h, 7)


# --- mutants ---

def s1_off_by_one(x, y):
    return (s1_canonical(x, y) + 1) % len(x)


def s1_sign_flipped(x, y):
    return (-s1_canonical(x, y)) % len(x)


def s2_linear_not_circular(x, h):
    y = np.convolve(x, h)
    return y[: len(x)]


def s2_conjugate_product(x, h):
    return np.fft.ifft(np.fft.fft(x) * np.conj(np.fft.fft(h))).real


def s3_missing_pad(x, h):
    n = max(len(x), len(h))
    y = np.fft.ifft(np.fft.fft(x, n=n) * np.fft.fft(h, n=n)).real
    return y


def s3_circular_wrap(x, h):
    n = max(len(x), len(h))
    return np.fft.ifft(np.fft.fft(x, n=n) * np.fft.fft(h, n=n)).real


def s4_lag0_is_mean(x):
    r = np.correlate(x, x, mode="full")
    r[len(x) - 1] = float(np.mean(x))
    return r


def s4_lag0_is_zero(x):
    r = np.correlate(x, x, mode="full")
    r[len(x) - 1] = 0.0
    return r


def s5_no_fold(f, fs, m):
    return float(f)


def s5_fold_old_nyquist(f, fs, m):
    return fold_alias_hz(f, float(fs))


def s6_forget_rescale(f_hat, fs_in, fs_out):
    return float(f_hat)


def s6_inverted_ratio(f_hat, fs_in, fs_out):
    return float(f_hat) * float(fs_out) / float(fs_in)


def s7_return_one_hz(fs):
    return 1.0


def s7_return_fs(fs):
    return float(fs)


def s8_impulse_at_zero():
    h = np.zeros(32)
    h[0] = 1.0
    return h


def s8_impulse_at_d_plus_1():
    h = np.zeros(32)
    h[8] = 1.0
    return h


CANONICAL = {
    "crosscorrelation_integer_delay": s1_canonical,
    "circular_convolution_theorem": s2_canonical,
    "linear_convolution_zero_padded_dft": s3_canonical,
    "autocorrelation_lag0_energy": s4_canonical,
    "decimation_alias_frequency": s5_canonical,
    "digital_frequency_rescale": s6_canonical,
    "nyquist_hz": s7_canonical,
    "integer_delay_impulse": s8_canonical,
}

ALTERNATE_VALID = {
    "crosscorrelation_integer_delay": s1_alt_correlate,
    "circular_convolution_theorem": s2_alt_time_domain,
    "linear_convolution_zero_padded_dft": s3_alt_convolve,
    "integer_delay_impulse": s8_alt_roll,
}

MUTANTS = {
    "crosscorrelation_integer_delay": {
        "off_by_one_lag": s1_off_by_one,
        "sign_flipped_lag": s1_sign_flipped,
    },
    "circular_convolution_theorem": {
        "linear_not_circular": s2_linear_not_circular,
        "conjugate_product": s2_conjugate_product,
    },
    "linear_convolution_zero_padded_dft": {
        "missing_pad": s3_missing_pad,
        "circular_wrap": s3_circular_wrap,
    },
    "autocorrelation_lag0_energy": {
        "lag0_is_mean": s4_lag0_is_mean,
        "lag0_is_zero": s4_lag0_is_zero,
    },
    "decimation_alias_frequency": {
        "no_fold": s5_no_fold,
        "fold_old_nyquist": s5_fold_old_nyquist,
    },
    "digital_frequency_rescale": {
        "forget_rescale": s6_forget_rescale,
        "inverted_ratio": s6_inverted_ratio,
    },
    "nyquist_hz": {
        "return_one_hz": s7_return_one_hz,
        "return_fs": s7_return_fs,
    },
    "integer_delay_impulse": {
        "impulse_at_zero": s8_impulse_at_zero,
        "impulse_at_D_plus_1": s8_impulse_at_d_plus_1,
    },
}
