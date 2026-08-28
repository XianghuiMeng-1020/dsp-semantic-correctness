"""Secondary H_INVALID scoring. Incomplete 20-task coverage. Do not invent a 20-task FAR."""
from __future__ import annotations

from experiments.icassp_10of10_hardening.phase3d_b.config import OUT_DIR
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
from src.verification.io_utils import dump_json


def score_invalid() -> dict:
    cat_map, th_map = load_frozen_maps()
    hi = load_challenge("H_INVALID.json")
    by = members_by_task(hi)
    represented = sorted(tid for tid, ms in by.items() if ms)
    out = {
        "H_INVALID_total": hi["n"],
        "tasks_represented": len(represented),
        "note": "SECONDARY_ONLY_INCOMPLETE_20_TASK_COVERAGE",
        "do_not_compute_20_task_macro_FAR": True,
        "metrics": {},
    }
    for metric in ("coeff", "resp"):
        accepted = 0
        n = 0
        tasks = []
        by_fam = {"fir": {"n": 0, "fa": 0}, "iir": {"n": 0, "fa": 0}}
        by_mut: dict[str, dict] = {}
        for tid, members in sorted(by.items()):
            if not members:
                continue
            task = get_task_rec(tid)
            crec = cat_map[(tid, metric)]
            th = th_map[(tid, metric)]
            tau = th["tau_maxsafe"]
            refs = prepare_refs(list(crec["catalog_ids"]), task, metric)
            occs = prepare_occs(members, task, metric)
            fa = 0
            for occ in occs:
                hit = catalog_min_distance(occ, refs, task, metric)
                ok = bool(hit["d"] is not None and tau is not None and hit["d"] <= float(tau))
                if ok:
                    fa += 1
                mut = (occ["member"].get("mutation_id") or occ["member"].get("mutation") or "unknown")
                by_mut.setdefault(str(mut), {"n": 0, "fa": 0})
                by_mut[str(mut)]["n"] += 1
                by_mut[str(mut)]["fa"] += int(ok)
            n += len(members)
            accepted += fa
            fac = task_factors(tid)
            fam = "fir" if fac["fir"] else "iir"
            by_fam[fam]["n"] += len(members)
            by_fam[fam]["fa"] += fa
            tasks.append(
                {
                    "task": tid,
                    "n": len(members),
                    "false_accept": fa,
                    "false_accept_rate": fa / len(members),
                }
            )
            print(f"[phase3d_b] invalid {metric} {tid} FA={fa}/{len(members)}", flush=True)
        out["metrics"][metric] = {
            "n": n,
            "false_accept": accepted,
            "false_accept_rate": None if n == 0 else accepted / n,
            "tasks_with_samples": tasks,
            "family": {
                k: {"n": v["n"], "false_accept": v["fa"], "rate": None if v["n"] == 0 else v["fa"] / v["n"]}
                for k, v in by_fam.items()
            },
            "mutation": {
                k: {"n": v["n"], "false_accept": v["fa"], "rate": None if v["n"] == 0 else v["fa"] / v["n"]}
                for k, v in sorted(by_mut.items())
            },
        }
    dump_json(OUT_DIR / "invalid_secondary.json", out)
    return out


if __name__ == "__main__":
    score_invalid()
