#!/usr/bin/env python3
"""Phase 2A validation: registry + independent specification checker."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.spec_checker import check_specification, get_task, load_registries  # noqa: E402
from src.suite_s_fixtures import ALTERNATE_VALID, CANONICAL, MUTANTS  # noqa: E402

ARM_N_PREFIX = {
    "fir_lowpass_spec": "fir_lp_loose_8k",
    "fir_bandpass_spec": "fir_bp_loose_8k",
    "fir_bandstop_spec": "fir_bs_loose_8k",
    "iir_lowpass_stable_spec": "iir_lp_loose_8k",
}


def load_filter(path: Path):
    if path.suffix == ".npy":
        return np.load(path)
    z = np.load(path)
    return {"b": z["b"], "a": z["a"]}


def check_arm_n_dir(folder: Path, expect_pass: bool) -> tuple[int, int, list[str]]:
    n_ok = n_tot = 0
    fails = []
    for p in sorted(folder.glob("*")):
        if p.suffix not in {".npy", ".npz"}:
            continue
        legacy = p.name.split("__")[0]
        tid = ARM_N_PREFIX[legacy]
        n_tot += 1
        out = check_specification(tid, load_filter(p))
        hit = out["pass"] == expect_pass
        n_ok += int(hit)
        if not hit:
            fails.append(f"{p.name} pass={out['pass']} residuals={out['residuals']}")
    return n_ok, n_tot, fails


def singleton_disagreement(tid: str, fn_a, fn_b) -> float:
    task = get_task(tid)
    tv = task["constraints"]["test_vector"]
    if tid == "integer_delay_impulse":
        a, b = np.asarray(fn_a(), float), np.asarray(fn_b(), float)
        n = min(len(a), len(b))
        return float(np.linalg.norm(a[:n] - b[:n]) / max(np.linalg.norm(b[:n]), 1e-18))
    if tid == "crosscorrelation_integer_delay":
        rng = np.random.default_rng(tv["seed"])
        x = rng.standard_normal(int(tv["N"]))
        y = np.roll(x, int(tv["L"]))
        return 0.0 if int(fn_a(x, y)) == int(fn_b(x, y)) else 1.0
    if tid == "circular_convolution_theorem":
        rng = np.random.default_rng(tv["seed"])
        x = rng.standard_normal(int(tv["N"]))
        h = rng.standard_normal(int(tv["N"]))
        ya, yb = np.asarray(fn_a(x, h), float), np.asarray(fn_b(x, h), float)
        return float(np.linalg.norm(ya - yb) / max(np.linalg.norm(yb), 1e-18))
    if tid == "linear_convolution_zero_padded_dft":
        rng = np.random.default_rng(tv["seed"])
        x = rng.standard_normal(int(tv["Nx"]))
        h = rng.standard_normal(int(tv["Nh"]))
        ya, yb = np.asarray(fn_a(x, h), float), np.asarray(fn_b(x, h), float)
        if ya.shape != yb.shape:
            return 1.0
        return float(np.linalg.norm(ya - yb) / max(np.linalg.norm(yb), 1e-18))
    return 0.0


def main() -> int:
    load_registries()
    report = {
        "suite_s_n": 0,
        "suite_n_n": 0,
        "arm_n_controls": None,
        "arm_n_mutants": None,
        "suite_s_canonical": None,
        "suite_s_mutants": None,
        "dropped_singletons": [],
        "failures": [],
    }

    s = json.loads((ROOT / "registry/suite_s.json").read_text(encoding="utf-8"))
    n = json.loads((ROOT / "registry/suite_n.json").read_text(encoding="utf-8"))
    report["suite_s_n"] = s["n_tasks"]
    report["suite_n_n"] = n["n_tasks"]
    print(f"registry Suite S: {s['n_tasks']}  Suite N: {n['n_tasks']}")
    if s["n_tasks"] != 8 or n["n_tasks"] != 20:
        print("REGISTRY_COUNT: FAIL")
        report["failures"].append("registry counts")
        (ROOT / "PHASE_2A_REGISTRY_CHECKER_REPORT.json").write_text(
            json.dumps(report, indent=2), encoding="utf-8"
        )
        return 1

    c_ok, c_n, c_fail = check_arm_n_dir(ROOT / "data/arm_n_valid_controls", True)
    m_ok, m_n, m_fail = check_arm_n_dir(ROOT / "data/arm_n_mutants", False)
    report["arm_n_controls"] = f"{c_ok}/{c_n}"
    report["arm_n_mutants"] = f"{m_ok}/{m_n}"
    print(f"Arm N controls S_t=1: {c_ok}/{c_n}")
    print(f"Arm N mutants  S_t=0: {m_ok}/{m_n}")
    if c_fail:
        print("CONTROL_FAILS", *c_fail, sep="\n  ")
        report["failures"].extend(c_fail)
    if m_fail:
        print("MUTANT_FAILS", *m_fail, sep="\n  ")
        report["failures"].extend(m_fail)
    if c_ok != 12 or c_n != 12 or m_ok != 12 or m_n != 12:
        print("ARM_N_CHECKER: FAIL — stop before Suite S expansion")
        (ROOT / "PHASE_2A_REGISTRY_CHECKER_REPORT.json").write_text(
            json.dumps(report, indent=2), encoding="utf-8"
        )
        return 1

    s_can_ok = s_can_n = 0
    s_mut_ok = s_mut_n = 0
    for tid, fn in CANONICAL.items():
        s_can_n += 1
        out = check_specification(tid, fn)
        s_can_ok += int(out["pass"])
        print(f"  S canonical {tid}: pass={out['pass']} other={out['residuals']['other_constraints']}")
        if not out["pass"]:
            report["failures"].append(f"canonical fail {tid}")
        if tid in ALTERNATE_VALID:
            alt = ALTERNATE_VALID[tid]
            out_alt = check_specification(tid, alt)
            d = singleton_disagreement(tid, fn, alt)
            print(f"    alt valid pass={out_alt['pass']} disagreement={d:.3e}")
            if out["pass"] and out_alt["pass"] and d > 0.05:
                report["dropped_singletons"].append(tid)
                print(f"    INVALID SINGLETON DESIGN: {tid}")

    for tid, mechs in MUTANTS.items():
        for name, fn in mechs.items():
            s_mut_n += 1
            out = check_specification(tid, fn)
            s_mut_ok += int(not out["pass"])
            print(f"  S mutant {tid}/{name}: pass={out['pass']}")
            if out["pass"]:
                report["failures"].append(f"mutant accepted {tid}/{name}")

    report["suite_s_canonical"] = f"{s_can_ok}/{s_can_n}"
    report["suite_s_mutants"] = f"{s_mut_ok}/{s_mut_n}"
    print(f"Suite S canonical S_t=1: {s_can_ok}/{s_can_n}")
    print(f"Suite S mutants  S_t=0: {s_mut_ok}/{s_mut_n}")

    blocked = bool(report["failures"] or report["dropped_singletons"])
    report["recommendation"] = "BLOCKED" if blocked else "READY_FOR_PHASE_2B"
    (ROOT / "PHASE_2A_REGISTRY_CHECKER_REPORT.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    print("RECOMMENDATION:", report["recommendation"])
    return 1 if blocked else 0


if __name__ == "__main__":
    raise SystemExit(main())
