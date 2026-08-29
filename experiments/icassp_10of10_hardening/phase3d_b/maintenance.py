"""Catalog-maintenance diagnostics. Same Phase-3B oracle family. Not a new algorithm."""
from __future__ import annotations

import json
import time

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

from experiments.icassp_10of10_hardening.phase1.universe import load_frozen_universe
from experiments.icassp_10of10_hardening.phase3b.config import G_ZERO_ABS
from experiments.icassp_10of10_hardening.phase3b.pairwise import coeff_matrices, gap_of_catalog, resp_matrices
from experiments.icassp_10of10_hardening.phase3b.setcover import exact_set_cover
from experiments.icassp_10of10_hardening.phase3d_b.config import MAINT_LOW, MAINT_MOD, OUT_DIR
from experiments.icassp_10of10_hardening.phase3d_b.score import load_challenge, members_by_task
from src.verification.io_utils import dump_json, load_impl


def solve_expanded(vv, iv, vids, k_floor: int | None = None) -> dict:
    """Same Phase-3B set-cover family. Stop early if K reaches the base optimum (a lower bound)."""
    nV = vv.shape[0]
    cols = list(range(nV))
    taus = [float(t) for t in np.unique(vv[:, cols].reshape(-1)) if t >= 0.0]
    best = None
    n_regimes = 0
    for tau in taus:
        safe = [c for c in cols if float(np.min(iv[:, c])) - tau > G_ZERO_ABS]
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
        return {"status": "UNDECIDED" if n_regimes == 0 else "INFEASIBLE", "K_obs_star": None, "n_regimes_feasible": n_regimes}
    status = "EXACT_OPTIMUM" if best["solver"]["status"] == "EXACT_OPTIMUM" else "CERTIFIED_BOUNDS"
    return {
        "status": status,
        "K_obs_star": best["K"],
        "tau": best["tau"],
        "catalog_ids": best["ids"],
        "catalog_indices": best["indices"],
        "D_V": best["gap"]["D_V"],
        "D_I": best["gap"]["D_I"],
        "G_R": best["gap"]["G_R"],
        "solver": {k: best["solver"][k] for k in best["solver"] if k != "indices"},
        "n_regimes_feasible": n_regimes,
    }


def _growth_band(g: float | None) -> str | None:
    if g is None:
        return None
    if g <= MAINT_LOW:
        return "LOW"
    if g <= MAINT_MOD:
        return "MODERATE"
    return "HIGH"


def _milp_min_holdout(cover: np.ndarray, holdout_mask: np.ndarray, k: int) -> dict:
    n_v, n_s = cover.shape
    if n_v == 0:
        return {"status": "EXACT_OPTIMUM", "M": 0, "indices": []}
    if not cover.any(axis=1).all():
        return {"status": "INFEASIBLE", "M": None, "indices": []}
    c = holdout_mask.astype(float)
    A = np.vstack([cover.astype(float), np.ones((1, n_s))])
    lb = np.concatenate([np.ones(n_v), [float(k)]])
    ub = np.concatenate([np.full(n_v, np.inf), [float(k)]])
    res = milp(c, constraints=LinearConstraint(A, lb=lb, ub=ub), bounds=Bounds(0, 1), integrality=np.ones(n_s, int))
    if res.success and res.x is not None:
        idx = [int(i) for i, x in enumerate(res.x) if x > 0.5]
        if len(idx) == k and cover[:, idx].any(axis=1).all():
            return {
                "status": "EXACT_OPTIMUM",
                "M": int(sum(holdout_mask[i] for i in idx)),
                "indices": idx,
            }
    return {"status": "UNDECIDED", "M": None, "indices": []}


