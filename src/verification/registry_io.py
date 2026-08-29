"""Load task registries without importing the construction checker."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
_CACHE = None

LEGACY_TO_SUITE_N = {
    "fir_lowpass_spec": "fir_lp_loose_8k",
    "fir_bandpass_spec": "fir_bp_loose_8k",
    "fir_bandstop_spec": "fir_bs_loose_8k",
    "iir_lowpass_stable_spec": "iir_lp_loose_8k",
}


def load_tasks() -> dict:
    global _CACHE
    if _CACHE is not None:
        return _CACHE
    tasks = {}
    for name in ("suite_s.json", "suite_n.json"):
        payload = json.loads((ROOT / "registry" / name).read_text(encoding="utf-8"))
        for t in payload["tasks"]:
            tasks[t["task_id"]] = t
            legacy = t.get("legacy_arm_n_id")
            if legacy:
                tasks[legacy] = t
    _CACHE = tasks
    return tasks


def get_task(task_id: str) -> dict:
    tasks = load_tasks()
    if task_id in tasks:
        return tasks[task_id]
    mapped = LEGACY_TO_SUITE_N.get(task_id)
    if mapped and mapped in tasks:
        return tasks[mapped]
    raise KeyError(f"unknown task_id: {task_id}")


def suite_n_tasks() -> list[dict]:
    payload = json.loads((ROOT / "registry" / "suite_n.json").read_text(encoding="utf-8"))
    return list(payload["tasks"])


def suite_s_tasks() -> list[dict]:
    payload = json.loads((ROOT / "registry" / "suite_s.json").read_text(encoding="utf-8"))
    return list(payload["tasks"])


def is_fir(task: dict) -> bool:
    return str(task["type"]).startswith("fir_")


def is_filter_task(task: dict) -> bool:
    return task.get("family") == "filter_specification"
