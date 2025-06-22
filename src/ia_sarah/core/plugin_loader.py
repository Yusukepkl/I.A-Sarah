"""Simple plugin loader using package entry points."""

from __future__ import annotations

import importlib
import importlib.metadata
import logging
import os
import sys
from pathlib import Path
from typing import Callable, Dict, Type

logger = logging.getLogger(__name__)

_CACHE: Dict[str, Dict[str, Type]] = {}


def _import_local_plugins() -> None:
    """Import modules inside ``ia_sarah.plugins`` package."""

    plugins_dir = Path(__file__).resolve().parents[1] / "plugins"
    for file in plugins_dir.glob("*.py"):
        if file.stem == "__init__":
            continue
        module_name = f"ia_sarah.plugins.{file.stem}"
        if module_name in sys.modules:
            continue
        try:
            importlib.import_module(module_name)
        except Exception as exc:  # noqa: BLE001
            logger.error(
                "Erro ao importar plugin local %s: %s", module_name, exc
            )


def list_plugins(group: str) -> list[str]:
    """Return the names of available plugins for ``group``."""
    load_entrypoints(group, lambda *_: None)
    return list(_CACHE.get(group, {}).keys())


def load_entrypoints(
    group: str, callback: Callable[[str, Type], None]
) -> None:
    """Load plugins from ``group`` and pass each to ``callback``.

    Uses an in-memory cache to avoid reloading on subsequent calls.
    """
    _import_local_plugins()
    if group not in _CACHE:
        registry: Dict[str, Type] = {}
        disabled = set(os.getenv("DISABLED_PLUGINS", "").split(","))
        entry_points = importlib.metadata.entry_points(group=group)
        for ep in entry_points:  # type: ignore[attr-defined]
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
        try:
            callback(name, obj)
        except Exception as exc:  # noqa: BLE001
            logger.error("Erro ao registrar plugin %s: %s", name, exc)


def reload_entrypoints(group: str) -> None:
    """Reload plugins for ``group`` ignoring any cached values."""

    _CACHE.pop(group, None)
    load_entrypoints(group, lambda *_: None)
