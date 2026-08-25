"""Execute a generated function under a restricted import surface."""

from __future__ import annotations

import builtins
import cmath
import io
import math
import statistics
from contextlib import redirect_stderr, redirect_stdout

import numpy as np
from scipy import signal as sp_signal


def exec_function(code: str, func_name: str):
    safe_names = {"open", "exec", "eval", "compile"}
    safe_builtins = {k: v for k, v in builtins.__dict__.items() if k not in safe_names}

    def _safe_import(name, globals=None, locals=None, fromlist=(), level=0):
        base = name.split(".")[0]
        if base not in {"numpy", "scipy", "math", "cmath", "statistics"}:
            raise ImportError(f"import of '{name}' is not allowed")
        return builtins.__import__(name, globals, locals, fromlist, level)

    safe_builtins["__import__"] = _safe_import
    ns = {
        "__builtins__": safe_builtins,
        "np": np,
        "numpy": np,
        "scipy": __import__("scipy"),
        "signal": sp_signal,
        "math": math,
        "cmath": cmath,
        "statistics": statistics,
    }
    try:
        with redirect_stderr(io.StringIO()), redirect_stdout(io.StringIO()):
            exec(compile(code, "<generated>", "exec"), ns)
    except Exception as exc:
        return None, f"EXEC_ERROR: {exc}"
    fn = ns.get(func_name)
    if fn is None or not callable(fn):
        return None, f"FUNCTION '{func_name}' NOT FOUND"
    return fn, None


def score_task(task: dict, fn) -> dict:
    unit_ok = False
    try:
        unit_ok = bool(task["unit_test"](fn))
    except Exception:
        unit_ok = False
    residual = None
    try:
        residual = float(task["residual"](fn, task["input_gen"]()))
    except Exception:
        residual = None
    semantic_fail = residual is not None and residual > float(task["threshold"])
    return {
        "executes": True,
        "unit_test_pass": unit_ok,
        "residual": residual,
        "semantic_fail": bool(semantic_fail),
        "core": bool(unit_ok and semantic_fail),
    }
