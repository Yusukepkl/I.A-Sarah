"""Camada de acesso a dados utilizando SQLite."""

import sqlite3
from contextlib import closing
from pathlib import Path
from typing import Iterable, Optional

DB_DIR = Path.home() / ".gestor_alunos"
DB_DIR.mkdir(parents=True, exist_ok=True)
DB_NAME = str(DB_DIR / "alunos.db")

# Allowed columns that can be updated via ``atualizar_aluno``. This helps avoid
# SQL injection by validating user provided column names before composing the
# query string.
VALID_UPDATE_FIELDS: set[str] = {
    "nome",
    "email",
    "data_inicio",
    "plano",
    "pagamento",
    "progresso",
    "dieta",
    "treino",
}

def init_db() -> None:
    """Cria as tabelas principais se ainda não existirem."""
    with closing(sqlite3.connect(DB_NAME)) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        with conn:
            conn.execute(
                """
            CREATE TABLE IF NOT EXISTS alunos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT,
                data_inicio TEXT,
                plano TEXT,
                pagamento TEXT,
                progresso TEXT,
                dieta TEXT,
                treino TEXT
            )
            """
            )
            # garante colunas extras ao atualizar versoes antigas do banco
            try:
                conn.execute("ALTER TABLE alunos ADD COLUMN email TEXT")
            except sqlite3.OperationalError:
                pass
            # tabela de planos de treino
            conn.execute(
                """
            CREATE TABLE IF NOT EXISTS planos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aluno_id INTEGER NOT NULL,
                nome TEXT NOT NULL,
                descricao TEXT,
                exercicios TEXT,
                FOREIGN KEY(aluno_id) REFERENCES alunos(id) ON DELETE CASCADE
            )
            """
            )
            try:
                conn.execute("ALTER TABLE alunos ADD COLUMN data_inicio TEXT")
            except sqlite3.OperationalError:
                pass

def listar_alunos() -> list[tuple]:
    """Retorna informações básicas de todos os alunos."""
    with closing(sqlite3.connect(DB_NAME)) as conn:
        cur = conn.execute(
            "SELECT id, nome, email, data_inicio FROM alunos ORDER BY nome"
        )
        return cur.fetchall()

def obter_aluno(aluno_id: int) -> Optional[tuple]:
    with closing(sqlite3.connect(DB_NAME)) as conn:
        cur = conn.execute(
            "SELECT id, nome, email, data_inicio, plano, pagamento, progresso, dieta, treino FROM alunos WHERE id=?",
            (aluno_id,)
        )
        return cur.fetchone()

def adicionar_aluno(nome: str, email: str) -> int:
    """Insere um novo aluno com a data atual e retorna o ID gerado."""
    from datetime import datetime

    data_inicio = datetime.now().strftime("%Y-%m-%d")
    with closing(sqlite3.connect(DB_NAME)) as conn:
        with conn:
            cur = conn.execute(
                "INSERT INTO alunos (nome, email, data_inicio) VALUES (?, ?, ?)",
                (nome, email, data_inicio),
            )
            return cur.lastrowid

def atualizar_aluno(aluno_id: int, campo: str, valor: str) -> None:
    """Update a single column of an existing aluno.

    Parameters
    ----------
    aluno_id : int
        Identifier of the aluno to update.
    campo : str
        Column name to update. Must be one of ``VALID_UPDATE_FIELDS``.
    valor : str
        New value for the column.
    """

    if campo not in VALID_UPDATE_FIELDS:
        raise ValueError(f"Invalid column name: {campo}")

    campo_validado = campo  # alias to emphasize validation happened

    with closing(sqlite3.connect(DB_NAME)) as conn:
        with conn:
            conn.execute(
                f"UPDATE alunos SET {campo_validado}=? WHERE id=?",
                (valor, aluno_id),
            )

def remover_aluno(aluno_id: int) -> None:
    with closing(sqlite3.connect(DB_NAME)) as conn:
        with conn:
            conn.execute("DELETE FROM alunos WHERE id=?", (aluno_id,))

# ----- Planos de treino -----

def listar_planos(aluno_id: int) -> list[tuple]:
    """Retorna todos os planos de treino de um aluno."""
    with closing(sqlite3.connect(DB_NAME)) as conn:
        cur = conn.execute(
            "SELECT id, nome, descricao, exercicios FROM planos WHERE aluno_id=? ORDER BY id",
            (aluno_id,),
        )
        return cur.fetchall()


def adicionar_plano(aluno_id: int, nome: str, descricao: str, exercicios_json: str) -> int:
    """Adiciona um novo plano de treino."""
    with closing(sqlite3.connect(DB_NAME)) as conn:
        with conn:
            cur = conn.execute(
                "INSERT INTO planos (aluno_id, nome, descricao, exercicios) VALUES (?, ?, ?, ?)",
                (aluno_id, nome, descricao, exercicios_json),
            )
            return cur.lastrowid


def atualizar_plano(plano_id: int, nome: str, descricao: str, exercicios_json: str) -> None:
    """Atualiza os dados de um plano de treino existente."""
    with closing(sqlite3.connect(DB_NAME)) as conn:
        with conn:
            conn.execute(
                "UPDATE planos SET nome=?, descricao=?, exercicios=? WHERE id=?",
                (nome, descricao, exercicios_json, plano_id),
            )


def remover_plano(plano_id: int) -> None:
    with closing(sqlite3.connect(DB_NAME)) as conn:
        with conn:
            conn.execute("DELETE FROM planos WHERE id=?", (plano_id,))