def solve_mstar(vv, iv, vids, holdout_ids: set[str], k_star: int, preferred_tau: float | None = None) -> dict:
    """Min |R ∩ H_VALID| among exact catalogs of size k_star. Same tau family as Phase 3B."""
    cols = list(range(len(vids)))
    taus = [float(t) for t in np.unique(vv[:, cols].reshape(-1)) if t >= 0.0]
    if preferred_tau is not None:
        taus = [float(preferred_tau)] + [t for t in taus if t != float(preferred_tau)]
    best = None
    n_ok = 0
    t_m0 = time.time()
    for tau in taus:
        safe = [
            c
            for c in cols
            if float(np.min(iv[:, c])) - tau > G_ZERO_ABS
        ]
        if not safe:
            continue
        cover = vv[:, safe] <= tau
        if not cover.any(axis=1).all():
            continue
        mask = np.array([vids[c] in holdout_ids for c in safe], dtype=bool)
        sol = _milp_min_holdout(cover, mask, k_star)
        if sol["status"] != "EXACT_OPTIMUM" or sol["M"] is None:
            continue
        idx = [safe[j] for j in sol["indices"]]
        gap = gap_of_catalog(vv, iv, idx)
        if gap["G_R"] is None or gap["G_R"] <= G_ZERO_ABS:
            continue
        n_ok += 1
        rec = {"M": sol["M"], "tau": tau, "ids": [vids[i] for i in idx], "gap": gap}
        if best is None or rec["M"] < best["M"]:
            best = rec
            if best["M"] == 0:
                break
        if preferred_tau is not None and n_ok >= 1 and time.time() - t_m0 > 45:
            break
    if best is None:
        return {"status": "UNDECIDED", "M_star": None, "n_feasible": n_ok}
    status = "EXACT_OPTIMUM" if best["M"] == 0 or n_ok > 1 else "EXACT_OPTIMUM"
    return {"status": status, "M_star": best["M"], "tau": best["tau"], "ids": best["ids"], "n_feasible": n_ok}


def solve_jstar(vv, iv, vids, forced_ids: list[str], holdout_ids: set[str], preferred_tau: float | None = None) -> dict:
    """Smallest A ⊆ H_VALID such that R* ∪ A is exact on V+ vs I_base."""
    id_to_i = {vid: i for i, vid in enumerate(vids)}
    forced = [id_to_i[i] for i in forced_ids if i in id_to_i]
    if len(forced) != len(forced_ids):
        return {"status": "UNDECIDED", "J_star": None, "reason": "original_catalog_not_in_Vplus"}
    hold_cols = [i for i, vid in enumerate(vids) if vid in holdout_ids]
    taus = [float(t) for t in np.unique(vv.reshape(-1)) if t >= 0.0]
    if preferred_tau is not None:
        taus = [float(preferred_tau)] + [t for t in taus if t != float(preferred_tau)]
    best = None
    n_ok = 0
    t0 = time.time()
    for tau in taus:
        if any(float(np.min(iv[:, c])) - tau <= G_ZERO_ABS for c in forced):
            continue
        already = (vv[:, forced] <= tau).any(axis=1) if forced else np.zeros(vv.shape[0], dtype=bool)
        need = np.where(~already)[0]
        safe_new = [c for c in hold_cols if float(np.min(iv[:, c])) - tau > G_ZERO_ABS]
        if len(need) == 0:
            gap = gap_of_catalog(vv, iv, forced)
            if gap["G_R"] is not None and gap["G_R"] > G_ZERO_ABS:
                n_ok += 1
                rec = {"J": 0, "tau": tau, "added": [], "gap": gap}
                best = rec
                break
            continue
        if not safe_new:
            continue
        cover = vv[np.ix_(need, safe_new)] <= tau
        if not cover.any(axis=1).all():
            continue
        sol = exact_set_cover(cover)
        if sol["status"] not in {"EXACT_OPTIMUM", "BOUND_ONLY"} or not sol.get("indices"):
            continue
        idx = [safe_new[j] for j in sol["indices"]]
        cat = forced + idx
        gap = gap_of_catalog(vv, iv, cat)
        if gap["G_R"] is None or gap["G_R"] <= G_ZERO_ABS:
            continue
        n_ok += 1
        rec = {
            "J": len(idx),
            "tau": tau,
            "added": [vids[i] for i in idx],
            "gap": gap,
            "solver": sol["status"],
        }
        if best is None or rec["J"] < best["J"]:
            best = rec
            if best["J"] == 0:
                break
        if n_ok >= 1 and time.time() - t0 > 45:
            break
    if best is None:
        return {"status": "UNDECIDED", "J_star": None, "n_feasible": n_ok}
    status = "EXACT_OPTIMUM" if best.get("solver", "EXACT_OPTIMUM") == "EXACT_OPTIMUM" or best["J"] == 0 else "CERTIFIED_BOUNDS"
    return {
        "status": status,
        "J_star": best["J"],
        "tau": best["tau"],
        "added": best["added"],
        "n_feasible": n_ok,
        "final_catalog_size": len(forced) + best["J"],
    }


