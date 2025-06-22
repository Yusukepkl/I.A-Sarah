from __future__ import annotations

from PySide6.QtCore import QEasingCurve, QPropertyAnimation
from PySide6.QtWidgets import (
    QPushButton,
    QFrame,
    QGraphicsDropShadowEffect,
)

from ia_sarah.core.interfaces.views.theme import Palette


class AnimatedButton(QPushButton):
    """QPushButton with simple hover and click animations."""

    def __init__(self, text: str = "", parent=None) -> None:
        super().__init__(text, parent)
        self._hover_anim: QPropertyAnimation | None = None
        self._click_anim: QPropertyAnimation | None = None
        self._base_geom = None
        self._shadow = QGraphicsDropShadowEffect(self)
        self._shadow.setBlurRadius(8)
        self._shadow.setOffset(0, 2)
        self._shadow.setColor(Palette.dark_gray)
        self._shadow.setEnabled(False)
        self.setGraphicsEffect(self._shadow)

    def enterEvent(self, event) -> None:  # noqa: D401 - Qt signature
        self._shadow.setEnabled(True)
        self._base_geom = self.geometry()
        self._animate_hover(True)
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:  # noqa: D401 - Qt signature
        self._animate_hover(False)
        self._shadow.setEnabled(False)
        super().leaveEvent(event)

    def mousePressEvent(self, event) -> None:  # noqa: D401 - Qt signature
        self._animate_click()
        super().mousePressEvent(event)

    def _animate_hover(self, entering: bool) -> None:
        start = self.geometry()
        end = (
            start.adjusted(-2, -2, 2, 2)
            if entering
            else (self._base_geom or start)
        )
        self._hover_anim = QPropertyAnimation(self, b"geometry")
        self._hover_anim.setDuration(150)
        self._hover_anim.setStartValue(start)
        self._hover_anim.setEndValue(end)
        self._hover_anim.setEasingCurve(QEasingCurve.OutQuad)
        self._hover_anim.start()
        if entering:
            color = Palette.vivid_orange.name()
            self.setStyleSheet(f"background-color: {color};")
        else:
            self.setStyleSheet("")

    def _animate_click(self) -> None:
        start = self.geometry()
        self._click_anim = QPropertyAnimation(self, b"geometry")
        self._click_anim.setDuration(200)
        self._click_anim.setKeyValueAt(0.5, start.adjusted(0, 2, 0, 2))
        self._click_anim.setEndValue(start)
        self._click_anim.setEasingCurve(QEasingCurve.OutBounce)
        self._click_anim.start()


class CardFrame(QFrame):
    """Container frame styled as a card with drop shadow."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("card")
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setOffset(0, 2)
        shadow.setColor(Palette.dark_gray)
        self.setGraphicsEffect(shadow)
