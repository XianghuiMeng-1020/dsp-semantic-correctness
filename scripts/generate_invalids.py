#!/usr/bin/env python3
"""Phase 2C Stage 4: Suite N invalid-by-construction mutants."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.mutants import applicable, generate_mutant  # noqa: E402
from src.spec_checker import check_specification  # noqa: E402

OUT = ROOT / "data" / "invalid"
MECHANISMS = ("M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8")


def _jsonable(x):
    if isinstance(x, dict):
        return {k: _jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_jsonable(v) for v in x]
    if isinstance(x, np.ndarray):
        return [float(v) for v in np.asarray(x, float).reshape(-1)]
    if isinstance(x, (np.floating, float)):
        v = float(x)
        return None if not math.isfinite(v) else v
    if isinstance(x, (np.integer, int)):
        return int(x)
    if isinstance(x, (np.bool_, bool)):
        return bool(x)
    return x


def _save(path: Path, impl):
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(impl, dict) and "b" in impl:
        np.savez(path.with_suffix(".npz"), b=np.asarray(impl["b"], float), a=np.asarray(impl["a"], float))
        return path.with_suffix(".npz")
    np.save(path.with_suffix(".npy"), np.asarray(impl, float))
    return path.with_suffix(".npy")


def main() -> int:
    tasks = json.loads((ROOT / "registry" / "suite_n.json").read_text(encoding="utf-8"))["tasks"]
    rows = []
    skipped = []
    not_applicable = []
    leaked = []
    for task in tasks:
        tid = task["task_id"]
        dest = OUT / tid
        dest.mkdir(parents=True, exist_ok=True)
        for mid in MECHANISMS:
            if not applicable(task, mid):
                not_applicable.append({"task_id": tid, "mechanism": mid})
                continue
            rec = generate_mutant(task, mid)
            if rec is None:
                skipped.append({"task_id": tid, "mechanism": mid, "reason": "S_t_still_1_or_design_failed"})
                print(f"  SKIP {tid} {mid}", flush=True)
                continue
            chk = check_specification(tid, rec["impl"])
            if chk["pass"]:
                leaked.append({"task_id": tid, "mechanism": mid})
                print(f"  LEAK {tid} {mid}", flush=True)
                continue
            path = _save(dest / f"{tid}__{mid}", rec["impl"])
            row = {
                "task_id": tid,
                "mechanism": mid,
                "source_parameters": _jsonable(rec["source_parameters"]),
                "S_t": False,
                "residuals": chk["residuals"],
                "label": "invalid-by-construction",
                "path": str(path.relative_to(ROOT)).replace("\\", "/"),
            }
            path.with_suffix(".json").write_text(json.dumps(row, indent=2), encoding="utf-8")
            rows.append(row)
            print(f"  OK {tid} {mid}", flush=True)
    payload = {
        "n_invalid": len(rows),
        "by_mechanism": {m: sum(1 for r in rows if r["mechanism"] == m) for m in MECHANISMS},
        "skipped": skipped,
        "not_applicable": not_applicable,
        "leaked_S_t_1": leaked,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "manifest.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    (OUT / "generation_log.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print("n_invalid", len(rows), "skipped", len(skipped), "n/a", len(not_applicable), "leaked", len(leaked))
    return 1 if leaked else 0


if __name__ == "__main__":
    raise SystemExit(main())
