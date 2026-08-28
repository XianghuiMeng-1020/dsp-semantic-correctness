"""Phase-3A reproduction. Does not write data/icassp_10of10 or Phase-0/1/2 JSON."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.icassp_10of10_hardening.phase3a.coefficient_run import run_coefficient  # noqa: E402
from experiments.icassp_10of10_hardening.phase3a.config import OUT_DIR  # noqa: E402
from experiments.icassp_10of10_hardening.phase3a.console_report import print_console  # noqa: E402
from experiments.icassp_10of10_hardening.phase3a.hierarchy import build_hierarchy  # noqa: E402
from experiments.icassp_10of10_hardening.phase3a.metric_audit import audit  # noqa: E402
from experiments.icassp_10of10_hardening.phase3a.novelty import decide  # noqa: E402
from experiments.icassp_10of10_hardening.phase3a.response_run import run_response  # noqa: E402
from experiments.icassp_10of10_hardening.phase3a.validation import synthetic_suite  # noqa: E402
from experiments.icassp_10of10_hardening.phase3a.verify_frozen import verify_all  # noqa: E402
from experiments.icassp_10of10_hardening.phase3a.write_reports import write_all_reports  # noqa: E402
from src.verification.io_utils import dump_json  # noqa: E402


def _headline(metric, coeff, resp, hier, val, nov) -> dict:
    nA = hier["coeff"]["counts"]["A"]
    nB = hier["coeff"]["counts"]["B"]
    n_sep = coeff["AMBIENT_SEPARABLE"]
    n_nos = coeff["NO_AMBIENT_CENTER"]
    exact_nc = sum(
        1
        for r in coeff["tasks"]
        if r["ambient_status"] == "NO_AMBIENT_CENTER"
        and r["certificate_strength"] == "EXACT_RATIONAL_CERTIFICATE"
    )
    if n_nos == 20:
        strongest_c = (
            "No unrestricted Euclidean center in the confirmatory coefficient embedding "
            "exactly recovers specification membership on any of the 20 frozen tasks."
        )
    elif n_sep >= 14:
        strongest_c = (
            "An unrestricted ambient center restores exact coefficient separability "
            "on a large majority of tasks; this is a novelty blocker."
        )
    else:
        strongest_c = (
            f"Ambient coefficient separability is mixed: {n_sep} separable, {n_nos} non-separable."
        )
    r_nos = resp["NO_AMBIENT_CENTER"]
    r_sep = resp["AMBIENT_SEPARABLE"]
    strongest_r = (
        f"On the confirmatory RMSE magnitude embedding, {r_nos}/20 tasks have no ambient center "
        f"and {r_sep}/20 are ambient-separable ({resp['precision_robust']} precision robustness)."
    )
    majority_sep = n_sep >= 14
    val_fail = val["verdict"] != "PASS" and val["verdict"] != "PASS_WITH_NUMERICAL_LIMITATION"
    blocker = "YES" if (majority_sep or val_fail or nov.get("blocker_majority_separable")) else "NO"
    verdict = "NOVELTY_BLOCKER_REQUIRES_PI_REVIEW" if blocker == "YES" else "READY_FOR_PI_PHASE3B_DECISION"
    if nA == 20:
        pos = "The bad-reference attack is closed in coefficient space: even an arbitrary ambient center fails."
        can = (
            "No single Euclidean-distance threshold center in the evaluated coefficient representation "
            "recovers specification membership over the frozen finite universe."
        )
    elif nB >= 14:
        pos = (
            "Phase-1 still stands: no observed valid reference restores coefficient separability. "
            "Phase-3A shows that an unrestricted ambient center does so on a large majority of tasks."
        )
        can = (
            "No observed valid realization in U_t restores a single-center coefficient oracle; "
            "that failure is not equivalent to the non-existence of any Euclidean center."
        )
    else:
        pos = "The three-level hierarchy distinguishes reference-choice failure from geometric incompatibility."
        can = (
            "Reference-oracle failure is not uniformly a bad-reference artifact; "
            "Level-3 must be cited with the Type A/B counts."
        )
    return {
        "branch": "research/icassp-final-10of10-scientific-hardening",
        "phase3a_tag": "icassp-10of10-phase3a-complete",
        "coeff_formula": metric["coefficient"]["exact_formula"],
        "coeff_euclidean": "YES" if metric["coefficient"]["euclidean_ball_equivalent"] else "NO",
        "resp_formula": metric["response"]["exact_formula"],
        "resp_euclidean": "YES" if metric["response"]["euclidean_ball_equivalent"] else "NO",
        "coeff_ambient_separable": n_sep,
        "coeff_ambient_nonseparable": n_nos,
        "coeff_undecided": coeff["UNDECIDED"],
        "exact_rational_no_center": exact_nc,
        "high_precision": coeff["HIGH_PRECISION_DUAL_CERTIFICATE"],
        "numerical_only": coeff["NUMERICAL_LP_ONLY"],
        "type_A": nA,
        "type_B": nB,
        "type_C": hier["coeff"]["counts"]["C"],
        "type_D": hier["coeff"]["counts"]["D"],
        "strongest_coeff": strongest_c,
        "resp_tasks": resp["n_tasks"],
        "resp_ambient_separable": r_sep,
        "resp_ambient_nonseparable": r_nos,
        "resp_undecided": resp["UNDECIDED"],
        "resp_precision_robust": resp["precision_robust"],
        "strongest_resp": strongest_r,
        "novelty_boundary": "CLEAR",
        "strongest_novelty": nov["Q3"],
        "strongest_attack": "A reviewer can still say the geometry is elementary and the oracle problem is old.",
        "gate_fixed_ref": nov["gates"]["FIXED_REFERENCE_ATTACK"],
        "gate_bad_ref": nov["gates"]["BAD_REFERENCE_ATTACK"],
        "gate_ambient": nov["gates"]["UNRESTRICTED_CENTER_ATTACK"],
        "gate_obvious": nov["gates"]["THEOREM_OBVIOUS_ATTACK"],
        "gate_oracle": nov["gates"]["KNOWN_ORACLE_ATTACK"],
        "KSTAR_NEXT": nov["KSTAR_NEXT"],
        "best_framing": nov["contribution"]["best"],
        "internal_novelty": f"{nov['internal_novelty_score']:.1f}",
        "scientific_blocker": blocker,
        "strongest_positive": pos,
        "strongest_negative": (
            "Generic sphere LP is not novel; response vectors are numerical; "
            "the result is a frozen finite-universe diagnostic, not a general impossibility theorem."
        ),
        "can_claim": can,
        "cannot_claim": (
            "The paper cannot claim that no metric, no multi-reference oracle, or no nonlinear "
            "boundary can recover validity, nor that specification-based verification is universally necessary."
        ),
        "verdict": verdict,
        "validation_verdict": val["verdict"],
    }


def run_science() -> dict:
    print("[phase3a] metric geometry audit", flush=True)
    metric = audit()
    dump_json(OUT_DIR / "metric_geometry.json", metric)
    print("[phase3a] synthetic validation", flush=True)
    syn = synthetic_suite()
    print("[phase3a] coefficient ambient-center", flush=True)
    coeff = run_coefficient()
    dump_json(OUT_DIR / "coefficient_ambient.json", coeff)
    print("[phase3a] response ambient-center", flush=True)
    resp = run_response()
    dump_json(OUT_DIR / "response_ambient.json", resp)
    hier = build_hierarchy(coeff, resp)
    dump_json(OUT_DIR / "hierarchy.json", hier)
    indep = coeff.get("independent_checks") or {}
    val_verdict = "PASS"
    if not syn["pass"] or not coeff["check_D_pass"] or not resp["check_D_pass"]:
        val_verdict = "FAIL"
    elif not all(v.get("pass") for v in indep.values()) and indep:
        val_verdict = "PASS_WITH_NUMERICAL_LIMITATION"
    validation = {
        "verdict": val_verdict,
        "synthetic": syn,
        "check_D_coeff": coeff["check_D_pass"],
        "check_D_resp": resp["check_D_pass"],
        "independent_checks": indep,
    }
    dump_json(OUT_DIR / "validation.json", validation)
    nov = decide(coeff, resp, hier, {})
    dump_json(OUT_DIR / "novelty.json", nov)
    headline = _headline(metric, coeff, resp, hier, validation, nov)
    dump_json(OUT_DIR / "headline.json", headline)
    return headline


def verify_existing() -> int:
    print("[phase3a] verify frozen original science + Phase-3A certificates", flush=True)
    result = verify_all()
    write_all_reports()
    print(
        f"[phase3a] verify ok={result['ok']} original={result['original_reproduction']} "
        f"phase3a={result['phase3a_reproduction']}",
        flush=True,
    )
    print_console(result)
    return 0 if result["ok"] else 1


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if (OUT_DIR / "headline.json").exists():
        return verify_existing()
    run_science()
    write_all_reports()
    return verify_existing()


if __name__ == "__main__":
    raise SystemExit(main())
