"""Modern ttkbootstrap-based GUI for managing students and workout plans."""

import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable
import ttkbootstrap as tb

import db
from pdf_utils import gerar_treino_pdf, sanitize_filename


class ExercicioRow(ttk.Frame):
    """Widget row representing an exercise in the plan editor."""

    def __init__(self, master: tk.Widget, remover, dados: dict | None = None) -> None:
        super().__init__(master)
        self.ex_id = None
        self.vars = {
            'nome': tk.StringVar(),
            'series': tk.StringVar(),
            'reps': tk.StringVar(),
            'peso': tk.StringVar(),
            'descanso': tk.StringVar(),
            'obs': tk.StringVar(),
        }
        if dados:
            self.ex_id = dados.get('id')
            for k in self.vars:
                self.vars[k].set(dados.get(k, ''))
        ttk.Entry(self, textvariable=self.vars['nome'], width=15).grid(row=0, column=0, padx=2, pady=2)
        ttk.Entry(self, textvariable=self.vars['series'], width=5).grid(row=0, column=1, padx=2)
        ttk.Entry(self, textvariable=self.vars['reps'], width=5).grid(row=0, column=2, padx=2)
        ttk.Entry(self, textvariable=self.vars['peso'], width=7).grid(row=0, column=3, padx=2)
        ttk.Entry(self, textvariable=self.vars['descanso'], width=8).grid(row=0, column=4, padx=2)
        ttk.Entry(self, textvariable=self.vars['obs'], width=15).grid(row=0, column=5, padx=2)
        ttk.Button(self, text="X", width=2, command=lambda: remover(self)).grid(row=0, column=6, padx=2)

    def get_data(self) -> dict:
        """Return the exercise information entered in this row."""
        data = {k: v.get().strip() for k, v in self.vars.items()}
        if self.ex_id is not None:
            data['id'] = self.ex_id
        return data


class PlanoModal(tb.Toplevel):
    """Modal window for creating or editing a training plan."""

    def __init__(
        self, aluno_id: int, ao_salvar: Callable[[], None], plano: dict | None = None
    ) -> None:
        """Construct the modal.

        Parameters
        ----------
        aluno_id: int
            Identifier of the student owning the plan.
        ao_salvar: Callable
            Callback executed after saving.
        plano: dict | None
            Existing plan data when editing.
        """
        super().__init__()
        self.geometry("650x450")
        self.grab_set()
        self.aluno_id = aluno_id
        self.ao_salvar = ao_salvar
        self.exercicios = []
        self.plano_id = None

        nome_var = tk.StringVar()
        self.title("Novo Plano de Treino" if plano is None else "Editar Plano de Treino")
        ttk.Label(self, text="Nome do Plano:").pack(anchor="w", padx=5, pady=5)
        ttk.Entry(self, textvariable=nome_var, width=40).pack(anchor="w", padx=5)

        ttk.Label(self, text="Descrição (opcional):").pack(anchor="w", padx=5, pady=(10,0))
        desc = tk.Text(self, height=3, width=50)
        desc.pack(anchor="w", padx=5)

        area = ttk.Frame(self)
        area.pack(fill="both", expand=True, pady=10)

        header = ttk.Frame(area)
        header.pack(fill="x")
        cols = ["Exercício", "Séries", "Reps", "Peso", "Descanso", "Obs"]
        for i, t in enumerate(cols):
            ttk.Label(header, text=t, font=("Segoe UI", 9, "bold")).grid(row=0, column=i, padx=2)

        def remover_row(row):
            row.destroy()
            self.exercicios.remove(row)

        def add_row(dados=None):
            row = ExercicioRow(area, remover_row, dados)
            row.pack(fill="x", pady=2, padx=5)
            self.exercicios.append(row)

        ttk.Button(self, text="Adicionar Exercício", command=lambda: add_row()).pack(pady=5)

        if plano:
            self.plano_id = plano.get('id')
            nome_var.set(plano.get('nome', ''))
            desc.insert('1.0', plano.get('descricao', '') or '')
            try:
                exs = json.loads(plano.get('exercicios') or '[]')
            except json.JSONDecodeError:
                exs = []
            if exs:
                for ex in exs:
                    add_row(ex)
            else:
                add_row()
        else:
            add_row()

        def salvar():
            nome = nome_var.get().strip()
            if not nome:
                messagebox.showwarning("Aviso", "Nome do plano obrigatório", parent=self)
                return
            descricao = desc.get("1.0", tk.END).strip()
            dados = [r.get_data() for r in self.exercicios if r.get_data().get('nome')]
            exercicios_json = json.dumps(dados, ensure_ascii=False)
            if self.plano_id:
                db.atualizar_plano(self.plano_id, nome, descricao, exercicios_json)
            else:
                db.adicionar_plano(self.aluno_id, nome, descricao, exercicios_json)
            self.destroy()
            self.ao_salvar()

        ttk.Button(self, text="Salvar", command=salvar).pack(pady=5)

