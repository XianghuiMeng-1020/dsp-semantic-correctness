"""Adequacy, diversity, attrition — no reference distances."""
from __future__ import annotations

import json
from collections import Counter, defaultdict

from experiments.icassp_10of10_hardening.phase3d_a.config import FIR_FAMILIES, IIR_FAMILIES, OUT_DIR
from src.verification.registry_io import suite_n_tasks


def _tasks():
    return suite_n_tasks()


def attrition(attempts: dict) -> list[dict]:
    rows = []
    key = defaultdict(lambda: {
        "attempts": 0,
        "generation_errors": 0,
        "grid_screen_fail": 0,
        "continuous_valid": 0,
        "continuous_invalid": 0,
        "undecided": 0,
        "exact_duplicates": 0,
        "H_VALID_admitted": 0,
    })
    for r in attempts["attempts"]:
        k = (r["task_id"], r["generator_id"])
        key[k]["attempts"] += 1
        if not r.get("generation_ok"):
            key[k]["generation_errors"] += 1
            continue
        if not r.get("grid_pass"):
            key[k]["grid_screen_fail"] += 1
            continue
        st = r.get("continuous_status")
        if st == "CERTIFIED_VALID":
            key[k]["continuous_valid"] += 1
        elif st == "CERTIFIED_INVALID":
            key[k]["continuous_invalid"] += 1
        elif st == "UNDECIDED":
            key[k]["undecided"] += 1
        if r.get("exact_duplicate"):
            key[k]["exact_duplicates"] += 1
        if r.get("label") == "H_VALID":
            key[k]["H_VALID_admitted"] += 1
    for (tid, gid), v in sorted(key.items()):
        rows.append({"task": tid, "generator": gid, **v})
    return rows


def invalid_attrition(hinv: dict) -> list[dict]:
    rows = []
    key = defaultdict(lambda: {
        "eligible_progenitors": 0,
        "attempts": 0,
        "certified_invalid": 0,
        "remained_valid": 0,
        "undecided": 0,
        "duplicates": 0,
        "admitted": 0,
    })
    seen_prog = defaultdict(set)
    for log in hinv.get("log") or []:
        k = (log["task_id"], log["mutation"])
        if log["progenitor"] not in seen_prog[k]:
            seen_prog[k].add(log["progenitor"])
            key[k]["eligible_progenitors"] += 1
        for step in log.get("ladder") or []:
            key[k]["attempts"] += 1
            st = step.get("continuous_status")
            if st == "CERTIFIED_INVALID":
                key[k]["certified_invalid"] += 1
            elif st == "CERTIFIED_VALID":
                key[k]["remained_valid"] += 1
            elif st == "UNDECIDED":
                key[k]["undecided"] += 1
            if step.get("exact_duplicate"):
                key[k]["duplicates"] += 1
        if log.get("admitted"):
            key[k]["admitted"] += 1
    for (tid, mut), v in sorted(key.items()):
        rows.append({"task": tid, "mutation": mut, **v})
    return rows


