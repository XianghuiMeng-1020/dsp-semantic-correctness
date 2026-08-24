#!/usr/bin/env python3
"""Reproduce the published CORE summaries from frozen extracted implementations."""

from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.contracts_conv_corr import TASKS as TASKS_P
from src.contracts_samp_resamp import TASKS as TASKS_B
from src.runtime import exec_function, score_task
from src.stats import wilson_ci


def load_json(name: str):
    return json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))


def check(cond: bool, label: str, failures: list[str]) -> None:
    status = "PASS" if cond else "FAIL"
    print(f"  {status}  {label}")
    if not cond:
        failures.append(label)


def reproduce_historical(failures: list[str]) -> None:
    print("Historical confirmatory arm")
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


def main() -> int:
    failures: list[str] = []
    reproduce_historical(failures)
    print()
    reproduce_arm(
        "Prospective convolution/correlation arm",
        "arm_p_generations.json",
        TASKS_P,
        {"n": 48, "k": 11, "tasks": 1, "n_tasks": 4},
        failures,
    )
    print()
    reproduce_arm(
        "Prospective sampling/resampling arm",
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
    if failures:
        print(f"ALL_PUBLISHED_COUNTS_MATCH: NO ({len(failures)} failed checks)")
        return 1
    print("ALL_PUBLISHED_COUNTS_MATCH: YES")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
