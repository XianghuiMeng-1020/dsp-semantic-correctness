"""Novelty / contribution / K* decision from frozen Phase-3A numbers. No manuscript edit."""
from __future__ import annotations


def decide(coeff: dict, resp: dict, hier: dict, prior: dict) -> dict:
    ca = hier["coeff"]["counts"]
    nA, nB, nC, nD = ca["A"], ca["B"], ca["C"], ca["D"]
    exact = coeff["EXACT_RATIONAL_CERTIFICATE"]
    high = coeff["HIGH_PRECISION_DUAL_CERTIFICATE"]
    num_only = coeff["NUMERICAL_LP_ONLY"]
    n_sep = coeff["AMBIENT_SEPARABLE"]
    n_nos = coeff["NO_AMBIENT_CENTER"]

    if nB >= 10 or nC >= 10:
        kstar = "HIGH_VALUE"
        kstar_r = (
            "Type B is the dominant coefficient outcome: an unrestricted Euclidean center "
            "(often a halfspace / center at infinity) recovers the frozen labels, but no "
            "observed valid realization does. The remaining reference-oracle question is "
            "exactly catalog complexity K* over observed valids. Phase 3A does not run K*."
        )
    elif nA >= 15:
        kstar = "MEDIUM_VALUE"
        kstar_r = (
            "Single Euclidean centers fail even when unrestricted. K* would ask a different "
            "question (union of occupant-centered balls). That is theoretically relevant and "
            "already partly addressed by the manuscript's K=1,3,5,all-library table. Exact K* "
            "is set-cover-like, page-costly on a 4-page paper, and is not required to support "
            "the Phase-3A Type-A statement. Not HIGH_VALUE: it would be another number, not a "
            "necessary novelty repair."
        )
    else:
        kstar = "LOW_VALUE"
        kstar_r = "Ambient results do not create a clean K* increment beyond the existing catalog table."

    if n_sep >= 14:
        blocker = True
        blocker_why = "unrestricted centers restore coefficient separability for a large majority of tasks"
    else:
        blocker = False
        blocker_why = None

    # scores 0-10
    if nA == 20 and exact + high >= 18:
        framing = "C"
        nov = 7.6
    elif nA >= 15:
        framing = "C"
        nov = 7.3
    elif nB >= 10:
        framing = "B"
        nov = 6.8
    else:
        framing = "B"
        nov = 6.4

    q4 = (
        "NO — a testing reviewer can correctly say the oracle problem and sphere LP are known, "
        "but cannot correctly say that this frozen DSP universe was already shown to be "
        "non-spherically-separable under the paper's confirmatory embedding with certificates."
    )
    q5 = (
        "YES, as methodology: the object is specification-defined filter membership versus "
        "realization-centered scoring, which is a DSP evaluation question. It is not a new designer."
    )
    if nB + nC >= 10:
        q5 = (
            "PARTIAL — ambient rescue would re-open 'a better geometric center exists' and weaken "
            "the claim that specification predicates are needed to represent validity."
        )

    attacks = {
        "N1": {
            "title": "The general oracle problem was known decades ago.",
            "severity_before": "HIGH",
            "evidence_after": "Confirmed. Weyuker 1982; Barr et al. TSE 2015. Q1=NO.",
            "residual": "LOW as a novelty claim; HIGH if the paper were sold as introducing oracles.",
            "defense": "Cite the oracle problem as background. Claim only the DSP reference-adequacy audit.",
            "more_science": "NO",
        },
        "N2": {
            "title": "Sphere separability by LP is textbook convex optimization.",
            "severity_before": "HIGH",
            "evidence_after": "Confirmed. Astorino–Gaudioso; Tax–Duin SVDD; Boyd–Vandenberghe. Q2=NO.",
            "residual": "LOW if named as a diagnostic; FATAL if named as a new theorem.",
            "defense": "Call Γ^amb an unrestricted-center adequacy diagnostic, not a new separator.",
            "more_science": "NO",
        },
        "N3": {
            "title": "The finite-set geometry is mathematically elementary.",
            "severity_before": "HIGH",
            "evidence_after": (
                f"Coefficient ambient: separable={n_sep} non-separable={n_nos}; "
                f"Type A/B/C/D = {nA}/{nB}/{nC}/{nD}; exact-rational={exact}."
            ),
            "residual": "MEDIUM. Elementary does not mean the DSP measurement was already done.",
            "defense": "Sell the hierarchy + certificates on S_t, not the expansion of ||i-c||^2.",
            "more_science": "NO unless certificates are only NUMERICAL_LP_ONLY.",
        },
        "N4": {
            "title": "The paper merely applies software-testing ideas to filters.",
            "severity_before": "HIGH",
            "evidence_after": "No matching DSP paper found that runs this three-level audit on independently labeled masks.",
            "residual": "MEDIUM. A reviewer can still call it 'testing applied to DSP'.",
            "defense": "The scientific object is mask-feasible sets vs realization balls — a filter-evaluation result.",
            "more_science": "Optional later: one more specification family. Not required to finish Phase 3A.",
        },
        "N5": {
            "title": "The result depends on one magnitude-mask task family.",
            "severity_before": "MEDIUM",
            "evidence_after": "Still 20 magnitude-mask tasks. Phase 3A did not add families.",
            "residual": "MEDIUM (scope, not a contradiction).",
            "defense": "State the universe explicitly. Do not claim all DSP correctness.",
            "more_science": "A second family would help a journal version; not Phase 3A.",
        },
        "N6": {
            "title": "The unrestricted center is not itself a realizable DSP implementation.",
            "severity_before": "MEDIUM",
            "evidence_after": (
                "Asymmetry is explicit: no ambient center ⇒ no realizable reference rescues a "
                "single-center Euclidean oracle; an ambient center ≠ a realizable filter."
            ),
            "residual": "LOW if Type A; HIGH if Type B is sold as 'a better filter exists'.",
            "defense": "Keep the asymmetry in any future sentence. Never infer realizability from a center.",
            "more_science": "NO",
        },
    }

    options = {
        "A": {
            "name": "conservative",
            "text": "Specification–reference mismatch, continuous correctness audit, and empirical geometry on the frozen corpus.",
            "novelty": "6.5",
            "icassp_fit": "8.0",
            "math": "9.0",
            "page_cost": "low",
            "resistance": "6.0 — still open to 'bad reference' until Level 3 is mentioned.",
        },
        "B": {
            "name": "geometry diagnostic",
            "text": "Fixed reference → best observed valid reference → unrestricted ambient center, with distinct symbols G_r, G_obs^*, Γ^amb.",
            "novelty": "7.2",
            "icassp_fit": "8.0",
            "math": "8.5",
            "page_cost": "medium (one table / one sentence)",
            "resistance": "8.0 if Type A dominates.",
        },
        "C": {
            "name": "reference-oracle adequacy audit",
            "text": (
                "Combine specification membership, continuous certification, fixed-center gap, "
                "observed-center robustness, and unrestricted-center separability certificates."
            ),
            "novelty": "7.6",
            "icassp_fit": "7.5",
            "math": "8.0",
            "page_cost": "medium-high on 4 pages; one paragraph + pointer to supplement if needed.",
            "resistance": "8.5 if certificates are exact or high-precision.",
        },
    }

    why = {
        "A": "Ambient results do not justify a stronger framing than the conservative package.",
        "B": "The three-level hierarchy is the new scientific object and fits a 4-page budget.",
        "C": "Type-A coefficient geometry plus certificates justify naming the whole audit, not only G_r.",
    }[framing]

    gates = {
        "FIXED_REFERENCE_ATTACK": "CLOSED" if nA + nB + nC == 20 else "PARTIAL",
        "BAD_REFERENCE_ATTACK": "CLOSED" if nA + nB == 20 and nC == 0 else ("PARTIAL" if nC else "CLOSED"),
        "UNRESTRICTED_CENTER_ATTACK": "CLOSED" if nA == 20 else ("PARTIAL" if nA >= 10 else "OPEN"),
        "THEOREM_OBVIOUS_ATTACK": "PARTIAL",
        "KNOWN_ORACLE_ATTACK": "PARTIAL",
    }
    if nC:
        gates["BAD_REFERENCE_ATTACK"] = "PARTIAL"

    return {
        "attacks": attacks,
        "KSTAR_NEXT": kstar,
        "kstar_rationale": kstar_r,
        "blocker_majority_separable": blocker,
        "blocker_why": blocker_why,
        "Q1": "NO",
        "Q2": "NO",
        "Q3": (
            "The manuscript-specific object is a certified three-level adequacy audit of "
            "realization-reference scoring against specification-defined FIR/IIR mask membership "
            "on a frozen independently labeled finite universe — not the oracle problem and not sphere LP."
        ),
        "Q4": q4,
        "Q5": q5,
        "contribution": {"options": options, "best": framing, "why": why},
        "gates": gates,
        "internal_novelty_score": nov,
        "certificate_counts": {"exact": exact, "high": high, "numerical": num_only},
        "resp_precision_robust": resp.get("precision_robust"),
    }
