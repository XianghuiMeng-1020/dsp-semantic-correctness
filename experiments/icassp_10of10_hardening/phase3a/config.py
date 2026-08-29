"""Phase-3A paths and numerical constants. Frozen Phase-0/1/2 artifacts are read-only."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = ROOT / "results" / "icassp_10of10_hardening" / "phase3a"
REPORT_DIR = ROOT / "reports" / "ICASSP_FINAL_10OF10"
PHASE1_DIR = ROOT / "results" / "icassp_10of10_hardening" / "phase1"
PHASE2A_DIR = ROOT / "results" / "icassp_10of10_hardening" / "phase2a"
PHASE2B_DIR = ROOT / "results" / "icassp_10of10_hardening" / "phase2b"

# Strict vs non-strict: manuscript exactness is G>0. Ambient uses the same sign convention.
GAMMA_POS_ABS = 1e-12
# Dual support / residual floors for classification (not for rewriting labels).
DUAL_SUPPORT_ABS = 1e-10
EQUALITY_RESIDUAL_ABS = 1e-8
# Affine-span numerical zero (lossless reduction: drop only null directions).
AFFINE_SV_REL = 1e-14
AFFINE_SV_ABS = 1e-14
# Independent-check tasks (manuscript occupants; two families).
INDEPENDENT_CHECK_TASKS = ("fir_lp_loose_8k", "iir_hp_tight_8k")
# Response precision re-evaluation grid (2x confirmatory FREQZ_N).
RESP_N_CONFIRMATORY = 131072
RESP_N_PRECISION = 262144

PROTOCOL_LOCK_COMMIT = "171703da17a81b4c8dfb73ed465912264bdd85e5"
STARTING_HEAD = "d7fd932cf34efbcc8e9ca99eac014ee15f92fbb9"
