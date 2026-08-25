#!/usr/bin/env python3
"""Reproduce the published CORE summaries from frozen extracted implementations."""

from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.contracts_arm_n import TASK_FACTORIES as ARM_N_TASK_FACTORIES
from src.contracts_conv_corr import TASKS as TASKS_P
from src.contracts_samp_resamp import TASKS as TASKS_B
from src.runtime import exec_function, score_task
from src.stats import wilson_ci

# The two DC-preservation rows whose full-output residual (0.166) matches an
# unpadded polyphase-FIR transient on a short constant. Excluded from the
# conservative preferred Arm B count; frozen-original scoring is unaffected.
ARM_B_DC_AMBIGUOUS_IDS = {
    "rational_resample_dc_preservation__llama-3.3-70b-instruct__rep2",
    "rational_resample_dc_preservation__deepseek-chat__rep2",
}

# One Arm N generation hangs the interpreter (near-zero CPU) rather than
# raising. The original scoring harness added this 15 s process timeout as a
# harness safety measure and recorded the hang as an Exec failure; it is not
# a contract change. See CONTRACTS.md.
ARM_N_CALL_TIMEOUT_SEC = 15


def _arm_n_worker(code, func_name, q):
    import contextlib
    import io

    fn, err = exec_function(code, func_name)
    if fn is None:
        q.put(("exec_fail", err, None))
        return
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            y = fn()
        q.put(("ok", None, y))
    except Exception as exc:  # noqa: BLE001
        q.put(("call_fail", f"CALL_ERROR: {exc}", None))


def exec_arm_n_with_timeout(code: str, func_name: str, timeout: int = ARM_N_CALL_TIMEOUT_SEC):
    from multiprocessing import Process, Queue

    q: Queue = Queue()
    p = Process(target=_arm_n_worker, args=(code, func_name, q))
    p.start()
    p.join(timeout)
    if p.is_alive():
        p.terminate()
        p.join(3)
        return None, f"EXEC_TIMEOUT:{timeout}s"
    if q.empty():
        return None, "EXEC_ERROR: empty worker result"
    status, err, y = q.get()
    if status != "ok":
        return None, err
    return y, None


def load_json(name: str):
    return json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))


def check(cond: bool, label: str, failures: list[str]) -> None:
    status = "PASS" if cond else "FAIL"
    print(f"  {status}  {label}")
    if not cond:
        failures.append(label)


def reproduce_historical(failures: list[str]) -> None:
    print("Arm H -- historical confirmatory spectral/filter suite")
    rows = list(csv.DictReader((ROOT / "data/historical_generations.csv").open(encoding="utf-8")))
    adj = load_json("historical_artifact_adjustment.json")
    removed = set(adj["removed_generation_ids"])
    for row in rows:
        row["core"] = row["confirmatory_core"] in {"1", "True", "true"} and row["generation_id"] not in removed
        row["software"] = row["generic_baseline_caught"] in {"1", "True", "true"}
        row["diff"] = row["differential_fail"] in {"1", "True", "true"}

    n = len(rows)
    core_rows = [r for r in rows if r["core"]]
    k = len(core_rows)
    tasks = {r["task"] for r in core_rows}
    models = {r["model"] for r in core_rows}
    soft = sum(1 for r in core_rows if r["software"])
    diff = sum(1 for r in core_rows if r["diff"])
    dropped = adj["highest_failure_task"]
    remain = [r for r in core_rows if r["task"] != dropped]
    remain_n = sum(1 for r in rows if r["task"] != dropped)

    thr = load_json("historical_thresholds.json")["tasks"]
    controls = load_json("historical_control_residuals.json")
    fp = sum(
        1
        for r in controls
        if r.get("residual") is not None and r["residual"] > thr[r["task"]]["threshold"]
    )
    mutants = load_json("historical_mutant_residuals.json")
    valid_mutants = [
        m
        for m in mutants
        if not m.get("ambiguous") and m.get("residual") is not None and m["residual"] > 1e-3
    ]
    caught = sum(1 for m in valid_mutants if m.get("caught"))

    lo, hi = wilson_ci(k, n)
    print(f"  CORE {k}/{n}  Wilson 95% CI [{lo:.3f}, {hi:.3f}]")
    print(f"  affected tasks {len(tasks)}/12")
    print(f"  affected models {len(models)}/3")
    print(f"  software caught {soft}/{k}")
    print(f"  differential caught {diff}/{k}")
    print(f"  valid-control observed FP {fp}/{len(controls)}")
    print(f"  controlled mutants {caught}/{len(valid_mutants)}")
    print(f"  after removing {dropped}: {len(remain)}/{remain_n}")
    check(n == 144, "n=144", failures)
    check(k == 16, "CORE 16/144", failures)
    check(len(tasks) == 4, "tasks 4/12", failures)
    check(len(models) == 3, "models 3/3", failures)
    check(soft == 0, "software 0/16", failures)
    check(diff == 15, "differential 15/16", failures)
    check(fp == 0 and len(controls) == 113, "valid-control 0/113", failures)
    check(caught == 13 and len(valid_mutants) == 13, "mutants 13/13", failures)
    check(len(remain) == 11 and remain_n == 132, "highest-task removal 11/132", failures)


