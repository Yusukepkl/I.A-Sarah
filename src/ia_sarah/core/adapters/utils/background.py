"""Helpers for running functions in background threads."""

from __future__ import annotations

import threading
import tkinter as tk
from typing import Any, Callable, Optional


def run_task(
    widget: tk.Widget,
    func: Callable[[], Any],
    on_success: Optional[Callable[[Any], None]] = None,
    on_error: Optional[Callable[[Exception], None]] = None,
) -> None:
    """Execute ``func`` in a background thread and invoke callbacks on the main thread."""

    def wrapper() -> None:
        try:
            result = func()
        except Exception as exc:  # noqa: BLE001
            if on_error:
                widget.after(0, on_error, exc)
        else:
            if on_success:
                widget.after(0, on_success, result)

    threading.Thread(target=wrapper, daemon=True).start()
