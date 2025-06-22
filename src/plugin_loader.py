"""Simple plugin loader using package entry points."""

from __future__ import annotations

import importlib.metadata
import logging
from typing import Callable, Type

logger = logging.getLogger(__name__)


def load_entrypoints(group: str, callback: Callable[[str, Type], None]) -> None:
    """Load plugins from ``group`` and pass each to ``callback``."""
    for ep in importlib.metadata.entry_points(group=group):  # type: ignore[arg-type]
        try:
            obj = ep.load()
            callback(ep.name, obj)
        except Exception as exc:  # noqa: BLE001
            logger.error("Failed to load plugin %s: %s", ep.name, exc)