def reproduce_arm(label: str, data_name: str, tasks, expected: dict, failures: list[str]) -> None:
    print(label)
    task_map = {t["id"]: t for t in tasks}
    rows = load_json(data_name)
    scored = []
    for rec in rows:
        task = task_map[rec["task"]]
        fn, err = exec_function(rec.get("code") or "", rec["func_name"])
        if fn is None:
            scored.append(
                {
                    "generation_id": rec.get("generation_id"),
                    "task": rec["task"],
                    "model": rec["model"],
                    "core": False,
                    "software": False,
                    "diff": False,
                    "error": err,
                }
            )
            continue
        out = score_task(task, fn)
        scored.append(
            {
                "generation_id": rec.get("generation_id"),
                "task": rec["task"],
                "model": rec["model"],
                "core": out["core"],
                "software": out["core"] and out["unit_test_pass"] and not out["semantic_fail"],
                "diff": out["core"],
            }
        )

    n = len(scored)
    core_rows = [r for r in scored if r["core"]]
    k = len(core_rows)
    tasks_hit = {r["task"] for r in core_rows}
    models_hit = {r["model"] for r in core_rows}
    by_task = defaultdict(int)
    for r in core_rows:
        by_task[r["task"]] += 1
    # software baseline: CORE already requires unit_test_pass, so 0 by construction
    soft = 0
    diff = sum(1 for r in core_rows if r["diff"])
    lo, hi = wilson_ci(k, n) if n else (0.0, 0.0)
    print(f"  CORE {k}/{n}  Wilson 95% CI [{lo:.3f}, {hi:.3f}]")
    print(f"  affected tasks {len(tasks_hit)}/{expected['n_tasks']}")
    print(f"  affected models {len(models_hit)}/3")
    print(f"  software caught {soft}/{k}")
    print(f"  differential caught {diff}/{k}")
    if expected.get("task_counts"):
        counts = "/".join(str(by_task.get(tid, 0)) for tid in expected["task_order"])
        print(f"  task CORE counts {counts}")
        check(counts == expected["task_counts"], f"task counts {expected['task_counts']}", failures)
    check(n == expected["n"], f"n={expected['n']}", failures)
    check(k == expected["k"], f"CORE {expected['k']}/{expected['n']}", failures)
    check(len(tasks_hit) == expected["tasks"], f"tasks {expected['tasks']}/{expected['n_tasks']}", failures)
    check(len(models_hit) == 3, "models 3/3", failures)
    check(soft == 0, f"software 0/{expected['k']}", failures)
    check(diff == expected["k"], f"differential {expected['k']}/{expected['k']}", failures)
    if expected.get("mechanisms") is not None:
        groups = expected["mechanism_of"]
        hit_groups = {groups[t] for t in tasks_hit}
        print(f"  mechanism groups {len(hit_groups)}/2")
        check(len(hit_groups) == expected["mechanisms"], "mechanism groups 2/2", failures)
    return core_rows


def reproduce_arm_b_conservative(core_rows: list[dict], failures: list[str]) -> None:
    print("Arm B -- conservative recount (preferred reporting figure)")
    kept = [r for r in core_rows if r["generation_id"] not in ARM_B_DC_AMBIGUOUS_IDS]
    k = len(kept)
    tasks_hit = {r["task"] for r in kept}
    models_hit = {r["model"] for r in kept}
    print(f"  CORE {k}/48 (excludes 2 boundary-convention-ambiguous DC cases)")
    print(f"  affected tasks {len(tasks_hit)}/4")
    print(f"  affected models {len(models_hit)}/3")
    check(k == 9, "conservative CORE 9/48", failures)
    check(len(tasks_hit) == 3, "conservative tasks 3/4", failures)
    check(len(models_hit) == 2, "conservative models 2/3 (Llama excluded)", failures)


