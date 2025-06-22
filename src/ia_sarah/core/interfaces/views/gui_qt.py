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
        self.dark = False
        self._init_toolbar()
        self._init_pages()

    def _init_toolbar(self) -> None:
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        btn_dashboard = AnimatedButton("Dashboard")
        btn_dashboard.clicked.connect(lambda: self.show_page("dashboard"))
        toolbar.addWidget(btn_dashboard)
        btn_alunos = AnimatedButton("Alunos")
        btn_alunos.clicked.connect(lambda: self.show_page("alunos"))
        toolbar.addWidget(btn_alunos)
        btn_config = AnimatedButton("Config")
        btn_config.clicked.connect(lambda: self.show_page("config"))
        toolbar.addWidget(btn_config)
        theme_btn = AnimatedButton("\u263e")
        theme_btn.clicked.connect(self.toggle_theme)
        toolbar.addWidget(theme_btn)

    def toggle_theme(self) -> None:
        self.dark = not self.dark
        self.setStyleSheet(stylesheet(self.dark))

    def _init_pages(self) -> None:
        dashboard = QWidget()
        dash_layout = QVBoxLayout(dashboard)
        dash_layout.addWidget(CardFrame())
        self.pages["dashboard"] = dashboard
        self.stack.addWidget(dashboard)

        alunos = QWidget()
        alunos_layout = QVBoxLayout(alunos)
        alunos_layout.addWidget(CardFrame())
        self.pages["alunos"] = alunos
        self.stack.addWidget(alunos)

        config = QWidget()
        config_layout = QVBoxLayout(config)
        config_layout.addWidget(CardFrame())
        self.pages["config"] = config
        self.stack.addWidget(config)

    def show_page(self, name: str) -> None:
        widget = self.pages.get(name)
        if widget:
            self._animate_transition(widget)

    def _animate_transition(self, widget: QWidget) -> None:
        current = self.stack.currentWidget()
        if current is widget:
            return
        if current:
            out_anim = QPropertyAnimation(current, b"pos")
            out_anim.setDuration(300)
            out_anim.setStartValue(current.pos())
            out_anim.setEndValue(current.pos() - QPoint(self.width(), 0))
            out_anim.setEasingCurve(QEasingCurve.InOutQuad)
            out_anim.start()
            fade_out = QPropertyAnimation(current, b"windowOpacity")
            fade_out.setDuration(300)
            fade_out.setStartValue(1.0)
            fade_out.setEndValue(0.0)
            fade_out.setEasingCurve(QEasingCurve.InOutQuad)
            fade_out.start()
        self.stack.setCurrentWidget(widget)
        widget.move(self.width(), 0)
        in_anim = QPropertyAnimation(widget, b"pos")
        in_anim.setDuration(300)
        in_anim.setStartValue(widget.pos())
        in_anim.setEndValue(QPoint(0, 0))
        in_anim.setEasingCurve(QEasingCurve.InOutQuad)
        in_anim.start()
        fade_in = QPropertyAnimation(widget, b"windowOpacity")
        fade_in.setDuration(300)
        fade_in.setStartValue(0.0)
        fade_in.setEndValue(1.0)
        fade_in.setEasingCurve(QEasingCurve.InOutQuad)
        fade_in.start()


def _show_splash(app: QApplication) -> None:
    splash_pix = QPixmap(400, 300)
    splash_pix.fill(Palette.dark_gray)
    splash = QSplashScreen(splash_pix)
    splash.setWindowFlag(Qt.WindowStaysOnTopHint)
    splash.setWindowOpacity(0.0)
    splash.show()
    anim_in = QPropertyAnimation(splash, b"windowOpacity")
    anim_in.setDuration(500)
    anim_in.setStartValue(0.0)
    anim_in.setEndValue(1.0)
    anim_in.start()
    QGuiApplication.processEvents()
    app.processEvents()

    def finish() -> None:
        anim_out = QPropertyAnimation(splash, b"windowOpacity")
        anim_out.setDuration(500)
        anim_out.setStartValue(1.0)
        anim_out.setEndValue(0.0)
        anim_out.finished.connect(splash.close)
        anim_out.start()

    anim_in.finished.connect(finish)


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

