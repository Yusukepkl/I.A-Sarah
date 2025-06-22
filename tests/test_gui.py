import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

import tkinter as tk
from unittest import mock
import pytest
from pyvirtualdisplay import Display
import shutil

import gui


@pytest.fixture(scope="module", autouse=True)
def _display():
    if shutil.which("Xvfb") is None:
        pytest.skip("Xvfb not available")
    disp = Display(visible=0, size=(800, 600))
    disp.start()
    yield
    disp.stop()


def _setup_frame(monkeypatch):
    """Create DetalhesFrame with patched dependencies."""
    monkeypatch.setattr(gui.controllers, "listar_planos", lambda _id: [])
    root = tk.Tk()
    root.withdraw()
    frame = gui.DetalhesFrame(
        root, (1, "Nome", "email", "2023-01-01"), lambda: None, lambda: None
    )
    return frame, root


def test_excluir_aluno_chama_remover(monkeypatch):
    frame, root = _setup_frame(monkeypatch)
    remover_mock = mock.MagicMock()
    monkeypatch.setattr(gui.controllers, "remover_aluno", remover_mock)
    monkeypatch.setattr(gui.messagebox, "askyesno", lambda *a, **k: True)
    monkeypatch.setattr(gui.messagebox, "showinfo", lambda *a, **k: None)

    def run_task(_widget, func, on_success=None, on_error=None):
        try:
            result = func()
        except Exception as exc:  # pragma: no cover - test helper
            if on_error:
                on_error(exc)
        else:
            if on_success:
                on_success(result)

    monkeypatch.setattr(gui, "run_task", run_task)
    frame.excluir_aluno()
    root.destroy()
    remover_mock.assert_called_once_with(1)


def test_excluir_plano_chama_remover(monkeypatch):
    frame, root = _setup_frame(monkeypatch)
    remover_mock = mock.MagicMock()
    monkeypatch.setattr(gui.controllers, "remover_plano", remover_mock)
    monkeypatch.setattr(gui.messagebox, "askyesno", lambda *a, **k: True)
    monkeypatch.setattr(gui.messagebox, "showinfo", lambda *a, **k: None)

    def run_task(_widget, func, on_success=None, on_error=None):
        try:
            result = func()
        except Exception as exc:  # pragma: no cover - test helper
            if on_error:
                on_error(exc)
        else:
            if on_success:
                on_success(result)

    monkeypatch.setattr(gui, "run_task", run_task)
    frame.excluir_plano(5)
    root.destroy()
    remover_mock.assert_called_once_with(5)
