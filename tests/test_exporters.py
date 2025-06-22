import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from ia_sarah.core.use_cases import controllers


EXERCISES = [{"nome": "Supino", "series": "3", "reps": "10"}]


def test_exportar_csv(tmp_path):
    out = tmp_path / "plan.csv"
    controllers.exportar_treino("csv", "Treino", EXERCISES, out)
    assert out.exists() and out.read_text().strip()


def test_exportar_xlsx(tmp_path):
    out = tmp_path / "plan.xlsx"
    controllers.exportar_treino("xlsx", "Treino", EXERCISES, out)
    assert out.exists() and out.stat().st_size > 0


def test_exportar_invalid(tmp_path):
    out = tmp_path / "plan.txt"
    try:
        controllers.exportar_treino("txt", "Treino", EXERCISES, out)
    except KeyError:
        pass
    else:
        assert False, "expected KeyError"
