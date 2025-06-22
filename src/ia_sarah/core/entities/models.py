from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Student:
    """Domain entity representing a student."""

    id: Optional[int]
    nome: str
    email: str
    data_inicio: str


@dataclass
class TrainingPlan:
    """Domain entity representing a training plan."""

    id: Optional[int]
    aluno_id: int
    nome: str
    descricao: str
    exercicios_json: str
