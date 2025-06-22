import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

import db


def test_add_update_delete_aluno(tmp_path):
    db.DB_NAME = str(tmp_path / "test.db")
    db.init_db()
    aluno_id = db.adicionar_aluno("Maria", "maria@test.com")
    aluno = db.obter_aluno(aluno_id)
    assert aluno[1] == "Maria"
    assert aluno[2] == "maria@test.com"
    db.atualizar_aluno(aluno_id, "nome", "Ana")
    aluno = db.obter_aluno(aluno_id)
    assert aluno[1] == "Ana"
    db.remover_aluno(aluno_id)
    assert db.obter_aluno(aluno_id) is None
    todos = db.listar_alunos()
    assert len(todos) == 0


def test_planos_crud(tmp_path):
    db.DB_NAME = str(tmp_path / "test.db")
    db.init_db()
    aluno_id = db.adicionar_aluno("Jose", "jose@test.com")
    plano_id = db.adicionar_plano(aluno_id, "Treino A", "descricao", "[]")
    planos = db.listar_planos(aluno_id)
    assert planos[0][0] == plano_id
    db.atualizar_plano(plano_id, "Treino B", "desc", "[]")
    planos = db.listar_planos(aluno_id)
    assert planos[0][1] == "Treino B"
    db.remover_plano(plano_id)
    planos = db.listar_planos(aluno_id)
    assert planos == []
