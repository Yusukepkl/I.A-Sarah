from __future__ import annotations

from PySide6.QtGui import QColor


class Palette:
    """Central color palette for the PySide interface."""

    electric_blue = QColor("#1e88e5")
    vivid_orange = QColor("#ff9800")
    dark_gray = QColor("#212121")
    light_gray = QColor("#f5f5f5")
    neon_green = QColor("#39ff14")


STYLESHEET = f"""
QMainWindow {{
    background-color: {Palette.light_gray.name()};
    color: {Palette.dark_gray.name()};
    font-family: 'Roboto', sans-serif;
}}
QToolBar {{
    background-color: {Palette.electric_blue.name()};
}}
QPushButton {{
    background-color: {Palette.electric_blue.name()};
    color: white;
    border: none;
    border-radius: 4px;
    padding: 6px 12px;
}}
QPushButton:hover {{
    background-color: {Palette.vivid_orange.name()};
}}
"""