CONFIG_FILE = "config.json"

def load_theme():
    """Load the saved UI theme from the configuration file."""

    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("theme", "superhero")
        except Exception:
            pass
    return "superhero"

def save_theme(theme: str) -> None:
    """Persist the chosen UI theme to disk."""

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump({"theme": theme}, f)

def abrir_modal_adicionar(atualizar: Callable[[], None]) -> None:
    """Open modal to create a new student and refresh list on save."""

    win = tb.Toplevel()
    win.title("Adicionar Aluno")
    win.grab_set()

    nome_var = tk.StringVar()
    email_var = tk.StringVar()

    ttk.Label(win, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    ttk.Entry(win, textvariable=nome_var, width=30).grid(row=0, column=1, padx=5, pady=5)
    ttk.Label(win, text="Email:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    ttk.Entry(win, textvariable=email_var, width=30).grid(row=1, column=1, padx=5, pady=5)

    def salvar():
        nome = nome_var.get().strip()
        email = email_var.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "Nome nao pode ser vazio", parent=win)
            return
        db.adicionar_aluno(nome, email)
        win.destroy()
        atualizar()

    ttk.Button(win, text="Salvar", command=salvar).grid(row=2, column=0, columnspan=2, pady=10)

class DetalhesFrame(ttk.Frame):
    """Panel showing detailed information about a student."""

    def __init__(
        self,
        master: tk.Widget,
        dados: tuple,
        voltar: Callable[[], None],
        atualizar_lista: Callable[[], None],
    ) -> None:
        """Create the frame.

        Parameters
        ----------
        master: Widget
            Parent container.
        dados: tuple
            Data returned from ``db.obter_aluno``.
        voltar: Callable
            Callback to return to the list view.
        atualizar_lista: Callable
            Function to refresh the list of students.
        """
        super().__init__(master)
        self.aluno_id = dados[0]
        self.voltar = voltar
        self.atualizar_lista = atualizar_lista
        self.configure(padding=20)

        ttk.Button(self, text="Voltar", command=self.voltar).pack(anchor="w")
        ttk.Label(self, text=dados[1], font=("Segoe UI", 12, "bold")).pack(anchor="w")
        ttk.Label(self, text=dados[2] or "-").pack(anchor="w")
        ttk.Label(self, text=f"Inicio: {dados[3]}").pack(anchor="w", pady=(0, 10))

        botoes = ttk.Frame(self)
        botoes.pack(fill="x", pady=5)
        ttk.Button(botoes, text="Excluir Aluno", command=self.excluir_aluno).pack(side="right")

        self.planos_frame = ttk.Labelframe(self, text="Planos de Treino")
        self.planos_frame.pack(fill="both", expand=True, pady=10)

        ttk.Button(self.planos_frame, text="Adicionar Plano", command=self.abrir_plano_modal).pack(pady=5)
        self.listar_planos()

    def listar_planos(self) -> None:
        """Refresh the list of workout plans for the student."""
        for child in self.planos_frame.winfo_children():
            if getattr(child, "is_card", False):
                child.destroy()
        planos = db.listar_planos(self.aluno_id)
        for pid, nome, descricao, exercicios in planos:
            card = ttk.Frame(self.planos_frame, padding=10, relief="ridge")
            card.is_card = True
            card.pack(fill="x", pady=5)
            ttk.Label(card, text=nome, font=("Segoe UI", 10, "bold")).pack(anchor="w")
            if descricao:
                ttk.Label(card, text=descricao).pack(anchor="w")
            try:
                exs = json.loads(exercicios) if exercicios else []
            except json.JSONDecodeError:
                exs = []
            for ex in exs:
                info = f"{ex.get('nome','')} - {ex.get('series','')}x{ex.get('reps','')}"
                if ex.get('peso'):
                    info += f" {ex.get('peso')}"
                if ex.get('descanso'):
                    info += f" descanso {ex.get('descanso')}"
                if ex.get('obs'):
                    info += f" ({ex.get('obs')})"
                ttk.Label(card, text=info).pack(anchor="w")
            btns = ttk.Frame(card)
            btns.pack(anchor="e", pady=(5,0))
            ttk.Button(btns, text="PDF", command=lambda n=nome,e=exercicios: self.gerar_plano_pdf(n,e)).pack(side="right")
            ttk.Button(btns, text="Editar", command=lambda p=(pid,nome,descricao,exercicios): self.editar_plano(p)).pack(side="right")
            ttk.Button(btns, text="Excluir", command=lambda i=pid: self.excluir_plano(i)).pack(side="right")

    def abrir_plano_modal(self) -> None:
        """Open dialog to create a new plan."""
        PlanoModal(self.aluno_id, self.listar_planos)

    def editar_plano(self, plano: tuple) -> None:
        """Open dialog to edit an existing plan."""
        p = {
            'id': plano[0],
            'nome': plano[1],
            'descricao': plano[2],
            'exercicios': plano[3],
        }
        PlanoModal(self.aluno_id, self.listar_planos, plano=p)

    def gerar_plano_pdf(self, nome: str, exercicios_json: str) -> None:
        """Generate a PDF file for the given plan."""
        try:
            exs = json.loads(exercicios_json) if exercicios_json else []
        except json.JSONDecodeError:
            exs = []
        if not exs:
            messagebox.showwarning("Aviso", "Plano sem exercícios", parent=self)
            return
        file_name = sanitize_filename(f"{self.aluno_id}_{nome}")
        path = f"treino_{file_name}.pdf"
        gerar_treino_pdf(f"Treino - {nome}", exs, path)
        messagebox.showinfo("PDF", f"Treino exportado como {path}", parent=self)

    def excluir_plano(self, plano_id: int) -> None:
        """Delete a plan after confirmation."""
        if messagebox.askyesno("Confirmar", "Excluir plano?", parent=self):
            db.remover_plano(plano_id)
            self.listar_planos()

    def excluir_aluno(self) -> None:
        """Remove this student from the database."""
        if messagebox.askyesno("Confirmar", "Excluir aluno?", parent=self):
            db.remover_aluno(self.aluno_id)
            self.atualizar_lista()
            self.voltar()

def criar_interface() -> None:
    """Launch the main application window."""

    db.init_db()
    theme = load_theme()
    app = tb.Window(themename=theme)
    app.title("Gestor de Alunos")

    def toggle_theme():
        new_theme = "superhero" if theme_var.get() else "flatly"
        app.style.theme_use(new_theme)
        save_theme(new_theme)

    header = ttk.Frame(app, padding=10)
    header.pack(fill="x")
    ttk.Label(header, text="Gestor de Alunos", font=("Segoe UI", 14, "bold")).pack(side="left")
    theme_var = tk.BooleanVar(value=theme=="superhero")
    tb.Checkbutton(
        header,
        text="Modo Escuro",
        variable=theme_var,
        command=toggle_theme,
        bootstyle="round-toggle",
    ).pack(side="right")

    main = ttk.Frame(app, padding=10)
    main.pack(fill="both", expand=True)

    list_frame = ttk.Frame(main)
    list_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(list_frame)
    scroll = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scroll.set)
    scroll.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    cards = ttk.Frame(canvas)
    canvas.create_window((0,0), window=cards, anchor="nw")

    detail_container = ttk.Frame(main)
    detail_container.pack(fill="both", expand=True)
    detail_container.pack_forget()

    def on_configure(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))
    cards.bind("<Configure>", on_configure)

    def show_list():
        for child in detail_container.winfo_children():
            child.destroy()
        detail_container.pack_forget()
        list_frame.pack(fill="both", expand=True)
        atualizar_cards()

    def show_detail(aluno_id):
        list_frame.pack_forget()
        for child in detail_container.winfo_children():
            child.destroy()
        dados = db.obter_aluno(aluno_id)
        DetalhesFrame(detail_container, dados, show_list, atualizar_cards).pack(fill="both", expand=True)
        detail_container.pack(fill="both", expand=True)

    def atualizar_cards():
        for child in cards.winfo_children():
            child.destroy()
        alunos = db.listar_alunos()
        if not alunos:
            ttk.Label(cards, text="Nenhum aluno cadastrado").pack(pady=20)
        for aid, nome, email, data_inicio in alunos:
            card = ttk.Frame(cards, padding=10, relief="ridge", borderwidth=1)
            card.pack(fill="x", pady=5)
            ttk.Label(card, text=nome, font=("Segoe UI", 11, "bold")).pack(anchor="w")
            ttk.Label(card, text=email or "-").pack(anchor="w")
            ttk.Label(card, text=f"Desde {data_inicio}").pack(anchor="w")
            card.bind("<Button-1>", lambda e, i=aid: show_detail(i))
            for w in card.winfo_children():
                w.bind("<Button-1>", lambda e, i=aid: show_detail(i))

    botoes = ttk.Frame(app, padding=10)
    botoes.pack(fill="x")
    ttk.Button(botoes, text="Adicionar Aluno", command=lambda: abrir_modal_adicionar(atualizar_cards)).pack()

    atualizar_cards()
    app.mainloop()

if __name__ == "__main__":
    criar_interface()
