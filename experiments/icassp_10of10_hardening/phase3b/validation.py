"""Independent optimality checks. Does not reuse the primary MILP call as the only evidence."""
from __future__ import annotations

import numpy as np

from experiments.icassp_10of10_hardening.phase1.universe import load_frozen_universe
from experiments.icassp_10of10_hardening.phase3b.config import G_ZERO_ABS
from experiments.icassp_10of10_hardening.phase3b.pairwise import coeff_matrices, gap_of_catalog
from experiments.icassp_10of10_hardening.phase3b.setcover import bitset_cover_k


def _pick_tasks(coeff: dict) -> list[str]:
    rows = [t for t in coeff["tasks"] if t["K_obs_star"] is not None]
    if not rows:
        return []
    by_n = sorted(rows, key=lambda t: t["n_valid"])
    by_k = sorted(rows, key=lambda t: t["K_obs_star"])
    picks = [
        by_n[0]["task"],
        by_n[-1]["task"],
        next(t["task"] for t in rows if t["task"].startswith("fir_") and "loose" in t["task"]),
        next(t["task"] for t in rows if t["task"].startswith("fir_") and "tight" in t["task"]),
        next(t["task"] for t in rows if t["task"].startswith("iir_") and "loose" in t["task"]),
        next(t["task"] for t in rows if t["task"].startswith("iir_") and "tight" in t["task"]),
        by_k[0]["task"],
        by_k[-1]["task"],
    ]
    # unique preserve order
    seen = []
    for p in picks:
        if p not in seen:
            seen.append(p)
    return seen


def validate(coeff: dict) -> dict:
    uni = {p["task_id"]: p for p in load_frozen_universe()["tasks"]}
    picks = _pick_tasks(coeff)
    by = {t["task"]: t for t in coeff["tasks"]}
    checks = []
    ok = True
    for tid in picks:
        t = by[tid]
        pack = uni[tid]
        vv, iv = coeff_matrices(pack["valids"], pack["primary_invalids"], pack["task"])
        idx = t["primary"].get("catalog_indices") or []
        gap = gap_of_catalog(vv, iv, idx)
        gap_ok = gap["G_R"] is not None and gap["G_R"] > G_ZERO_ABS
        stored = t["primary"].get("G_R")
        gap_match = stored is not None and abs(stored - gap["G_R"]) <= max(1e-12, 1e-9 * abs(stored))
        k = t["K_obs_star"]
        k_minus = None
        if k is not None and k >= 2 and idx:
            tau = t["primary"]["tau"]
            safe = [c for c in range(vv.shape[1]) if float(np.min(iv[:, c])) - tau > G_ZERO_ABS]
            cover = vv[:, safe] <= tau
            lower = bitset_cover_k(cover, k - 1)
            k_minus = lower is not None
            lower_ok = lower is None
        else:
            lower_ok = True
        rec_ok = bool(gap_ok and gap_match and lower_ok and t["primary"].get("status") == "EXACT_OPTIMUM")
        ok = ok and rec_ok
        checks.append(
            {
                "task": tid,
                "k": k,
                "gap_ok": gap_ok,
                "gap_match": gap_match,
                "k_minus_feasible": k_minus,
                "lower_bound_ok": lower_ok,
                "pass": rec_ok,
            }
        )
    k1_bad = [t["task"] for t in coeff["tasks"] if t["K_obs_star"] == 1]
    verdict = "PASS" if ok and not k1_bad else ("FAIL" if k1_bad or not any(c["pass"] for c in checks) else "PASS_WITH_LIMITATIONS")
    if k1_bad:
        verdict = "FAIL"
    return {"verdict": verdict, "checks": checks, "unexpected_k1": k1_bad, "n_checked": len(checks)}
