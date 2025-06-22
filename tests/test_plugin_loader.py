import importlib
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

import ia_sarah.core.plugin_loader as loader
from ia_sarah.core.plugin_loader import load_entrypoints, list_plugins


class Dummy:
    pass


def test_load_entrypoints(monkeypatch):
    eps = [
        type("ep", (), {"name": "dummy", "load": lambda self: Dummy})(),
    ]
    monkeypatch.setattr(importlib.metadata, "entry_points", lambda group=None: eps)  # type: ignore[attr-defined]
    registry = {}
    load_entrypoints("dummy", lambda n, o: registry.update({n: o}))
    assert registry["dummy"] is Dummy


def test_disable_plugin(monkeypatch):
    eps = [type("ep", (), {"name": "dummy", "load": lambda self: Dummy})()]
    monkeypatch.setattr(importlib.metadata, "entry_points", lambda group=None: eps)  # type: ignore[attr-defined]
    monkeypatch.setenv("DISABLED_PLUGINS", "dummy")
    loader._CACHE = {}
    registry = {}
    load_entrypoints("dummy", lambda n, o: registry.update({n: o}))
    assert registry == {}
    assert list_plugins("dummy") == []