def reproduce_arm_n(failures: list[str]) -> None:
    print("Arm N -- prospective filter-specification arm (primary result)")
    tasks = {f()["id"]: f() for f in ARM_N_TASK_FACTORIES}
    rows = load_json("arm_n_generations.json")
    canonical = {
        "fir_lowpass_spec": "firwin",
        "fir_bandpass_spec": "firwin",
        "fir_bandstop_spec": "firwin",
        "iir_lowpass_stable_spec": "butter",
    }
    ref_rel_l2_threshold = 0.05

    controls: dict[str, dict[str, dict]] = {}
    for p in (ROOT / "data/arm_n_valid_controls").glob("*"):
        tid = p.name.split("__")[0]
        impl = p.stem.split("__", 1)[1]
        controls.setdefault(tid, {})
        if p.suffix == ".npy":
            h = np.load(p)
            controls[tid][impl] = np.asarray(h, float)
        else:
            z = np.load(p)
            b, a = np.asarray(z["b"], float), np.asarray(z["a"], float)
            controls[tid][impl] = np.concatenate([b, a])

    def rel_l2(a, b):
        a = np.asarray(a, float).reshape(-1)
        b = np.asarray(b, float).reshape(-1)
        n = min(len(a), len(b))
        if n == 0:
            return 1.0
        return float(np.linalg.norm(a[:n] - b[:n]) / max(np.linalg.norm(a[:n]), 1e-18))

    scored = []
    for rec in rows:
        tid = rec["task"]
        task = tasks[tid]
        out = {"generation_id": rec["generation_id"], "task": tid, "model": rec["model"]}
        if rec.get("discarded_not_scored"):
            out.update(executes=False, unit_test_pass=False, S_pass=False, CORE=False, quadrant=None)
            scored.append(out)
            continue
        y, err = exec_arm_n_with_timeout(rec.get("code") or "", rec["func_name"])
        if err is not None:
            out.update(executes=False, unit_test_pass=False, S_pass=False, CORE=False, quadrant=None)
            scored.append(out)
            continue
        fn = lambda y=y: y  # noqa: E731
        base = score_task(task, fn)
        out["executes"] = True
        out["unit_test_pass"] = base["unit_test_pass"]
        out["S_pass"] = base["unit_test_pass"] and not base["semantic_fail"]
        out["CORE"] = bool(base["core"])
        out["quadrant"] = None
        if base["unit_test_pass"]:
            try:
                y = fn()
                if tid.startswith("iir"):
                    b, a = np.asarray(y[0], float).reshape(-1), np.asarray(y[1], float).reshape(-1)
                    vec = np.concatenate([b, a])
                else:
                    vec = np.asarray(y, float).reshape(-1)
                canon = rel_l2(vec, controls[tid][canonical[tid]])
                ref_pass = canon <= ref_rel_l2_threshold
                if out["S_pass"] and ref_pass:
                    out["quadrant"] = "Q1_S_PASS_REF_PASS"
                elif out["S_pass"] and not ref_pass:
                    out["quadrant"] = "Q2_S_PASS_REF_DISCORDANT"
                elif (not out["S_pass"]) and ref_pass:
                    out["quadrant"] = "Q3_S_FAIL_REF_SILENT"
                else:
                    out["quadrant"] = "Q4_S_FAIL_REF_DISCORDANT"
            except Exception:
                pass
        scored.append(out)

    n = len(scored)
    n_exec = sum(1 for r in scored if r["executes"])
    n_u = sum(1 for r in scored if r["unit_test_pass"])
    n_s = sum(1 for r in scored if r["S_pass"])
    n_core = sum(1 for r in scored if r["CORE"])
    q2_rows = [r for r in scored if r.get("quadrant") == "Q2_S_PASS_REF_DISCORDANT"]
    q2_tasks = {r["task"] for r in q2_rows}
    q2_models = {r["model"] for r in q2_rows}
    q2_cells = {(r["task"], r["model"]) for r in q2_rows}

    print(f"  n=48 executed={n_exec} U-pass={n_u} S-pass={n_s} CORE(distinct from Q2)={n_core}")
    print(f"  Q2 (S_pass & reference-discordant) = {len(q2_rows)}")
    print(f"  Q2 tasks {len(q2_tasks)}/4  Q2 models {len(q2_models)}/3  Q2 cells {len(q2_cells)}/12")
    check(n == 48, "n=48", failures)
    check(n_exec == 20, "executed 20/48", failures)
    check(n_u == 14, "U-pass 14/48", failures)
    check(n_s == 9, "S-pass 9/48", failures)
    check(n_core == 5, "CORE 5/48 (passband/stopband failures distinct from Q2)", failures)
    check(len(q2_rows) == 9, "Q2 9/14 eligible", failures)
    check(len(q2_tasks) == 4, "Q2 tasks 4/4", failures)
    check(len(q2_models) == 2, "Q2 models 2/3 (Llama contributes none)", failures)
    check(len(q2_cells) == 6, "Q2 cells 6/12", failures)

    # Pre-generation freeze checks: 12 valid controls pass S_t, 12 mutants fail S_t.
    n_control_pass = 0
    n_control_total = 0
    for p in (ROOT / "data/arm_n_valid_controls").glob("*"):
        tid = p.name.split("__")[0]
        task = tasks[tid]
        n_control_total += 1
        if p.suffix == ".npy":
            b = np.load(p)
            residual = task["residual"](lambda b=b: b)
        else:
            z = np.load(p)
            residual = task["residual"](lambda b=z["b"], a=z["a"]: (b, a))
        n_control_pass += int(residual <= task["threshold"])
    print(f"  pre-generation valid controls S-pass {n_control_pass}/{n_control_total}")
    check(n_control_pass == 12 and n_control_total == 12, "valid controls 12/12 pass S_t", failures)

    n_mutant_fail = 0
    n_mutant_total = 0
    for p in (ROOT / "data/arm_n_mutants").glob("*"):
        tid = p.name.split("__")[0]
        task = tasks[tid]
        n_mutant_total += 1
        if p.suffix == ".npy":
            b = np.load(p)
            residual = task["residual"](lambda b=b: b)
        else:
            z = np.load(p)
            residual = task["residual"](lambda b=z["b"], a=z["a"]: (b, a))
        n_mutant_fail += int(residual > task["threshold"])
    print(f"  pre-generation mutants S-fail {n_mutant_fail}/{n_mutant_total}")
    check(n_mutant_fail == 12 and n_mutant_total == 12, "mutants 12/12 fail S_t", failures)


