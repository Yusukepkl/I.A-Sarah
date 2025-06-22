from __future__ import annotations

from PySide6.QtCore import QEasingCurve, QPropertyAnimation, Qt
from PySide6.QtGui import QGuiApplication, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QSplashScreen,
    QStackedWidget,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from ia_sarah.core.use_cases import controllers

from .theme import Palette, stylesheet
from .widgets_qt import AnimatedButton, CardFrame


class MainWindow(QMainWindow):
    """Base window using QStackedWidget for navigation."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Sarah 4.0")
        self.resize(900, 600)
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        self.pages: dict[str, QWidget] = {}
        self._init_toolbar()
        self._init_pages()

    def _init_toolbar(self) -> None:
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        btn_dashboard = AnimatedButton("Dashboard")
        btn_dashboard.clicked.connect(lambda: self.show_page("dashboard"))
        toolbar.addWidget(btn_dashboard)

    def _init_pages(self) -> None:
        dashboard = QWidget()
        layout = QVBoxLayout()
        card = CardFrame()
        layout.addWidget(card)
        dashboard.setLayout(layout)
        self.pages["dashboard"] = dashboard
        self.stack.addWidget(dashboard)

    def show_page(self, name: str) -> None:
        widget = self.pages.get(name)
        if widget:
            self._animate_transition(widget)

    def _animate_transition(self, widget: QWidget) -> None:
        current = self.stack.currentWidget()
        if current is widget:
            return
        self.stack.setCurrentWidget(widget)
        if current:
            anim_out = QPropertyAnimation(current, b"windowOpacity")
            anim_out.setDuration(300)
            anim_out.setStartValue(1.0)
            anim_out.setEndValue(0.0)
            anim_out.setEasingCurve(QEasingCurve.InOutQuad)
            anim_out.start()
        anim_in = QPropertyAnimation(widget, b"windowOpacity")
        anim_in.setDuration(300)
        anim_in.setStartValue(0.0)
        anim_in.setEndValue(1.0)
        anim_in.setEasingCurve(QEasingCurve.InOutQuad)
        anim_in.start()


def _show_splash(app: QApplication) -> None:
    splash_pix = QPixmap(400, 300)
    splash_pix.fill(Palette.dark_gray)
    splash = QSplashScreen(splash_pix)
    splash.setWindowFlag(Qt.WindowStaysOnTopHint)
    splash.setWindowOpacity(0.0)
    splash.show()
    anim = QPropertyAnimation(splash, b"windowOpacity")
    anim.setDuration(500)
    anim.setStartValue(0.0)
    anim.setEndValue(1.0)
    anim.start()
    QGuiApplication.processEvents()
    app.processEvents()
    anim.finished.connect(lambda: splash.close())


def criar_interface() -> None:
    """Launch the PySide6 interface."""

    controllers.init_app()
    app = QApplication([])
    app.setStyleSheet(stylesheet())
    _show_splash(app)
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    criar_interface()

