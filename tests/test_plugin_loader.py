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


def test_reload_entrypoints(monkeypatch):
    loader._CACHE = {}
    eps1 = [type("ep", (), {"name": "dummy1", "load": lambda self: Dummy})()]
    monkeypatch.setattr(importlib.metadata, "entry_points", lambda group=None: eps1)
    assert list_plugins("dummy") == ["dummy1"]

    eps2 = [type("ep", (), {"name": "dummy2", "load": lambda self: Dummy})()]
    monkeypatch.setattr(importlib.metadata, "entry_points", lambda group=None: eps2)
    loader.reload_entrypoints("dummy")
    assert list_plugins("dummy") == ["dummy2"]
