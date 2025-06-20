"""Interface principal da aplicação."""

from __future__ import annotations

import json
import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tb

import db
from pdf_utils import gerar_treino_pdf, sanitize_filename
from config_manager import load_theme, save_theme
from widgets import PlanoModal


def abrir_modal_adicionar(atualizar: callable) -> None:
    """Mostra janela para adicionar um aluno."""
    win = tb.Toplevel()
    win.title("Adicionar Aluno")
    win.grab_set()
    win.grid_columnconfigure(1, weight=1)

    nome_var = tk.StringVar()
    email_var = tk.StringVar()

    ttk.Label(win, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    ttk.Entry(win, textvariable=nome_var, width=30).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    ttk.Label(win, text="Email:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    ttk.Entry(win, textvariable=email_var, width=30).grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    def salvar() -> None:
        nome = nome_var.get().strip()
        email = email_var.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "Nome não pode ser vazio", parent=win)
            return
        db.adicionar_aluno(nome, email)
        messagebox.showinfo("Sucesso", "Aluno adicionado com sucesso!", parent=win)
        win.destroy()
        atualizar()

    ttk.Button(win, text="Salvar", command=salvar).grid(row=2, column=0, columnspan=2, pady=10)


class DetalhesFrame(ttk.Frame):
    """Mostra detalhes e planos de um aluno."""

    def __init__(self, master: tk.Widget, dados: tuple, voltar: callable, atualizar_lista: callable) -> None:
        super().__init__(master)
        self.aluno_id = dados[0]
        self.voltar = voltar
        self.atualizar_lista = atualizar_lista
        self.configure(padding=20)

        ttk.Button(self, text="Voltar", command=self.voltar).pack(anchor="w")
        ttk.Label(self, text=dados[1], font=("Segoe UI", 12, "bold")).pack(anchor="w")
        ttk.Label(self, text=dados[2] or "-").pack(anchor="w")
        ttk.Label(self, text=f"Início: {dados[3]}").pack(anchor="w", pady=(0, 10))

        botoes = ttk.Frame(self)
        botoes.pack(fill="x", pady=5)
        ttk.Button(botoes, text="Excluir Aluno", command=self.excluir_aluno).pack(side="right")

        self.planos_frame = ttk.Labelframe(self, text="Planos de Treino")
        self.planos_frame.pack(fill="both", expand=True, pady=10)

        self.listar_planos()
        ttk.Button(self.planos_frame, text="Adicionar Plano", command=self.abrir_plano_modal).pack(pady=5)

    def listar_planos(self) -> None:
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
            btns.pack(anchor="e", pady=(5, 0))
            ttk.Button(btns, text="PDF", command=lambda n=nome, e=exercicios: self.gerar_plano_pdf(n, e)).pack(side="right")
            ttk.Button(btns, text="Editar", command=lambda p=(pid, nome, descricao, exercicios): self.editar_plano(p)).pack(side="right")
            ttk.Button(btns, text="Excluir", command=lambda i=pid: self.excluir_plano(i)).pack(side="right")

    def abrir_plano_modal(self) -> None:
        PlanoModal(self.aluno_id, self._salvar_plano)

    def editar_plano(self, plano: tuple) -> None:
        p = {"id": plano[0], "nome": plano[1], "descricao": plano[2], "exercicios": plano[3]}
        PlanoModal(self.aluno_id, self._salvar_plano, plano=p)

    def _salvar_plano(self, aluno_id: int, nome: str, descricao: str, exercicios_json: str, plano_id: int | None) -> None:
        if plano_id:
            db.atualizar_plano(plano_id, nome, descricao, exercicios_json)
        else:
            db.adicionar_plano(aluno_id, nome, descricao, exercicios_json)
        self.listar_planos()

    def gerar_plano_pdf(self, nome: str, exercicios_json: str) -> None:
        try:
            exs = json.loads(exercicios_json) if exercicios_json else []
        except json.JSONDecodeError:
            exs = []
        if not exs:
            messagebox.showwarning("Aviso", "Plano sem exercícios", parent=self)
            return
        file_name = sanitize_filename(f"{self.aluno_id}_{nome}")
        path = f"treino_{file_name}.pdf"
        pb = ttk.Progressbar(self, mode="indeterminate")
        pb.pack(fill="x", pady=5)
        pb.start()
        self.update_idletasks()
        try:
            gerar_treino_pdf(f"Treino - {nome}", exs, path)
        finally:
            pb.stop()
            pb.destroy()
        messagebox.showinfo("PDF", f"Treino exportado como {path}", parent=self)

    def excluir_plano(self, plano_id: int) -> None:
        if messagebox.askyesno("Confirmar", "Excluir plano?", parent=self):
            db.remover_plano(plano_id)
            self.listar_planos()
            messagebox.showinfo("Sucesso", "Plano excluído", parent=self)

    def excluir_aluno(self) -> None:
        if messagebox.askyesno("Confirmar", "Excluir aluno?", parent=self):
            db.remover_aluno(self.aluno_id)
            self.atualizar_lista()
            self.voltar()
            messagebox.showinfo("Sucesso", "Aluno excluído", parent=self)


def criar_interface() -> None:
    """Cria e exibe a interface principal."""
    db.init_db()
    theme = load_theme()
    app = tb.Window(themename=theme)
    app.title("Gestor de Alunos")

    def toggle_theme() -> None:
        new_theme = "superhero" if theme_var.get() else "flatly"
        app.style.theme_use(new_theme)
        save_theme(new_theme)

    header = ttk.Frame(app, padding=10)
    header.pack(fill="x")
    ttk.Label(header, text="Gestor de Alunos", font=("Segoe UI", 14, "bold")).pack(side="left")
    theme_var = tk.BooleanVar(value=theme == "superhero")
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
    canvas.create_window((0, 0), window=cards, anchor="nw")

    detail_container = ttk.Frame(main)
    detail_container.pack(fill="both", expand=True)
    detail_container.pack_forget()

    def on_configure(event=None) -> None:
        canvas.configure(scrollregion=canvas.bbox("all"))

    cards.bind("<Configure>", on_configure)

    def show_list() -> None:
        for child in detail_container.winfo_children():
            child.destroy()
        detail_container.pack_forget()
        list_frame.pack(fill="both", expand=True)
        atualizar_cards()

    def show_detail(aluno_id: int) -> None:
        list_frame.pack_forget()
        for child in detail_container.winfo_children():
            child.destroy()
        dados = db.obter_aluno(aluno_id)
        DetalhesFrame(detail_container, dados, show_list, atualizar_cards).pack(fill="both", expand=True)
        detail_container.pack(fill="both", expand=True)

    def atualizar_cards() -> None:
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
