"""Phase-3D-B locked paths, hashes, and descriptive bands."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = ROOT / "results" / "icassp_10of10_hardening" / "phase3d_b"
REPORT_DIR = ROOT / "reports" / "ICASSP_FINAL_10OF10"
PHASE1_DIR = ROOT / "results" / "icassp_10of10_hardening" / "phase1"
PHASE3A_DIR = ROOT / "results" / "icassp_10of10_hardening" / "phase3a"
PHASE3B_DIR = ROOT / "results" / "icassp_10of10_hardening" / "phase3b"
PHASE3C_DIR = ROOT / "results" / "icassp_10of10_hardening" / "phase3c"
PHASE3DA_DIR = ROOT / "results" / "icassp_10of10_hardening" / "phase3d_a"
FROZEN_DIR = ROOT / "data" / "icassp_10of10"

G_ZERO_ABS = 1e-15
STARTING_HEAD = "8ae58fd14aca92b236a920a1678f5de396e2a5f5"
CHALLENGE_FROZEN = "8ccb7f18f1b9f48ce8c4f40ff6df202bdec6862e"
CHALLENGE_FROZEN_TAG = "icassp-10of10-phase3d-a-challenge-frozen"
PREUNBLIND_TAG = "icassp-10of10-phase3d-b-preunblind-lock"

TRANSFER_ROBUST = 0.95
TRANSFER_PARTIAL = 0.75
MAINT_LOW = 0.10
MAINT_MOD = 0.30

FIR_FAMILIES = ("F1_remez", "F2_firls", "F3_freqsamp", "F4_window")
IIR_FAMILIES = ("I1_butter", "I2_cheby1", "I3_cheby2", "I4_ellip")

LOCKED = {
    "manuscript/w4/paper.tex": "4750d3937e9dca9881eaf17ae71d8f92f51096407ad790b1041afcb46c8a4ed7",
    "manuscript/w4/paper.pdf": "69890c7a3f909bf6ea442155c0f37393da2d50f43de15e2685bd1ae345f1bc9c",
    "registry/suite_n.json": "d3fa49ff14f808b733a284b4281e3f574399b5a41282179d3ecbb66b8d3750c3",
    "registry/suite_s.json": "70bb415ad89cd8276a304385d93d85d71bf537d567955a703fe34e43864c7e2a",
    "data/icassp_10of10/recertify.json": "8813dd637962f6e28d6511295cfb105f10bc517ecc937b56db3edf2f39c2539a",
    "data/icassp_10of10/feasible_probe.json": "bad0223edec5b62ef72e05dd17c2a8eb135f1f0831d10b0dfdf4da314e0a6b10",
    "data/icassp_10of10/multi_reference.json": "44a5d333b85c82c36fdc980b541bad1a268ce8df9ca734da3f0ddd2df79e1a67",
    "results/icassp_10of10_hardening/phase1/headline.json": "9436f80e2c7c0933396f6f7052794ca314f37bfbc7407b08240d8527c1d02fed",
    "results/icassp_10of10_hardening/phase1/best_observed_reference.json": "bf4875dabab15906a8998dd5455f2b10dc68b1ef499213e6fd422e87cfc7bb49",
    "results/icassp_10of10_hardening/phase2a/headline.json": "85351e9f0110f0f73548106f1cda218578eac5d6ee884e84071ea3a2389a312b",
    "results/icassp_10of10_hardening/phase2b/headline.json": "e9bca10784521afdcb598229f10c79137776ef595610f666f358461cc4e3a927",
    "results/icassp_10of10_hardening/phase3a/headline.json": "a42a897568f8e497085398fcaf5845d4dfec2014b7cfd6cbc7eb94a1d343522f",
    "results/icassp_10of10_hardening/phase3b/headline.json": "fdbf6eb1a4bec0a76123533ba909c76f781d5ba59788ee60724d1b4ad85286b0",
    "results/icassp_10of10_hardening/phase3b/reference_catalog_complexity.json": "92c1c94c4c4de6a4ff660da3c3abd87f6022ae67f11534ad24459cfa7f11d061",
    "results/icassp_10of10_hardening/phase3c/leakage.json": "d02fb07b073ed6f1fd6648fb0f57d130e6b29ebee286cca02fc5488f0c2f962f",
    "results/icassp_10of10_hardening/phase3d_a/H_VALID.json": "8e02b28762ed28bccf0c6e8dec8c7ad28c021eb7ee791d13cbf2ec3f9de5dac1",
    "results/icassp_10of10_hardening/phase3d_a/H_INVALID.json": "61b37f89cca8941f1d9d3c30ecf08d6308e2e721adf7a200f5e158daa55d48fa",
    "results/icassp_10of10_hardening/phase3d_a/CHALLENGE_MANIFEST.sha256": "e104433f4b0721682034c8f4f08c04e5356feae8ee4bfe14518a0602d24f0498",
}

CHALLENGE_FILES = (
    "results/icassp_10of10_hardening/phase3d_a/H_VALID.json",
    "results/icassp_10of10_hardening/phase3d_a/H_INVALID.json",
    "results/icassp_10of10_hardening/phase3d_a/all_attempts.json",
    "results/icassp_10of10_hardening/phase3d_a/seed_manifest.json",
    "results/icassp_10of10_hardening/phase3d_a/CHALLENGE_MANIFEST.sha256",
)