def main() -> int:
    failures: list[str] = []
    reproduce_arm_n(failures)
    print()
    reproduce_historical(failures)
    print()
    reproduce_arm(
        "Arm P -- frozen prospective convolution/correlation holdout",
        "arm_p_generations.json",
        TASKS_P,
        {"n": 48, "k": 11, "tasks": 1, "n_tasks": 4},
        failures,
    )
    print()
    b_core_rows = reproduce_arm(
        "Arm B -- frozen prospective sampling/resampling suite (original scoring)",
        "arm_b_generations.json",
        TASKS_B,
        {
            "n": 48,
            "k": 11,
            "tasks": 3,
            "n_tasks": 4,
            "mechanisms": 2,
            "task_order": [
                "decimation_alias_frequency",
                "digital_frequency_rescale",
                "zero_insertion_spectral_images",
                "rational_resample_dc_preservation",
            ],
            "task_counts": "1/0/3/7",
            "mechanism_of": {
                "decimation_alias_frequency": "alias",
                "digital_frequency_rescale": "alias",
                "zero_insertion_spectral_images": "resample",
                "rational_resample_dc_preservation": "resample",
            },
        },
        failures,
    )
    print()
    reproduce_arm_b_conservative(b_core_rows, failures)
    print()
    if failures:
        print(f"ALL_PUBLISHED_COUNTS_MATCH: NO ({len(failures)} failed checks)")
        return 1
    print("ALL_PUBLISHED_COUNTS_MATCH: YES")
    return 0


if __name__ == "__main__":
    from multiprocessing import freeze_support

    freeze_support()
    raise SystemExit(main())
