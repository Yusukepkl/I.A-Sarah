import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from ia_sarah.core.use_cases import controllers


def test_listar_exportadores():
    formatos = controllers.listar_exportadores()
    assert "pdf" in formatos
    assert "csv" in formatos
    assert "xlsx" in formatos
