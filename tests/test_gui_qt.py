import sys
from importlib import import_module
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))


def test_import_qt_interface():
    try:
        gui_qt = import_module("ia_sarah.core.interfaces.views.gui_qt")
    except Exception as exc:  # pragma: no cover - env issues
        pytest.skip(f"PySide6 not available: {exc}")
    assert hasattr(gui_qt, "criar_interface")


def test_stylesheet_string():
    try:
        theme = import_module("ia_sarah.core.interfaces.views.theme")
    except Exception as exc:  # pragma: no cover - env issues
        pytest.skip(f"PySide6 not available: {exc}")
    css = theme.stylesheet()
    assert isinstance(css, str) and "QPushButton" in css


def test_alunos_page(tmp_path):
    try:
        gui_qt = import_module("ia_sarah.core.interfaces.views.gui_qt")
    except Exception as exc:  # pragma: no cover - env issues
        pytest.skip(f"PySide6 not available: {exc}")
    # use temporary db
    import ia_sarah.core.adapters.repositories.db as db

    db.DB_NAME = str(tmp_path / "test_gui.db")
    db.init_db()

    page = gui_qt.AlunosPage()
    page.load_data()
    assert page.table.rowCount() == 0


def test_planos_page(tmp_path):
    try:
        gui_qt = import_module("ia_sarah.core.interfaces.views.gui_qt")
    except Exception as exc:  # pragma: no cover - env issues
        pytest.skip(f"PySide6 not available: {exc}")
    import ia_sarah.core.adapters.repositories.db as db

    db.DB_NAME = str(tmp_path / "test_gui.db")
    db.init_db()
    aluno_id = db.adicionar_aluno("Joao", "joao@test.com")
    page = gui_qt.PlanosPage(aluno_id)
    page.load_data()
    assert page.table.rowCount() == 0
