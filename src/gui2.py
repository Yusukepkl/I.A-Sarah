import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tb

import db


class ExercicioRow(ttk.Frame):
    def __init__(self, master, remover):
        super().__init__(master)
        self.vars = {
            'nome': tk.StringVar(),
            'series': tk.StringVar(),
            'reps': tk.StringVar(),
            'descanso': tk.StringVar(),
            'obs': tk.StringVar(),
        }
        ttk.Entry(self, textvariable=self.vars['nome'], width=15).grid(row=0, column=0, padx=2, pady=2)
        ttk.Entry(self, textvariable=self.vars['series'], width=5).grid(row=0, column=1, padx=2)
        ttk.Entry(self, textvariable=self.vars['reps'], width=5).grid(row=0, column=2, padx=2)
        ttk.Entry(self, textvariable=self.vars['descanso'], width=8).grid(row=0, column=3, padx=2)
        ttk.Entry(self, textvariable=self.vars['obs'], width=15).grid(row=0, column=4, padx=2)
        ttk.Button(self, text="X", width=2, command=lambda: remover(self)).grid(row=0, column=5, padx=2)

    def get_data(self):
        return {k: v.get().strip() for k, v in self.vars.items()}


class PlanoModal(tb.Toplevel):
    def __init__(self, aluno_id, ao_salvar):
        super().__init__()
        self.title("Novo Plano de Treino")
        self.geometry("600x400")
        self.grab_set()
        self.aluno_id = aluno_id
        self.ao_salvar = ao_salvar
        self.exercicios = []

        nome_var = tk.StringVar()
        ttk.Label(self, text="Nome do Plano:").pack(anchor="w", padx=5, pady=5)
        ttk.Entry(self, textvariable=nome_var, width=40).pack(anchor="w", padx=5)

        ttk.Label(self, text="Descrição (opcional):").pack(anchor="w", padx=5, pady=(10,0))
        desc = tk.Text(self, height=3, width=50)
        desc.pack(anchor="w", padx=5)

        area = ttk.Frame(self)
        area.pack(fill="both", expand=True, pady=10)

        def remover_row(row):
            row.destroy()
            self.exercicios.remove(row)

        def add_row():
            row = ExercicioRow(area, remover_row)
            row.pack(fill="x", pady=2, padx=5)
            self.exercicios.append(row)

        ttk.Button(self, text="Adicionar Exercício", command=add_row).pack(pady=5)
        add_row()

        def salvar():
            nome = nome_var.get().strip()
            if not nome:
                messagebox.showwarning("Aviso", "Nome do plano obrigatório", parent=self)
                return
            descricao = desc.get("1.0", tk.END).strip()
            dados = [r.get_data() for r in self.exercicios if r.get_data().get('nome')]
            exercicios_json = json.dumps(dados, ensure_ascii=False)
            db.adicionar_plano(self.aluno_id, nome, descricao, exercicios_json)
            self.destroy()
            self.ao_salvar()

        ttk.Button(self, text="Salvar", command=salvar).pack(pady=5)

CONFIG_FILE = "config.json"

def load_theme():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("theme", "superhero")
        except Exception:
            pass
    return "superhero"

def save_theme(theme: str):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump({"theme": theme}, f)

def abrir_modal_adicionar(atualizar):
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

class DetalhesWindow(tb.Toplevel):
    def __init__(self, dados, atualizar_lista):
        super().__init__()
        self.title("Detalhes do Aluno")
        self.aluno_id = dados[0]
        self.atualizar_lista = atualizar_lista
        self.configure(padx=20, pady=20)

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

        ttk.Button(self, text="Fechar", command=self.destroy).pack(pady=5)

    def listar_planos(self):
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
                if ex.get('descanso'):
                    info += f" descanso {ex.get('descanso')}"
                if ex.get('obs'):
                    info += f" ({ex.get('obs')})"
                ttk.Label(card, text=info).pack(anchor="w")
            btns = ttk.Frame(card)
            btns.pack(anchor="e", pady=(5,0))
            ttk.Button(btns, text="Excluir", command=lambda i=pid: self.excluir_plano(i)).pack(side="right")

    def abrir_plano_modal(self):
        PlanoModal(self.aluno_id, self.listar_planos)

    def excluir_plano(self, plano_id):
        if messagebox.askyesno("Confirmar", "Excluir plano?", parent=self):
            db.remover_plano(plano_id)
            self.listar_planos()

    def excluir_aluno(self):
        if messagebox.askyesno("Confirmar", "Excluir aluno?", parent=self):
            db.remover_aluno(self.aluno_id)
            self.atualizar_lista()
            self.destroy()

def criar_interface():
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

    canvas = tk.Canvas(main)
    scroll = ttk.Scrollbar(main, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scroll.set)
    scroll.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    cards = ttk.Frame(canvas)
    canvas.create_window((0,0), window=cards, anchor="nw")

    def on_configure(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))
    cards.bind("<Configure>", on_configure)

    def abrir_detalhes(aluno_id):
        dados = db.obter_aluno(aluno_id)
        DetalhesWindow(dados, atualizar_cards)

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
            card.bind("<Button-1>", lambda e, i=aid: abrir_detalhes(i))
            for w in card.winfo_children():
                w.bind("<Button-1>", lambda e, i=aid: abrir_detalhes(i))

    botoes = ttk.Frame(app, padding=10)
    botoes.pack(fill="x")
    ttk.Button(botoes, text="Adicionar Aluno", command=lambda: abrir_modal_adicionar(atualizar_cards)).pack()

    atualizar_cards()
    app.mainloop()

if __name__ == "__main__":
    criar_interface()
