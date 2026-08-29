"""Observed-valid reference catalog complexity for one metric."""
from __future__ import annotations

import json

import numpy as np

from experiments.icassp_10of10_hardening.phase1.universe import load_frozen_universe
from experiments.icassp_10of10_hardening.phase3b.config import (
    FROZEN_DIR,
    G_ZERO_ABS,
    PHASE1_DIR,
    RHO_HIGH,
    RHO_LOW,
    RHO_MOD,
)
from experiments.icassp_10of10_hardening.phase3b.pairwise import coeff_matrices, gap_of_catalog, resp_matrices
from experiments.icassp_10of10_hardening.phase3b.setcover import exact_set_cover


def _existing_k(multi: list, tid: str, metric: str) -> dict:
    row = next(r for r in multi if r["task_id"] == tid)
    out = {}
    for ks in row["k_sweep"]:
        k = ks["K"]
        exact = bool((ks.get(metric) or {}).get("exact_threshold_exists"))
        if k == 1:
            out["K1"] = exact
        elif k == 3:
            out["K3"] = exact
        elif k == 5:
            out["K5"] = exact
        elif isinstance(k, str) and str(k).startswith("all"):
            out["all_library"] = exact
            out["all_library_n"] = ks.get("available")
    return out


def _phase1_k1(p1: dict, tid: str, metric: str) -> dict:
    rec = p1[tid][metric]
    return {
        "canonical_G": rec["canonical_G_frozen"],
        "best_observed_G": rec["Gobs_star"],
        "canonical_exact": bool(rec["canonical_G_frozen"] is not None and rec["canonical_G_frozen"] > G_ZERO_ABS),
        "best_observed_exact": bool(rec["Gobs_star"] is not None and rec["Gobs_star"] > G_ZERO_ABS),
    }


def _burden(rho: float | None) -> str | None:
    if rho is None:
        return None
    if rho <= RHO_LOW:
        return "low"
    if rho <= RHO_MOD:
        return "moderate"
    if rho <= RHO_HIGH:
        return "high"
    return "near_enumerative"


def _collisions(vv: np.ndarray, iv: np.ndarray, vids: list[str], iids: list[str]) -> list[dict]:
    hits = []
    for r in range(vv.shape[1]):
        for i in range(iv.shape[0]):
            if float(iv[i, r]) <= G_ZERO_ABS:
                hits.append({"valid": vids[r], "invalid": iids[i], "d": float(iv[i, r])})
    return hits


def solve_task(vv: np.ndarray, iv: np.ndarray, vids: list[str], candidate_cols: list[int] | None = None) -> dict:
    nV = vv.shape[0]
    cols = list(range(nV)) if candidate_cols is None else list(candidate_cols)
    if not cols:
        return {"status": "UNDECIDED", "K_obs_star": None, "reason": "no_candidates"}
    taus = np.unique(vv[:, cols].reshape(-1))
    taus = [float(t) for t in taus if t >= 0.0]
    best = None
    n_regimes = 0
    for tau in taus:
        safe = [c for c in cols if float(np.min(iv[:, c])) > tau + 0.0 and float(np.min(iv[:, c])) - tau > G_ZERO_ABS]
        if not safe:
            continue
        cover = vv[:, safe] <= tau
        if not cover.any(axis=1).all():
            continue
        n_regimes += 1
        sol = exact_set_cover(cover)
        if sol["status"] not in {"EXACT_OPTIMUM", "BOUND_ONLY"} or not sol["indices"]:
            continue
        idx = [safe[j] for j in sol["indices"]]
        gap = gap_of_catalog(vv, iv, idx)
        if gap["G_R"] is None or gap["G_R"] <= G_ZERO_ABS:
            continue
        rec = {
            "tau": tau,
            "K": len(idx),
            "indices": idx,
            "ids": [vids[i] for i in idx],
            "gap": gap,
            "solver": sol,
            "n_safe": len(safe),
        }
        if best is None or rec["K"] < best["K"] or (rec["K"] == best["K"] and rec["gap"]["G_R"] > best["gap"]["G_R"]):
            best = rec
            if best["K"] == 1:
                break
    if best is None:
        return {
            "status": "UNDECIDED" if n_regimes == 0 else "INFEASIBLE",
            "K_obs_star": None,
            "n_regimes_feasible": n_regimes,
        }
    status = best["solver"]["status"]
    if status == "BOUND_ONLY":
        opt = "BOUND_ONLY"
    else:
        opt = "EXACT_OPTIMUM"
    covers = {}
    for i in best["indices"]:
        covers[vids[i]] = [vids[v] for v in range(nV) if vv[v, i] <= best["tau"]]
    nearest_inv = {}
    for i in best["indices"]:
        j = int(np.argmin(iv[:, i]))
        nearest_inv[vids[i]] = {"invalid_index": j, "d": float(iv[j, i])}
    return {
        "status": opt,
        "K_obs_star": best["K"],
        "tau": best["tau"],
        "catalog_ids": best["ids"],
        "catalog_indices": best["indices"],
        "D_V": best["gap"]["D_V"],
        "D_I": best["gap"]["D_I"],
        "G_R": best["gap"]["G_R"],
        "covers": covers,
        "nearest_invalid": nearest_inv,
        "solver": {k: best["solver"][k] for k in best["solver"] if k != "indices"},
        "n_regimes_feasible": n_regimes,
    }


