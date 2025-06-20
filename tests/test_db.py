import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

import db


def test_add_and_get_aluno(tmp_path):
    db.DB_NAME = str(tmp_path / "test.db")
    db.init_db()
    aluno_id = db.adicionar_aluno("Maria", "maria@test.com")
    aluno = db.obter_aluno(aluno_id)
    assert aluno[1] == "Maria"
    assert aluno[2] == "maria@test.com"
    todos = db.listar_alunos()
    assert any(a[0] == aluno_id for a in todos)


def test_planos(tmp_path):
    db.DB_NAME = str(tmp_path / "test.db")
    db.init_db()
    aluno_id = db.adicionar_aluno("Jose", "jose@test.com")
    plano_id = db.adicionar_plano(aluno_id, "Treino A", "descricao", "[]")
    planos = db.listar_planos(aluno_id)
    assert len(planos) == 1
    assert planos[0][0] == plano_id
