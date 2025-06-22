from __future__ import annotations

from PySide6.QtGui import QColor


class Palette:
    """Central color palette for the PySide interface."""

    # primary / secondary / neutral colours
    electric_blue = QColor("#2979ff")
    vivid_orange = QColor("#ff6d00")
    dark_gray = QColor("#212121")
    white = QColor("#ffffff")
    neon_green = QColor("#39ff14")


def stylesheet(dark: bool = False) -> str:
    """Return the default QSS stylesheet for the application."""

    bg = Palette.dark_gray.name() if dark else Palette.white.name()
    fg = Palette.white.name() if dark else Palette.dark_gray.name()

    return f"""
    * {{
        font-family: 'Roboto', sans-serif;
    }}
    QMainWindow {{
        background: {bg};
        color: {fg};
    }}
    QToolBar {{
        background: {Palette.dark_gray.name()};
    }}
    QPushButton {{
        background-color: {Palette.electric_blue.name()};
        color: {Palette.white.name()};
        border-radius: 6px;
        padding: 6px 12px;
    }}
    QPushButton:hover {{
        background-color: {Palette.vivid_orange.name()};
    }}
    QFrame#card {{
        background-color: {Palette.white.name()};
        border-radius: 10px;
    }}
    """

