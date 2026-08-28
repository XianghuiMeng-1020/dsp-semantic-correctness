"""Score frozen H_VALID against the predeclared reference hierarchy."""
from __future__ import annotations

import json

from experiments.icassp_10of10_hardening.phase3d_b.config import OUT_DIR
from experiments.icassp_10of10_hardening.phase3d_b.score import (
    catalog_min_distance,
    get_task_rec,
    load_challenge,
    members_by_task,
    prepare_occs,
    prepare_refs,
)
from src.verification.io_utils import dump_json


def _oracle_ids(orec: dict, metric: str) -> list[str] | None:
    if orec.get("defined") is False:
        return None
    key = f"catalog_ids_{metric}"
    if key in orec:
        return list(orec[key] or [])
    ids = orec.get("catalog_ids")
    if ids is None:
        return None
    return list(ids)


def score_hierarchy() -> dict:
    hier = json.loads((OUT_DIR / "FROZEN_HIERARCHY_PREUNBLIND.json").read_text(encoding="utf-8"))
    hv = load_challenge("H_VALID.json")
    by = members_by_task(hv)
    names = (
        "canonical_k1",
        "best_observed_k1",
        "published_k3",
        "published_k5",
        "all_library",
        "kstar_obs",
    )
    rows = []
    for name in names:
        rec = {"oracle": name}
        for metric in ("coeff", "resp"):
            accepted = 0
            n = 0
            exact_n = 0
            defined_n = 0
            per_task = []
            for t in hier["tasks"]:
                tid = t["task"]
                orec = t["oracles"][name]
                ids = _oracle_ids(orec, metric)
                th = orec.get(metric) or {}
                tau = th.get("tau_maxsafe")
                base_exact = bool(th.get("base_exact"))
                members = by.get(tid) or []
                if not ids or tau is None:
                    per_task.append({"task": tid, "defined": False, "n": len(members)})
                    continue
                defined_n += 1
                if base_exact:
                    exact_n += 1
                task = get_task_rec(tid)
                refs = prepare_refs(ids, task, metric)
                occs = prepare_occs(members, task, metric)
                acc = 0
                for occ in occs:
                    hit = catalog_min_distance(occ, refs, task, metric)
                    if hit["d"] is not None and hit["d"] <= float(tau):
                        acc += 1
                n += len(members)
                accepted += acc
                per_task.append(
                    {
                        "task": tid,
                        "defined": True,
                        "n": len(members),
                        "accepted": acc,
                        "transfer": acc / len(members) if members else None,
                        "base_exact": base_exact,
                        "K": len(ids),
                        "tau_maxsafe": tau,
                    }
                )
            rec[f"{metric}_base_exact_tasks"] = exact_n
            rec[f"{metric}_defined_tasks"] = defined_n
            rec[f"{metric}_H_VALID_n"] = n
            rec[f"{metric}_accepted"] = accepted
            rec[f"{metric}_transfer"] = None if n == 0 else accepted / n
            rec[f"{metric}_base_exact"] = exact_n == 20
            rec[f"{metric}_tasks"] = per_task
            print(f"[phase3d_b] hierarchy {name} {metric} transfer={rec[f'{metric}_transfer']}", flush=True)
        rows.append(rec)
    out = {
        "holdout_used_in_oracle_or_threshold": False,
        "threshold": "MAX_SAFE_BASE_ONLY",
        "oracles": rows,
    }
    dump_json(OUT_DIR / "hierarchy_transfer.json", out)
    return out


if __name__ == "__main__":
    score_hierarchy()
