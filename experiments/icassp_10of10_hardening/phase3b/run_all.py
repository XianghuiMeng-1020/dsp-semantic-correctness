"""Phase-3B reproduction. Does not write Phase-0/1/2/3A artifacts."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.icassp_10of10_hardening.phase3b.ambient_vs import classify  # noqa: E402
from experiments.icassp_10of10_hardening.phase3b.config import OUT_DIR  # noqa: E402
from experiments.icassp_10of10_hardening.phase3b.console_report import print_console  # noqa: E402
from experiments.icassp_10of10_hardening.phase3b.novelty import decide  # noqa: E402
from experiments.icassp_10of10_hardening.phase3b.rcc import run_metric, summarize  # noqa: E402
from experiments.icassp_10of10_hardening.phase3b.validation import validate  # noqa: E402
from experiments.icassp_10of10_hardening.phase3b.verify_frozen import verify_all  # noqa: E402
from experiments.icassp_10of10_hardening.phase3b.write_reports import write_all_reports  # noqa: E402
from src.verification.io_utils import dump_json  # noqa: E402


def _lib_counts(bundle: dict) -> tuple[int, int]:
    yes = no = 0
    for t in bundle["tasks"]:
        st = t["library"].get("status")
        if st == "EXACT_OPTIMUM" and t["library"].get("K_obs_star"):
            yes += 1
        else:
            no += 1
    return yes, no


def _headline(cs, rs, avs, nov, val, lib_yes, lib_no) -> dict:
    bands = cs["bands"]
    strongest_c = (
        f"Observed-valid coefficient RCC has median K*={cs['median_k']} "
        f"(ρ median {cs['median_rho']}); verdict {nov['catalog_verdict']}."
    )
    strongest_r = (
        f"Response RCC median K*={rs['median_k']}; {rs['k1']} tasks have K*=1."
    )
    if avs["counts"]["R2"] >= avs["counts"]["R1"]:
        avs_s = "An abstract ambient center often exists, but a compact realizable catalog does not."
    else:
        avs_s = "Where an ambient center exists, a compact realizable catalog sometimes recovers membership."
    blocker = nov["scientific_blocker"]
    verdict = "NOVELTY_BLOCKER_REQUIRES_PI_REVIEW" if blocker == "YES" else "READY_FOR_PI_FINAL_NOVELTY_DECISION"
    return {
        "coeff_exact": cs["exact_optimum"],
        "coeff_bound": cs["bound_only"],
        "coeff_und": cs["undecided"],
        "coeff_k1": cs["k1"],
        "coeff_k2": cs["k2"],
        "coeff_k35": cs["k3_5"],
        "coeff_k610": cs["k6_10"],
        "coeff_kgt10": cs["k_gt10"],
        "coeff_med_k": cs["median_k"],
        "coeff_min_k": cs["min_k"],
        "coeff_max_k": cs["max_k"],
        "coeff_med_rho": cs["median_rho"],
        "coeff_min_rho": cs["min_rho"],
        "coeff_max_rho": cs["max_rho"],
        "coeff_low": bands["low"],
        "coeff_mod": bands["moderate"],
        "coeff_high": bands["high"],
        "coeff_near": bands["near_enumerative"],
        "coeff_collisions": cs["zero_distance_collisions"],
        "catalog_verdict": nov["catalog_verdict"],
        "strongest_coeff": strongest_c,
        "resp_n": rs["n_tasks"],
        "resp_exact": rs["exact_optimum"],
        "resp_k1": rs["k1"],
        "resp_med_k": rs["median_k"],
        "resp_med_rho": rs["median_rho"],
        "resp_verdict": nov.get("resp_verdict") or "N/A",
        "strongest_resp": strongest_r,
        "lib_yes": lib_yes,
        "lib_no": lib_no,
        "lib_n": lib_yes + lib_no,
        "R1": avs["counts"]["R1"],
        "R2": avs["counts"]["R2"],
        "R3": avs["counts"]["R3"],
        "R4": avs["counts"]["R4"],
        "strongest_avs": avs_s,
        "novelty_boundary": "CLEAR",
        "atk_K1": nov["attacks"]["K1"],
        "atk_K2": nov["attacks"]["K2"],
        "atk_K3": nov["attacks"]["K3"],
        "atk_K4": nov["attacks"]["K4"],
        "atk_K5": nov["attacks"]["K5"],
        "atk_K6": nov["attacks"]["K6"],
        "best_framing": nov["best_framing"],
        "internal_novelty": f"{nov['internal_novelty']:.1f}",
        "novelty_gate": nov["NOVELTY_10OF10_GATE"],
        "strongest_novelty": nov["strongest_novelty"],
        "strongest_attack": nov["strongest_attack"],
        "scientific_blocker": blocker,
        "strongest_positive": strongest_c,
        "strongest_negative": (
            "K* is a finite-universe diagnostic; set-cover/prototype selection are not novel; "
            "an ambient center is not a realizable filter."
        ),
        "can_claim": (
            "On this frozen universe, exact realization-reference matching requires a catalog "
            "of observed valid implementations whose size is reported per task; it is not K=1."
        ),
        "cannot_claim": (
            "The paper cannot claim a new set-cover algorithm, an infinite-set catalog size, "
            "or that specification checking is universally necessary."
        ),
        "verdict": verdict,
        "validation_verdict": val["verdict"],
    }


def run_science() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print("[phase3b] coefficient RCC", flush=True)
    coeff = run_metric("coeff")
    print("[phase3b] response RCC", flush=True)
    resp = run_metric("resp")
    cs, rs = summarize(coeff), summarize(resp)
    dump_json(OUT_DIR / "coeff_summary.json", cs)
    dump_json(OUT_DIR / "resp_summary.json", rs)
    dump_json(
        OUT_DIR / "reference_catalog_complexity.json",
        {"coeff": coeff, "resp": resp, "definition": "K_obs_star = min |R| over observed valids for existing min-distance common-threshold oracle"},
    )
    print("[phase3b] validation", flush=True)
    val = validate(coeff)
    dump_json(OUT_DIR / "validation.json", val)
    avs = classify(coeff, resp)
    dump_json(OUT_DIR / "ambient_vs_catalog.json", avs)
    nov = decide(cs, rs, avs, val)
    dump_json(OUT_DIR / "novelty.json", nov)
    lib_yes, lib_no = _lib_counts(coeff)
    hl = _headline(cs, rs, avs, nov, val, lib_yes, lib_no)
    dump_json(OUT_DIR / "headline.json", hl)


def verify_existing() -> int:
    print("[phase3b] verify frozen original science + Phase-3B catalogs", flush=True)
    result = verify_all()
    write_all_reports()
    print(
        f"[phase3b] verify ok={result['ok']} original={result['original_reproduction']} "
        f"phase3b={result['phase3b_reproduction']}",
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
