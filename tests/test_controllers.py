import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from ia_sarah.core.use_cases import controllers


def test_listar_exportadores():
    formatos = controllers.listar_exportadores()
    assert "pdf" in formatos
    assert "csv" in formatos
    assert "xlsx" in formatos


def test_adicionar_completo_e_backup(tmp_path):
    controllers.db.DB_NAME = str(tmp_path / "test.db")
    controllers.init_app()
    aluno_id = controllers.adicionar_aluno_completo(
        "Eva",
        "eva@test.com",
        plano="Especial",
    )
    from ia_sarah.core.adapters.repositories import db

    dados = db.obter_aluno(aluno_id)
    assert dados and dados[4] == "Especial"

    backup = tmp_path / "copy.sqlite"
    controllers.backup_dados(backup)
    assert backup.exists() and backup.stat().st_size > 0


def test_adicionar_com_plano_pdf(tmp_path):
    controllers.db.DB_NAME = str(tmp_path / "test.db")
    controllers.init_app()
    pdf_file = tmp_path / "treino.pdf"
    aluno_id, plano_id = controllers.adicionar_aluno_com_plano_pdf(
        "Leo",
        "leo@test.com",
        plano="Treino B",
        descricao="desc",
        exercicios_json="[]",
        pdf_dest=pdf_file,
    )
    assert pdf_file.exists() and pdf_file.stat().st_size > 0
    assert aluno_id > 0 and plano_id > 0
