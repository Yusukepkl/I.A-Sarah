"""Plugins for exporting training data in various formats."""

from __future__ import annotations

import csv
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterable

import openpyxl
from fpdf import FPDF

from ia_sarah.core.plugin_loader import load_entrypoints

logger = logging.getLogger(__name__)


class Exporter(ABC):
    """Base interface for data exporters."""

    @abstractmethod
    def export(self, title: str, exercises: Iterable[dict], path: Path) -> None:
        """Export the data."""
        raise NotImplementedError


class PDFExporter(Exporter):
    """Export data to a PDF file."""

    def export(self, title: str, exercises: Iterable[dict], path: Path) -> None:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_title(title)
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=title, ln=True, align="C")
        for ex in exercises:
            line = f"{ex.get('nome','')} - {ex.get('series','')}x{ex.get('reps','')}"
            if ex.get("peso"):
                line += f" {ex['peso']}"
            if ex.get("descanso"):
                line += f" descanso {ex['descanso']}"
            if ex.get("obs"):
                line += f" ({ex['obs']})"
            pdf.multi_cell(0, 10, txt=line)
        try:
            pdf.output(str(path))
        except OSError as exc:
            logger.error("Erro ao exportar PDF: %s", exc)
            raise


class CSVExporter(Exporter):
    """Export data to a CSV file."""

    def export(self, title: str, exercises: Iterable[dict], path: Path) -> None:
        try:
            with path.open("w", newline="", encoding="utf-8") as csvfile:
                writer = (
                    csv.DictWriter(csvfile, fieldnames=list(exercises[0].keys()))
                    if exercises
                    else csv.DictWriter(csvfile, fieldnames=[])
                )
                writer.writeheader()
                for ex in exercises:
                    writer.writerow(ex)
        except OSError as exc:
            logger.error("Erro ao exportar CSV: %s", exc)
            raise


class ExcelExporter(Exporter):
    """Export data to an Excel file using ``openpyxl``."""

    def export(self, title: str, exercises: Iterable[dict], path: Path) -> None:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = title
        if exercises:
            ws.append(list(exercises[0].keys()))
            for ex in exercises:
                ws.append([ex.get(k, "") for k in exercises[0].keys()])
        try:
            wb.save(path)
        except OSError as exc:
            logger.error("Erro ao exportar Excel: %s", exc)
            raise


_REGISTRY: dict[str, type[Exporter]] = {}


def register_exporter(fmt: str, cls: type[Exporter]) -> None:
    """Register a new exporter class."""
    _REGISTRY[fmt] = cls


def get_exporter(fmt: str) -> Exporter:
    """Instantiate an exporter by format name."""
    if fmt not in _REGISTRY:
        raise KeyError(f"Exporter {fmt} not registered")
    return _REGISTRY[fmt]()


# Register default exporters on import
register_exporter("pdf", PDFExporter)
register_exporter("csv", CSVExporter)
register_exporter("xlsx", ExcelExporter)

# Load external exporter plugins
load_entrypoints("ia_sarah.exporters", register_exporter)
