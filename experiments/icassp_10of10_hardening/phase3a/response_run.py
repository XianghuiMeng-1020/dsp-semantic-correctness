"""Response-space ambient-center analysis (secondary; numerically generated |H|)."""
from __future__ import annotations

import json

import numpy as np

from experiments.icassp_10of10_hardening.phase1.universe import load_frozen_universe
from experiments.icassp_10of10_hardening.phase3a.ambient_lp import classify_margin, solve_ambient, solve_primal
from experiments.icassp_10of10_hardening.phase3a.certificates import strength_for_task, verify_dual_numeric
from experiments.icassp_10of10_hardening.phase3a.config import PHASE1_DIR, RESP_N_CONFIRMATORY, RESP_N_PRECISION
from experiments.icassp_10of10_hardening.phase3a.embeddings import affine_span_reduce, embed_response_task
from experiments.icassp_10of10_hardening.phase3a.validation import check_canonical_separable_not_impossible


def _phase1_rows() -> dict:
    raw = json.loads((PHASE1_DIR / "best_observed_reference.json").read_text(encoding="utf-8"))
    return {r["task_id"]: r for r in raw["tasks"]}


def _kind_from_pair(p, d) -> str:
    if p.get("status") == "INF_SEPARABLE":
        return "AMBIENT_SEPARABLE"
    return classify_margin(p.get("gamma"))


def run_response() -> dict:
    uni = load_frozen_universe()
    p1 = _phase1_rows()
    tasks = []
    for pack in uni["tasks"]:
        tid = pack["task_id"]
        task = pack["task"]
        emb = embed_response_task(pack["valids"], pack["primary_invalids"], task, n=RESP_N_CONFIRMATORY)
        red = affine_span_reduce(emb["V"], emb["I"])
        V, I = red["V"], red["I"]
        primal, dual, kind_base = solve_ambient(V, I)
        emb2 = embed_response_task(pack["valids"], pack["primary_invalids"], task, n=RESP_N_PRECISION)
        red2 = affine_span_reduce(emb2["V"], emb2["I"])
        p2 = solve_primal(red2["V"], red2["I"], method="highs")
        kind2 = _kind_from_pair(p2, None)
        if kind2 == "UNDECIDED" and kind_base != "UNDECIDED":
            prec = "undecided"
            kind = kind_base
        elif kind_base == kind2:
            prec = "stable"
            kind = kind_base
        elif kind_base == "UNDECIDED":
            prec = "undecided"
            kind = "UNDECIDED"
        else:
            prec = "precision-sensitive"
            kind = "UNDECIDED"
        strength = strength_for_task(kind, primal, dual, None, None)
        if strength == "EXACT_RATIONAL_CERTIFICATE":
            strength = "HIGH_PRECISION_DUAL_CERTIFICATE"
        p1r = p1[tid]["resp"]
        canon_g = float(p1r["canonical_G_frozen"])
        gobs = float(p1r["Gobs_star"])
        dn = verify_dual_numeric(V, I, dual["lambda"]) if dual.get("lambda") is not None else None
        row = {
            "task": tid,
            "family": pack["family"],
            "n_valid": emb["V"].shape[0],
            "n_invalid": emb["I"].shape[0],
            "full_dim": emb["dim"],
            "reduced_dim": red["dim"],
            "n_dropped": red["n_dropped"],
            "rmse_scale": emb["rmse_scale"],
            "canonical_G": canon_g,
            "best_observed_valid_reference": gobs,
            "ambient_status": kind,
            "ambient_margin": primal.get("gamma"),
            "dual_margin": dual.get("gamma"),
            "precision_n": [RESP_N_CONFIRMATORY, RESP_N_PRECISION],
            "precision_kind": [kind_base, kind2],
            "precision_stability": prec,
            "exact_single_center_exists": kind == "AMBIENT_SEPARABLE",
            "certificate_strength": strength,
            "dual_numeric": dn,
            "check_D": check_canonical_separable_not_impossible(canon_g, kind),
        }
        tasks.append(row)
        print(
            f"[phase3a] resp {tid} m={emb['dim']} red={red['dim']} {kind} "
            f"γ={primal.get('gamma')} prec={prec}",
            flush=True,
        )
    n_sep = sum(1 for r in tasks if r["ambient_status"] == "AMBIENT_SEPARABLE")
    n_nos = sum(1 for r in tasks if r["ambient_status"] == "NO_AMBIENT_CENTER")
    n_und = sum(1 for r in tasks if r["ambient_status"] == "UNDECIDED")
    stabilities = {r["precision_stability"] for r in tasks}
    if stabilities == {"stable"}:
        robust = "YES"
    elif "precision-sensitive" in stabilities:
        robust = "MIXED"
    else:
        robust = "MIXED"
    return {
        "run": True,
        "metric": "band-masked RMSE of |H| on FREQZ_N=131072; Euclidean up to 1/sqrt(m)",
        "n_tasks": len(tasks),
        "AMBIENT_SEPARABLE": n_sep,
        "NO_AMBIENT_CENTER": n_nos,
        "UNDECIDED": n_und,
        "precision_robust": robust,
        "check_D_pass": all(r["check_D"] for r in tasks),
        "tasks": tasks,
    }
