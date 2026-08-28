"""Reconstruct Phase-3B catalogs and base-only thresholds. No H_VALID scoring."""
from __future__ import annotations

import json
import math
from pathlib import Path

from experiments.icassp_10of10_hardening.phase3d_b.config import (
    FROZEN_DIR,
    G_ZERO_ABS,
    OUT_DIR,
    PHASE1_DIR,
    PHASE3B_DIR,
    ROOT,
)
from src.verification.io_utils import dump_json, sha256_file


def tau_maxsafe(d_i: float | None) -> float | None:
    if d_i is None or not math.isfinite(float(d_i)):
        return None
    return math.nextafter(float(d_i), float("-inf"))


def tau_mid(d_v: float | None, d_i: float | None) -> float | None:
    if d_v is None or d_i is None:
        return None
    return 0.5 * (float(d_v) + float(d_i))


def _threshold_record(d_v, d_i) -> dict:
    if d_v is None or d_i is None:
        return {
            "D_V": None,
            "D_I": None,
            "base_gap": None,
            "tau_maxsafe": None,
            "tau_mid": None,
            "ok": False,
            "reason": "missing_D",
            "base_exact": False,
        }
    dv, di = float(d_v), float(d_i)
    gap = di - dv
    tmax = tau_maxsafe(di)
    tmid = tau_mid(dv, di)
    exact = bool(dv < di and gap > G_ZERO_ABS)
    ok = bool(tmax is not None and tmax < di)
    covers = bool(tmax is not None and tmax >= dv)
    return {
        "D_V": dv,
        "D_I": di,
        "base_gap": gap,
        "tau_maxsafe": tmax,
        "tau_mid": tmid,
        "ok": ok,
        "base_exact": exact,
        "covers_base_valids": covers,
        "rejects_base_invalids": bool(tmax is not None and tmax < di),
        "convention": "tau_maxsafe = math.nextafter(D_I, -inf); tau_mid = (D_V+D_I)/2",
        "holdout_used": False,
    }


def _library_path(tid: str, method: str) -> str | None:
    for ext in (".npy", ".npz"):
        rel = f"data/valid/library/{tid}__{method}{ext}"
        if (ROOT / rel).exists():
            return rel
    return None


def _multi_row(multi: list, tid: str) -> dict:
    return next(r for r in multi if r["task_id"] == tid)


def _sweep_entry(row: dict, want) -> dict | None:
    for ks in row["k_sweep"]:
        k = ks["K"]
        if want == "all" and isinstance(k, str) and str(k).startswith("all"):
            return ks
        if k == want:
            return ks
    return None


def _methods_to_ids(tid: str, methods: list[str]) -> dict:
    ids = []
    missing = []
    for m in methods:
        p = _library_path(tid, m)
        if p is None:
            missing.append(m)
        else:
            ids.append(p)
    return {"catalog_ids": ids, "methods": list(methods), "missing_methods": missing}


def freeze_catalogs() -> dict:
    src = PHASE3B_DIR / "reference_catalog_complexity.json"
    rcc = json.loads(src.read_text(encoding="utf-8"))
    tasks = []
    for metric in ("coeff", "resp"):
        for t in rcc[metric]["tasks"]:
            p = t["primary"]
            ids = list(p.get("catalog_ids") or [])
            tasks.append(
                {
                    "task": t["task"],
                    "family": t.get("family"),
                    "metric": metric,
                    "n_valid_base": t["n_valid"],
                    "n_invalid_base": t["n_invalid"],
                    "status": p.get("status"),
                    "K_obs_star": p.get("K_obs_star"),
                    "catalog_ids": ids,
                    "catalog_ids_sorted": sorted(ids),
                    "catalog_indices": list(p.get("catalog_indices") or []),
                    "stored_tau": p.get("tau"),
                    "tie_rule": "phase3b_stored_witness; no re-optimization; lex-smallest sorted ID tuple only if multiple stored",
                    "reoptimized": False,
                    "holdout_used_in_selection": False,
                }
            )
    return {
        "source": "results/icassp_10of10_hardening/phase3b/reference_catalog_complexity.json",
        "source_sha256": sha256_file(src),
        "derived_only_from_phase3b": True,
        "holdout_used_in_derivation": False,
        "reoptimized": False,
        "tasks": tasks,
    }


def freeze_thresholds(catalogs: dict) -> dict:
    src = PHASE3B_DIR / "reference_catalog_complexity.json"
    rcc = json.loads(src.read_text(encoding="utf-8"))
    by = {(t["task"], t["metric"]): t["primary"] for metric in ("coeff", "resp") for t in rcc[metric]["tasks"]}
    tasks = []
    for rec in catalogs["tasks"]:
        p = by[(rec["task"], rec["metric"])]
        th = _threshold_record(p.get("D_V"), p.get("D_I"))
        th.update(
            {
                "task": rec["task"],
                "family": rec.get("family"),
                "metric": rec["metric"],
                "K_obs_star": rec["K_obs_star"],
                "primary_threshold": "MAX_SAFE_BASE_ONLY",
                "secondary_threshold": "MIDPOINT_BASE_ONLY",
                "holdout_used_in_threshold_selection": False,
            }
        )
        tasks.append(th)
    return {
        "source": "results/icassp_10of10_hardening/phase3b/reference_catalog_complexity.json",
        "source_sha256": sha256_file(src),
        "derived_only_from_phase3b_base_D": True,
        "holdout_used_in_derivation": False,
        "tau_maxsafe_rule": "math.nextafter(D_I, -inf); largest IEEE-754 binary64 strictly below D_I",
        "tau_mid_rule": "(D_V + D_I) / 2; secondary only",
        "tasks": tasks,
    }


