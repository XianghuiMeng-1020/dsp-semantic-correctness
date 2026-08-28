"""Coefficient-space ambient-center analysis on the frozen Phase-1 universe."""
from __future__ import annotations

import json

from experiments.icassp_10of10_hardening.phase1.universe import load_frozen_universe
from experiments.icassp_10of10_hardening.phase3a.ambient_lp import classify_margin, solve_dual, solve_primal, unpack_support
from experiments.icassp_10of10_hardening.phase3a.certificates import (
    reconstruct_dual_weights,
    strength_for_task,
    verify_dual_numeric,
    verify_primal_exact,
)
from experiments.icassp_10of10_hardening.phase3a.config import INDEPENDENT_CHECK_TASKS, PHASE1_DIR
from experiments.icassp_10of10_hardening.phase3a.embeddings import affine_span_reduce, embed_coeff_task
from experiments.icassp_10of10_hardening.phase3a.validation import check_canonical_separable_not_impossible, second_optimizer_check


def _phase1_rows() -> dict:
    raw = json.loads((PHASE1_DIR / "best_observed_reference.json").read_text(encoding="utf-8"))
    return {r["task_id"]: r for r in raw["tasks"]}


def run_coefficient() -> dict:
    uni = load_frozen_universe()
    p1 = _phase1_rows()
    tasks = []
    indep = {}
    for pack in uni["tasks"]:
        tid = pack["task_id"]
        family = pack["family"]
        emb = embed_coeff_task(pack["valids"], pack["primary_invalids"], family)
        red = affine_span_reduce(emb["V"], emb["I"])
        V, I = red["V"], red["I"]
        primal = solve_primal(V, I, method="highs")
        dual = solve_dual(V, I, method="highs")
        kind = classify_margin("+INF" if primal.get("status") == "INF_SEPARABLE" else primal.get("gamma"))
        exact_p = None
        exact_d = None
        if primal.get("c") is not None:
            exact_p = verify_primal_exact(V, I, primal["c"])
            if exact_p.get("gamma_positive"):
                kind = "AMBIENT_SEPARABLE"
            elif exact_p.get("gamma_nonpositive") and kind == "AMBIENT_SEPARABLE":
                # numerical positive slack failed exact check: do not claim separability
                kind = "NO_AMBIENT_CENTER" if (dual.get("gamma") is not None and float(dual["gamma"]) <= 0) else "UNDECIDED"
        if dual.get("lambda") is not None:
            exact_d = reconstruct_dual_weights(V, I, dual["lambda"])
            if exact_d.get("no_center_exact"):
                kind = "NO_AMBIENT_CENTER"
            elif exact_d.get("separator_exact"):
                kind = "AMBIENT_SEPARABLE"
        strength = strength_for_task(kind, primal, dual, exact_p, exact_d)
        dn = verify_dual_numeric(V, I, dual["lambda"]) if dual.get("lambda") is not None else None
        p1c = p1[tid]["coeff"]
        canon_g = float(p1c["canonical_G_frozen"])
        gobs = float(p1c["Gobs_star"])
        row = {
            "task": tid,
            "family": family,
            "n_valid": emb["V"].shape[0],
            "n_invalid": emb["I"].shape[0],
            "full_dim": emb["dim"],
            "dim": red["dim"],
            "n_dropped": red["n_dropped"],
            "orientation": emb["orientation"],
            "canonical_G": canon_g,
            "best_observed_valid_reference": gobs,
            "ambient_status": kind,
            "ambient_margin": primal.get("gamma"),
            "dual_margin": dual.get("gamma"),
            "exact_single_center_exists": kind == "AMBIENT_SEPARABLE",
            "certificate_strength": strength,
            "center": primal.get("c"),
            "primal": {k: primal[k] for k in primal if k not in {"c", "dual_marginals"}},
            "dual_numeric": dn,
            "exact_primal": exact_p,
            "exact_dual": {k: exact_d[k] for k in exact_d if k != "support"} if exact_d else None,
            "dual_support": ((exact_d or {}).get("support") or unpack_support(dual["lambda"], V.shape[0], I.shape[0]))
            if dual.get("lambda") is not None
            else None,
            "check_D": check_canonical_separable_not_impossible(canon_g, kind),
        }
        if tid in INDEPENDENT_CHECK_TASKS:
            indep[tid] = second_optimizer_check(V, I)
            row["second_optimizer"] = indep[tid]
        tasks.append(row)
        print(
            f"[phase3a] coeff {tid} dim={emb['dim']} V={emb['V'].shape[0]} I={emb['I'].shape[0]} "
            f"{kind} γ={primal.get('gamma')} strength={strength}",
            flush=True,
        )
    n_sep = sum(1 for r in tasks if r["ambient_status"] == "AMBIENT_SEPARABLE")
    n_nos = sum(1 for r in tasks if r["ambient_status"] == "NO_AMBIENT_CENTER")
    n_und = sum(1 for r in tasks if r["ambient_status"] == "UNDECIDED")
    return {
        "metric": "d_coeff_canonical / d_coeff_mag_equiv in oriented padded embedding",
        "n_tasks": len(tasks),
        "AMBIENT_SEPARABLE": n_sep,
        "NO_AMBIENT_CENTER": n_nos,
        "UNDECIDED": n_und,
        "EXACT_RATIONAL_CERTIFICATE": sum(1 for r in tasks if r["certificate_strength"] == "EXACT_RATIONAL_CERTIFICATE"),
        "HIGH_PRECISION_DUAL_CERTIFICATE": sum(1 for r in tasks if r["certificate_strength"] == "HIGH_PRECISION_DUAL_CERTIFICATE"),
        "NUMERICAL_LP_ONLY": sum(1 for r in tasks if r["certificate_strength"] == "NUMERICAL_LP_ONLY"),
        "check_D_pass": all(r["check_D"] for r in tasks),
        "independent_checks": indep,
        "tasks": tasks,
    }
