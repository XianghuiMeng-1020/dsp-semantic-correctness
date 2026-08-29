"""Blocked transfer / maintenance / secondary / invalid analyses.

Do not score a leaked Type-I set as an external holdout.
Do not re-fit Phase-3B catalogs on the constructed-only 412.
"""
from __future__ import annotations

from experiments.icassp_10of10_hardening.phase3c.config import (
    MAINT_LOW,
    MAINT_MOD,
    TRANSFER_PARTIAL,
    TRANSFER_ROBUST,
)


def blocked_transfer(leak: dict) -> dict:
    return {
        "run": False,
        "reason": leak["blocker"],
        "corpus": leak["corpus"],
        "leakage_verdict": leak["verdict"],
        "coefficient": {
            "run": False,
            "tasks": None,
            "holdout_valid_total": None,
            "accepted": None,
            "rejected": None,
            "pooled_transfer_accept": None,
            "task_macro_mean": None,
            "task_macro_median": None,
            "tasks_ge_95": None,
            "tasks_75_95": None,
            "tasks_lt_75": None,
            "worst_task_transfer": None,
            "verdict": "NOT_SCORED",
        },
        "response": {
            "run": False,
            "holdout_valid_total": None,
            "pooled_transfer_accept": None,
            "task_macro_median": None,
            "tasks_ge_95": None,
            "tasks_lt_75": None,
            "verdict": "N/A",
        },
        "hierarchy": {
            "canonical_k1_coeff": None,
            "best_observed_k1_coeff": None,
            "k3_coeff": None,
            "k5_coeff": None,
            "all_library_coeff": None,
            "kstar_obs_coeff": None,
            "canonical_response": None,
            "kstar_obs_response": None,
            "key_finding": (
                "Hierarchy transfer was not scored because the intended Type-I set "
                "leaked into Phase-3B catalog selection."
            ),
        },
        "bands_locked": {
            "robust": TRANSFER_ROBUST,
            "partial": TRANSFER_PARTIAL,
        },
    }


def blocked_maintenance() -> dict:
    return {
        "run": False,
        "reason": "PHASE3C_HOLDOUT_LEAKAGE_BLOCKER",
        "tasks_exact": None,
        "tasks_bounded": None,
        "base_median_k": 23.0,
        "expanded_median_k": None,
        "median_delta_k": None,
        "median_relative_growth": None,
        "low": None,
        "moderate": None,
        "high": None,
        "tasks_unavoidable_new": None,
        "median_m_star": None,
        "max_m_star": None,
        "verdict": "INCONCLUSIVE",
        "bands_locked": {"low": MAINT_LOW, "moderate": MAINT_MOD},
        "note": (
            "Expanded K* would require admitting a holdout that is already inside "
            "Phase-3B V_t. That is not catalog maintenance; it is a restatement of "
            "the already-computed Phase-3B K*."
        ),
    }


def secondary_holdouts(inv: dict) -> dict:
    return {
        "eligible": inv["eligible_secondary"],
        "n_eligible": len(inv["eligible_secondary"]),
        "consistent_with_primary": "N/A",
        "note": (
            "No pre-existing certified-valid corpus is both task-mapped and excluded "
            "from Phase-3B V_t. Generated-code witnesses lack stored implementations. "
            "First-principles, library, and random occupants are inside the 412."
        ),
    }


def external_invalid() -> dict:
    return {
        "EXTERNAL_INVALID_TRANSFER": "NOT_AVAILABLE",
        "reason": "Replaced at runtime by optional_invalid.score_optional_invalids.",
    }


def dsp_mechanism() -> dict:
    return {
        "run": False,
        "same_order": "Not scored: intended Type-I same-order probes leaked into catalog fitting.",
        "type_i": "Not scored as an external holdout. Type-I probes were Phase-3B valids.",
        "loose_vs_tight": "Not scored.",
        "filter_type": "Not scored.",
        "rejected_still_certified": "N/A",
        "verdict": "WEAK",
        "note": (
            "A DSP-mechanism table on leaked in-sample probes would not isolate "
            "realization diversity outside the fitting universe."
        ),
    }
