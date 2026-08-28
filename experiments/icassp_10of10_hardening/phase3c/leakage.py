"""Leakage audit for the intended Type-I holdout against Phase-3B fitting."""
from __future__ import annotations

from experiments.icassp_10of10_hardening.phase3c.inventory import build_inventory


def audit_leakage(inv: dict | None = None) -> dict:
    inv = inv or build_inventory()
    cat = inv["catalog_probe_stats"]
    checks = {
        "part_of_base_V": True,
        "part_of_base_I": False,
        "candidate_reference_in_phase3b": True,
        "distances_affected_phase3b_Kstar": True,
        "labels_affected_threshold_selection": True,
        "catalog_changed_after_holdout_score": False,
        "coefficient_identical_to_selected_reference": True,
        "response_identical_to_selected_reference": "not_scored_after_blocker",
    }
    first_five_clean = not (
        checks["part_of_base_V"]
        or checks["part_of_base_I"]
        or checks["candidate_reference_in_phase3b"]
        or checks["distances_affected_phase3b_Kstar"]
        or checks["labels_affected_threshold_selection"]
    )
    return {
        "corpus": "type_i_feasible_probes_1260",
        "verdict": "MATERIAL_LEAKAGE",
        "primary_transfer_valid": False,
        "first_five_relevant_checks_clean": first_five_clean,
        "blocker": "PHASE3C_HOLDOUT_LEAKAGE_BLOCKER",
        "checks": checks,
        "evidence": {
            "phase3b_V_includes_probes": True,
            "probe_n": inv["probe_n"],
            "constructed_n": inv["constructed_n"],
            "cid_overlap_constructed_probe": inv["cid_overlap_constructed_probe"],
            "probe_catalog_refs": cat["probe_catalog_refs"],
            "total_catalog_refs": cat["total_catalog_refs"],
            "tasks_with_probe_reference": cat["tasks_with_probe_reference"],
            "note": (
                "FIR Phase-3B n_valid equals constructed + probes. "
                f"{cat['probe_catalog_refs']} of {cat['total_catalog_refs']} "
                "coefficient catalog members are probe_candidates paths."
            ),
        },
        "do_not_score_as_holdout": True,
    }
