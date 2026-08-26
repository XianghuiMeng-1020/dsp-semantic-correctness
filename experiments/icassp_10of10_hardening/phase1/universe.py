"""Load the frozen manuscript universe. Labels are read, never recomputed."""
from __future__ import annotations

import json
from pathlib import Path

from experiments.icassp_10of10_hardening.phase1.config import FROZEN_DIR, ROOT
from src.verification.io_utils import load_impl
from src.verification.registry_io import get_task, is_fir, suite_n_tasks


def _load_json(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def load_frozen_universe() -> dict:
    recert = json.loads((FROZEN_DIR / "recertify.json").read_text(encoding="utf-8"))
    probe = json.loads((FROZEN_DIR / "feasible_probe.json").read_text(encoding="utf-8"))
    boundary = json.loads((FROZEN_DIR / "boundary_invalids.json").read_text(encoding="utf-8"))
    canon_meta = _load_json("data/valid/canonical.json")
    task_metrics = json.loads((FROZEN_DIR / "task_metrics.json").read_text(encoding="utf-8"))
    metrics_by_tid = {r["task_id"]: r for r in task_metrics}

    constructed_valids = []
    for r in recert["valids"]:
        if r["independent_label"] != "VALID":
            continue
        constructed_valids.append(
            {
                "cid": r["id"],
                "task_id": r["task_id"],
                "role": "constructed_valid",
                "source": r.get("source"),
                "impl": load_impl(r["id"]),
                "family": r["family"],
            }
        )

    mechanism_invalids = []
    for r in recert["invalids"]:
        if r["independent_label"] != "INVALID":
            continue
        mechanism_invalids.append(
            {
                "cid": r["id"],
                "task_id": r["task_id"],
                "role": "mechanism_invalid",
                "source": r.get("source"),
                "impl": load_impl(r["id"]),
                "family": r["family"],
            }
        )

    probe_valids = []
    for r in probe["rows"]:
        if not r.get("genuine_same_order") or not r.get("path"):
            continue
        if not r.get("independent_ok"):
            continue
        probe_valids.append(
            {
                "cid": r["path"],
                "task_id": r["task_id"],
                "role": "probe_valid",
                "source": "feasible_set_probe",
                "impl": load_impl(r["path"]),
                "family": "fir",
            }
        )

    boundary_invalids = []
    for r in boundary:
        if r.get("independent_ok"):
            continue
        path = r.get("path") or r.get("cid")
        boundary_invalids.append(
            {
                "cid": path,
                "task_id": r["task_id"],
                "role": "boundary_invalid",
                "source": r.get("mechanism"),
                "impl": load_impl(path),
                "family": "fir" if is_fir(get_task(r["task_id"])) else "iir",
            }
        )

    canonical = {}
    for tid, meta in canon_meta.items():
        canonical[tid] = {
            "cid": meta["path"],
            "task_id": tid,
            "role": "canonical_reference",
            "impl": load_impl(meta["path"]),
        }

    tasks = []
    for task in suite_n_tasks():
        tid = task["task_id"]
        vv = [x for x in constructed_valids if x["task_id"] == tid]
        pv = [x for x in probe_valids if x["task_id"] == tid]
        ii_m = [x for x in mechanism_invalids if x["task_id"] == tid]
        ii_b = [x for x in boundary_invalids if x["task_id"] == tid]
        # Dedup cids if a probe path collided (should not)
        seen = set()
        valids = []
        for x in vv + pv:
            if x["cid"] in seen:
                continue
            seen.add(x["cid"])
            valids.append(x)
        tasks.append(
            {
                "task": task,
                "task_id": tid,
                "family": "fir" if is_fir(task) else "iir",
                "valids": valids,
                "constructed_valids": vv,
                "probe_valids": pv,
                "mechanism_invalids": ii_m,
                "boundary_invalids": ii_b,
                "primary_invalids": ii_m + ii_b,
                "canonical": canonical[tid],
                "frozen_metrics": metrics_by_tid[tid],
            }
        )

    return {
        "tasks": tasks,
        "n_constructed_valids": len(constructed_valids),
        "n_probe_valids": len(probe_valids),
        "n_mechanism_invalids": len(mechanism_invalids),
        "n_boundary_invalids": len(boundary_invalids),
    }
