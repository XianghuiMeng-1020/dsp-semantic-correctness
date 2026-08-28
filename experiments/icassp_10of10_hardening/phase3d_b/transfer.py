"""Primary H_VALID transfer against frozen Phase-3B catalogs and thresholds."""
from __future__ import annotations

import json
from statistics import mean, median

from experiments.icassp_10of10_hardening.phase3d_a.certify import certify_candidate
from experiments.icassp_10of10_hardening.phase3d_b.config import (
    OUT_DIR,
    TRANSFER_PARTIAL,
    TRANSFER_ROBUST,
)
from experiments.icassp_10of10_hardening.phase3d_b.score import (
    catalog_min_distance,
    get_task_rec,
    load_challenge,
    load_frozen_maps,
    members_by_task,
    prepare_occs,
    prepare_refs,
    task_factors,
)
from src.verification.io_utils import dump_json, load_impl


def _band(rate: float) -> str:
    if rate >= TRANSFER_ROBUST:
        return "ROBUST"
    if rate >= TRANSFER_PARTIAL:
        return "PARTIAL"
    return "FRAGILE"


def _verdict(task_rates: list[float], n_fragile: int, n_robust: int) -> str:
    if not task_rates:
        return "PROSPECTIVE_TRANSFER_INCONCLUSIVE"
    if n_robust >= 18 and n_fragile == 0:
        return "PROSPECTIVE_TRANSFER_ROBUST"
    if n_fragile >= 3 and median(task_rates) < TRANSFER_PARTIAL:
        return "PROSPECTIVE_TRANSFER_STRONG_FAILURE"
    if n_fragile >= 2 and (max(task_rates) - min(task_rates)) >= 0.20:
        return "PROSPECTIVE_TRANSFER_MIXED"
    if n_robust == len(task_rates):
        return "PROSPECTIVE_TRANSFER_ROBUST"
    if n_fragile == 0 and median(task_rates) >= TRANSFER_ROBUST:
        return "PROSPECTIVE_TRANSFER_ROBUST"
    return "PROSPECTIVE_TRANSFER_MIXED"


def _macro(rows: list[dict], pred) -> float | None:
    xs = [r["transfer"] for r in rows if pred(r)]
    return None if not xs else float(mean(xs))


def _summarize(rows: list[dict], accepted: int, rejected: int, n: int) -> dict:
    rates = [r["transfer"] for r in rows]
    n_ge95 = sum(1 for r in rates if r >= TRANSFER_ROBUST)
    n_mid = sum(1 for r in rates if TRANSFER_PARTIAL <= r < TRANSFER_ROBUST)
    n_lt75 = sum(1 for r in rates if r < TRANSFER_PARTIAL)
    return {
        "H_VALID": n,
        "tasks": len(rows),
        "accepted": accepted,
        "rejected": rejected,
        "pooled_transfer": None if n == 0 else accepted / n,
        "task_macro_mean": float(mean(rates)) if rates else None,
        "task_macro_median": float(median(rates)) if rates else None,
        "min_task_transfer": min(rates) if rates else None,
        "max_task_transfer": max(rates) if rates else None,
        "tasks_ge95": n_ge95,
        "tasks_75_95": n_mid,
        "tasks_lt75": n_lt75,
        "fir_macro": _macro(rows, lambda r: r["factors"]["fir"]),
        "iir_macro": _macro(rows, lambda r: r["factors"]["iir"]),
        "loose_macro": _macro(rows, lambda r: r["factors"]["loose"]),
        "tight_macro": _macro(rows, lambda r: r["factors"]["tight"]),
        "lp_macro": _macro(rows, lambda r: r["factors"]["filter_type"] == "lp"),
        "hp_macro": _macro(rows, lambda r: r["factors"]["filter_type"] == "hp"),
        "bp_macro": _macro(rows, lambda r: r["factors"]["filter_type"] == "bp"),
        "bs_macro": _macro(rows, lambda r: r["factors"]["filter_type"] == "bs"),
        "verdict": _verdict(rates, n_lt75, n_ge95),
        "rows": rows,
    }


def recertify_h_valid(hv: dict) -> dict:
    fail = []
    n_ok = 0
    for i, m in enumerate(hv["members"]):
        task = get_task_rec(m["task_id"])
        impl = load_impl(m["id"])
        rec = certify_candidate(task, impl)
        if rec.get("status") != "CERTIFIED_VALID":
            fail.append({"id": m["id"], "status": rec.get("status"), "detail": rec})
        else:
            n_ok += 1
        if i % 50 == 0:
            print(f"[phase3d_b] recertify H_VALID {i}/{hv['n']}", flush=True)
    return {
        "n": hv["n"],
        "certified_valid": n_ok,
        "fail": fail,
        "all_still_certified": n_ok == hv["n"] and not fail,
    }


