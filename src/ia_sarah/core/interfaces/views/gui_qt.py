from __future__ import annotations

import json

from PySide6.QtCore import QEasingCurve, QPropertyAnimation, Qt, QPoint
from PySide6.QtGui import QGuiApplication, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QMessageBox,
    QLabel,
    QListWidget,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QInputDialog,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSplashScreen,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from ia_sarah.core.use_cases import controllers
from ia_sarah.core.entities.models import TrainingPlan, Student

from .theme import Palette, stylesheet
from .widgets_qt import AnimatedButton, CardFrame


def show_feedback(parent: QWidget, message: str, error: bool = False) -> None:
    """Display success or error notification."""

    if error:
        QMessageBox.critical(parent, "Erro", message)
    else:
        QMessageBox.information(parent, "Sucesso", message)


class StudentDialog(QDialog):
    """Simple dialog to edit student information."""

    def __init__(self, nome: str = "", email: str = "", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Aluno")
        layout = QFormLayout(self)
        self.nome_edit = QLineEdit(nome)
        self.email_edit = QLineEdit(email)
        layout.addRow("Nome:", self.nome_edit)
        layout.addRow("Email:", self.email_edit)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_data(self) -> tuple[str, str]:
        return self.nome_edit.text(), self.email_edit.text()


class PlanDialog(QDialog):
    """Dialog to create or edit a training plan."""

    def __init__(
        self,
        nome: str = "",
        descricao: str = "",
        exercicios: str = "",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("Plano")
        layout = QFormLayout(self)
        self.nome_edit = QLineEdit(nome)
        self.desc_edit = QLineEdit(descricao)
        self.ex_edit = QLineEdit(exercicios)
        layout.addRow("Nome:", self.nome_edit)
        layout.addRow("Descri\u00e7\u00e3o:", self.desc_edit)
        layout.addRow("Exerc\u00edcios:", self.ex_edit)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_data(self) -> tuple[str, str, str]:
        return (
            self.nome_edit.text(),
            self.desc_edit.text(),
            self.ex_edit.text(),
        )


class DashboardPage(QWidget):
    """Simple dashboard with statistics."""

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        card_stats = CardFrame()
        stats_layout = QVBoxLayout(card_stats)
        self.total_label = QLabel()
        stats_layout.addWidget(self.total_label)
        layout.addWidget(card_stats)

        card_recent = CardFrame()
        recent_layout = QVBoxLayout(card_recent)
        recent_layout.addWidget(QLabel("Planos recentes:"))
        self.plans_list = QListWidget()
        recent_layout.addWidget(self.plans_list)
        layout.addWidget(card_recent)

        self.load_data()

    def load_data(self) -> None:
        total = controllers.contar_alunos()
        self.total_label.setText(f"Total de alunos: {total}")
        self.plans_list.clear()
        for _id, nome, aluno in controllers.listar_planos_recentes(5):
            self.plans_list.addItem(f"{nome} - {aluno}")


class AlunosPage(QWidget):
    """Page with CRUD operations for students."""

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["ID", "Nome", "Email"])
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Adicionar")
        self.edit_btn = QPushButton("Editar")
        self.del_btn = QPushButton("Excluir")
        self.plan_btn = QPushButton("Planos")
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.del_btn)
        btn_layout.addWidget(self.plan_btn)
        layout.addLayout(btn_layout)

        self.add_btn.clicked.connect(self.adicionar)
        self.edit_btn.clicked.connect(self.editar)
        self.del_btn.clicked.connect(self.excluir)
        self.plan_btn.clicked.connect(self.abrir_planos)
        self.table.itemDoubleClicked.connect(lambda *_: self.editar())

        self.load_data()

    def load_data(self) -> None:
        self.table.setRowCount(0)
        for row, aluno in enumerate(controllers.listar_alunos()):
            self.table.insertRow(row)
            values = (aluno.id, aluno.nome, aluno.email)
            for col, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                self.table.setItem(row, col, item)

    def _selected_id(self) -> int | None:
        row = self.table.currentRow()
        if row < 0:
            return None
        item = self.table.item(row, 0)
        if item:
            return int(item.text())
        return None

    def adicionar(self) -> None:
        dlg = StudentDialog(parent=self)
        if dlg.exec() == QDialog.Accepted:
            nome, email = dlg.get_data()
            if nome:
                try:
                    controllers.adicionar_aluno(nome, email)
                except Exception as exc:  # pragma: no cover - runtime errors
                    show_feedback(self, f"Erro ao adicionar aluno: {exc}", True)
                else:
                    show_feedback(self, "Aluno adicionado com sucesso!")
                    self.load_data()

    def editar(self) -> None:
        aluno_id = self._selected_id()
        if aluno_id is None:
            return
        aluno = controllers.obter_aluno(aluno_id)
        if aluno is None:
            return
        dlg = StudentDialog(aluno.nome, aluno.email or "", self)
        if dlg.exec() == QDialog.Accepted:
            nome, email = dlg.get_data()
            try:
                controllers.atualizar_aluno(aluno_id, "nome", nome)
                controllers.atualizar_aluno(aluno_id, "email", email)
            except Exception as exc:  # pragma: no cover - runtime errors
                show_feedback(self, f"Erro ao atualizar aluno: {exc}", True)
            else:
                show_feedback(self, "Aluno atualizado com sucesso!")
                self.load_data()

    def excluir(self) -> None:
        aluno_id = self._selected_id()
        if aluno_id is None:
            return
        try:
            controllers.remover_aluno(aluno_id)
        except Exception as exc:  # pragma: no cover - runtime errors
            show_feedback(self, f"Erro ao remover aluno: {exc}", True)
        else:
            show_feedback(self, "Aluno removido com sucesso!")
            self.load_data()

    def abrir_planos(self) -> None:
        aluno_id = self._selected_id()
        if aluno_id is None:
            return
        dlg = QDialog(self)
        dlg.setWindowTitle("Planos do Aluno")
        layout = QVBoxLayout(dlg)
        page = PlanosPage(aluno_id)
        layout.addWidget(page)
        close_btn = QDialogButtonBox(QDialogButtonBox.Close)
        close_btn.rejected.connect(dlg.reject)
        layout.addWidget(close_btn)
        dlg.exec()


