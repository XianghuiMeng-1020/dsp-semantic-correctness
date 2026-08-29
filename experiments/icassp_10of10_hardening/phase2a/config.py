"""Phase-2A output locations. Frozen baseline and Phase-1 paths are read-only."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = ROOT / "results" / "icassp_10of10_hardening" / "phase2a"
REPORT_DIR = ROOT / "reports" / "ICASSP_FINAL_10OF10"
FROZEN_DIR = ROOT / "data" / "icassp_10of10"
PHASE1_DIR = ROOT / "results" / "icassp_10of10_hardening" / "phase1"
