"""Frozen experiment configuration. Do not retune after seeing results."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SEED = 20260826
BOOTSTRAP_B = 10000
DISCORD_TAU_DESCRIPTIVE = 0.05  # operating point only, not the claim
GENUINE_EPS = 1e-8
NEAR_SCALE_RESID = 1e-10
K_GRID = (1, 3, 5)
LIBRARY_ORDER_FIR = ("firwin", "remez", "firls", "firwin2", "firls")
LIBRARY_ORDER_IIR = ("butter", "cheby1", "cheby2", "ellip")
OUT_DIR = ROOT / "data" / "icassp_10of10"
REPORT_DIR = ROOT / "reports" / "ICASSP_10OF10"
PROBE_CAND_DIR = OUT_DIR / "probe_candidates"
BOUNDARY_DIR = OUT_DIR / "boundary_invalids"
VERIFIER_VERSION = "independent_spec_verifier/1.0"
