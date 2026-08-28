"""Save/load challenge implementations without timestamps."""
from __future__ import annotations

import io
import zipfile

import numpy as np

from experiments.icassp_10of10_hardening.phase3d_a.config import ROOT
from src.verification.io_utils import load_impl, sha256_file


def rel_path(task_id: str, tag: str, family: str) -> str:
    ext = ".npy" if family == "fir" else ".npz"
    return f"results/icassp_10of10_hardening/phase3d_a/impls/{task_id}/{tag}{ext}"


def _savez_deterministic(path, **arrays) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_STORED, allowZip64=False) as zf:
        for name in sorted(arrays):
            bio = io.BytesIO()
            np.lib.format.write_array(bio, np.asanyarray(arrays[name]), allow_pickle=False)
            info = zipfile.ZipInfo(filename=f"{name}.npy")
            info.date_time = (1980, 1, 1, 0, 0, 0)
            info.compress_type = zipfile.ZIP_STORED
            zf.writestr(info, bio.getvalue())


def save_impl(rel: str, family: str, impl) -> str:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    if family == "fir":
        np.save(path, np.asarray(impl, float).reshape(-1))
    else:
        _savez_deterministic(
            path,
            b=np.asarray(impl["b"], float).reshape(-1),
            a=np.asarray(impl["a"], float).reshape(-1),
        )
    return sha256_file(path)


def load_saved(rel: str):
    return load_impl(rel)