class PlanosPage(QWidget):
    """List and edit training plans for a student."""

    def __init__(self, aluno_id: int) -> None:
        super().__init__()
        self.aluno_id = aluno_id
        layout = QVBoxLayout(self)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["ID", "Nome", "Descri\u00e7\u00e3o"])
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Adicionar")
        self.edit_btn = QPushButton("Editar")
        self.del_btn = QPushButton("Excluir")
        self.export_btn = QPushButton("Exportar")
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.del_btn)
        btn_layout.addWidget(self.export_btn)
        layout.addLayout(btn_layout)

        self.add_btn.clicked.connect(self.adicionar)
        self.edit_btn.clicked.connect(self.editar)
        self.del_btn.clicked.connect(self.excluir)
        self.export_btn.clicked.connect(self.exportar)
        self.table.itemDoubleClicked.connect(lambda *_: self.editar())

        self.load_data()

    def load_data(self) -> None:
        self.table.setRowCount(0)
        for row, plano in enumerate(controllers.listar_planos(self.aluno_id)):
            self.table.insertRow(row)
            values = (plano.id, plano.nome, plano.descricao)
            for col, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                self.table.setItem(row, col, item)

    def _selected_id(self) -> int | None:
        row = self.table.currentRow()
        if row < 0:
            return None
        item = self.table.item(row, 0)
        if item:
            return int(item.text())
        return None

    def _get_plano(self, plano_id: int) -> TrainingPlan | None:
        for p in controllers.listar_planos(self.aluno_id):
            if p.id == plano_id:
                return p
        return None

    def adicionar(self) -> None:
        dlg = PlanDialog(parent=self)
        if dlg.exec() == QDialog.Accepted:
            nome, desc, ex = dlg.get_data()
            if nome:
                try:
                    controllers.adicionar_plano(self.aluno_id, nome, desc, ex)
                except Exception as exc:  # pragma: no cover - runtime errors
                    show_feedback(self, f"Erro ao adicionar plano: {exc}", True)
                else:
                    show_feedback(self, "Plano adicionado com sucesso!")
                    self.load_data()

    def editar(self) -> None:
        plano_id = self._selected_id()
        if plano_id is None:
            return
        plano = self._get_plano(plano_id)
        if plano is None:
            return
        dlg = PlanDialog(plano.nome, plano.descricao or "", plano.exercicios_json or "", self)
        if dlg.exec() == QDialog.Accepted:
            nome, desc, ex = dlg.get_data()
            try:
                controllers.atualizar_plano(plano_id, nome, desc, ex)
            except Exception as exc:  # pragma: no cover - runtime errors
                show_feedback(self, f"Erro ao atualizar plano: {exc}", True)
            else:
                show_feedback(self, "Plano atualizado com sucesso!")
                self.load_data()

    def excluir(self) -> None:
        plano_id = self._selected_id()
        if plano_id is None:
            return
        try:
            controllers.remover_plano(plano_id)
        except Exception as exc:  # pragma: no cover - runtime errors
            show_feedback(self, f"Erro ao remover plano: {exc}", True)
        else:
            show_feedback(self, "Plano removido com sucesso!")
            self.load_data()

    def exportar(self) -> None:
        plano_id = self._selected_id()
        if plano_id is None:
            return
        plano = self._get_plano(plano_id)
        if plano is None:
            return
        try:
            exercicios = json.loads(plano.exercicios_json or "[]")
            if not isinstance(exercicios, list):
                exercicios = []
        except Exception:
            exercicios = []
        formatos = ["pdf", "csv", "xlsx"]
        fmt, ok = QInputDialog.getItem(
            self, "Formato", "Escolha o formato:", formatos, 0, False
        )
        if not ok or not fmt:
            return
        default_name = controllers.sanitize_filename(plano.nome) + f".{fmt}"
        path, _ = QFileDialog.getSaveFileName(self, "Exportar", default_name, f"*.{fmt}")
        if not path:
            return
        try:
            controllers.exportar_treino(fmt, plano.nome, exercicios, path)
        except Exception as exc:  # pragma: no cover - runtime errors
            show_feedback(self, f"Erro ao exportar: {exc}", True)
        else:
            show_feedback(self, "Exporta\u00e7\u00e3o conclu\u00edda!")


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
        dashboard = DashboardPage()
        self.pages["dashboard"] = dashboard
        self.stack.addWidget(dashboard)

        alunos = AlunosPage()
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

