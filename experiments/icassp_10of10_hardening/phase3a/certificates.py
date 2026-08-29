"""Exact-rational and high-precision certificates for the ambient-center dual/primal."""
from __future__ import annotations

from fractions import Fraction

import numpy as np

from experiments.icassp_10of10_hardening.phase3a.config import (
    DUAL_SUPPORT_ABS,
    EQUALITY_RESIDUAL_ABS,
    GAMMA_POS_ABS,
)


def f64_to_q(x: float) -> Fraction:
    return Fraction(*float(x).as_integer_ratio())


def vec_to_q(x: np.ndarray) -> list[Fraction]:
    return [f64_to_q(float(v)) for v in np.asarray(x, float).reshape(-1)]


def qdot(a: list[Fraction], b: list[Fraction]) -> Fraction:
    return sum((x * y for x, y in zip(a, b)), Fraction(0))


def qnorm2(a: list[Fraction]) -> Fraction:
    return sum((x * x for x in a), Fraction(0))


def _gauss_q(A: list[list[Fraction]], b: list[Fraction]) -> list[Fraction] | None:
    n = len(b)
    m = len(A[0]) if A else 0
    if n != m:
        return None
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        if M[piv][col] == 0:
            return None
        M[col], M[piv] = M[piv], M[col]
        div = M[col][col]
        for j in range(col, n + 1):
            M[col][j] /= div
        for r in range(n):
            if r == col:
                continue
            fac = M[r][col]
            if fac == 0:
                continue
            for j in range(col, n + 1):
                M[r][j] -= fac * M[col][j]
    return [M[i][n] for i in range(n)]


def reconstruct_dual_weights(V: np.ndarray, I: np.ndarray, lam: np.ndarray) -> dict:
    """Solve the dual equalities on a basic support using exact binary64 rationals."""
    nv, d = V.shape
    ni = I.shape[0]
    order = np.argsort(-np.asarray(lam, float))
    support = [int(k) for k in order if float(lam[k]) > DUAL_SUPPORT_ABS]
    if not support:
        return {"ok": False, "reason": "empty_support", "strength": "NUMERICAL_LP_ONLY"}
    if d > 36:
        return {
            "ok": False,
            "reason": "dimension_above_exact_rational_cap",
            "dim": d,
            "strength": "HIGH_PRECISION_DUAL_CERTIFICATE",
        }

    Vq = [vec_to_q(v) for v in V]
    Iq = [vec_to_q(i) for i in I]
    selected = []
    mat = []
    for k in support:
        vi, ii = divmod(k, ni)
        col = np.concatenate([I[ii] - V[vi], np.ones(1)])
        trial = np.array(mat + [col], float)
        if np.linalg.matrix_rank(trial, tol=1e-10) > len(selected):
            selected.append((vi, ii, k))
            mat.append(col)
        if len(selected) == d + 1:
            break
    if len(selected) < d + 1:
        return {
            "ok": False,
            "reason": "underdetermined_support",
            "n_support": len(selected),
            "strength": "HIGH_PRECISION_DUAL_CERTIFICATE",
        }
    cols_q = []
    for vi, ii, _k in selected:
        diff = [Iq[ii][j] - Vq[vi][j] for j in range(d)]
        cols_q.append(diff + [Fraction(1)])
    A = [[cols_q[j][r] for j in range(d + 1)] for r in range(d + 1)]
    rhs = [Fraction(0)] * d + [Fraction(1)]
    sol = _gauss_q(A, rhs)
    if sol is None:
        return {"ok": False, "reason": "singular_basis", "strength": "HIGH_PRECISION_DUAL_CERTIFICATE"}
    if any(w < 0 for w in sol):
        return {"ok": False, "reason": "negative_basic_weight", "strength": "HIGH_PRECISION_DUAL_CERTIFICATE"}
    return _verify_reconstructed(Vq, Iq, selected, sol, d)


