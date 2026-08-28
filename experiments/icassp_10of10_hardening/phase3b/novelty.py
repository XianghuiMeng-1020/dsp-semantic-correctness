"""Phase-3B novelty / framing from frozen RCC numbers. Bands were locked before inspection."""
from __future__ import annotations

from experiments.icassp_10of10_hardening.phase3b.config import RHO_LOW


def catalog_verdict(summary: dict) -> str:
    n = summary["n_tasks"]
    if summary["exact_optimum"] < n:
        return "CATALOG_ANALYSIS_INCONCLUSIVE"
    high_near = summary["bands"]["high"] + summary["bands"]["near_enumerative"]
    tiny = summary["k1"] + summary["k2"] + summary["k3_5"]  # used only as a count later
    low_or_le3 = summary["bands"]["low"] + sum(
        1 for _ in range(0)
    )
    # Locked rule: WEAK if >=15 tasks have K*<=3 or Low burden.
    # We pass an extra field from caller if needed; compute from summary buckets.
    le3 = summary["k1"] + summary["k2"] + summary["k3_5"]
    # k3_5 includes 3,4,5 so K*<=3 is k1+k2 + part of k3_5. Conservative WEAK uses k1+k2 only plus low band.
    if high_near >= 15:
        return "CATALOG_BURDEN_STRONG"
    if summary.get("k_le3", summary["k1"] + summary["k2"]) >= 15 or summary["bands"]["low"] >= 15:
        return "CATALOG_BURDEN_WEAK"
    return "CATALOG_BURDEN_MIXED"


def decide(coeff_sum: dict, resp_sum: dict | None, avs: dict, val: dict) -> dict:
    verdict = catalog_verdict(coeff_sum)
    le3 = coeff_sum.get("k_le3", coeff_sum["k1"] + coeff_sum["k2"])
    small = le3
    blocker = (
        verdict == "CATALOG_BURDEN_WEAK"
        or val.get("verdict") == "FAIL"
        or coeff_sum["undecided"] > 2
        or le3 >= 15
    )
    # Novelty gate: nontrivial burden + disclaimers. Do not inflate.
    nontrivial = verdict in {"CATALOG_BURDEN_STRONG", "CATALOG_BURDEN_MIXED"} and coeff_sum["exact_optimum"] == 20
    gate = (
        nontrivial
        and verdict != "CATALOG_BURDEN_WEAK"
        and coeff_sum["median_k"] is not None
        and coeff_sum["median_k"] >= 4
    )
    framing = "B"
    score = 7.2 if verdict == "CATALOG_BURDEN_STRONG" else (6.9 if verdict == "CATALOG_BURDEN_MIXED" else 6.4)
    if verdict == "CATALOG_BURDEN_WEAK":
        framing = "A"
        score = 6.2
    return {
        "catalog_verdict": verdict,
        "best_framing": framing,
        "internal_novelty": score,
        "NOVELTY_10OF10_GATE": "PASS" if gate else "NOT_YET",
        "scientific_blocker": "YES" if blocker else "NO",
        "Q_setcover_novel": "NO",
        "Q_prototype_novel": "NO",
        "close_dsp_same_audit": "NO",
        "attacks": {
            "K1": "PARTIAL",
            "K2": "PARTIAL",
            "K3": "OPEN",
            "K4": "PARTIAL",
            "K5": "PARTIAL",
            "K6": "PARTIAL",
        },
        "strongest_novelty": (
            "On a frozen, independently labeled FIR/IIR mask universe, the existing "
            "min-distance common-threshold reference oracle requires a measurable catalog "
            "of actual specification-valid realizations to reproduce specification membership. "
            "That burden number is a finite-universe adequacy diagnostic, not a new set-cover method."
        ),
        "strongest_attack": "A reviewer can still say this is prototype selection on a finite labeled set.",
        "kstar_extends_k135": bool(coeff_sum.get("median_k") and coeff_sum["median_k"] > 5),
        "small_k_count": small,
        "rho_low_cutoff": RHO_LOW,
        "resp_verdict": None if resp_sum is None else catalog_verdict(resp_sum).replace("CATALOG_BURDEN_", "").replace("CATALOG_ANALYSIS_", ""),
        "le3_bucket": le3,
        "avs_counts": avs["counts"],
    }
