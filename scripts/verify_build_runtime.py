#!/usr/bin/env python3
"""
Preflight checks for build/runtime dependencies required by packaged installers.

This script is intentionally strict: if a required module is missing or broken,
the build must fail rather than producing a broken installer.
"""

from __future__ import annotations

import importlib
import sys


REQUIRED_MODULES = (
    "PyInstaller",
    "markdown",
    "tkinter",
)


def _check_module(name: str) -> None:
    try:
        importlib.import_module(name)
    except Exception as exc:  # pragma: no cover - defensive preflight
        raise RuntimeError(f"Missing required module '{name}': {exc}") from exc


def _check_tk_runtime() -> None:
    try:
        import tkinter as tk
        tcl = tk.Tcl()
        patchlevel = tcl.eval("info patchlevel")
        print(f"Tk runtime detected (Tcl/Tk {patchlevel})")
    except Exception as exc:  # pragma: no cover - defensive preflight
        raise RuntimeError(
            f"tkinter is installed but unusable ({exc}). Install a Python build with working Tcl/Tk."
        ) from exc


def main() -> int:
    print("Running build preflight checks...")
    for module_name in REQUIRED_MODULES:
        _check_module(module_name)
        print(f"OK: {module_name}")

    _check_tk_runtime()
    print("All build preflight checks passed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(f"\nERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
