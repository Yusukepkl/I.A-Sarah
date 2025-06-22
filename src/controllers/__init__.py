"""Application controllers bridging GUI and data layer."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Iterable

from repositories import db
from services import pdf_utils
from services.exporters import get_exporter
from utils.config_manager import load_theme as _load_theme
from utils.config_manager import save_theme as _save_theme

logger = logging.getLogger(__name__)


# ----- Config -----


def load_theme() -> str:
    """Load theme from configuration."""
    return _load_theme()


def save_theme(theme: str) -> None:
    """Persist theme selection."""
    _save_theme(theme)


# ----- Alunos -----


def init_app() -> None:
    """Initialize application database."""
    db.init_db()


def listar_alunos() -> list[tuple]:
    """Return list of students."""
    return db.listar_alunos()


def obter_aluno(aluno_id: int) -> tuple | None:
    """Retrieve single student."""
    return db.obter_aluno(aluno_id)


def adicionar_aluno(nome: str, email: str) -> int:
    """Create a new student."""
    return db.adicionar_aluno(nome, email)


def atualizar_aluno(aluno_id: int, campo: str, valor: str) -> None:
    """Update a student field."""
    db.atualizar_aluno(aluno_id, campo, valor)


def remover_aluno(aluno_id: int) -> None:
    """Remove a student."""
    db.remover_aluno(aluno_id)


# ----- Planos -----


def listar_planos(aluno_id: int) -> list[tuple]:
    """Return plans for a student."""
    return db.listar_planos(aluno_id)


def adicionar_plano(
    aluno_id: int, nome: str, descricao: str, exercicios_json: str
) -> int:
    """Create a new plan."""
    return db.adicionar_plano(aluno_id, nome, descricao, exercicios_json)


def atualizar_plano(
    plano_id: int, nome: str, descricao: str, exercicios_json: str
) -> None:
    """Update an existing plan."""
    db.atualizar_plano(plano_id, nome, descricao, exercicios_json)


def remover_plano(plano_id: int) -> None:
    """Delete a plan."""
    db.remover_plano(plano_id)


# ----- Exportação -----


def exportar_treino(
    fmt: str, titulo: str, exercicios: Iterable[dict], caminho: Path | str
) -> None:
    """Export a training plan using a registered exporter."""
    exporter = get_exporter(fmt)
    exporter.export(titulo, exercicios, Path(caminho))


# ----- PDF compatibilidade -----


def gerar_treino_pdf(
    titulo: str, exercicios: Iterable[dict], caminho: Path | str
) -> None:
    """Generate training plan PDF (legacy function)."""
    exportar_treino("pdf", titulo, exercicios, caminho)


def sanitize_filename(nome: str) -> str:
    """Expose filename sanitization."""
    return pdf_utils.sanitize_filename(nome)
