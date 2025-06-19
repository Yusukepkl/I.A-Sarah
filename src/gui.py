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
        labels = ["Plano", "Pagamento", "Progresso", "Dieta", "Treino"]
        self.campos = {}
        for i, campo in enumerate(labels, start=2):
            ttk.Label(self, text=campo).grid(row=i, column=0, sticky='w', pady=2)
            texto = tk.Text(self, width=40, height=3)
            texto.grid(row=i, column=1, pady=2)
            valor = dados[i] if dados[i] else ""
            texto.insert('1.0', valor)
            self.campos[campo.lower()] = texto

        ttk.Button(self, text="Salvar", command=self.salvar).grid(row=7, column=0, pady=5)
        ttk.Button(self, text="Treino PDF", command=self.gerar_treino_pdf).grid(row=7, column=1, pady=5)
        ttk.Button(self, text="Dieta PDF", command=self.gerar_dieta_pdf).grid(row=8, column=1, pady=5)

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
    app = tb.Window(themename="darkly")
    app.title("Gestor de Alunos - Personal Trainer")

    frame = ttk.Frame(app, padding=10)
    frame.pack(fill='both', expand=True)

    lb = tk.Listbox(frame, width=40, height=10)
    lb.grid(row=0, column=0, columnspan=2, pady=5)

    entrada = ttk.Entry(frame, width=30)
    entrada.grid(row=1, column=0, pady=5)
    ttk.Button(frame, text="Adicionar", command=lambda: adicionar_aluno(lb, entrada)).grid(row=1, column=1)

    ttk.Button(frame, text="Detalhes", command=lambda: abrir_detalhes(lb)).grid(row=2, column=0, pady=5)
    ttk.Button(frame, text="Remover", command=lambda: remover_aluno(lb)).grid(row=2, column=1, pady=5)

    atualizar_lista(lb)

    app.mainloop()

if __name__ == "__main__":
    criar_interface()
