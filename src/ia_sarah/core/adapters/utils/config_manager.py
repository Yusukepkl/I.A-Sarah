"""Utilities for persisting simple application configuration."""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict

logger = logging.getLogger(__name__)

CONFIG_FILE: Path = Path(
    os.getenv(
        "CONFIG_FILE",
        str(Path(__file__).resolve().parents[2] / "config.json"),
    )
)


def load_config() -> Dict[str, Any]:
    """Load configuration from disk.

    Returns
    -------
    dict
        Configuration values or an empty dictionary when the file is missing
        or invalid.
    """

    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:  # pragma: no cover - I/O
            logger.error("Erro ao ler configuração: %s", exc)
    return {}


def save_config(config: Dict[str, Any]) -> None:
    """Persist configuration to disk."""

    try:
        CONFIG_FILE.write_text(json.dumps(config, ensure_ascii=False), encoding="utf-8")
    except OSError as exc:  # pragma: no cover - I/O
        logger.error("Erro ao salvar configuração: %s", exc)
        raise


def delete_config() -> None:
    """Remove configuration file if it exists."""

    try:
        if CONFIG_FILE.exists():
            CONFIG_FILE.unlink()
    except OSError as exc:  # pragma: no cover - I/O
        logger.error("Erro ao excluir configuração: %s", exc)
        raise


def load_theme() -> str:
    """Return the saved theme name or a default."""

    config = load_config()
    return config.get("theme", "superhero")


def update_config(updates: Dict[str, Any]) -> None:
    """Merge and persist configuration updates."""

    config = load_config()
    config.update(updates)
    save_config(config)


def save_theme(theme: str) -> None:
    """Persist the selected theme."""

    update_config({"theme": theme})