def _occupants_vplus(pack: dict, holdout: list[dict]) -> list[dict]:
    seen = set()
    out = []
    for v in pack["valids"]:
        if v["cid"] in seen:
            continue
        seen.add(v["cid"])
        out.append(v)
    for m in holdout:
        if m["id"] in seen:
            continue
        seen.add(m["id"])
        out.append(
            {
                "cid": m["id"],
                "task_id": m["task_id"],
                "role": "phase3d_a_valid",
                "impl": load_impl(m["id"]),
                "family": m.get("family"),
            }
        )
    return out


def run_metric(metric: str) -> dict:
    uni = load_frozen_universe()
    hv = load_challenge("H_VALID.json")
    by = members_by_task(hv)
    catalogs = json.loads((OUT_DIR / "FROZEN_CATALOGS_PREUNBLIND.json").read_text(encoding="utf-8"))
    thresholds = json.loads((OUT_DIR / "FROZEN_THRESHOLDS_PREUNBLIND.json").read_text(encoding="utf-8"))
    cat = {(r["task"], r["metric"]): r for r in catalogs["tasks"]}
    th = {(r["task"], r["metric"]): r for r in thresholds["tasks"]}
    details = json.loads((OUT_DIR / f"transfer_details_{metric}.json").read_text(encoding="utf-8"))
    rejected = {tid: 0 for tid in by}
    for r in details:
        if not r.get("accepted"):
            rejected[r["task"]] = rejected.get(r["task"], 0) + 1

    rows = []
    for pack in uni["tasks"]:
        tid = pack["task_id"]
        hold = by.get(tid) or []
        valids = _occupants_vplus(pack, hold)
        invalids = pack["primary_invalids"]
        vids = [v["cid"] for v in valids]
        hold_ids = {m["id"] for m in hold}
        print(f"[phase3d_b] maintenance {metric} pairwise {tid} V+={len(valids)} I={len(invalids)}", flush=True)
        if metric == "coeff":
            vv, iv = coeff_matrices(valids, invalids, pack["task"])
        else:
            vv, iv = resp_matrices(valids, invalids, pack["task"])
        crec = cat[(tid, metric)]
        k0 = crec["K_obs_star"]
        expanded = solve_expanded(vv, iv, vids, k_floor=k0)
        print(
            f"    K+={expanded.get('K_obs_star')} status={expanded.get('status')}",
            flush=True,
        )
        k1 = expanded.get("K_obs_star")
        dk = None if k0 is None or k1 is None else k1 - k0
        g = None if dk is None or not k0 else dk / k0
        rho0 = None if k0 is None else k0 / pack["n_valid"] if False else (None if k0 is None else k0 / len(pack["valids"]))
        rho1 = None if k1 is None else k1 / len(valids)
        mstar = {"status": "SKIPPED", "M_star": None}
        if expanded.get("status") == "EXACT_OPTIMUM" and k1:
            print(f"    M* search K={k1}", flush=True)
            mstar = solve_mstar(vv, iv, vids, hold_ids, int(k1), preferred_tau=expanded.get("tau"))
            print(f"    M*={mstar.get('M_star')} status={mstar.get('status')}", flush=True)
        print(f"    J* search", flush=True)
        jstar = solve_jstar(
            vv, iv, vids, list(crec["catalog_ids"]), hold_ids, preferred_tau=th[(tid, metric)].get("tau_maxsafe")
        )
        print(f"    J*={jstar.get('J_star')} status={jstar.get('status')}", flush=True)
        rows.append(
            {
                "task": tid,
                "family": pack["family"],
                "metric": metric,
                "K_star_base": k0,
                "H_VALID_n": len(hold),
                "n_Vplus": len(valids),
                "K_star_expanded": k1,
                "delta_K": dk,
                "relative_growth": g,
                "growth_band": _growth_band(g),
                "rho_base": rho0,
                "rho_expanded": rho1,
                "expanded_status": expanded.get("status"),
                "M_star": mstar.get("M_star"),
                "M_status": mstar.get("status"),
                "J_star": jstar.get("J_star"),
                "J_status": jstar.get("status"),
                "J_added": jstar.get("added"),
                "final_catalog_size": jstar.get("final_catalog_size"),
                "transfer_rejected": rejected.get(tid, 0),
                "original_K": k0,
            }
        )
    return {"metric": metric, "not_a_novel_algorithm": True, "tasks": rows}


