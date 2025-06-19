import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tb

import db

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
    def __init__(self, dados):
        super().__init__()
        self.title("Detalhes do Aluno")
        self.configure(padx=20, pady=20)
        ttk.Label(self, text=dados[1], font=("Segoe UI", 12, "bold")).pack(anchor="w")
        ttk.Label(self, text=dados[2] or "-").pack(anchor="w")
        ttk.Label(self, text=f"Inicio: {dados[3]}").pack(anchor="w", pady=(0,10))
        ttk.Button(self, text="Fechar", command=self.destroy).pack()

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
    tb.Switch(header, text="Modo Escuro", variable=theme_var, command=toggle_theme).pack(side="right")

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
        DetalhesWindow(dados)

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
