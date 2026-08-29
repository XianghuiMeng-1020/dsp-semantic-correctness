"""Deterministic seeds. No candidate generation. No catalog I/O."""
from __future__ import annotations

import hashlib

from experiments.icassp_10of10_hardening.phase3d_a.config import (
    ATTEMPTS_PER_FAMILY,
    FIR_FAMILIES,
    IIR_FAMILIES,
    OUT_DIR,
    SEED_PREFIX,
)
from src.verification.registry_io import is_fir, suite_n_tasks
from src.verification.io_utils import dump_json


def seed_record(task_id: str, generator_id: str, attempt_index: int) -> dict:
    material = f"{SEED_PREFIX}|{task_id}|{generator_id}|{attempt_index}"
    digest = hashlib.sha256(material.encode("utf-8")).hexdigest()
    seed_u64 = int(digest[:16], 16)
    return {
        "task_id": task_id,
        "generator_id": generator_id,
        "attempt_index": int(attempt_index),
        "seed_material": material,
        "sha256": digest,
        "seed_u64": seed_u64,
    }


def build_manifest() -> dict:
    rows = []
    for task in suite_n_tasks():
        tid = task["task_id"]
        fams = FIR_FAMILIES if is_fir(task) else IIR_FAMILIES
        for gid in fams:
            for a in range(ATTEMPTS_PER_FAMILY):
                rows.append(seed_record(tid, gid, a))
    return {
        "seed_prefix": SEED_PREFIX,
        "hash_algorithm": "sha256",
        "material_template": "PHASE3D_A|{task_id}|{generator_id}|{attempt_index}",
        "n_attempts": len(rows),
        "attempts": rows,
        "note": "Seeds frozen before candidate generation. No seed replacement.",
    }


def write_manifest() -> dict:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    man = build_manifest()
    dump_json(OUT_DIR / "seed_manifest.json", man)
    return man


if __name__ == "__main__":
    m = write_manifest()
    print(f"wrote {m['n_attempts']} seeds")
