"""Canonical embeddings matching Phase-1 confirmatory distances. No metric rewrite."""
from __future__ import annotations

import numpy as np
from scipy import signal as sp_signal

from src.verification.canonicalize import TRIM_ABS, canonicalize_fir, canonicalize_iir, unpack
from src.verification.distances import RESP_N

from experiments.icassp_10of10_hardening.phase3a.config import AFFINE_SV_ABS, AFFINE_SV_REL


def _orient_fir(h: np.ndarray) -> np.ndarray:
    """Magnitude-equivalence section: first nonzero tap >= 0 (TRIM_ABS)."""
    h = np.asarray(h, float).copy()
    nz = np.where(np.abs(h) >= TRIM_ABS)[0]
    if len(nz) and float(h[nz[0]]) < 0.0:
        h = -h
    return h


def coeff_vector(impl, family: str) -> np.ndarray:
    if family == "fir":
        return _orient_fir(canonicalize_fir(impl).h)
    can = canonicalize_iir(impl)
    return np.concatenate([np.asarray(can.b, float), np.asarray(can.a, float)])


def coeff_dim_parts(impl, family: str) -> tuple[int, int]:
    if family == "fir":
        return int(len(canonicalize_fir(impl).h)), 0
    can = canonicalize_iir(impl)
    return int(len(can.b)), int(len(can.a))


def embed_coeff_task(valids: list[dict], invalids: list[dict], family: str) -> dict:
    """Zero-pad all occupants to the task-max canonical length (same as pairwise _pad_eq)."""
    if family == "fir":
        n = max(coeff_dim_parts(o["impl"], "fir")[0] for o in valids + invalids)
        def pad(impl):
            h = coeff_vector(impl, "fir")
            out = np.zeros(n, float)
            out[: len(h)] = h
            return out
    else:
        nb = max(coeff_dim_parts(o["impl"], "iir")[0] for o in valids + invalids)
        na = max(coeff_dim_parts(o["impl"], "iir")[1] for o in valids + invalids)

        def pad(impl):
            can = canonicalize_iir(impl)
            b = np.zeros(nb, float)
            a = np.zeros(na, float)
            b[: len(can.b)] = can.b
            a[: len(can.a)] = can.a
            return np.concatenate([b, a])

    V = np.stack([pad(o["impl"]) for o in valids], axis=0)
    I = np.stack([pad(o["impl"]) for o in invalids], axis=0)
    return {
        "V": V,
        "I": I,
        "dim": int(V.shape[1]),
        "family": family,
        "orientation": "fir_first_nonzero_nonneg" if family == "fir" else "iir_a0_1_concat_ba",
        "valid_ids": [o["cid"] for o in valids],
        "invalid_ids": [o["cid"] for o in invalids],
    }


def _freqz_mag(impl, fs: float, n: int) -> tuple[np.ndarray, np.ndarray]:
    b, a = unpack(impl)
    if a is None:
        w, H = sp_signal.freqz(b, worN=n, fs=fs)
    else:
        try:
            sos = sp_signal.tf2sos(b, a)
            w, H = sp_signal.sosfreqz(sos, worN=n, fs=fs)
        except Exception:
            w, H = sp_signal.freqz(b, a, worN=n, fs=fs)
    return w, np.abs(H)


def band_mask(w: np.ndarray, task: dict) -> np.ndarray:
    mask = np.zeros_like(w, dtype=bool)
    for band in list(task["pass_band"]) + list(task["stop_band"]):
        mask |= (w >= float(band["f0"])) & (w <= float(band["f1"]))
    return mask


def embed_response_task(valids: list[dict], invalids: list[dict], task: dict, n: int = RESP_N) -> dict:
    """Band-masked |H| vectors. RMSE = (1/sqrt(m)) * Euclidean on this embedding."""
    fs = float(task["sampling_rate"])
    w0, _ = _freqz_mag(valids[0]["impl"], fs, n)
    mask = band_mask(w0, task)
    m = int(np.count_nonzero(mask))

    def vec(impl):
        w, mag = _freqz_mag(impl, fs, n)
        if w.shape != w0.shape or not np.allclose(w, w0, rtol=0.0, atol=0.0):
            # Same worN/fs must produce the same grid; tolerate tiny float noise only.
            if w.shape != w0.shape or np.max(np.abs(w - w0)) > 1e-12:
                raise RuntimeError("response grid mismatch")
        return np.asarray(mag[mask], float)

    V = np.stack([vec(o["impl"]) for o in valids], axis=0)
    I = np.stack([vec(o["impl"]) for o in invalids], axis=0)
    return {
        "V": V,
        "I": I,
        "dim": m,
        "n_grid": n,
        "mask_count": m,
        "rmse_scale": float(1.0 / np.sqrt(m)) if m else None,
        "valid_ids": [o["cid"] for o in valids],
        "invalid_ids": [o["cid"] for o in invalids],
    }


def affine_span_reduce(V: np.ndarray, I: np.ndarray) -> dict:
    """Isometric embedding of the affine hull of frozen occupants. No PCA truncation.

    Occupants lie in an affine subspace A. Pairwise Euclidean distances are determined
    by the Gram matrix of (x - x0). A sphere in the ambient space separates the
    occupants iff a sphere in A does: for c = c_A + c_perp,
    ||x-c||^2 - ||y-c||^2 = ||x-c_A||^2 - ||y-c_A||^2 for every x,y in A.
    """
    X = np.concatenate([V, I], axis=0)
    x0 = X[0]
    D = X[1:] - x0
    if D.size == 0:
        Y = np.zeros((X.shape[0], 0), float)
        return {"V": Y[: len(V)], "I": Y[len(V) :], "dim": 0, "full_dim": int(X.shape[1]), "n_dropped": int(X.shape[1]), "sv_min_kept": None}
    # Economy SVD of D (n-1 x m): D = U S Vt, rows live in span of Vt[:rank]
    _, s, vt = np.linalg.svd(D, full_matrices=False)
    cutoff = max(AFFINE_SV_ABS, AFFINE_SV_REL * float(s[0]) if len(s) else 0.0)
    keep = int(np.sum(s > cutoff))
    basis = vt[:keep]
    Y = (X - x0) @ basis.T
    return {
        "V": Y[: len(V)],
        "I": Y[len(V) :],
        "dim": keep,
        "full_dim": int(X.shape[1]),
        "n_dropped": int(X.shape[1]) - keep,
        "sv_min_kept": float(s[keep - 1]) if keep else None,
        "sv_max_dropped": float(s[keep]) if keep < len(s) else None,
        "cutoff": cutoff,
    }
