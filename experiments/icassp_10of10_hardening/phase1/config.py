"""Phase-1 output locations. Frozen baseline paths are read-only."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = ROOT / "results" / "icassp_10of10_hardening" / "phase1"
REPORT_DIR = ROOT / "reports" / "ICASSP_FINAL_10OF10"
FROZEN_DIR = ROOT / "data" / "icassp_10of10"
TIE_ABS = 1e-15
G_ZERO_ABS = 1e-15
# Four tasks for independent brute-force Check 3
CHECK3_TASKS = (
    "fir_lp_loose_8k",
    "fir_lp_tight_8k",
    "iir_lp_loose_8k",
    "iir_hp_tight_8k",
)
