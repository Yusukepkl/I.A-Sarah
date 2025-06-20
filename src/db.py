"""Simple SQLite database helpers used by the training manager GUI."""

import sqlite3
from contextlib import closing

DB_NAME = "alunos.db"


def init_db() -> None:
    """Create required tables if they do not yet exist."""
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
    """Return id, name, email and start date for all students."""
    with closing(sqlite3.connect(DB_NAME)) as conn:
        cur = conn.execute(
            "SELECT id, nome, email, data_inicio FROM alunos ORDER BY nome"
        )
        return cur.fetchall()

def obter_aluno(aluno_id: int) -> tuple | None:
    """Return complete information for a single student."""
    with closing(sqlite3.connect(DB_NAME)) as conn:
        cur = conn.execute(
            "SELECT id, nome, email, data_inicio, plano, pagamento, progresso, dieta, treino FROM alunos WHERE id=?",
            (aluno_id,)
        )
        return cur.fetchone()

def adicionar_aluno(nome: str, email: str) -> int:
    """Insert a new student and return its generated id."""
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
    """Update a single field of a student record."""
    with closing(sqlite3.connect(DB_NAME)) as conn:
        with conn:
            conn.execute(f"UPDATE alunos SET {campo}=? WHERE id=?", (valor, aluno_id))

def remover_aluno(aluno_id: int) -> None:
    """Delete a student by id."""
    with closing(sqlite3.connect(DB_NAME)) as conn:
        with conn:
            conn.execute("DELETE FROM alunos WHERE id=?", (aluno_id,))

# ----- Planos de treino -----

def listar_planos(aluno_id: int) -> list[tuple]:
    """Return all workout plans registered for a student."""
    with closing(sqlite3.connect(DB_NAME)) as conn:
        cur = conn.execute(
            "SELECT id, nome, descricao, exercicios FROM planos WHERE aluno_id=? ORDER BY id",
            (aluno_id,),
        )
        return cur.fetchall()


def adicionar_plano(
    aluno_id: int, nome: str, descricao: str, exercicios_json: str
) -> int:
    """Create a new workout plan and return its generated id."""
    with closing(sqlite3.connect(DB_NAME)) as conn:
        with conn:
            cur = conn.execute(
                "INSERT INTO planos (aluno_id, nome, descricao, exercicios) VALUES (?, ?, ?, ?)",
                (aluno_id, nome, descricao, exercicios_json),
            )
            return cur.lastrowid


def atualizar_plano(
    plano_id: int, nome: str, descricao: str, exercicios_json: str
) -> None:
    """Update the information for an existing plan."""
    with closing(sqlite3.connect(DB_NAME)) as conn:
        with conn:
            conn.execute(
                "UPDATE planos SET nome=?, descricao=?, exercicios=? WHERE id=?",
                (nome, descricao, exercicios_json, plano_id),
            )


def remover_plano(plano_id: int) -> None:
    """Remove a workout plan by id."""
    with closing(sqlite3.connect(DB_NAME)) as conn:
        with conn:
            conn.execute("DELETE FROM planos WHERE id=?", (plano_id,))
