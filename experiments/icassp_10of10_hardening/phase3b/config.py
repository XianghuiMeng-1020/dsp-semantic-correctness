"""Phase-3B paths and locked interpretation bands. Frozen older artifacts are read-only."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = ROOT / "results" / "icassp_10of10_hardening" / "phase3b"
REPORT_DIR = ROOT / "reports" / "ICASSP_FINAL_10OF10"
PHASE1_DIR = ROOT / "results" / "icassp_10of10_hardening" / "phase1"
PHASE3A_DIR = ROOT / "results" / "icassp_10of10_hardening" / "phase3a"
FROZEN_DIR = ROOT / "data" / "icassp_10of10"

G_ZERO_ABS = 1e-15
PROTOCOL_LOCK_COMMIT = "714a8ee78b71f42e1f6914303444b06b51917f1c"
STARTING_HEAD = "be675b8f2d319f999ca9b1f9515f09dc2f3aef6d"

# Locked before any K* inspection (PHASE3B_PROTOCOL_LOCK.md).
RHO_LOW = 0.10
RHO_MOD = 0.30
RHO_HIGH = 0.70

VALIDATION_TASKS_MIN = (
    "smallest",
    "largest",
    "fir_loose",
    "fir_tight",
    "iir_loose",
    "iir_tight",
    "kmin",
    "kmax",
)
