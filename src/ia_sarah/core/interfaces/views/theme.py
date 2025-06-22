from __future__ import annotations

from PySide6.QtGui import QColor


class Palette:
    """Paleta de cores central utilizada na interface Qt."""

    electric_blue = QColor("#2979ff")
    vivid_orange = QColor("#ff6d00")
    dark_gray = QColor("#212121")
    white = QColor("#ffffff")
    neon_green = QColor("#39ff14")
    light_gray = QColor("#f0f0f0")


def stylesheet(dark: bool = False) -> str:
    """Retorna o QSS padrão da aplicação."""

    bg = Palette.dark_gray.name() if dark else Palette.white.name()
    fg = Palette.white.name() if dark else Palette.dark_gray.name()
    alt = Palette.dark_gray.lighter(130).name() if dark else Palette.light_gray.name()

    return f"""
    * {{
        font-family: 'Segoe UI', 'Roboto', sans-serif;
    }}
    QMainWindow {{
        background: {bg};
        color: {fg};
    }}
    QToolBar {{
        background: {Palette.dark_gray.name()};
        border: none;
    }}
    QPushButton {{
        background-color: {Palette.electric_blue.name()};
        color: {Palette.white.name()};
        border-radius: 8px;
        padding: 6px 12px;
    }}
    QPushButton:hover {{
        background-color: {Palette.vivid_orange.name()};
    }}
    QFrame#card {{
        background-color: {Palette.white.name()};
        border-radius: 12px;
        padding: 8px;
    }}
    QTableWidget {{
        gridline-color: transparent;
        selection-background-color: {Palette.vivid_orange.name()};
        selection-color: {Palette.white.name()};
        alternate-background-color: {alt};
    }}
    QHeaderView::section {{
        background-color: {Palette.dark_gray.name()};
        color: {Palette.white.name()};
        padding: 4px;
        border: none;
    }}
    """
