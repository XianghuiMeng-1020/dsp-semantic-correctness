"""Locked invalid mutations. S_t only; no reference distances."""
from __future__ import annotations

import numpy as np

from experiments.icassp_10of10_hardening.phase3d_a.config import MUTATION_LADDER
from src.verification.canonicalize import unpack


def _scale(arrs) -> float:
    cat = np.concatenate([np.asarray(x, float).reshape(-1) for x in arrs])
    nrm = float(np.linalg.norm(cat))
    return nrm if nrm > 1e-18 else 1.0


def mutate_fir(h: np.ndarray, kind: str, seed_u64: int, digest: str, eps: float) -> np.ndarray:
    h = np.asarray(h, float).reshape(-1).copy()
    n = len(h)
    i = int(seed_u64 % n)
    s = 1.0 if int(digest[16], 16) % 2 == 0 else -1.0
    sigma = _scale([h])
    delta = s * float(eps) * sigma
    if kind == "M1":
        h[i] = h[i] + delta
        return h
    j = n - 1 - i
    if i == j:
        h[i] = h[i] + delta
    else:
        h[i] = h[i] + delta
        h[j] = h[j] + delta
    return h


def mutate_iir(impl: dict, kind: str, seed_u64: int, digest: str, eps: float) -> dict:
    b, a = unpack(impl)
    b = np.asarray(b, float).reshape(-1).copy()
    a = np.asarray(a, float).reshape(-1).copy()
    s = 1.0 if int(digest[16], 16) % 2 == 0 else -1.0
    sigma = _scale([b, a])
    delta = s * float(eps) * sigma
    if kind == "M1":
        pool = list(range(len(b))) + list(range(1, len(a)))  # exclude a0
        if not pool:
            pool = list(range(len(b)))
        i = int(seed_u64 % len(pool))
        idx = pool[i]
        if idx < len(b):
            b[idx] = b[idx] + delta
        else:
            a[idx - len(b) + 1] = a[idx - len(b) + 1] + delta
        return {"b": b, "a": a}
    fac = 1.0 + s * float(eps)
    a[1:] = a[1:] * fac
    a[0] = 1.0
    return {"b": b, "a": a}
