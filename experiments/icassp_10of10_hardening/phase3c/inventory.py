"""Provenance inventory of pre-Phase-3C valid/invalid corpora."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from experiments.icassp_10of10_hardening.phase3c.config import FROZEN_DIR, PHASE3B_DIR, ROOT
from src.verification.io_utils import sha256_file


def _norm(rel: str) -> str:
    return str(rel).replace("\\", "/")


def _load(rel: Path | str):
    p = ROOT / rel if not isinstance(rel, Path) else rel
    return json.loads(p.read_text(encoding="utf-8"))


def _constructed_valids(recert: dict) -> list[dict]:
    return [r for r in recert["valids"] if r.get("independent_label") == "VALID"]


def _constructed_invalids(recert: dict) -> list[dict]:
    return [r for r in recert["invalids"] if r.get("independent_label") == "INVALID"]


def _probe_valids(probe: dict) -> list[dict]:
    return [
        r
        for r in probe["rows"]
        if r.get("genuine_same_order") and r.get("path") and r.get("independent_ok")
    ]


def _catalog_probe_stats(rcc: dict) -> dict:
    per = []
    total_refs = 0
    probe_refs = 0
    tasks_with_probe_ref = 0
    for t in rcc["coeff"]["tasks"]:
        ids = [_norm(x) for x in t["primary"].get("catalog_ids") or []]
        n_p = sum(1 for i in ids if "probe_candidates" in i)
        total_refs += len(ids)
        probe_refs += n_p
        if n_p:
            tasks_with_probe_ref += 1
        per.append(
            {
                "task": t["task"],
                "n_valid": t["n_valid"],
                "K_obs_star": t["K_obs_star"],
                "catalog_n": len(ids),
                "probe_in_catalog": n_p,
            }
        )
    return {
        "total_catalog_refs": total_refs,
        "probe_catalog_refs": probe_refs,
        "tasks_with_probe_reference": tasks_with_probe_ref,
        "per_task": per,
    }


def _disk_valid_files() -> list[str]:
    out = []
    for sub in ("data/valid/library", "data/valid/random", "data/valid/first_principles"):
        p = ROOT / sub
        if not p.exists():
            continue
        for f in p.rglob("*"):
            if f.suffix in {".npy", ".npz"}:
                out.append(_norm(str(f.relative_to(ROOT))))
    return out


def build_inventory() -> dict:
    recert = _load(FROZEN_DIR / "recertify.json")
    probe = _load(FROZEN_DIR / "feasible_probe.json")
    rcc = _load(PHASE3B_DIR / "reference_catalog_complexity.json")
    gen = _load(FROZEN_DIR / "generated_witness.json")
    constructed = _constructed_valids(recert)
    invalids = _constructed_invalids(recert)
    probes = _probe_valids(probe)
    constructed_ids = {_norm(r["id"]) for r in constructed}
    probe_ids = {_norm(r["path"]) for r in probes}
    phase3b_v = constructed_ids | probe_ids
    disk = _disk_valid_files()
    invalid_ids = {_norm(r["id"]) for r in invalids}
    extra_disk = sorted(p for p in disk if p not in constructed_ids)
    flips = recert.get("summary", {}).get("flips") or []
    flip_invalids = [
        {
            "id": _norm(f["id"]),
            "task_id": f["task_id"],
            "previous_label": f.get("previous_label"),
            "independent_label": f.get("independent_label"),
            "in_phase3b_V": _norm(f["id"]) in phase3b_v,
            "in_phase3b_I": _norm(f["id"]) in invalid_ids,
        }
        for f in flips
        if f.get("independent_label") == "INVALID"
    ]
    optional_invalid_ok = all(
        (not r["in_phase3b_V"]) and (not r["in_phase3b_I"]) for r in flip_invalids
    ) and bool(flip_invalids)
    failed_probes = [
        r
        for r in probe["rows"]
        if r.get("path")
        and (not r.get("genuine_same_order") or not r.get("independent_ok"))
    ]
    gen_ok = [g for g in gen if g.get("independent_ok")]
    gen_impl_keys = any(
        any(k in g for k in ("path", "coeff", "b", "npy", "artifact_path")) for g in gen
    )
    cat = _catalog_probe_stats(rcc)
    overlap_cid = constructed_ids & probe_ids

    rows = [
        {
            "corpus": "manuscript_constructed_valids_412",
            "existed_pre_phase3c": True,
            "in_base_412": True,
            "tasks_mapped": sorted({r["task_id"] for r in constructed}),
            "independently_certified": True,
            "used_in_phase3b_catalog_selection": True,
            "eligible_external_holdout": False,
            "n": len(constructed),
            "reason": "These occupants are the constructed part of Phase-3B V_t and were candidate references.",
        },
        {
            "corpus": "type_i_feasible_probes_1260",
            "existed_pre_phase3c": True,
            "in_base_412": False,
            "tasks_mapped": sorted({r["task_id"] for r in probes}),
            "independently_certified": True,
            "used_in_phase3b_catalog_selection": True,
            "eligible_external_holdout": False,
            "n": len(probes),
            "reason": (
                "Phase-3B load_frozen_universe() sets valids = constructed + probe_valids. "
                "Probes were candidate references; many were selected into R*."
            ),
        },
        {
            "corpus": "first_principles_occupants",
            "existed_pre_phase3c": True,
            "in_base_412": True,
            "tasks_mapped": sorted({r["task_id"] for r in constructed if r.get("source") == "first_principles"}),
            "independently_certified": True,
            "used_in_phase3b_catalog_selection": True,
            "eligible_external_holdout": False,
            "n": sum(1 for r in constructed if r.get("source") == "first_principles"),
            "reason": "Subset of the 412 constructed valids.",
        },
        {
            "corpus": "library_occupants_in_412",
            "existed_pre_phase3c": True,
            "in_base_412": True,
            "tasks_mapped": sorted({r["task_id"] for r in constructed if r.get("source") == "library"}),
            "independently_certified": True,
            "used_in_phase3b_catalog_selection": True,
            "eligible_external_holdout": False,
            "n": sum(1 for r in constructed if r.get("source") == "library"),
            "reason": "Subset of the 412 constructed valids.",
        },
        {
            "corpus": "random_occupants_in_412",
            "existed_pre_phase3c": True,
            "in_base_412": True,
            "tasks_mapped": sorted({r["task_id"] for r in constructed if r.get("source") == "random"}),
            "independently_certified": True,
            "used_in_phase3b_catalog_selection": True,
            "eligible_external_holdout": False,
            "n": sum(1 for r in constructed if r.get("source") == "random"),
            "reason": "Subset of the 412 constructed valids.",
        },
        {
            "corpus": "generated_code_witness_records",
            "existed_pre_phase3c": True,
            "in_base_412": False,
            "tasks_mapped": sorted({g["task_id"] for g in gen if g.get("task_id")}),
            "independently_certified": False,
            "used_in_phase3b_catalog_selection": False,
            "eligible_external_holdout": False,
            "n": len(gen),
            "n_independent_ok": len(gen_ok),
            "reason": (
                "Pre-existing generation metadata only. No stored coefficient/response artifacts "
                f"(impl_keys_present={gen_impl_keys}). Cannot be scored under frozen S_t semantics."
            ),
        },
        {
            "corpus": "failed_or_non_genuine_type_i_probe_rows",
            "existed_pre_phase3c": True,
            "in_base_412": False,
            "tasks_mapped": sorted({r["task_id"] for r in failed_probes if r.get("task_id")}),
            "independently_certified": False,
            "used_in_phase3b_catalog_selection": False,
            "eligible_external_holdout": False,
            "n": len(failed_probes),
            "reason": "Not independently certified valid. Invalid as a valid-holdout.",
        },
        {
            "corpus": "mechanism_invalids",
            "existed_pre_phase3c": True,
            "in_base_412": False,
            "tasks_mapped": sorted({r["task_id"] for r in invalids}),
            "independently_certified": True,
            "used_in_phase3b_catalog_selection": True,
            "eligible_external_holdout": False,
            "n": len(invalids),
            "reason": "Used as Phase-3B primary invalids for D_I and tau. Not a valid holdout.",
        },
        {
            "corpus": "boundary_invalids",
            "existed_pre_phase3c": True,
            "in_base_412": False,
            "tasks_mapped": "frozen_boundary_invalids.json",
            "independently_certified": True,
            "used_in_phase3b_catalog_selection": True,
            "eligible_external_holdout": False,
            "n": "see_boundary_invalids.json",
            "reason": "Used as Phase-3B primary invalids for D_I and tau. Not a valid holdout.",
        },
        {
            "corpus": "independent_invalid_label_flips",
            "existed_pre_phase3c": True,
            "in_base_412": False,
            "tasks_mapped": sorted({r["task_id"] for r in flip_invalids}),
            "independently_certified": True,
            "used_in_phase3b_catalog_selection": False,
            "eligible_external_holdout": False,
            "eligible_external_invalid": optional_invalid_ok,
            "n": len(flip_invalids),
            "reason": (
                "Four library firwin2 occupants were previously labeled valid and independently "
                "certified INVALID. They are absent from Phase-3B V_t and from recertify invalids "
                "used for D_I. Eligible only as optional external-invalid transfer, not as valid holdout."
            ),
        },
        {
            "corpus": "disk_valid_npy_not_in_recertify_412",
            "existed_pre_phase3c": True,
            "in_base_412": False,
            "tasks_mapped": [],
            "independently_certified": False,
            "used_in_phase3b_catalog_selection": False,
            "eligible_external_holdout": False,
            "n": len(extra_disk),
            "reason": (
                "After excluding the 412 constructed valids, leftover npy files are the same "
                "four independent-INVALID label flips (path-normalized)."
            ),
        },
    ]

    eligible = [r for r in rows if r["eligible_external_holdout"]]
    blocker = "PHASE3C_HOLDOUT_LEAKAGE_BLOCKER"
    return {
        "primary_holdout_designation": None,
        "primary_holdout_name": None,
        "blocker": blocker,
        "blocker_reason": (
            "The 1260 Type-I probes existed before Phase 3C and are continuously certified, "
            "but they were members of Phase-3B V_t and candidate/selected references. "
            "They are not an independent external holdout."
        ),
        "constructed_n": len(constructed),
        "constructed_sources": dict(Counter(r.get("source") for r in constructed)),
        "probe_n": len(probes),
        "probe_unique": len(probe_ids),
        "probe_per_task": dict(sorted(Counter(r["task_id"] for r in probes).items())),
        "probe_task_coverage": len({r["task_id"] for r in probes}),
        "cid_overlap_constructed_probe": len(overlap_cid),
        "extra_disk_valid_files": extra_disk,
        "label_flip_invalids": flip_invalids,
        "optional_external_invalid_eligible": optional_invalid_ok,
        "catalog_probe_stats": cat,
        "generated_n": len(gen),
        "generated_independent_ok": len(gen_ok),
        "generated_impl_keys_present": gen_impl_keys,
        "eligible_primary": [r["corpus"] for r in eligible],
        "eligible_secondary": [],
        "corpora": rows,
        "hashes": {
            "recertify.json": sha256_file(FROZEN_DIR / "recertify.json"),
            "feasible_probe.json": sha256_file(FROZEN_DIR / "feasible_probe.json"),
            "reference_catalog_complexity.json": sha256_file(
                PHASE3B_DIR / "reference_catalog_complexity.json"
            ),
        },
        "dedup_rule": (
            "Exact IEEE-754 identity after Phase-1 coefficient canonicalize. "
            "Not applied: no eligible holdout."
        ),
    }