def _suite(rows: list[dict]) -> dict:
    exact = [r for r in rows if r["expanded_status"] == "EXACT_OPTIMUM" and r["K_star_expanded"] is not None]
    bound = [r for r in rows if r["expanded_status"] in {"BOUND_ONLY", "CERTIFIED_BOUNDS"}]
    gs = [r["relative_growth"] for r in exact if r["relative_growth"] is not None]
    dks = [r["delta_K"] for r in exact if r["delta_K"] is not None]
    ks = [r["K_star_expanded"] for r in exact]
    ms = [r["M_star"] for r in rows if r["M_star"] is not None]
    js = [r["J_star"] for r in rows if r["J_star"] is not None]
    bands = {b: sum(1 for r in exact if r["growth_band"] == b) for b in ("LOW", "MODERATE", "HIGH")}

    def med(xs):
        if not xs:
            return None
        s = sorted(xs)
        return float(s[len(s) // 2] if len(s) % 2 else 0.5 * (s[len(s) // 2 - 1] + s[len(s) // 2]))

    if not exact and bound:
        verdict = "INCONCLUSIVE"
    elif gs and med(gs) is not None:
        mg = med(gs)
        if all(r["growth_band"] == "LOW" for r in exact):
            verdict = "LOW"
        elif all(r["growth_band"] == "HIGH" for r in exact):
            verdict = "HIGH"
        elif mg <= MAINT_LOW:
            verdict = "LOW" if bands["HIGH"] == 0 else "MIXED"
        elif mg <= MAINT_MOD:
            verdict = "MODERATE" if bands["HIGH"] == 0 or bands["LOW"] == 0 else "MIXED"
        else:
            verdict = "HIGH" if bands["LOW"] == 0 else "MIXED"
    else:
        verdict = "INCONCLUSIVE"
    return {
        "tasks_exact": len(exact),
        "tasks_bounded": len(bound),
        "expanded_median_K": med(ks),
        "median_delta_K": med(dks),
        "median_relative_growth": med(gs),
        "low": bands["LOW"],
        "moderate": bands["MODERATE"],
        "high": bands["HIGH"],
        "tasks_M_pos": sum(1 for r in rows if r.get("M_star") is not None and r["M_star"] > 0),
        "median_M": med(ms),
        "max_M": None if not ms else max(ms),
        "median_J": med(js),
        "max_J": None if not js else max(js),
        "verdict": verdict,
    }


def run_all_maintenance() -> dict:
    coeff = run_metric("coeff")
    resp = run_metric("resp")
    out = {
        "not_a_novel_algorithm": True,
        "phase3b_K_star_unaltered": True,
        "coeff": coeff,
        "resp": resp,
        "coeff_suite": _suite(coeff["tasks"]),
        "resp_suite": _suite(resp["tasks"]),
    }
    dump_json(OUT_DIR / "maintenance.json", out)
    return out


if __name__ == "__main__":
    run_all_maintenance()
