"""SQLite data access layer."""

from __future__ import annotations

import logging
import sqlite3
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

DB_DIR: Path = Path(__file__).resolve().parents[5] / "data"
DB_DIR.mkdir(parents=True, exist_ok=True)
DB_NAME: str = str(DB_DIR / "db.sqlite")

MIGRATIONS: list[str] = [
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
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS planos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER NOT NULL,
        nome TEXT NOT NULL,
        descricao TEXT,
        exercicios TEXT,
        FOREIGN KEY(aluno_id) REFERENCES alunos(id) ON DELETE CASCADE
    );
    """,
]

# Allowed columns that can be updated via ``atualizar_aluno``.
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
    """Create or upgrade database schema."""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            cur = conn.execute("PRAGMA user_version")
            (version,) = cur.fetchone()
            for idx, script in enumerate(MIGRATIONS, start=1):
                if idx > version:
                    conn.executescript(script)
                    conn.execute(f"PRAGMA user_version = {idx}")
    except sqlite3.Error as exc:  # pragma: no cover - database errors
        logger.error("Erro ao inicializar banco: %s", exc)
        raise


def listar_alunos() -> list[tuple]:
    """Return basic information for all students."""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cur = conn.execute(
                "SELECT id, nome, email, data_inicio FROM alunos ORDER BY nome"
            )
            return cur.fetchall()
    except sqlite3.Error as exc:  # pragma: no cover - database errors
        logger.error("Erro ao listar alunos: %s", exc)
        raise


def obter_aluno(aluno_id: int) -> Optional[tuple]:
    """Return full information for one student."""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cur = conn.execute(
                "SELECT id, nome, email, data_inicio, plano, pagamento, progresso, dieta, treino FROM alunos WHERE id=?",
                (aluno_id,),
            )
            return cur.fetchone()
    except sqlite3.Error as exc:  # pragma: no cover - database errors
        logger.error("Erro ao obter aluno: %s", exc)
        raise


def adicionar_aluno(nome: str, email: str) -> int:
    """Insert a new student and return generated id."""
    from datetime import datetime

    data_inicio = datetime.now().strftime("%Y-%m-%d")
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cur = conn.execute(
                "INSERT INTO alunos (nome, email, data_inicio) VALUES (?, ?, ?)",
                (nome, email, data_inicio),
            )
            return cur.lastrowid
    except sqlite3.Error as exc:  # pragma: no cover - database errors
        logger.error("Erro ao adicionar aluno: %s", exc)
        raise


def atualizar_aluno(aluno_id: int, campo: str, valor: str) -> None:
    """Update a single column of an existing student."""
    if campo not in VALID_UPDATE_FIELDS:
        raise ValueError(f"Invalid column name: {campo}")
    try:
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute(
                f"UPDATE alunos SET {campo}=? WHERE id=?",
                (valor, aluno_id),
            )
    except sqlite3.Error as exc:  # pragma: no cover - database errors
        logger.error("Erro ao atualizar aluno: %s", exc)
        raise


def remover_aluno(aluno_id: int) -> None:
    """Delete a student."""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute("DELETE FROM alunos WHERE id=?", (aluno_id,))
    except sqlite3.Error as exc:  # pragma: no cover - database errors
        logger.error("Erro ao remover aluno: %s", exc)
        raise


# ----- Planos de treino -----


def listar_planos(aluno_id: int) -> list[tuple]:
    """Return all training plans for a student."""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cur = conn.execute(
                "SELECT id, nome, descricao, exercicios FROM planos WHERE aluno_id=? ORDER BY id",
                (aluno_id,),
            )
            return cur.fetchall()
    except sqlite3.Error as exc:  # pragma: no cover - database errors
        logger.error("Erro ao listar planos: %s", exc)
        raise


def adicionar_plano(
    aluno_id: int, nome: str, descricao: str, exercicios_json: str
) -> int:
    """Add a new training plan."""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cur = conn.execute(
                "INSERT INTO planos (aluno_id, nome, descricao, exercicios) VALUES (?, ?, ?, ?)",
                (aluno_id, nome, descricao, exercicios_json),
            )
            return cur.lastrowid
    except sqlite3.Error as exc:  # pragma: no cover - database errors
        logger.error("Erro ao adicionar plano: %s", exc)
        raise


def atualizar_plano(
    plano_id: int, nome: str, descricao: str, exercicios_json: str
) -> None:
    """Update an existing training plan."""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute(
                "UPDATE planos SET nome=?, descricao=?, exercicios=? WHERE id=?",
                (nome, descricao, exercicios_json, plano_id),
            )
    except sqlite3.Error as exc:  # pragma: no cover - database errors
        logger.error("Erro ao atualizar plano: %s", exc)
        raise


def remover_plano(plano_id: int) -> None:
    """Delete a training plan."""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute("DELETE FROM planos WHERE id=?", (plano_id,))
    except sqlite3.Error as exc:  # pragma: no cover - database errors
        logger.error("Erro ao remover plano: %s", exc)
        raise


def contar_alunos() -> int:
    """Return the total number of students."""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cur = conn.execute("SELECT COUNT(*) FROM alunos")
            (total,) = cur.fetchone()
            return int(total)
    except sqlite3.Error as exc:  # pragma: no cover - database errors
        logger.error("Erro ao contar alunos: %s", exc)
        raise


def listar_planos_recentes(limit: int = 5) -> list[tuple]:
    """Return the most recently created plans with student names."""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cur = conn.execute(
                """
            SELECT planos.id, planos.nome, alunos.nome
            FROM planos
            JOIN alunos ON planos.aluno_id = alunos.id
            ORDER BY planos.id DESC
            LIMIT ?
            """,
                (limit,),
            )
            return cur.fetchall()
    except sqlite3.Error as exc:  # pragma: no cover - database errors
        logger.error("Erro ao listar planos recentes: %s", exc)
        raise
