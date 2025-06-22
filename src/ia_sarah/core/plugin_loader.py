"""Simple plugin loader using package entry points."""

from __future__ import annotations

import importlib.metadata
import logging
from typing import Callable, Type, Dict

logger = logging.getLogger(__name__)

_CACHE: Dict[str, Dict[str, Type]] = {}


def load_entrypoints(group: str, callback: Callable[[str, Type], None]) -> None:
    """Load plugins from ``group`` and pass each to ``callback``.

    Uses an in-memory cache to avoid reloading on subsequent calls.
    """
    if group not in _CACHE:
        registry: Dict[str, Type] = {}
        for ep in importlib.metadata.entry_points(group=group):  # type: ignore[arg-type]
            try:
                obj = ep.load()
                registry[ep.name] = obj
            except Exception as exc:  # noqa: BLE001
                logger.error("Failed to load plugin %s: %s", ep.name, exc)
        _CACHE[group] = registry
    for name, obj in _CACHE[group].items():
        callback(name, obj)
