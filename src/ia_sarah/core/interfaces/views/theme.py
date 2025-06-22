from __future__ import annotations

from PySide6.QtGui import QColor


class Palette:
    """Central color palette for the PySide interface."""

    electric_blue = QColor("#1e88e5")
    vivid_orange = QColor("#ff9800")
    dark_gray = QColor("#212121")
    light_gray = QColor("#f5f5f5")
    neon_green = QColor("#39ff14")


def stylesheet() -> str:
    """Return the default QSS stylesheet for the application."""

    return f"""
    QPushButton {{
        background-color: {Palette.electric_blue.name()};
        color: white;
        border-radius: 4px;
        padding: 4px 10px;
    }}
    QPushButton:hover {{
        background-color: {Palette.vivid_orange.name()};
    }}
    QFrame#card {{
        background-color: {Palette.light_gray.name()};
        border-radius: 8px;
    }}
    """

