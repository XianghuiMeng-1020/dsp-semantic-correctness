"""Optional false-acceptance audit on catalog-excluded certified invalids.

Does not retune tau. Does not replace the blocked valid-holdout analysis.
"""
from __future__ import annotations

from experiments.icassp_10of10_hardening.phase1.best_observed import d_coeff
from src.verification.io_utils import load_impl
from src.verification.registry_io import get_task


def score_optional_invalids(inv: dict, freeze: dict) -> dict:
    rows = inv.get("label_flip_invalids") or []
    if not rows or not inv.get("optional_external_invalid_eligible"):
        return {
            "EXTERNAL_INVALID_TRANSFER": "NOT_AVAILABLE",
            "reason": "No catalog-excluded certified-invalid holdout.",
            "n": 0,
            "rows": [],
        }
    by_task = {(t["task"], t["metric"]): t for t in freeze["tasks"]}
    out_rows = []
    accepted = 0
    for rec in rows:
        tid = rec["task_id"]
        cat = by_task.get((tid, "coeff"))
        if not cat or not cat.get("tau_safe", {}).get("ok"):
            out_rows.append({**rec, "scored": False, "reason": "missing_frozen_catalog"})
            continue
        task = get_task(tid)
        h = load_impl(rec["id"])
        ds = []
        for rid in cat["catalog_ids"]:
            href = load_impl(rid)
            ds.append(d_coeff(h, href, task))
        dmin = min(ds) if ds else None
        tau = cat["tau_safe"]["tau_safe"]
        false_accept = bool(dmin is not None and dmin <= tau)
        accepted += int(false_accept)
        out_rows.append(
            {
                "id": rec["id"],
                "task_id": tid,
                "in_phase3b_V": rec["in_phase3b_V"],
                "in_phase3b_I": rec["in_phase3b_I"],
                "d_min_coeff": dmin,
                "tau_safe": tau,
                "false_accept": false_accept,
                "K_obs_star": cat["K_obs_star"],
            }
        )
    n = len(out_rows)
    return {
        "EXTERNAL_INVALID_TRANSFER": "RUN_OPTIONAL_LABEL_FLIPS",
        "reason": (
            "Four independently certified INVALID library firwin2 occupants were not in "
            "Phase-3B V or I. Scored against frozen Phase-3B coefficient catalogs and "
            "base-only tau_safe. Not a valid holdout."
        ),
        "n": n,
        "false_accept": accepted,
        "false_reject_as_invalid": n - accepted,
        "false_accept_rate": (accepted / n) if n else None,
        "rows": out_rows,
    }
