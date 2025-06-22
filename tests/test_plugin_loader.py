import importlib
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from plugin_loader import load_entrypoints


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
