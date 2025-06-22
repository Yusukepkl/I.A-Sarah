"""Componentes visuais reutilizáveis para a aplicação."""

import json
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable, Optional

import ttkbootstrap as tb


def _fade_in(win: tk.Toplevel, step: float = 0.1) -> None:
    """Increase window opacity until fully visible."""
    alpha = win.attributes("-alpha") or 0
    alpha += step
    if alpha >= 1:
        win.attributes("-alpha", 1.0)
    else:
        win.attributes("-alpha", alpha)
        win.after(20, _fade_in, win, step)


def _fade_out_destroy(win: tk.Toplevel, step: float = 0.1) -> None:
    """Fade out the window and destroy it."""
    alpha = win.attributes("-alpha") or 1
    alpha -= step
    if alpha <= 0:
        win.destroy()
    else:
        win.attributes("-alpha", alpha)
        win.after(20, _fade_out_destroy, win, step)


class ExercicioRow(ttk.Frame):
    """Linha de entrada para um exercício do plano."""

    def __init__(
        self,
        master: tk.Widget,
        remover: Callable[["ExercicioRow"], None],
        dados: Optional[dict] = None,
    ) -> None:
        super().__init__(master)
        self.ex_id: Optional[int] = None
        self.vars = {
            "nome": tk.StringVar(),
            "series": tk.StringVar(),
            "reps": tk.StringVar(),
            "peso": tk.StringVar(),
            "descanso": tk.StringVar(),
            "obs": tk.StringVar(),
        }
        if dados:
            self.ex_id = dados.get("id")
            for k in self.vars:
                self.vars[k].set(dados.get(k, ""))
        ttk.Entry(self, textvariable=self.vars["nome"], width=15).grid(
            row=0, column=0, padx=2, pady=2
        )
        ttk.Entry(self, textvariable=self.vars["series"], width=5).grid(
            row=0, column=1, padx=2
        )
        ttk.Entry(self, textvariable=self.vars["reps"], width=5).grid(
            row=0, column=2, padx=2
        )
        ttk.Entry(self, textvariable=self.vars["peso"], width=7).grid(
            row=0, column=3, padx=2
        )
        ttk.Entry(self, textvariable=self.vars["descanso"], width=8).grid(
            row=0, column=4, padx=2
        )
        ttk.Entry(self, textvariable=self.vars["obs"], width=15).grid(
            row=0, column=5, padx=2
        )
        ttk.Button(self, text="X", width=2, command=lambda: remover(self)).grid(
            row=0, column=6, padx=2
        )

    def get_data(self) -> dict:
        """Retorna os dados preenchidos."""
        data = {k: v.get().strip() for k, v in self.vars.items()}
        if self.ex_id is not None:
            data["id"] = self.ex_id
        return data


class PlanoModal(tb.Toplevel):
    """Janela para criação ou edição de planos de treino."""

    def __init__(
        self,
        aluno_id: int,
        salvar: Callable[[int, str, str, str, Optional[int]], None],
        plano: Optional[dict] = None,
    ) -> None:
        super().__init__()
        self.geometry("650x450")
        self.attributes("-alpha", 0.0)
        _fade_in(self)
        self.protocol("WM_DELETE_WINDOW", lambda: _fade_out_destroy(self))
        self.grab_set()
        self.aluno_id = aluno_id
        self.salvar = salvar
        self.exercicios: list[ExercicioRow] = []
        self.plano_id: Optional[int] = None

        nome_var = tk.StringVar()
        self.title(
            "Novo Plano de Treino" if plano is None else "Editar Plano de Treino"
        )
        ttk.Label(self, text="Nome do Plano:").pack(anchor="w", padx=5, pady=5)
        ttk.Entry(self, textvariable=nome_var, width=40).pack(anchor="w", padx=5)

        ttk.Label(self, text="Descrição (opcional):").pack(
            anchor="w", padx=5, pady=(10, 0)
        )
        desc = tk.Text(self, height=3, width=50)
        desc.pack(anchor="w", padx=5)

        area = ttk.Frame(self)
        area.pack(fill="both", expand=True, pady=10)

        header = ttk.Frame(area)
        header.pack(fill="x")
        cols = ["Exercício", "Séries", "Reps", "Peso", "Descanso", "Obs"]
        for i, t in enumerate(cols):
            ttk.Label(header, text=t, font=("Segoe UI", 9, "bold")).grid(
                row=0, column=i, padx=2
            )

        def remover_row(row: ExercicioRow) -> None:
            row.destroy()
            self.exercicios.remove(row)

        def add_row(dados: Optional[dict] = None) -> None:
            row = ExercicioRow(area, remover_row, dados)
            row.pack(fill="x", pady=2, padx=5)
            self.exercicios.append(row)

        ttk.Button(self, text="Adicionar Exercício", command=lambda: add_row()).pack(
            pady=5
        )

        if plano:
            self.plano_id = plano.get("id")
            nome_var.set(plano.get("nome", ""))
            desc.insert("1.0", plano.get("descricao", "") or "")
            try:
                exs = json.loads(plano.get("exercicios") or "[]")
            except json.JSONDecodeError:
                exs = []
            if exs:
                for ex in exs:
                    add_row(ex)
            else:
                add_row()
        else:
            add_row()

        def salvar_click() -> None:
            nome = nome_var.get().strip()
            if not nome:
                messagebox.showwarning(
                    "Aviso", "Nome do plano obrigatório", parent=self
                )
                return
            descricao = desc.get("1.0", tk.END).strip()
            dados = [r.get_data() for r in self.exercicios if r.get_data().get("nome")]
            exercicios_json = json.dumps(dados, ensure_ascii=False)
            self.salvar(self.aluno_id, nome, descricao, exercicios_json, self.plano_id)
            _fade_out_destroy(self)

        ttk.Button(self, text="Salvar", command=salvar_click).pack(pady=5)
