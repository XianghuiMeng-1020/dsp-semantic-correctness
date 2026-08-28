"""Phase-3C paths and locked interpretation bands. Frozen older artifacts are read-only."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = ROOT / "results" / "icassp_10of10_hardening" / "phase3c"
REPORT_DIR = ROOT / "reports" / "ICASSP_FINAL_10OF10"
PHASE1_DIR = ROOT / "results" / "icassp_10of10_hardening" / "phase1"
PHASE2A_DIR = ROOT / "results" / "icassp_10of10_hardening" / "phase2a"
PHASE2B_DIR = ROOT / "results" / "icassp_10of10_hardening" / "phase2b"
PHASE3A_DIR = ROOT / "results" / "icassp_10of10_hardening" / "phase3a"
PHASE3B_DIR = ROOT / "results" / "icassp_10of10_hardening" / "phase3b"
FROZEN_DIR = ROOT / "data" / "icassp_10of10"

G_ZERO_ABS = 1e-15
STARTING_HEAD = "7a0c670a5273f34aff1a3fb00842ddf1ea01aa85"
PROTOCOL_LOCK_COMMIT = "5de9d2c582893252e0370d145b958cb2803396a2"
PHASE3B_COMPLETE = "7a0c670a5273f34aff1a3fb00842ddf1ea01aa85"

# Locked before any holdout scoring (PHASE3C_PROTOCOL_LOCK.md).
TRANSFER_ROBUST = 0.95
TRANSFER_PARTIAL = 0.75
MAINT_LOW = 0.10
MAINT_MOD = 0.30
