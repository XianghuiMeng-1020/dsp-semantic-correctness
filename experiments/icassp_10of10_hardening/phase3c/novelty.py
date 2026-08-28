"""Phase-3C novelty gate. Internal score is not the PI gate."""
from __future__ import annotations


def decide(inv: dict, leak: dict) -> dict:
    attacks = {
        "C1_still_finite": "OPEN",
        "C2_just_prototype_testset": "PARTIAL",
        "C3_typei_too_similar": "PARTIAL",
        "C4_holdout_only_fir": "OPEN",
        "C5_st_wins_by_definition": "PARTIAL",
        "C6_maintenance_is_setcover": "PARTIAL",
        "C7_not_all_reference_matching": "PARTIAL",
        "C8_not_dsp": "PARTIAL",
    }
    n_closed_or_partial = sum(1 for v in attacks.values() if v in {"CLOSED", "PARTIAL"})
    high_open = ["C1_still_finite", "C4_holdout_only_fir"]
    gate_conditions = {
        "technical_correctness_10": True,
        "generic_test_oracle_disclaimed": True,
        "generic_prototype_disclaimed": True,
        "ambient_impossibility_disclaimed": True,
        "phase3b_rcc_exact_preserved": True,
        "genuinely_frozen_catalog_excluded_holdout": False,
        "nontrivial_transfer_or_maintenance": False,
        "dsp_interpretable": False,
        "no_close_dsp_same_audit": True,
        "three_sentence_contribution": True,
        "fits_4page": True,
        "redteam_7of8_no_high_open": False,
    }
    gate = all(gate_conditions.values())
    return {
        "EXTERNAL_TRANSFER": "EXTERNAL_TRANSFER_INCONCLUSIVE",
        "best_framing": "B",
        "internal_novelty": 6.4,
        "NOVELTY_10OF10_GATE": "PASS" if gate else "NOT_YET",
        "gate_conditions": gate_conditions,
        "attacks": attacks,
        "n_closed_or_partial": n_closed_or_partial,
        "high_severity_open": high_open,
        "generic_prototype_transfer": "KNOWN",
        "specification_conformance": "KNOWN",
        "close_dsp_same_audit": "NO",
        "novelty_boundary": "PARTIAL",
        "scientific_blocker": "YES",
        "blocker": leak["blocker"],
        "strongest_novelty": (
            "Phase 3C does not add an external-validity transfer result. "
            "It does establish that the confirmatory Type-I corpus cannot be sold as a "
            "catalog-excluded holdout: those 1260 probes were inside Phase-3B V_t, and "
            "467 of 825 coefficient catalog members are probe paths. The finite-universe "
            "attack therefore remains open. Generic prototype selection and specification "
            "conformance testing remain known; no close DSP paper with the same "
            "catalog-excluded transfer/maintenance audit was found."
        ),
        "strongest_attack": (
            "Without a catalog-excluded certified-valid holdout, K* remains a finite-universe "
            "diagnostic and cannot be promoted to an external-validity claim."
        ),
        "manuscript_safe_claim": (
            "On the frozen confirmatory universe, exact realization-reference scoring requires "
            "a catalog of observed specification-valid implementations (Phase-3B median "
            "coefficient K*=23). The previously frozen Type-I probe set cannot be used to "
            "claim out-of-catalog transfer, because those probes were candidate and selected "
            "references when K* was computed. The paper still cannot claim that reference "
            "matching is generally impossible, that an ambient center cannot exist, or that "
            "generic prototype selection is novel."
        ),
        "eligible_primary": inv["eligible_primary"],
        "framing_scores": {
            "A": {
                "novelty": 6.2,
                "dsp": 8.0,
                "simplicity": 8.5,
                "page4": 8.5,
                "reviewer_resistance": 6.0,
                "note": "Already established in Phase 1.",
            },
            "B": {
                "novelty": 6.4,
                "dsp": 8.0,
                "simplicity": 7.0,
                "page4": 7.0,
                "reviewer_resistance": 6.5,
                "note": "Hierarchy plus exact RCC; Phase 3C did not add transfer.",
            },
            "C": {
                "novelty": 5.5,
                "dsp": 7.0,
                "simplicity": 5.0,
                "page4": 4.5,
                "reviewer_resistance": 3.5,
                "note": "Certified extensibility is not established; do not claim C.",
            },
            "D": {
                "novelty": 6.3,
                "dsp": 8.0,
                "simplicity": 7.5,
                "page4": 8.0,
                "reviewer_resistance": 7.0,
                "note": "Conservative fallback if the manuscript stays on specification-defined correctness.",
            },
        },
    }
