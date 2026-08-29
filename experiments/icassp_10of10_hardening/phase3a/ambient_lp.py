"""Unrestricted single-center LP. Independent of Phase-1 gap_for_reference."""
from __future__ import annotations

import numpy as np
from scipy.optimize import linprog

from experiments.icassp_10of10_hardening.phase3a.config import GAMMA_POS_ABS


def _pairs(V: np.ndarray, I: np.ndarray):
    nv, d = V.shape
    ni = I.shape[0]
    # A_ub x <= b :  2 c·(i-v) + γ <= ||i||^2 - ||v||^2
    n = nv * ni
    A = np.empty((n, d + 1), float)
    b = np.empty(n, float)
    k = 0
    i_norm = np.einsum("ij,ij->i", I, I)
    v_norm = np.einsum("ij,ij->i", V, V)
    for vi in range(nv):
        diff = I - V[vi]
        A[k : k + ni, :d] = 2.0 * diff
        A[k : k + ni, d] = 1.0
        b[k : k + ni] = i_norm - v_norm[vi]
        k += ni
    return A, b


def _uniform_scale(V: np.ndarray, I: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    """Isotropic scale so typical coordinate RMS is O(1). Preserves sphere separability and sign(Γ)."""
    X = np.concatenate([V, I], axis=0)
    rms = float(np.sqrt(np.mean(X * X))) if X.size else 1.0
    s = rms if rms > 1e-12 else 1.0
    return V / s, I / s, s


def linear_separable(V: np.ndarray, I: np.ndarray, method: str = "highs") -> dict:
    """Sufficient test: a halfspace separator implies an unbounded ambient-center margin."""
    nv, d = V.shape
    ni = I.shape[0]
    n = nv * ni
    A = np.empty((n, d + 1), float)
    b = np.zeros(n)
    k = 0
    for vi in range(nv):
        diff = I - V[vi]
        A[k : k + ni, :d] = -diff
        A[k : k + ni, d] = 1.0
        k += ni
    bounds = [(-1.0, 1.0)] * d + [(None, None)]
    c_obj = np.zeros(d + 1)
    c_obj[-1] = -1.0
    res = linprog(c_obj, A_ub=A, b_ub=b, bounds=bounds, method=method)
    gamma = float(res.x[-1]) if res.success and res.x is not None else None
    return {
        "success": bool(res.success),
        "gamma": gamma,
        "linearly_separable": bool(gamma is not None and gamma > GAMMA_POS_ABS),
        "message": str(res.message),
    }


def solve_primal(V: np.ndarray, I: np.ndarray, method: str = "highs") -> dict:
    """max γ  s.t. 2c^T(i-v)+γ <= ||i||^2-||v||^2."""
    if V.size == 0 or I.size == 0:
        return {"status": "UNDECIDED", "reason": "empty_set", "gamma": None, "c": None, "method": method}
    d = int(V.shape[1])
    A, b = _pairs(V, I)
    c_obj = np.zeros(d + 1)
    c_obj[-1] = -1.0  # minimize -γ
    res = linprog(c_obj, A_ub=A, b_ub=b, bounds=[(None, None)] * (d + 1), method=method)
    out = {
        "method": method,
        "success": bool(res.success),
        "status_code": int(res.status),
        "message": str(res.message),
        "n_constraints": int(A.shape[0]),
        "dim": d,
        "n_valid": int(V.shape[0]),
        "n_invalid": int(I.shape[0]),
    }
    if res.status == 3:
        out.update({"status": "INF_SEPARABLE", "gamma": "+INF", "c": None, "unbounded": True})
        return out
    if not res.success or res.x is None:
        out.update({"status": "UNDECIDED", "gamma": None, "c": None, "unbounded": False})
        return out
    x = np.asarray(res.x, float)
    gamma = float(x[-1])
    center = x[:-1]
    slacks = b - A @ x
    min_slack = float(np.min(slacks)) if len(slacks) else None
    dual = None
    if getattr(res, "ineqlin", None) is not None and getattr(res.ineqlin, "marginals", None) is not None:
        dual = np.asarray(res.ineqlin.marginals, float)
    out.update(
        {
            "status": "SOLVED",
            "gamma": gamma,
            "c": center,
            "c_norm": float(np.linalg.norm(center)),
            "min_slack": min_slack,
            "unbounded": False,
            "dual_marginals": dual,
        }
    )
    return out


def solve_dual(V: np.ndarray, I: np.ndarray, method: str = "highs") -> dict:
    """min Σ λ(||i||^2-||v||^2)  s.t. Σλ(i-v)=0, Σλ=1, λ>=0."""
    nv, d = V.shape
    ni = I.shape[0]
    n = nv * ni
    i_norm = np.einsum("ij,ij->i", I, I)
    v_norm = np.einsum("ij,ij->i", V, V)
    cost = np.empty(n, float)
    A_eq = np.empty((d + 1, n), float)
    k = 0
    for vi in range(nv):
        diff = I - V[vi]
        cost[k : k + ni] = i_norm - v_norm[vi]
        A_eq[:d, k : k + ni] = diff.T
        A_eq[d, k : k + ni] = 1.0
        k += ni
    beq = np.zeros(d + 1)
    beq[-1] = 1.0
    res = linprog(cost, A_eq=A_eq, b_eq=beq, bounds=[(0.0, None)] * n, method=method)
    out = {
        "method": method,
        "success": bool(res.success),
        "status_code": int(res.status),
        "message": str(res.message),
        "n_weights": n,
        "dim": d,
    }
    if res.status == 2:
        out.update({"status": "DUAL_INFEASIBLE", "gamma": None, "lambda": None})
        return out
    if not res.success or res.x is None:
        out.update({"status": "UNDECIDED", "gamma": None, "lambda": None})
        return out
    lam = np.asarray(res.x, float)
    obj = float(cost @ lam)
    eq_res = A_eq @ lam - beq
    out.update(
        {
            "status": "SOLVED",
            "gamma": obj,
            "lambda": lam,
            "eq_residual_inf": float(np.max(np.abs(eq_res))),
            "sum_lambda": float(np.sum(lam)),
            "n_support": int(np.sum(lam > 1e-12)),
        }
    )
    return out


def solve_ambient(V: np.ndarray, I: np.ndarray) -> tuple[dict, dict, str]:
    """Scale-stable primal/dual with linear-separability fallback. Sign(Γ) is the scientific object."""
    Vs, Is, scale = _uniform_scale(V, I)
    primal = None
    dual = None
    for method in ("highs", "highs-ipm"):
        p = solve_primal(Vs, Is, method=method)
        d = solve_dual(Vs, Is, method=method)
        p["scale"] = scale
        if p.get("status") == "INF_SEPARABLE" or d.get("status") == "DUAL_INFEASIBLE":
            p["status"] = "INF_SEPARABLE"
            p["gamma"] = "+INF"
            return p, d, "AMBIENT_SEPARABLE"
        if p.get("status") == "SOLVED" or d.get("status") == "SOLVED":
            primal, dual = p, d
            if p.get("status") == "SOLVED" and p.get("c") is not None:
                p["c"] = np.asarray(p["c"], float) * scale
                if isinstance(p.get("gamma"), (int, float)):
                    p["gamma"] = float(p["gamma"]) * (scale ** 2)
            if d.get("status") == "SOLVED" and isinstance(d.get("gamma"), (int, float)):
                d["gamma"] = float(d["gamma"]) * (scale ** 2)
            break
        primal, dual = p, d
    lin = linear_separable(Vs, Is, method="highs")
    if primal is None:
        primal = {"status": "UNDECIDED", "gamma": None, "c": None, "method": "none"}
    if dual is None:
        dual = {"status": "UNDECIDED", "gamma": None, "lambda": None}
    primal["linear_probe"] = lin
    if lin.get("linearly_separable"):
        primal["status"] = "INF_SEPARABLE"
        primal["gamma"] = "+INF"
        return primal, dual, "AMBIENT_SEPARABLE"
    kind = classify_margin(primal.get("gamma") if primal.get("status") != "INF_SEPARABLE" else "+INF")
    if kind == "UNDECIDED" and dual.get("status") == "SOLVED" and dual.get("gamma") is not None:
        kind = classify_margin(dual["gamma"])
        primal["gamma"] = dual["gamma"]
        primal["status"] = "SOLVED_VIA_DUAL"
    return primal, dual, kind


def classify_margin(gamma) -> str:
    if gamma == "+INF":
        return "AMBIENT_SEPARABLE"
    if gamma is None:
        return "UNDECIDED"
    g = float(gamma)
    if g > GAMMA_POS_ABS:
        return "AMBIENT_SEPARABLE"
    return "NO_AMBIENT_CENTER"


def pair_index(vi: int, ii: int, n_invalid: int) -> int:
    return vi * n_invalid + ii


def unpack_support(lam: np.ndarray, n_valid: int, n_invalid: int, floor: float = 1e-12) -> list[dict]:
    rows = []
    for k, w in enumerate(lam):
        if w <= floor:
            continue
        vi, ii = divmod(k, n_invalid)
        rows.append({"v_index": int(vi), "i_index": int(ii), "weight": float(w)})
    rows.sort(key=lambda r: (-r["weight"], r["v_index"], r["i_index"]))
    return rows
