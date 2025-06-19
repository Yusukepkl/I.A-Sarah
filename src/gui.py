import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tb

import db
from pdf_utils import gerar_pdf, sanitize_filename


def atualizar_lista(lb):
    lb.delete(0, tk.END)
    for aluno in db.listar_alunos():
        progresso = aluno[2] if aluno[2] else "0"
        lb.insert(tk.END, f"{aluno[0]} - {aluno[1]} ({progresso}%)")

def abrir_detalhes(lb):
    selecionado = lb.curselection()
    if not selecionado:
        return
    item = lb.get(selecionado[0])
    aluno_id = int(item.split(" - ")[0])
    dados = db.obter_aluno(aluno_id)
    DetalhesWindow(aluno_id, dados)


def atualizar_card(lb, widgets):
    selecionado = lb.curselection()
    if not selecionado:
        widgets["nome"].config(text="")
        widgets["progresso"].config(text="")
        return
    item = lb.get(selecionado[0])
    aluno_id = int(item.split(" - ")[0])
    dados = db.obter_aluno(aluno_id)
    widgets["nome"].config(text=dados[1])
    progresso = dados[4] if dados[4] else "0"
    widgets["progresso"].config(text=f"Progresso: {progresso}%")

class DetalhesWindow(tk.Toplevel):
    def __init__(self, aluno_id, dados):
        super().__init__()
        self.title(f"Detalhes do Aluno {dados[1]}")
        self.aluno_id = aluno_id
        self.nome = dados[1]
        self.configure(padx=20, pady=20)
        self.campos = {}

        labels = ["Plano", "Pagamento", "Dieta", "Treino"]
        for offset, campo in enumerate(labels, start=2):
            ttk.Label(self, text=campo, font=("Segoe UI", 10, "bold")).grid(
                row=offset if campo != "Dieta" and campo != "Treino" else offset + 1,
                column=0,
                sticky="w",
                pady=2,
            )
            texto = tk.Text(self, width=45, height=3, font=("Segoe UI", 10))
            texto.grid(row=offset if campo != "Dieta" and campo != "Treino" else offset + 1, column=1, pady=2)
            idx = {
                "Plano": 2,
                "Pagamento": 3,
                "Dieta": 5,
                "Treino": 6,
            }[campo]
            valor = dados[idx] if dados[idx] else ""
            texto.insert("1.0", valor)
            self.campos[campo.lower()] = texto

        # seção de progresso com barra
        ttk.Label(self, text="Progresso", font=("Segoe UI", 10, "bold")).grid(
            row=4, column=0, sticky="w", pady=2
        )
        prog_frame = ttk.Frame(self)
        prog_frame.grid(row=4, column=1, pady=2, sticky="ew")
        prog_frame.columnconfigure(0, weight=1)
        self.progresso_var = tk.IntVar(
            value=int(dados[4]) if dados[4] and str(dados[4]).isdigit() else 0
        )
        ttk.Progressbar(
            prog_frame,
            maximum=100,
            variable=self.progresso_var,
            length=200,
        ).grid(row=0, column=0, sticky="ew")
        ttk.Spinbox(
            prog_frame, from_=0, to=100, textvariable=self.progresso_var, width=5
        ).grid(row=0, column=1, padx=5)
        self.campos["progresso"] = self.progresso_var

        botoes = ttk.Frame(self)
        botoes.grid(row=7, column=0, columnspan=2, pady=10)
        ttk.Button(botoes, text="Salvar", command=self.salvar).pack(side="left", padx=5)
        ttk.Button(botoes, text="Treino PDF", command=self.gerar_treino_pdf).pack(side="left", padx=5)
        ttk.Button(botoes, text="Dieta PDF", command=self.gerar_dieta_pdf).pack(side="left", padx=5)

    def salvar(self):
        for campo, widget in self.campos.items():
            if isinstance(widget, tk.IntVar):
                valor = str(widget.get())
            else:
                valor = widget.get('1.0', tk.END).strip()
            db.atualizar_aluno(self.aluno_id, campo, valor)
        messagebox.showinfo("Salvo", "Dados atualizados")

    def gerar_treino_pdf(self):
        treino = self.campos['treino'].get('1.0', tk.END).strip()
        nome_file = sanitize_filename(self.nome)
        caminho = f"treino_{nome_file}.pdf"
        gerar_pdf(f"Treino de {self.nome}", treino, caminho)
        messagebox.showinfo("PDF", f"Treino exportado como {caminho}")

    def gerar_dieta_pdf(self):
        dieta = self.campos['dieta'].get('1.0', tk.END).strip()
        nome_file = sanitize_filename(self.nome)
        caminho = f"dieta_{nome_file}.pdf"
        gerar_pdf(f"Dieta de {self.nome}", dieta, caminho)
        messagebox.showinfo("PDF", f"Dieta exportada como {caminho}")


def adicionar_aluno(lb, entrada):
    nome = entrada.get().strip()
    if nome:
        db.adicionar_aluno(nome)
        atualizar_lista(lb)
        entrada.delete(0, tk.END)
    else:
        messagebox.showwarning("Aviso", "Nome não pode ser vazio")


def remover_aluno(lb):
    selecionado = lb.curselection()
    if not selecionado:
        return
    item = lb.get(selecionado[0])
    aluno_id = int(item.split(" - ")[0])
    if messagebox.askyesno("Confirmar", "Deseja remover o aluno?"):
        db.remover_aluno(aluno_id)
        atualizar_lista(lb)


def criar_interface():
    db.init_db()

    # tema inspirado em aplicativos modernos de treino
    app = tb.Window(themename="superhero")
    app.title("Gestor de Alunos - Personal Trainer")

    style = app.style
    style.configure("TLabel", font=("Segoe UI", 10))
    style.configure("TButton", font=("Segoe UI", 10, "bold"))
    style.configure("TEntry", font=("Segoe UI", 10))

    frame = ttk.Frame(app, padding=20)
    frame.pack(fill="both", expand=True)
    frame.columnconfigure(0, weight=1)

    # painel com lista de alunos
    lista_frame = ttk.Frame(frame)
    lista_frame.grid(row=0, column=0, sticky="nswe")
    ttk.Label(lista_frame, text="Alunos", font=("Segoe UI", 12, "bold")).pack(pady=(0, 5))

    lb = tk.Listbox(lista_frame, width=40, height=15, font=("Segoe UI", 10))
    lb.pack(side="left", fill="y")
    scroll = ttk.Scrollbar(lista_frame, orient="vertical", command=lb.yview)
    scroll.pack(side="left", fill="y")
    lb.config(yscrollcommand=scroll.set)

    entrada = ttk.Entry(lista_frame)
    entrada.pack(pady=(10, 2), fill="x")
    ttk.Button(lista_frame, text="Adicionar", command=lambda: adicionar_aluno(lb, entrada)).pack(fill="x")
    ttk.Button(lista_frame, text="Remover", command=lambda: remover_aluno(lb)).pack(pady=2, fill="x")
    ttk.Button(lista_frame, text="Detalhes", command=lambda: abrir_detalhes(lb)).pack(fill="x")

    # abrir detalhes ao dar duplo clique
    lb.bind("<Double-Button-1>", lambda e: abrir_detalhes(lb))
    atualizar_lista(lb)

    app.mainloop()
if __name__ == "__main__":
    criar_interface()