def run_metric(metric: str) -> dict:
    uni = load_frozen_universe()
    multi = json.loads((FROZEN_DIR / "multi_reference.json").read_text(encoding="utf-8"))
    p1 = {r["task_id"]: r for r in json.loads((PHASE1_DIR / "best_observed_reference.json").read_text(encoding="utf-8"))["tasks"]}
    tasks = []
    for pack in uni["tasks"]:
        tid = pack["task_id"]
        valids = pack["valids"]
        invalids = pack["primary_invalids"]
        vids = [v["cid"] for v in valids]
        iids = [v["cid"] for v in invalids]
        print(f"[phase3b] {metric} pairwise {tid} V={len(valids)} I={len(invalids)}", flush=True)
        if metric == "coeff":
            vv, iv = coeff_matrices(valids, invalids, pack["task"])
        else:
            vv, iv = resp_matrices(valids, invalids, pack["task"])
        collisions = _collisions(vv, iv, vids, iids)
        primary = solve_task(vv, iv, vids)
        lib_idx = [j for j, v in enumerate(valids) if v.get("source") == "library"]
        library = solve_task(vv, iv, vids, candidate_cols=lib_idx) if lib_idx else {"status": "NO_LIBRARY", "K_obs_star": None}
        kstar = primary.get("K_obs_star")
        rho = None if kstar is None else kstar / len(valids)
        row = {
            "task": tid,
            "family": pack["family"],
            "metric": metric,
            "n_valid": len(valids),
            "n_invalid": len(invalids),
            "self_distance_max": float(np.max(np.diag(vv))),
            "zero_distance_collisions": collisions,
            "existing": _existing_k(multi, tid, metric),
            "phase1": _phase1_k1(p1, tid, metric),
            "primary": primary,
            "library": library,
            "K_obs_star": kstar,
            "rho": rho,
            "burden_band": _burden(rho),
        }
        tasks.append(row)
        print(
            f"    {tid} K*={kstar} ρ={rho} status={primary.get('status')} collisions={len(collisions)}",
            flush=True,
        )
    return {"metric": metric, "tasks": tasks}


def summarize(bundle: dict) -> dict:
    rows = [t for t in bundle["tasks"] if t["K_obs_star"] is not None]
    exact = sum(1 for t in bundle["tasks"] if t["primary"].get("status") == "EXACT_OPTIMUM")
    bound = sum(1 for t in bundle["tasks"] if t["primary"].get("status") == "BOUND_ONLY")
    und = sum(1 for t in bundle["tasks"] if t["primary"].get("status") not in {"EXACT_OPTIMUM", "BOUND_ONLY"})
    ks = [t["K_obs_star"] for t in rows]
    rhos = [t["rho"] for t in rows]
    bands = {b: sum(1 for t in rows if t["burden_band"] == b) for b in ("low", "moderate", "high", "near_enumerative")}

    def cnt(pred):
        return sum(1 for k in ks if pred(k))

    collisions = sum(len(t["zero_distance_collisions"]) for t in bundle["tasks"])
    return {
        "n_tasks": len(bundle["tasks"]),
        "exact_optimum": exact,
        "bound_only": bound,
        "undecided": und,
        "k1": cnt(lambda k: k == 1),
        "k2": cnt(lambda k: k == 2),
        "k_le3": cnt(lambda k: k <= 3),
        "k3_5": cnt(lambda k: 3 <= k <= 5),
        "k6_10": cnt(lambda k: 6 <= k <= 10),
        "k_gt10": cnt(lambda k: k > 10),
        "median_k": float(np.median(ks)) if ks else None,
        "min_k": min(ks) if ks else None,
        "max_k": max(ks) if ks else None,
        "median_rho": float(np.median(rhos)) if rhos else None,
        "min_rho": min(rhos) if rhos else None,
        "max_rho": max(rhos) if rhos else None,
        "bands": bands,
        "zero_distance_collisions": collisions,
        "n_with_k": len(rows),
    }