def score_metric(metric: str, hv: dict, cat_map: dict, th_map: dict, which_tau: str) -> dict:
    by = members_by_task(hv)
    rows = []
    accepted = 0
    rejected = 0
    witnesses = []
    details = []
    for tid, members in sorted(by.items()):
        task = get_task_rec(tid)
        crec = cat_map[(tid, metric)]
        th = th_map[(tid, metric)]
        tau = th["tau_maxsafe"] if which_tau == "maxsafe" else th["tau_mid"]
        refs = prepare_refs(list(crec["catalog_ids"]), task, metric)
        occs = prepare_occs(members, task, metric)
        acc = 0
        rej = 0
        for occ in occs:
            hit = catalog_min_distance(occ, refs, task, metric)
            d = hit["d"]
            ok = bool(d is not None and tau is not None and d <= float(tau))
            rec = {
                "id": occ["cid"],
                "task": tid,
                "generator_id": occ["member"]["generator_id"],
                "continuous_status": occ["member"].get("continuous_status"),
                "S_t_status": "CERTIFIED_VALID",
                "metric": metric,
                "threshold_kind": which_tau,
                "threshold": tau,
                "d": d,
                "nearest_id": hit["nearest_id"],
                "accepted": ok,
                "excess": None if d is None or tau is None else float(d) - float(tau),
            }
            details.append(rec)
            if ok:
                acc += 1
            else:
                rej += 1
                witnesses.append(rec)
        n = len(members)
        rate = acc / n if n else None
        rows.append(
            {
                "task": tid,
                "H_VALID_n": n,
                "K_star_base": crec["K_obs_star"],
                "tau": tau,
                "D_V": th["D_V"],
                "D_I": th["D_I"],
                "accepted": acc,
                "rejected": rej,
                "transfer": rate,
                "external_FRR": None if rate is None else 1.0 - rate,
                "band": None if rate is None else _band(rate),
                "factors": task_factors(tid),
            }
        )
        accepted += acc
        rejected += rej
        print(f"[phase3d_b] {metric} {which_tau} {tid} acc={acc}/{n} transfer={rate}", flush=True)
    summary = _summarize(rows, accepted, rejected, hv["n"])
    summary["metric"] = metric
    summary["threshold_kind"] = which_tau
    return {"summary": summary, "witnesses": witnesses, "details": details}


def _sensitivity(primary_rows: list[dict], mid_rows: list[dict]) -> str:
    by_p = {r["task"]: r["band"] for r in primary_rows}
    changed = [r["task"] for r in mid_rows if r["band"] != by_p[r["task"]]]
    v_p = _verdict(
        [r["transfer"] for r in primary_rows],
        sum(1 for r in primary_rows if r["band"] == "FRAGILE"),
        sum(1 for r in primary_rows if r["band"] == "ROBUST"),
    )
    v_m = _verdict(
        [r["transfer"] for r in mid_rows],
        sum(1 for r in mid_rows if r["band"] == "FRAGILE"),
        sum(1 for r in mid_rows if r["band"] == "ROBUST"),
    )
    if not changed:
        return "ROBUST_TO_THRESHOLD_CHOICE"
    if v_p != v_m:
        return "MATERIALLY_SENSITIVE"
    return "SOMEWHAT_SENSITIVE"


def run_primary() -> dict:
    cat_map, th_map = load_frozen_maps()
    hv = load_challenge("H_VALID.json")
    recert = recertify_h_valid(hv)
    dump_json(OUT_DIR / "h_valid_recertify.json", recert)
    if not recert["all_still_certified"]:
        raise RuntimeError("H_VALID continuous recertification failed; STOP for PI review")

    coeff = score_metric("coeff", hv, cat_map, th_map, "maxsafe")
    resp = score_metric("resp", hv, cat_map, th_map, "maxsafe")
    dump_json(OUT_DIR / "transfer_coeff.json", coeff["summary"])
    dump_json(OUT_DIR / "transfer_resp.json", resp["summary"])
    dump_json(OUT_DIR / "rejected_valid_witnesses.json", {
        "note": "Reference rejection is not evidence of invalidity. Every member remains continuously certified valid.",
        "coeff": coeff["witnesses"],
        "resp": resp["witnesses"],
    })
    dump_json(OUT_DIR / "transfer_details_coeff.json", coeff["details"])
    dump_json(OUT_DIR / "transfer_details_resp.json", resp["details"])

    coeff_mid = score_metric("coeff", hv, cat_map, th_map, "mid")
    resp_mid = score_metric("resp", hv, cat_map, th_map, "mid")
    dump_json(OUT_DIR / "transfer_coeff_mid.json", coeff_mid["summary"])
    dump_json(OUT_DIR / "transfer_resp_mid.json", resp_mid["summary"])
    sens = {
        "coeff": _sensitivity(coeff["summary"]["rows"], coeff_mid["summary"]["rows"]),
        "resp": _sensitivity(resp["summary"]["rows"], resp_mid["summary"]["rows"]),
        "primary_threshold": "MAX_SAFE_BASE_ONLY",
        "secondary_threshold": "MIDPOINT_BASE_ONLY",
    }
    dump_json(OUT_DIR / "threshold_sensitivity.json", sens)
    return {
        "recert": recert,
        "coeff": coeff["summary"],
        "resp": resp["summary"],
        "coeff_mid": coeff_mid["summary"],
        "resp_mid": resp_mid["summary"],
        "sensitivity": sens,
    }


if __name__ == "__main__":
    run_primary()
