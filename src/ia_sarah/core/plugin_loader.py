"""Simple plugin loader using package entry points."""

from __future__ import annotations

import importlib.metadata
import logging
import os
from typing import Callable, Dict, Type

logger = logging.getLogger(__name__)

_CACHE: Dict[str, Dict[str, Type]] = {}


def list_plugins(group: str) -> list[str]:
    """Return the names of available plugins for ``group``."""
    load_entrypoints(group, lambda *_: None)
    return list(_CACHE.get(group, {}).keys())


def load_entrypoints(group: str, callback: Callable[[str, Type], None]) -> None:
    """Load plugins from ``group`` and pass each to ``callback``.

    Uses an in-memory cache to avoid reloading on subsequent calls.
    """
    if group not in _CACHE:
        registry: Dict[str, Type] = {}
        disabled = set(os.getenv("DISABLED_PLUGINS", "").split(","))
        for ep in importlib.metadata.entry_points(group=group):  # type: ignore[arg-type]
            if ep.name in disabled:
                logger.info("Plugin %s desabilitado", ep.name)
                continue
            try:
                obj = ep.load()
                registry[ep.name] = obj
            except Exception as exc:  # noqa: BLE001
                logger.error("Failed to load plugin %s: %s", ep.name, exc)
        _CACHE[group] = registry
    for name, obj in _CACHE[group].items():
        callback(name, obj)
