from __future__ import annotations

from PySide6.QtCore import QEasingCurve, QPropertyAnimation, QRect
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import (
    QFrame,
    QPushButton,
    QGraphicsDropShadowEffect,
)

from .theme import Palette


class AnimatedButton(QPushButton):
    """Button with simple hover and click animations."""

    def __init__(self, text: str = "", parent=None) -> None:
        super().__init__(text, parent)
        self._base_geom: QRect | None = None
        self._hover_anim = QPropertyAnimation(self, b"geometry", self)
        self._hover_anim.setEasingCurve(QEasingCurve.OutQuad)
        self._hover_anim.setDuration(150)
        self._press_anim = QPropertyAnimation(self, b"geometry", self)
        self._press_anim.setEasingCurve(QEasingCurve.OutCubic)
        self._press_anim.setDuration(120)
        effect = QGraphicsDropShadowEffect(blurRadius=8)
        effect.setColor(Palette.neon_green)
        effect.setOffset(0, 2)
        self.setGraphicsEffect(effect)
        effect.setEnabled(False)

    def enterEvent(self, event):
        if self._base_geom is None:
            self._base_geom = self.geometry()
        end = self._base_geom.adjusted(-2, -2, 2, 2)
        self._hover_anim.stop()
        self._hover_anim.setStartValue(self.geometry())
        self._hover_anim.setEndValue(end)
        self._hover_anim.start()
        if self.graphicsEffect():
            self.graphicsEffect().setEnabled(True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        if self._base_geom:
            self._hover_anim.stop()
            self._hover_anim.setStartValue(self.geometry())
            self._hover_anim.setEndValue(self._base_geom)
            self._hover_anim.start()
        if self.graphicsEffect():
            self.graphicsEffect().setEnabled(False)
        super().leaveEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        if self._base_geom:
            end = self._base_geom.adjusted(0, 2, 0, -2)
            self._press_anim.stop()
            self._press_anim.setStartValue(self.geometry())
            self._press_anim.setEndValue(end)
            self._press_anim.start()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if self._base_geom:
            self._press_anim.stop()
            self._press_anim.setStartValue(self.geometry())
            self._press_anim.setEndValue(self._base_geom)
            self._press_anim.start()
        super().mouseReleaseEvent(event)


class Card(QFrame):
    """Simple card container with rounded corners and shadow."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setStyleSheet(
            f"background-color: {Palette.light_gray.name()}; border-radius: 8px;"
        )
        shadow = QGraphicsDropShadowEffect(blurRadius=12)
        shadow.setOffset(0, 3)
        shadow.setColor(Palette.dark_gray)
        self.setGraphicsEffect(shadow)

