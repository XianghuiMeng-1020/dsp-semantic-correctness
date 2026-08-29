"""Phase-2B output locations. Frozen Phase-0/1/2A paths are read-only."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = ROOT / "results" / "icassp_10of10_hardening" / "phase2b"
REPORT_DIR = ROOT / "reports" / "ICASSP_FINAL_10OF10"
FROZEN_DIR = ROOT / "data" / "icassp_10of10"
PHASE1_DIR = ROOT / "results" / "icassp_10of10_hardening" / "phase1"
PHASE2A_DIR = ROOT / "results" / "icassp_10of10_hardening" / "phase2a"

PREVIOUSLY_UNDECIDED_FIR = [
    {
        "task_id": "fir_bs_tight_8k",
        "cid": "data/valid/first_principles/fir_bs_tight_8k__frequency_sampling__shortest.npy",
    },
    {
        "task_id": "fir_bs_tight_16k",
        "cid": "data/valid/first_principles/fir_bs_tight_16k__frequency_sampling__shortest.npy",
    },
]
