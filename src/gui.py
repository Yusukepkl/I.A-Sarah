import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tb

import db
from pdf_utils import gerar_pdf


def atualizar_lista(lb):
    lb.delete(0, tk.END)
    for aluno in db.listar_alunos():
        lb.insert(tk.END, f"{aluno[0]} - {aluno[1]}")

def abrir_detalhes(lb):
    selecionado = lb.curselection()
    if not selecionado:
        return
    item = lb.get(selecionado[0])
    aluno_id = int(item.split(" - ")[0])
    dados = db.obter_aluno(aluno_id)
    DetalhesWindow(aluno_id, dados)

class DetalhesWindow(tk.Toplevel):
    def __init__(self, aluno_id, dados):
        super().__init__()
        self.title(f"Detalhes do Aluno {dados[1]}")
        self.aluno_id = aluno_id
        self.configure(padx=20, pady=20)
        labels = ["Plano", "Pagamento", "Progresso", "Dieta", "Treino"]
        self.campos = {}
        for i, campo in enumerate(labels, start=2):
            ttk.Label(self, text=campo, font=("Segoe UI", 10, "bold")).grid(row=i, column=0, sticky="w", pady=2)
            texto = tk.Text(self, width=45, height=3, font=("Segoe UI", 10))
            texto.grid(row=i, column=1, pady=2)
            valor = dados[i] if dados[i] else ""
            texto.insert("1.0", valor)
            self.campos[campo.lower()] = texto

        botoes = ttk.Frame(self)
        botoes.grid(row=7, column=0, columnspan=2, pady=10)
        ttk.Button(botoes, text="Salvar", command=self.salvar).pack(side="left", padx=5)
        ttk.Button(botoes, text="Treino PDF", command=self.gerar_treino_pdf).pack(side="left", padx=5)
        ttk.Button(botoes, text="Dieta PDF", command=self.gerar_dieta_pdf).pack(side="left", padx=5)

    def salvar(self):
        for campo, widget in self.campos.items():
            valor = widget.get('1.0', tk.END).strip()
            db.atualizar_aluno(self.aluno_id, campo, valor)
        messagebox.showinfo("Salvo", "Dados atualizados")

    def gerar_treino_pdf(self):
        treino = self.campos['treino'].get('1.0', tk.END)
        gerar_pdf("Treino", treino, f"treino_{self.aluno_id}.pdf")
        messagebox.showinfo("PDF", "Treino exportado")

    def gerar_dieta_pdf(self):
        dieta = self.campos['dieta'].get('1.0', tk.END)
        gerar_pdf("Dieta", dieta, f"dieta_{self.aluno_id}.pdf")
        messagebox.showinfo("PDF", "Dieta exportada")


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
    # tema mais claro e moderno para uma aparência revitalizada
    app = tb.Window(themename="minty")
    app.title("Gestor de Alunos - Personal Trainer")

    # aplicação de fontes padronizadas para todos os widgets
    style = app.style
    style.configure("TLabel", font=("Segoe UI", 10))
    style.configure("TButton", font=("Segoe UI", 10, "bold"))
    style.configure("TEntry", font=("Segoe UI", 10))

    frame = ttk.Frame(app, padding=20)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="Alunos Cadastrados", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 5))

    lb = tk.Listbox(frame, width=40, height=10, font=("Segoe UI", 10))
    lb.grid(row=1, column=0, columnspan=2, pady=5)

    entrada = ttk.Entry(frame, width=30)
    entrada.grid(row=2, column=0, pady=5, sticky="ew")
    ttk.Button(frame, text="Adicionar", command=lambda: adicionar_aluno(lb, entrada)).grid(row=2, column=1, padx=5)

    botoes = ttk.Frame(frame)
    botoes.grid(row=3, column=0, columnspan=2, pady=10)
    ttk.Button(botoes, text="Detalhes", command=lambda: abrir_detalhes(lb)).pack(side="left", padx=5)
    ttk.Button(botoes, text="Remover", command=lambda: remover_aluno(lb)).pack(side="left", padx=5)

    frame.columnconfigure(0, weight=1)
    atualizar_lista(lb)

    app.mainloop()

if __name__ == "__main__":
    criar_interface()