def freeze_hierarchy_identities() -> dict:
    """Freeze hierarchy catalog IDs and base-only stored D_V/D_I. No H_VALID I/O."""
    multi = json.loads((FROZEN_DIR / "multi_reference.json").read_text(encoding="utf-8"))
    p1 = json.loads((PHASE1_DIR / "best_observed_reference.json").read_text(encoding="utf-8"))
    canon = json.loads((ROOT / "data" / "valid" / "canonical.json").read_text(encoding="utf-8"))
    rcc = json.loads((PHASE3B_DIR / "reference_catalog_complexity.json").read_text(encoding="utf-8"))
    p1_by = {r["task_id"]: r for r in p1["tasks"]}
    recert = json.loads((FROZEN_DIR / "recertify.json").read_text(encoding="utf-8"))
    library_by_task: dict[str, list[str]] = {}
    for r in recert["valids"]:
        if r.get("independent_label") != "VALID":
            continue
        cid = r["id"]
        if "/library/" not in cid.replace("\\", "/"):
            continue
        library_by_task.setdefault(r["task_id"], []).append(cid)
    for tid in library_by_task:
        library_by_task[tid] = sorted(set(library_by_task[tid]))

    tasks = []
    for t in rcc["coeff"]["tasks"]:
        tid = t["task"]
        prow = _multi_row(multi, tid)
        p1t = p1_by[tid]
        oracles = {}
        # canonical K=1
        cpath = canon[tid]["path"]
        canon_coeff = next(
            (x for x in p1t["coeff"].get("all_refs") or [] if x.get("ref_id") == cpath),
            None,
        )
        canon_resp = next(
            (x for x in p1t["resp"].get("all_refs") or [] if x.get("ref_id") == cpath),
            None,
        )
        oracles["canonical_k1"] = {
            "catalog_ids": [cpath],
            "coeff": _threshold_record(
                None if canon_coeff is None else canon_coeff.get("D_V"),
                None if canon_coeff is None else canon_coeff.get("D_I"),
            ),
            "resp": _threshold_record(
                None if canon_resp is None else canon_resp.get("D_V"),
                None if canon_resp is None else canon_resp.get("D_I"),
            ),
            "identity_source": "data/valid/canonical.json",
        }
        oracles["best_observed_k1"] = {
            "catalog_ids_coeff": [p1t["coeff"]["best_reference_id"]],
            "catalog_ids_resp": [p1t["resp"]["best_reference_id"]],
            "coeff": _threshold_record(p1t["coeff"].get("best_DV"), p1t["coeff"].get("best_DI")),
            "resp": _threshold_record(p1t["resp"].get("best_DV"), p1t["resp"].get("best_DI")),
            "identity_source": "phase1/best_observed_reference.json best_reference_id (stored; not retied)",
        }
        for label, want in (("published_k3", 3), ("published_k5", 5), ("all_library", "all")):
            ks = _sweep_entry(prow, want)
            if ks is None:
                oracles[label] = {"defined": False, "reason": "no_sweep_entry"}
                continue
            mapped = _methods_to_ids(tid, list(ks.get("methods") or []))
            if label == "all_library":
                mapped = {
                    "catalog_ids": library_by_task.get(tid, []),
                    "methods": list(ks.get("methods") or []),
                    "missing_methods": [],
                    "available": ks.get("available"),
                }
            oracles[label] = {
                "K": ks.get("K"),
                "defined": bool(mapped["catalog_ids"]),
                **mapped,
                "coeff": _threshold_record((ks.get("coeff") or {}).get("D_V"), (ks.get("coeff") or {}).get("D_I")),
                "resp": _threshold_record((ks.get("resp") or {}).get("D_V"), (ks.get("resp") or {}).get("D_I")),
                "identity_source": "data/icassp_10of10/multi_reference.json + library paths",
            }
        kstar_c = next(x for x in rcc["coeff"]["tasks"] if x["task"] == tid)["primary"]
        kstar_r = next(x for x in rcc["resp"]["tasks"] if x["task"] == tid)["primary"]
        oracles["kstar_obs"] = {
            "catalog_ids_coeff": list(kstar_c.get("catalog_ids") or []),
            "catalog_ids_resp": list(kstar_r.get("catalog_ids") or []),
            "coeff": _threshold_record(kstar_c.get("D_V"), kstar_c.get("D_I")),
            "resp": _threshold_record(kstar_r.get("D_V"), kstar_r.get("D_I")),
            "identity_source": "phase3b reference_catalog_complexity.json primary",
        }
        tasks.append({"task": tid, "family": t.get("family"), "oracles": oracles})
    return {
        "holdout_used_in_identity_or_threshold": False,
        "note": "Hierarchy identities and D_V/D_I are copied from frozen Phase-1 / multi_reference / Phase-3B artifacts. No H_VALID distance is computed here.",
        "tasks": tasks,
    }


def write_frozen_package() -> dict:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    catalogs = freeze_catalogs()
    thresholds = freeze_thresholds(catalogs)
    hierarchy = freeze_hierarchy_identities()
    dump_json(OUT_DIR / "FROZEN_CATALOGS_PREUNBLIND.json", catalogs)
    dump_json(OUT_DIR / "FROZEN_THRESHOLDS_PREUNBLIND.json", thresholds)
    dump_json(OUT_DIR / "FROZEN_HIERARCHY_PREUNBLIND.json", hierarchy)
    return {"catalogs": catalogs, "thresholds": thresholds, "hierarchy": hierarchy}


if __name__ == "__main__":
    write_frozen_package()
    print("wrote frozen catalog/threshold/hierarchy package", flush=True)
