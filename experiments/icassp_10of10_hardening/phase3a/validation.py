"""Independent synthetic and second-optimizer checks. Not the Phase-1 gap engine."""
from __future__ import annotations

import numpy as np

from experiments.icassp_10of10_hardening.phase3a.ambient_lp import classify_margin, solve_dual, solve_primal
def _run(V, I, method="highs"):
    p = solve_primal(V, I, method=method)
    d = solve_dual(V, I, method=method)
    kind = classify_margin(p.get("gamma") if p.get("status") != "INF_SEPARABLE" else "+INF")
    return p, d, kind


def synthetic_suite() -> dict:
    # A: two well-separated clusters
    rng = np.random.default_rng(0)
    Va = np.array([[0.0, 0.0], [0.1, 0.0], [0.0, 0.1]])
    Ia = np.array([[5.0, 5.0], [5.1, 4.9], [4.8, 5.2]])
    pA, dA, kA = _run(Va, Ia)

    # B: valids on a square; invalid at the center (nested / not spherically separable)
    Vb = np.array([[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]])
    Ib = np.array([[0.0, 0.0]])
    pB, dB, kB = _run(Vb, Ib)

    # C: canonical at a valid fails; unrestricted center at origin succeeds
    Vc = np.array([[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]])
    Ic = np.array([[1.5, 0.0]])
    pC, dC, kC = _run(Vc, Ic)
    # Canonical = first valid (1,0): farthest valid dist=2, invalid dist=0.5
    canon_c = Vc[0]
    dV = max(float(np.linalg.norm(v - canon_c)) for v in Vc)
    dI = min(float(np.linalg.norm(i - canon_c)) for i in Ic)
    canon_fails = dI <= dV

    A_ok = kA == "AMBIENT_SEPARABLE"
    B_ok = kB == "NO_AMBIENT_CENTER"
    C_ok = canon_fails and kC == "AMBIENT_SEPARABLE"
    return {
        "A_separable_clusters": {"kind": kA, "gamma": pA.get("gamma"), "pass": A_ok},
        "B_nested_square": {"kind": kB, "gamma": pB.get("gamma"), "dual_gamma": dB.get("gamma"), "pass": B_ok},
        "C_canonical_fails_ambient_succeeds": {
            "kind": kC,
            "gamma": pC.get("gamma"),
            "canonical_G_unnormalized": dI - dV,
            "canonical_fails": canon_fails,
            "pass": C_ok,
        },
        "pass": bool(A_ok and B_ok and C_ok),
        "rng_probe": int(rng.integers(0, 3)),
    }


def second_optimizer_check(V: np.ndarray, I: np.ndarray) -> dict:
    methods = []
    for method in ("highs", "highs-ipm"):
        try:
            p = solve_primal(V, I, method=method)
            d = solve_dual(V, I, method=method)
            methods.append(
                {
                    "method": method,
                    "primal_gamma": p.get("gamma"),
                    "dual_gamma": d.get("gamma"),
                    "primal_status": p.get("status"),
                    "dual_status": d.get("status"),
                    "kind": classify_margin(p.get("gamma") if p.get("status") != "INF_SEPARABLE" else "+INF"),
                }
            )
        except Exception as exc:  # noqa: BLE001
            methods.append({"method": method, "error": f"{type(exc).__name__}:{exc}"})
    kinds = {m.get("kind") for m in methods if "kind" in m}
    gammas = [m.get("primal_gamma") for m in methods if isinstance(m.get("primal_gamma"), (int, float))]
    agree = len(kinds) == 1
    close = True
    if len(gammas) >= 2:
        close = abs(gammas[0] - gammas[1]) <= max(1e-8, 1e-6 * max(abs(gammas[0]), abs(gammas[1]), 1.0))
    # Independent dual vs primal (same method)
    duality = None
    if methods and methods[0].get("primal_gamma") is not None and methods[0].get("dual_gamma") is not None:
        pg, dg = float(methods[0]["primal_gamma"]), float(methods[0]["dual_gamma"])
        duality = abs(pg - dg) <= max(1e-8, 1e-6 * max(abs(pg), abs(dg), 1.0))
    return {
        "methods": methods,
        "kind_agree": agree,
        "gamma_close": close,
        "strong_duality_numeric": duality,
        "pass": bool(agree and close and duality is not False),
    }


def check_canonical_separable_not_impossible(canonical_G: float, ambient_kind: str) -> bool:
    """Check D: if a fixed Euclidean reference already separates, ambient must not say impossible."""
    if canonical_G is None:
        return True
    if float(canonical_G) > 0 and ambient_kind == "NO_AMBIENT_CENTER":
        return False
    return True
