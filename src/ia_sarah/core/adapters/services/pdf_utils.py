"""Utilities to create PDF reports."""

from __future__ import annotations

import logging
import unicodedata
from pathlib import Path
from typing import Iterable

from fpdf import FPDF

logger = logging.getLogger(__name__)


def sanitize_filename(nome: str) -> str:
    """Return a safe filename removing accents and non-alphanumerics."""
    nfkd = unicodedata.normalize("NFKD", nome)
    ascii_only = nfkd.encode("ASCII", "ignore").decode("ASCII")
    return "".join(c if c.isalnum() else "_" for c in ascii_only).lower()


def gerar_pdf(titulo: str, conteudo: str, caminho: Path | str) -> None:
    """Generate a simple PDF with free content."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_title(titulo)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=titulo, ln=True, align="C")
    pdf.multi_cell(0, 10, txt=conteudo)
    try:
        pdf.output(str(caminho))
    except OSError as exc:  # pragma: no cover - filesystem errors
        logger.error("Erro ao gerar PDF: %s", exc)
        raise


def gerar_treino_pdf(
    titulo: str, exercicios: Iterable[dict], caminho: Path | str
) -> None:
    """Generate a structured PDF with an exercise list."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_title(titulo)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=titulo, ln=True, align="C")
    for ex in exercicios:
        linha = f"{ex.get('nome', '')} - {ex.get('series', '')}x{ex.get('reps', '')}"
        if ex.get("peso"):
            linha += f" {ex['peso']}"
        if ex.get("descanso"):
            linha += f" descanso {ex['descanso']}"
        if ex.get("obs"):
            linha += f" ({ex['obs']})"
        pdf.multi_cell(0, 10, txt=linha)
    try:
        pdf.output(str(caminho))
    except OSError as exc:  # pragma: no cover - filesystem errors
        logger.error("Erro ao gerar PDF de treino: %s", exc)
        raise
