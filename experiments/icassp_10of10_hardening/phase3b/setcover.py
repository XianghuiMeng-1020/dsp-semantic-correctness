"""Exact minimum set cover. Not claimed as a new algorithm."""
from __future__ import annotations

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp


def _greedy(cover: np.ndarray) -> list[int]:
    n_v, n_s = cover.shape
    need = np.ones(n_v, dtype=bool)
    chosen = []
    while need.any():
        scores = cover[need].sum(axis=0)
        scores = np.where(np.isin(np.arange(n_s), chosen), -1, scores)
        j = int(np.argmax(scores))
        if scores[j] <= 0:
            return []
        chosen.append(j)
        need &= ~cover[:, j]
    return chosen


def exact_set_cover(cover: np.ndarray) -> dict:
    """cover: (n_valid, n_sets) bool. Return minimum column subset covering every row."""
    n_v, n_s = cover.shape
    if n_v == 0:
        return {"status": "EXACT_OPTIMUM", "k": 0, "indices": [], "method": "empty"}
    if not cover.any(axis=1).all():
        return {"status": "INFEASIBLE", "k": None, "indices": [], "method": "uncovered_row"}
    greedy = _greedy(cover)
    if n_s <= 16:
        best = None
        limit = len(greedy) if greedy else n_s
        for k in range(1, limit + 1):
            found = _enum_k(cover, k)
            if found is not None:
                best = found
                break
        if best is None and greedy:
            best = greedy
        return {
            "status": "EXACT_OPTIMUM",
            "k": len(best),
            "indices": [int(i) for i in best],
            "method": "exhaustive",
            "greedy_k": len(greedy) if greedy else None,
        }
    c = np.ones(n_s, float)
    A = cover.astype(float)
    cons = LinearConstraint(A, lb=np.ones(n_v), ub=np.full(n_v, np.inf))
    res = milp(c, constraints=cons, bounds=Bounds(0, 1), integrality=np.ones(n_s, int))
    if res.success and res.x is not None:
        idx = [int(i) for i, x in enumerate(res.x) if x > 0.5]
        if cover[:, idx].any(axis=1).all():
            return {
                "status": "EXACT_OPTIMUM",
                "k": len(idx),
                "indices": idx,
                "method": "scipy_milp_highs",
                "greedy_k": len(greedy) if greedy else None,
                "milp_message": str(res.message),
            }
    if greedy:
        return {
            "status": "BOUND_ONLY",
            "k": None,
            "indices": [int(i) for i in greedy],
            "upper": len(greedy),
            "method": "greedy_fallback",
        }
    return {"status": "UNDECIDED", "k": None, "indices": [], "method": "fail"}


def _enum_k(cover: np.ndarray, k: int) -> list[int] | None:
    n_s = cover.shape[1]
    chosen = []

    def rec(start, left):
        if left == 0:
            if cover[:, chosen].any(axis=1).all():
                return True
            return False
        for j in range(start, n_s - left + 1):
            chosen.append(j)
            if rec(j + 1, left - 1):
                return True
            chosen.pop()
        return False

    if rec(0, k):
        return list(chosen)
    return None


def bitset_cover_k(cover: np.ndarray, k: int) -> list[int] | None:
    """Independent exact check: exists a cover of size k?"""
    return _enum_k(cover, k) if cover.shape[1] <= 24 or k <= 4 else _milp_at_most(cover, k)


def _milp_at_most(cover: np.ndarray, k: int) -> list[int] | None:
    n_v, n_s = cover.shape
    c = np.ones(n_s, float)
    A = np.vstack([cover.astype(float), np.ones((1, n_s))])
    lb = np.concatenate([np.ones(n_v), [0.0]])
    ub = np.concatenate([np.full(n_v, np.inf), [float(k)]])
    res = milp(c, constraints=LinearConstraint(A, lb=lb, ub=ub), bounds=Bounds(0, 1), integrality=np.ones(n_s, int))
    if res.success and res.x is not None:
        idx = [int(i) for i, x in enumerate(res.x) if x > 0.5]
        if len(idx) <= k and cover[:, idx].any(axis=1).all():
            return idx
    return None
