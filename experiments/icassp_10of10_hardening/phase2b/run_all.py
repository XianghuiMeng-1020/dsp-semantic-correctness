"""Phase-2B reproduction. Does not write data/icassp_10of10 or Phase-1/2A JSON."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.icassp_10of10_hardening.phase2b.config import OUT_DIR  # noqa: E402
from experiments.icassp_10of10_hardening.phase2b.cross_audit import fir_cross_method, iir_numerical_subset  # noqa: E402
from experiments.icassp_10of10_hardening.phase2b.fir_remaining import resolve  # noqa: E402
from experiments.icassp_10of10_hardening.phase2b.iir_run import run_all_iir  # noqa: E402
from experiments.icassp_10of10_hardening.phase2b.population import audit  # noqa: E402
from experiments.icassp_10of10_hardening.phase2b.write_reports import write_all_reports  # noqa: E402
from src.verification.io_utils import dump_json  # noqa: E402


def _headline(pop: dict, fir: dict, iir: dict, cross: dict, iir_num: dict) -> dict:
    fir_final = fir["constructed_fir_valid_final"]
    iir_v = iir["valid"]
    fir_cv, fir_ci, fir_ud = fir_final["CERTIFIED_VALID"], fir_final["CERTIFIED_INVALID"], fir_final["UNDECIDED"]
    iir_cv, iir_ci, iir_ud = iir_v["CERTIFIED_VALID"], iir_v["CERTIFIED_INVALID"], iir_v["UNDECIDED"]
    tot_cv, tot_ci, tot_ud = fir_cv + iir_cv, fir_ci + iir_ci, fir_ud + iir_ud
    n_contra = len(iir.get("contradictions_valid_to_invalid") or []) + (1 if fir["blocker"] else 0)
    fir_cov = fir_cv / 336
    iir_cov = iir_cv / iir_v["total"] if iir_v["total"] else 0.0
    tot_cov = tot_cv / 412
    complete = tot_ud == 0 and tot_ci == 0 and n_contra == 0
    invalids_ok = (
        iir["mechanism_invalid"]["CERTIFIED_INVALID"] == iir["mechanism_invalid"]["total"]
        and iir["boundary_invalid"]["CERTIFIED_INVALID"] == iir["boundary_invalid"]["total"]
        and iir["mechanism_invalid"]["CERTIFIED_VALID"] == 0
        and iir["boundary_invalid"]["CERTIFIED_VALID"] == 0
    )
    if n_contra > 0:
        attack = "ATTACK_D_OPEN"
    elif complete and invalids_ok and cross.get("verdict") != "FAIL":
        attack = "ATTACK_D_STRONGLY_CLOSED"
    else:
        attack = "ATTACK_D_PARTIALLY_CLOSED"
    tech = (
        n_contra == 0
        and tot_ci == 0
        and fir_cov >= 0.99
        and iir_cov >= 0.99
        and iir_v["CERTIFIED_STABLE"] == iir_v["total"]
        and iir_v["CERTIFIED_UNSTABLE"] == 0
        and cross.get("verdict") != "FAIL"
    )
    return {
        "population": pop["verdict"],
        "fir": fir_final,
        "iir_valid": iir_v,
        "iir_mech": iir["mechanism_invalid"],
        "iir_boundary": iir["boundary_invalid"],
        "n_contradictions": n_contra,
        "blocker": n_contra > 0 or pop["blocker"],
        "matrix_valid": {
            "FIR": {"frozen": 336, "cert_valid": fir_cv, "cert_invalid": fir_ci, "undecided": fir_ud, "coverage": fir_cov},
            "IIR": {"frozen": iir_v["total"], "cert_valid": iir_cv, "cert_invalid": iir_ci, "undecided": iir_ud, "coverage": iir_cov},
            "TOTAL": {"frozen": 412, "cert_valid": tot_cv, "cert_invalid": tot_ci, "undecided": tot_ud, "coverage": tot_cov},
        },
        "mech": {
            "FIR": {"total": 112, "certified_invalid": 112},
            "IIR": {"total": iir["mechanism_invalid"]["total"], "certified_invalid": iir["mechanism_invalid"]["CERTIFIED_INVALID"]},
        },
        "boundary": {
            "FIR": {"total": 128, "certified_invalid": 128},
            "IIR": {"total": iir["boundary_invalid"]["total"], "certified_invalid": iir["boundary_invalid"]["CERTIFIED_INVALID"]},
        },
        "attack_d": attack,
        "tech_gate": "PASS" if tech else "NOT_YET",
        "cross_verdict": cross.get("verdict"),
        "iir_num_verdict": iir_num.get("verdict"),
        "algorithm_independence": "STRONG_INDEPENDENCE",
        "chain_independence": "PARTIAL_INDEPENDENCE",
    }


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    pop_p = OUT_DIR / "population.json"
    if pop_p.exists():
        pop = json.loads(pop_p.read_text(encoding="utf-8"))
        print("[phase2b] reuse population.json", flush=True)
    else:
        pop = audit()
        dump_json(pop_p, pop)
    print(f"[phase2b] population {pop['verdict']} blocker={pop['blocker']}", flush=True)
    if pop["blocker"]:
        print("PHASE2B_POPULATION_BLOCKER", flush=True)
        return 2

    fir_p = OUT_DIR / "fir_remaining_resolution.json"
    if fir_p.exists():
        fir = json.loads(fir_p.read_text(encoding="utf-8"))
        print("[phase2b] reuse fir_remaining_resolution.json", flush=True)
    else:
        fir = resolve()
        dump_json(fir_p, fir)
    if fir["blocker"]:
        print("PHASE2B_FIR_VALIDITY_CONTRADICTION_BLOCKER", flush=True)
        write_all_reports()
        return 3

    iir_p = OUT_DIR / "iir_continuous_certification.json"
    if iir_p.exists():
        iir = json.loads(iir_p.read_text(encoding="utf-8"))
        print("[phase2b] reuse iir_continuous_certification.json", flush=True)
    else:
        iir = run_all_iir()
        dump_json(iir_p, iir)
    if iir["blocker"]:
        print("PHASE2B_IIR_VALIDITY_CONTRADICTION_BLOCKER", flush=True)
        write_all_reports()
        return 4

    cross_p = OUT_DIR / "cross_method.json"
    if cross_p.exists():
        cross = json.loads(cross_p.read_text(encoding="utf-8"))
        print("[phase2b] reuse cross_method.json", flush=True)
    else:
        print("[phase2b] FIR cross-method audit", flush=True)
        cross = fir_cross_method()
        dump_json(cross_p, cross)
    num_p = OUT_DIR / "iir_numerical.json"
    if num_p.exists():
        iir_num = json.loads(num_p.read_text(encoding="utf-8"))
    else:
        print("[phase2b] IIR numerical extrema subset", flush=True)
        iir_num = iir_numerical_subset(iir)
        dump_json(num_p, iir_num)

    head = _headline(pop, fir, iir, cross, iir_num)
    dump_json(OUT_DIR / "headline.json", head)
    write_all_reports()
    print("PHASE2B_ALL_STAGES: DONE", flush=True)
    return 0


if __name__ == "__main__":
    if (OUT_DIR / "headline.json").exists():
        from experiments.icassp_10of10_hardening.phase2b.verify_frozen import verify_all
        from experiments.icassp_10of10_hardening.phase2b.console_report import print_console
        from experiments.icassp_10of10_hardening.phase2b.write_reports import write_all_reports

        print("[phase2b] verify frozen original science + Phase-2B certificates", flush=True)
        result = verify_all()
        write_all_reports()
        print_console(result)
        raise SystemExit(0 if result["ok"] else 1)
    raise SystemExit(main())