def adequacy(hv: dict, hi: dict) -> dict:
    tasks = [t["task_id"] for t in _tasks()]
    fir_t = [t["task_id"] for t in _tasks() if str(t["type"]).startswith("fir_")]
    iir_t = [t["task_id"] for t in _tasks() if str(t["type"]).startswith("iir_")]
    vc = Counter(m["task_id"] for m in hv["members"])
    ic = Counter(m["task_id"] for m in hi["members"])
    n_v, n_i = len(hv["members"]), len(hi["members"])
    n_v_fir = sum(1 for m in hv["members"] if m["family"] == "fir")
    n_v_iir = n_v - n_v_fir
    n_i_fir = sum(1 for m in hi["members"] if m["family"] == "fir")
    fam_ok = 0
    for tid in tasks:
        fams = {m["generator_id"] for m in hv["members"] if m["task_id"] == tid}
        if len(fams) >= 2:
            fam_ok += 1
    gates = {
        "H_VALID_ge_200": n_v >= 200,
        "H_INVALID_ge_200": n_i >= 200,
        "all_tasks_ge5_valid": all(vc[t] >= 5 for t in tasks),
        "all_tasks_ge5_invalid": all(ic[t] >= 5 for t in tasks),
        "fir_valid_ge_160": n_v_fir >= 160,
        "iir_valid_ge_20": n_v_iir >= 20,
        "generator_diversity": fam_ok >= 15,
    }
    adequate = all(gates.values())
    return {
        "n_valid": n_v,
        "n_invalid": n_i,
        "n_valid_fir": n_v_fir,
        "n_valid_iir": n_v_iir,
        "n_invalid_fir": n_i_fir,
        "n_invalid_iir": n_i - n_i_fir,
        "valid_per_task": dict(vc),
        "invalid_per_task": dict(ic),
        "tasks_ge5_valid": sum(1 for t in tasks if vc[t] >= 5),
        "tasks_ge10_valid": sum(1 for t in tasks if vc[t] >= 10),
        "tasks_ge5_invalid": sum(1 for t in tasks if ic[t] >= 5),
        "min_valid": min(vc[t] for t in tasks) if tasks else 0,
        "max_valid": max(vc[t] for t in tasks) if tasks else 0,
        "min_invalid": min(ic[t] for t in tasks) if tasks else 0,
        "families_ge2_tasks": fam_ok,
        "gates": gates,
        "PROSPECTIVE_CHALLENGE": "ADEQUATE" if adequate else "PROSPECTIVE_CHALLENGE_INADEQUATE",
        "fir_families": list(FIR_FAMILIES),
        "iir_families": list(IIR_FAMILIES),
    }


def diversity(hv: dict) -> dict:
    by_fam = Counter(m["generator_id"] for m in hv["members"])
    by_type = Counter()
    by_tight = Counter()
    orders = []
    for m in hv["members"]:
        tid = m["task_id"]
        parts = tid.split("_")
        by_type[parts[1]] += 1
        by_tight[parts[2]] += 1
        meta = m.get("impl_meta") or {}
        if "n_taps" in meta:
            orders.append(meta["n_taps"])
        elif "n_a" in meta:
            orders.append(max(0, int(meta["n_a"]) - 1))
    margins = []
    near = 0
    for m in hv["members"]:
        sm = m.get("spec_margin_grid") or {}
        vals = [float(sm[k]) for k in sm if sm[k] is not None]
        if not vals:
            continue
        worst = max(vals)
        margins.append(worst)
        if worst <= 1e-4:
            near += 1
    margins.sort()

    def q(p):
        if not margins:
            return None
        i = int(round(p * (len(margins) - 1)))
        return margins[i]

    return {
        "by_generator": dict(by_fam),
        "by_filter_type": dict(by_type),
        "by_loose_tight": dict(by_tight),
        "order_min": min(orders) if orders else None,
        "order_max": max(orders) if orders else None,
        "margin_min": margins[0] if margins else None,
        "margin_q1": q(0.25),
        "margin_median": q(0.5),
        "margin_q3": q(0.75),
        "margin_max": margins[-1] if margins else None,
        "near_boundary_count": near,
        "n_with_margin": len(margins),
    }


def no_transfer_scan() -> dict:
    forbidden = (
        "TransferAccept",
        "external FRR",
        "ExternalFRR",
        "expanded K",
        "K*_expanded",
        "catalog maintenance",
        "holdout accepted",
        "d_R(h)",
        "PHASE3B selected catalog distance",
    )
    hits = []
    for p in list(OUT_DIR.rglob("*")):
        if not p.is_file():
            continue
        if p.suffix not in {".json", ".md", ".txt"}:
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        for tok in forbidden:
            if tok in text:
                hits.append({"path": str(p.relative_to(OUT_DIR.parent.parent.parent)), "token": tok})
    return {"hits": hits, "verdict": "PHASE3D_A_BLINDING_VIOLATION" if hits else "CLEAN"}
