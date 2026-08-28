"""Phase-3D-A locked constants. Generation must not import Phase-3B/3A catalogs."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = ROOT / "results" / "icassp_10of10_hardening" / "phase3d_a"
REPORT_DIR = ROOT / "reports" / "ICASSP_FINAL_10OF10"
IMPL_DIR = OUT_DIR / "impls"
FROZEN_DIR = ROOT / "data" / "icassp_10of10"

STARTING_HEAD = "4f6d498ad26065962ebba80e8aa019dfbe8ec1c2"
SEED_PREFIX = "PHASE3D_A"

ATTEMPTS_PER_TASK = 48
ATTEMPTS_PER_FAMILY = 12

FIR_FAMILIES = ("F1_remez", "F2_firls", "F3_freqsamp", "F4_window")
IIR_FAMILIES = ("I1_butter", "I2_cheby1", "I3_cheby2", "I4_ellip")

# Odd tap counts inside the existing scientific FIR search range [21, 401].
# Upper end 101 avoids extreme orders chosen to stress reference transfer.
FIR_N_GRID = (21, 25, 31, 37, 43, 49, 55, 61, 71, 81, 91, 101)

# Remez band weights. 2-band (lp/hp) and 3-band (bp/bs).
REMEZ_W2 = (
    (1.0, 1.0),
    (1.0, 2.0),
    (2.0, 1.0),
    (1.0, 3.0),
    (3.0, 1.0),
    (1.0, 4.0),
    (4.0, 1.0),
    (1.0, 5.0),
    (5.0, 1.0),
    (2.0, 3.0),
    (3.0, 2.0),
    (1.0, 1.5),
)
REMEZ_W3 = (
    (1.0, 1.0, 1.0),
    (1.0, 2.0, 1.0),
    (2.0, 1.0, 2.0),
    (1.0, 3.0, 1.0),
    (3.0, 1.0, 3.0),
    (1.0, 4.0, 1.0),
    (2.0, 1.0, 1.0),
    (1.0, 1.0, 2.0),
    (1.0, 5.0, 1.0),
    (4.0, 1.0, 4.0),
    (1.5, 1.0, 1.5),
    (1.0, 2.0, 3.0),
)

# F3 designed-transition placement: fraction of the free-transition width
# used to inset the designed (not S_t) pass/stop interface from each edge.
F3_EDGE_ALPHA = (0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60)

# IIR orders inside existing scientific range [2, 12].
IIR_ORDER_GRID = (2, 3, 4, 5, 6, 7, 8, 9, 10, 4, 6, 8)
# Placement of designed cutoff inside the free transition (lp/hp only).
IIR_FC_FRAC = (0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75)
# Fractions of the textbook pass-ripple / stop-attenuation targets (inside/beyond mask slack).
IIR_RP_FRAC = (0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95, 0.40, 0.50, 0.60, 0.80)
IIR_RS_FRAC = (1.00, 1.05, 1.10, 1.15, 1.20, 1.25, 1.30, 1.40, 1.10, 1.20, 1.00, 1.50)

MUTATION_LADDER = (1e-5, 1e-4, 1e-3, 1e-2)

FORBIDDEN_OPEN = (
    "results/icassp_10of10_hardening/phase3b/reference_catalog_complexity.json",
    "results/icassp_10of10_hardening/phase3b/headline.json",
    "results/icassp_10of10_hardening/phase3a/coefficient_ambient.json",
    "results/icassp_10of10_hardening/phase3a/response_ambient.json",
    "results/icassp_10of10_hardening/phase3a/hierarchy.json",
    "results/icassp_10of10_hardening/phase1/best_observed_reference.json",
)

FALLBACK_FIR = ("F1_remez", "F2_firls", "F3_freqsamp", "F4_window")
FALLBACK_IIR = ("I1_butter", "I2_cheby1", "I3_cheby2", "I4_ellip")
