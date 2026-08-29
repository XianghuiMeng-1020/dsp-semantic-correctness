"""DSP-native Type-I feasible-set probing.

Directions are frozen before observing disagreement. Every accepted
candidate must later pass the independent verifier.

This is a numerical LP on a finite frequency grid, not a proof that
the continuous feasible set is nonempty in a given direction.
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import linprog

from src.verification.canonicalize import canonicalize_fir, is_type1
from src.verification.registry_io import is_fir

PROBE_SEED = 20260826
CONSTRAINT_PTS_PER_BAND = 512
LINPROG_METHOD = "highs"


def response_type(task: dict) -> str:
    return str(task["type"]).split("_", 1)[1]


# registry_io may not have response_type_safe — define locally
def _rtype(task: dict) -> str:
    return str(task["type"]).split("_", 1)[1]


def type1_from_theta(theta: np.ndarray) -> np.ndarray:
    theta = np.asarray(theta, float).reshape(-1)
    return np.concatenate([theta[:-1], theta[-1:], theta[-2::-1]])


def theta_from_type1(h: np.ndarray) -> np.ndarray:
    h = np.asarray(h, float).reshape(-1)
    m = (len(h) - 1) // 2
    return h[: m + 1].copy()


def amplitude_matrix(n_taps: int, omega: np.ndarray) -> np.ndarray:
    """A(ω) = θ[M] + 2 Σ_k θ[M-k] cos(kω), θ = first half including center."""
    m = (n_taps - 1) // 2
    c = np.zeros((len(omega), m + 1), float)
    c[:, m] = 1.0
    for k in range(1, m + 1):
        c[:, m - k] = 2.0 * np.cos(k * omega)
    return c


def band_omegas(task: dict, n_pts: int = CONSTRAINT_PTS_PER_BAND):
    fs = float(task["sampling_rate"])
    rows = []
    for band in list(task["pass_band"]) + list(task["stop_band"]):
        f = np.linspace(float(band["f0"]), float(band["f1"]), int(n_pts))
        omega = 2.0 * np.pi * f / fs
        role = "pass" if float(band["lo"]) >= 0.5 else "stop"
        rows.append((omega, float(band["lo"]), float(band["hi"]), role, f))
    return rows


def constraint_system(task: dict, n_taps: int):
    blocks = []
    bounds_ub = []
    meta = []
    floor = float(task.get("residual_floor") or 1e-6)
    for omega, lo, hi, role, f in band_omegas(task):
        span = max(hi - lo, 1e-6)
        # Predetermined interior margin so grid-feasible vertices survive
        # the denser independent verifier. Not tuned per candidate.
        margin = max(20.0 * floor * span, 2e-4)
        if hi - lo <= 2.0 * margin:
            margin = 0.25 * span
        lo_s, hi_s = lo + margin, hi - margin
        a = amplitude_matrix(n_taps, omega)
        blocks.append(a)
        bounds_ub.append(np.full(len(omega), hi_s))
        meta.append((role, "upper", f, hi_s))
        if role == "pass":
            blocks.append(-a)
            bounds_ub.append(np.full(len(omega), -lo_s))
            meta.append((role, "lower", f, lo_s))
        else:
            blocks.append(-a)
            bounds_ub.append(np.full(len(omega), hi_s))
            meta.append((role, "neg_upper", f, hi_s))
    A_ub = np.vstack(blocks)
    b_ub = np.concatenate(bounds_ub)
    return A_ub, b_ub


def frozen_directions(n_theta: int, extras: list[np.ndarray] | None = None) -> list[dict]:
    """Predetermined directions. extras must themselves be predetermined (library diffs)."""
    rng = np.random.default_rng(PROBE_SEED)
    dirs = []
    eye = np.eye(n_theta)
    for i in range(n_theta):
        dirs.append({"name": f"basis_{i}", "q": eye[i], "family": "basis"})
    dirs.append({"name": "all_ones", "q": np.ones(n_theta), "family": "tap_combo"})
    alt = np.ones(n_theta)
    alt[1::2] = -1.0
    dirs.append({"name": "alternating", "q": alt, "family": "tap_combo"})
    e0 = np.zeros(n_theta)
    e0[0] = 1.0
    dirs.append({"name": "first_tap", "q": e0, "family": "tap_combo"})
    em = np.zeros(n_theta)
    em[-1] = 1.0
    dirs.append({"name": "center_tap", "q": em, "family": "tap_combo"})
    for i in range(16):
        q = rng.standard_normal(n_theta)
        nrm = float(np.linalg.norm(q))
        if nrm < 1e-18:
            continue
        dirs.append({"name": f"random_{i:02d}", "q": q / nrm, "family": "random_frozen_seed"})
    if extras:
        for j, q in enumerate(extras):
            q = np.asarray(q, float).reshape(-1)
            if len(q) != n_theta:
                continue
            nrm = float(np.linalg.norm(q))
            if nrm < 1e-18:
                continue
            dirs.append({"name": f"library_diff_{j}", "q": q / nrm, "family": "library_diff"})
    # normalize all
    out = []
    for d in dirs:
        q = np.asarray(d["q"], float)
        nrm = float(np.linalg.norm(q))
        if nrm < 1e-18:
            continue
        out.append({**d, "q": q / nrm})
    return out


def probe_direction(task: dict, n_taps: int, q: np.ndarray, sense: str = "max"):
    A_ub, b_ub = constraint_system(task, n_taps)
    c = -np.asarray(q, float) if sense == "max" else np.asarray(q, float)
    try:
        res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=(None, None), method=LINPROG_METHOD)
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "reason": f"linprog_exception:{type(exc).__name__}"}
    if not res.success or res.x is None:
        return {"ok": False, "reason": f"infeasible_or_fail:{res.message}"}
    theta = np.asarray(res.x, float)
    h = type1_from_theta(theta)
    return {"ok": True, "theta": theta, "h": h, "fun": float(res.fun), "nit": int(res.nit)}


def eligible_type1_fir(task: dict) -> bool:
    return is_fir(task) and _rtype(task) in {"lp", "hp", "bp", "bs"}


def backoff_to_independent(task_id: str, href, h_star, n_bisect: int = 24):
    """Line search h(α)=(1-α)h_r+α h* for the largest independently valid α.

    Predetermined numerical repair. Directions are not changed.
    """
    from src.verification.independent_spec_verifier import verify_ok

    href = np.asarray(href, float).reshape(-1)
    h_star = np.asarray(h_star, float).reshape(-1)
    if len(href) != len(h_star):
        return None, 0.0, "length_mismatch"
    if verify_ok(task_id, h_star, grid_n=8192):
        return h_star, 1.0, "vertex"
    lo, hi = 0.0, 1.0
    best, best_a = None, 0.0
    n_bisect = min(int(n_bisect), 12)
    for _ in range(n_bisect):
        mid = 0.5 * (lo + hi)
        h = (1.0 - mid) * href + mid * h_star
        if verify_ok(task_id, h):
            lo = mid
            best, best_a = h, mid
        else:
            hi = mid
    if best is None or best_a <= 1e-8:
        return None, best_a, "backoff_collapsed_to_reference"
    return best, best_a, "backoff"


def run_probes_for_task(task: dict, href, library_same_order: list) -> list[dict]:
    if not eligible_type1_fir(task):
        return []
    cref = canonicalize_fir(href)
    if not cref.type1:
        return [{"ok": False, "reason": "reference_not_type1", "name": "ref_check"}]
    n_taps = cref.n_taps
    theta_r = theta_from_type1(cref.h)
    extras = []
    for h in library_same_order:
        ch = canonicalize_fir(h)
        if ch.n_taps == n_taps and is_type1(ch.h):
            extras.append(theta_from_type1(ch.h) - theta_r)
    dirs = frozen_directions(len(theta_r), extras)
    results = []
    for d in dirs:
        for sense in ("max", "min"):
            out = probe_direction(task, n_taps, d["q"], sense=sense)
            rec = {
                "direction": d["name"],
                "family": d["family"],
                "sense": sense,
                "n_taps": n_taps,
            }
            rec.update(out)
            results.append(rec)
    return results
