"""Application controllers bridging GUI and data layer."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Iterable

from ia_sarah.core.adapters.repositories import db
from ia_sarah.core.entities.models import Student, TrainingPlan
from ia_sarah.core.adapters.services import pdf_utils
from ia_sarah.core.adapters.services.exporters import get_exporter, _REGISTRY
from ia_sarah.core.adapters.utils.config_manager import load_theme as _load_theme
from ia_sarah.core.adapters.utils.config_manager import save_theme as _save_theme
from ia_sarah.core.adapters.utils.config_manager import load_config as _load_config
from ia_sarah.core.adapters.utils.config_manager import update_config as _update_config

logger = logging.getLogger(__name__)


# ----- Config -----


def load_theme() -> str:
    """Return the saved UI theme.

    Returns
    -------
    str
        Theme name.
    """
    return _load_theme()


def save_theme(theme: str) -> None:
    """Persist selected theme.

    Parameters
    ----------
    theme:
        Theme name to persist.
    """
    _save_theme(theme)


def load_config() -> dict:
    """Load full configuration dictionary.

    Returns
    -------
    dict
        Key/value pairs stored on disk.
    """
    return _load_config()


def update_config(data: dict) -> None:
    """Merge configuration updates and persist them.

    Parameters
    ----------
    data:
        Mapping with new configuration values.
    """
    _update_config(data)


# ----- Alunos -----


def init_app() -> None:
    """Initialize application database."""
    db.init_db()


def listar_alunos() -> list[Student]:
    """List all registered students.

    Returns
    -------
    list[tuple]
        Tuples with basic student data.
    """
    records = db.listar_alunos()
    return [Student(id=r[0], nome=r[1], email=r[2], data_inicio=r[3]) for r in records]


def obter_aluno(aluno_id: int) -> Student | None:
    """Retrieve single student record.

    Parameters
    ----------
    aluno_id:
        Identifier of the student.

    Returns
    -------
    tuple | None
        Complete student information or ``None`` when not found.
    """
    r = db.obter_aluno(aluno_id)
    if r is None:
        return None
    return Student(id=r[0], nome=r[1], email=r[2], data_inicio=r[3])


def adicionar_aluno(nome: str, email: str) -> int:
    """Create a new student entry.

    Parameters
    ----------
    nome:
        Student name.
    email:
        Contact e-mail.

    Returns
    -------
    int
        Database id of the created record.
    """
    return db.adicionar_aluno(nome, email)


def adicionar_aluno_completo(
    nome: str,
    email: str,
    data_inicio: str | None = None,
    plano: str | None = None,
    pagamento: str | None = None,
    progresso: str | None = None,
    dieta: str | None = None,
    treino: str | None = None,
) -> int:
    """Create a student filling all optional fields."""

    return db.adicionar_aluno_completo(
        nome, email, data_inicio, plano, pagamento, progresso, dieta, treino
    )


def atualizar_aluno(aluno_id: int, campo: str, valor: str) -> None:
    """Update a single field of a student.

    Parameters
    ----------
    aluno_id:
        Student identifier.
    campo:
        Column name to update.
    valor:
        New value.
    """
    db.atualizar_aluno(aluno_id, campo, valor)


def remover_aluno(aluno_id: int) -> None:
    """Remove a student record.

    Parameters
    ----------
    aluno_id:
        Id of the record to delete.
    """
    db.remover_aluno(aluno_id)


# ----- Planos -----


def listar_planos(aluno_id: int) -> list[TrainingPlan]:
    """Return plans for a student.

    Parameters
    ----------
    aluno_id:
        Student id whose plans will be listed.

    Returns
    -------
    list[tuple]
        Plan records.
    """
    records = db.listar_planos(aluno_id)
    return [
        TrainingPlan(id=r[0], aluno_id=aluno_id, nome=r[1], descricao=r[2], exercicios_json=r[3])
        for r in records
    ]


def adicionar_plano(
    aluno_id: int, nome: str, descricao: str, exercicios_json: str
) -> int:
    """Create a new training plan.

    Parameters
    ----------
    aluno_id:
        Owner student id.
    nome:
        Plan name.
    descricao:
        Text description.
    exercicios_json:
        JSON array with exercises.

    Returns
    -------
    int
        Generated identifier for the plan.
    """
    return db.adicionar_plano(aluno_id, nome, descricao, exercicios_json)


def atualizar_plano(
    plano_id: int, nome: str, descricao: str, exercicios_json: str
) -> None:
    """Update an existing plan.

    Parameters
    ----------
    plano_id:
        Identifier of the plan.
    nome:
        Updated name.
    descricao:
        Updated description.
    exercicios_json:
        Updated exercise list in JSON.
    """
    db.atualizar_plano(plano_id, nome, descricao, exercicios_json)


def remover_plano(plano_id: int) -> None:
    """Delete a plan.

    Parameters
    ----------
    plano_id:
        Plan identifier to remove.
    """
    db.remover_plano(plano_id)


# ----- Dashboard stats -----


def contar_alunos() -> int:
    """Return total number of students.

    Returns
    -------
    int
        Quantity of registered students.
    """
    return db.contar_alunos()


def listar_planos_recentes(limit: int = 5) -> list[tuple]:
    """Return most recent plans with student names.

    Parameters
    ----------
    limit:
        Maximum number of plans to return.

    Returns
    -------
    list[tuple]
        Recent plan data.
    """
    return db.listar_planos_recentes(limit)


def backup_dados(dest: str | Path) -> None:
    """Create a copy of the database at ``dest``."""

    db.backup_database(dest)


def listar_exportadores() -> list[str]:
    """Listar formatos de exportação disponíveis."""

    return list(_REGISTRY.keys())


# ----- Exportação -----


def exportar_treino(
    fmt: str, titulo: str, exercicios: Iterable[dict], caminho: Path | str
) -> None:
    """Export a training plan using a registered exporter.

    Parameters
    ----------
    fmt:
        Export format registered as plugin.
    titulo:
        Title of the plan.
    exercicios:
        Iterable with exercise dictionaries.
    caminho:
        Destination path for the export file.
    """
    exporter = get_exporter(fmt)
    exporter.export(titulo, exercicios, Path(caminho))


# ----- PDF Utils -----


def sanitize_filename(nome: str) -> str:
    """Expose filename sanitization utility.

    Parameters
    ----------
    nome:
        Raw filename.

    Returns
    -------
    str
        Sanitized filename safe for saving on disk.
    """
    return pdf_utils.sanitize_filename(nome)
