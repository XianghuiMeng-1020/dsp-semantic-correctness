"""Pairwise confirmatory distances. Uses Phase-1 d_coeff / d_resp_from_mags."""
from __future__ import annotations

import numpy as np

from experiments.icassp_10of10_hardening.phase1.best_observed import _band_mask, cache_mags, d_coeff, d_resp_from_mags


def coeff_matrices(valids: list[dict], invalids: list[dict], task: dict) -> tuple[np.ndarray, np.ndarray]:
    nV, nI = len(valids), len(invalids)
    vv = np.zeros((nV, nV), float)
    iv = np.zeros((nI, nV), float)
    for r, ref in enumerate(valids):
        for v, occ in enumerate(valids):
            vv[v, r] = d_coeff(occ["impl"], ref["impl"], task)
        for i, occ in enumerate(invalids):
            iv[i, r] = d_coeff(occ["impl"], ref["impl"], task)
    return vv, iv


def resp_matrices(valids: list[dict], invalids: list[dict], task: dict) -> tuple[np.ndarray, np.ndarray]:
    fs = float(task["sampling_rate"])
    cache_mags(valids + invalids, fs)
    mask = _band_mask(valids[0]["_w"], task)
    nV, nI = len(valids), len(invalids)
    vv = np.zeros((nV, nV), float)
    iv = np.zeros((nI, nV), float)
    for r, ref in enumerate(valids):
        for v, occ in enumerate(valids):
            vv[v, r] = d_resp_from_mags(occ["_mag"], ref["_mag"], mask)
        for i, occ in enumerate(invalids):
            iv[i, r] = d_resp_from_mags(occ["_mag"], ref["_mag"], mask)
    return vv, iv


def gap_of_catalog(vv: np.ndarray, iv: np.ndarray, idx: list[int]) -> dict:
    if not idx:
        return {"D_V": None, "D_I": None, "G_R": None}
    dv = float(np.max(np.min(vv[:, idx], axis=1)))
    di = float(np.min(np.min(iv[:, idx], axis=1)))
    return {"D_V": dv, "D_I": di, "G_R": di - dv}