def _verify_reconstructed(Vq, Iq, meta, weights: list[Fraction], d: int) -> dict:
    acc_diff = [Fraction(0)] * d
    acc_sum = Fraction(0)
    acc_obj = Fraction(0)
    stored = []
    for (vi, ii, k), w in zip(meta, weights):
        if w == 0:
            continue
        diff = [Iq[ii][j] - Vq[vi][j] for j in range(d)]
        for j in range(d):
            acc_diff[j] += w * diff[j]
        acc_sum += w
        acc_obj += w * (qnorm2(Iq[ii]) - qnorm2(Vq[vi]))
        stored.append({"v_index": int(vi), "i_index": int(ii), "pair_index": int(k), "weight_num": int(w.numerator), "weight_den": int(w.denominator)})
    eq_ok = all(x == 0 for x in acc_diff) and acc_sum == 1
    obj_nonpos = acc_obj <= 0
    return {
        "ok": bool(eq_ok),
        "exact_equalities": bool(eq_ok),
        "dual_objective": f"{acc_obj.numerator}/{acc_obj.denominator}",
        "dual_objective_nonpositive": bool(obj_nonpos),
        "sum_lambda": f"{acc_sum.numerator}/{acc_sum.denominator}",
        "n_support": len(stored),
        "support": stored,
        "strength": "EXACT_RATIONAL_CERTIFICATE" if eq_ok and obj_nonpos else (
            "EXACT_RATIONAL_CERTIFICATE" if eq_ok and not obj_nonpos else "HIGH_PRECISION_DUAL_CERTIFICATE"
        ),
        "separator_exact": bool(eq_ok and acc_obj > 0),
        "no_center_exact": bool(eq_ok and acc_obj <= 0),
    }


def verify_primal_exact(V: np.ndarray, I: np.ndarray, c: np.ndarray) -> dict:
    """Evaluate Γ(c) = min_{v,i} [||i||^2-||v||^2-2c·(i-v)] in exact binary64 rationals."""
    cq = vec_to_q(c)
    Vq = [vec_to_q(v) for v in V]
    Iq = [vec_to_q(i) for i in I]
    best = None
    pair = None
    for vi, v in enumerate(Vq):
        nv = qnorm2(v)
        for ii, i in enumerate(Iq):
            val = qnorm2(i) - nv - 2 * qdot(cq, [i[j] - v[j] for j in range(len(cq))])
            if best is None or val < best:
                best = val
                pair = (vi, ii)
    return {
        "gamma_exact": f"{best.numerator}/{best.denominator}" if best is not None else None,
        "gamma_positive": bool(best is not None and best > 0),
        "gamma_nonpositive": bool(best is not None and best <= 0),
        "witness_pair": {"v_index": pair[0], "i_index": pair[1]} if pair else None,
        "strength": "EXACT_RATIONAL_CERTIFICATE" if best is not None else "UNDECIDED",
    }


def verify_dual_numeric(V: np.ndarray, I: np.ndarray, lam: np.ndarray) -> dict:
    nv, d = V.shape
    ni = I.shape[0]
    i_norm = np.einsum("ij,ij->i", I, I)
    v_norm = np.einsum("ij,ij->i", V, V)
    acc = np.zeros(d, float)
    obj = 0.0
    s = 0.0
    for k, w in enumerate(lam):
        if w == 0.0:
            continue
        vi, ii = divmod(k, ni)
        acc += w * (I[ii] - V[vi])
        obj += w * (i_norm[ii] - v_norm[vi])
        s += w
    return {
        "sum_lambda": float(s),
        "eq_residual_inf": float(np.max(np.abs(acc))) if d else 0.0,
        "dual_objective": float(obj),
        "eq_ok": bool(abs(s - 1.0) <= EQUALITY_RESIDUAL_ABS and (d == 0 or np.max(np.abs(acc)) <= EQUALITY_RESIDUAL_ABS)),
    }


def strength_for_task(kind: str, primal: dict, dual: dict, exact_primal: dict | None, exact_dual: dict | None) -> str:
    if kind == "UNDECIDED":
        return "UNDECIDED"
    if kind == "AMBIENT_SEPARABLE":
        if exact_primal and exact_primal.get("gamma_positive"):
            return "EXACT_RATIONAL_CERTIFICATE"
        if primal.get("gamma") == "+INF":
            return "HIGH_PRECISION_DUAL_CERTIFICATE"
        g = primal.get("gamma")
        if g is not None and float(g) > GAMMA_POS_ABS and primal.get("min_slack", 0) > GAMMA_POS_ABS:
            return "HIGH_PRECISION_DUAL_CERTIFICATE"
        return "NUMERICAL_LP_ONLY"
    # NO_AMBIENT_CENTER
    if exact_dual and exact_dual.get("no_center_exact"):
        return "EXACT_RATIONAL_CERTIFICATE"
    dn = dual.get("eq_residual_inf")
    g = dual.get("gamma")
    if dual.get("status") == "SOLVED" and dn is not None and dn <= EQUALITY_RESIDUAL_ABS and g is not None and float(g) <= GAMMA_POS_ABS:
        return "HIGH_PRECISION_DUAL_CERTIFICATE"
    if primal.get("status") == "SOLVED" and primal.get("gamma") is not None and float(primal["gamma"]) <= GAMMA_POS_ABS:
        return "NUMERICAL_LP_ONLY"
    return "UNDECIDED"
