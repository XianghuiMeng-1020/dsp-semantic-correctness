"""Fail if generation tries to open Phase-3B/3A catalog artifacts."""
from __future__ import annotations

import builtins
from contextlib import contextmanager
from pathlib import Path

from experiments.icassp_10of10_hardening.phase3d_a.config import FORBIDDEN_OPEN, ROOT

_FORBIDDEN = {str(Path(p).as_posix()).replace("\\", "/") for p in FORBIDDEN_OPEN}


def _norm(path) -> str:
    try:
        p = Path(path)
        if not p.is_absolute():
            p = (ROOT / p).resolve()
        else:
            p = p.resolve()
        rel = p.relative_to(ROOT.resolve()).as_posix()
        return rel.replace("\\", "/")
    except Exception:
        return str(path).replace("\\", "/")


def is_forbidden(path) -> bool:
    rel = _norm(path)
    if rel in _FORBIDDEN:
        return True
    return any(rel.endswith(f) or f in rel.replace("\\", "/") for f in _FORBIDDEN)


@contextmanager
def forbid_catalog_io():
    real_open = builtins.open

    def guarded(file, *args, **kwargs):
        if is_forbidden(file):
            raise RuntimeError(f"PHASE3D_A_BLINDING_VIOLATION: refused open {file}")
        return real_open(file, *args, **kwargs)

    builtins.open = guarded
    try:
        yield
    finally:
        builtins.open = real_open
