"""Interface principal da aplicação."""

from __future__ import annotations

import json
import tkinter as tk
from tkinter import PhotoImage, messagebox, ttk

import ttkbootstrap as tb
from ttkbootstrap.icons import Icon

import controllers
from controllers import (adicionar_aluno, atualizar_plano, gerar_treino_pdf,
                         listar_alunos, listar_planos, load_theme, obter_aluno,
                         remover_aluno, remover_plano, sanitize_filename,
                         save_theme)
from utils.background import run_task

from .widgets import PlanoModal

DEFAULT_PAD = 10


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


def _add_hover_animation(frame: ttk.Frame, hover_color: str = "#f0f0f0") -> None:
    """Add simple hover animation on the given frame.

    Some themed ``ttk`` widgets (like ``ttkbootstrap.Frame``) do not support the
    ``background`` option. In that case the animation falls back to simply
    changing the relief without colour fading.
    """

    try:
        normal = frame.cget("background")
    except tk.TclError:
        normal = None
    job = {"id": None}

    def fade(start: str, end: str, i: int = 0, steps: int = 5) -> None:
        if start is None or end is None:
            return
        r1, g1, b1 = frame.winfo_rgb(start)
        r2, g2, b2 = frame.winfo_rgb(end)
        r = int(r1 + (r2 - r1) * i / steps)
        g = int(g1 + (g2 - g1) * i / steps)
        b = int(b1 + (b2 - b1) * i / steps)
        try:
            frame.configure(background=f"#{r>>8:02x}{g>>8:02x}{b>>8:02x}")
        except tk.TclError:
            return
        if i < steps:
            job["id"] = frame.after(20, fade, start, end, i + 1, steps)
        else:
            job["id"] = None

    def on_enter(_event) -> None:
        if job["id"]:
            frame.after_cancel(job["id"])
        frame.configure(relief="raised")
        try:
            current = frame.cget("background")
        except tk.TclError:
            current = None
        fade(current, hover_color)

    def on_leave(_event) -> None:
        if job["id"]:
            frame.after_cancel(job["id"])
        frame.configure(relief="solid")
        try:
            current = frame.cget("background")
        except tk.TclError:
            current = None
        fade(current, normal)

    for w in [frame] + list(frame.winfo_children()):
        w.bind("<Enter>", on_enter)
        w.bind("<Leave>", on_leave)


def abrir_modal_adicionar(atualizar: callable) -> None:
    """Mostra janela para adicionar um aluno."""
    win = tb.Toplevel()
    win.title("Adicionar Aluno")
    win.attributes("-alpha", 0.0)
    _fade_in(win)
    win.protocol("WM_DELETE_WINDOW", lambda: _fade_out_destroy(win))
    win.grab_set()
    win.grid_columnconfigure(1, weight=1)

    nome_var = tk.StringVar()
    email_var = tk.StringVar()

    ttk.Label(win, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    ttk.Entry(win, textvariable=nome_var, width=30).grid(
        row=0, column=1, padx=5, pady=5, sticky="ew"
    )
    ttk.Label(win, text="Email:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    ttk.Entry(win, textvariable=email_var, width=30).grid(
        row=1, column=1, padx=5, pady=5, sticky="ew"
    )

    def salvar() -> None:
        nome = nome_var.get().strip()
        email = email_var.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "Nome não pode ser vazio", parent=win)
            return
        pb = ttk.Progressbar(win, mode="indeterminate")
        pb.grid(row=3, column=0, columnspan=2, pady=5, sticky="ew")
        pb.start()
        win.update_idletasks()

        def on_success(_res: object | None = None) -> None:
            pb.stop()
            pb.destroy()
            messagebox.showinfo("Sucesso", "Aluno adicionado com sucesso!", parent=win)
            _fade_out_destroy(win)
            atualizar()

        def on_error(err: Exception) -> None:  # pragma: no cover - gui feedback
            pb.stop()
            pb.destroy()
            messagebox.showerror(
                "Erro", f"Falha ao adicionar aluno:\n{err}", parent=win
            )

        run_task(win, lambda: adicionar_aluno(nome, email), on_success, on_error)

    ttk.Button(win, text="Salvar", command=salvar).grid(
        row=2, column=0, columnspan=2, pady=DEFAULT_PAD
    )


class DetalhesFrame(ttk.Frame):
    """Mostra detalhes e planos de um aluno."""

    def __init__(
        self,
        master: tk.Widget,
        dados: tuple,
        voltar: callable,
        atualizar_lista: callable,
    ) -> None:
        super().__init__(master)
        self.aluno_id = dados[0]
        self.voltar = voltar
        self.atualizar_lista = atualizar_lista
        self.configure(padding=DEFAULT_PAD)

        ttk.Button(self, text="Voltar", command=self.voltar).pack(anchor="w")
        ttk.Label(self, text=dados[1], style="Header.TLabel").pack(anchor="w")
        ttk.Label(self, text=dados[2] or "-").pack(anchor="w")
        ttk.Label(self, text=f"Início: {dados[3]}").pack(
            anchor="w", pady=(0, DEFAULT_PAD)
        )

        botoes = ttk.Frame(self, padding=DEFAULT_PAD)
        botoes.pack(fill="x", pady=DEFAULT_PAD)
        ttk.Button(botoes, text="Excluir Aluno", command=self.excluir_aluno).pack(
            side="right"
        )

        self.planos_frame = ttk.Labelframe(self, text="Planos de Treino")
        self.planos_frame.pack(fill="both", expand=True, pady=DEFAULT_PAD)

        self.listar_planos()
        ttk.Button(
            self.planos_frame, text="Adicionar Plano", command=self.abrir_plano_modal
        ).pack(pady=DEFAULT_PAD)

    def listar_planos(self) -> None:
        for child in self.planos_frame.winfo_children():
            if getattr(child, "is_card", False):
                child.destroy()
        planos = listar_planos(self.aluno_id)
        for pid, nome, descricao, exercicios in planos:
            card = tb.Frame(self.planos_frame, padding=10, bootstyle="card")
            card.is_card = True
            card.pack(fill="x", pady=5)
            ttk.Label(card, text=nome, style="CardTitle.TLabel").pack(anchor="w")
            if descricao:
                ttk.Label(card, text=descricao).pack(anchor="w")
            try:
                exs = json.loads(exercicios) if exercicios else []
            except json.JSONDecodeError:
                exs = []
            for ex in exs:
                info = (
                    f"{ex.get('nome','')} - {ex.get('series','')}x{ex.get('reps','')}"
                )
                if ex.get("peso"):
                    info += f" {ex.get('peso')}"
                if ex.get("descanso"):
                    info += f" descanso {ex.get('descanso')}"
                if ex.get("obs"):
                    info += f" ({ex.get('obs')})"
                ttk.Label(card, text=info).pack(anchor="w")
            btns = ttk.Frame(card, padding=DEFAULT_PAD)
            btns.pack(anchor="e", pady=(5, 0))
            ttk.Button(
                btns,
                text="PDF",
                command=lambda n=nome, e=exercicios: self.gerar_plano_pdf(n, e),
            ).pack(side="right")
            ttk.Button(
                btns,
                text="Editar",
                command=lambda p=(pid, nome, descricao, exercicios): self.editar_plano(
                    p
                ),
            ).pack(side="right")
            ttk.Button(
                btns, text="Excluir", command=lambda i=pid: self.excluir_plano(i)
            ).pack(side="right")

    def abrir_plano_modal(self) -> None:
        PlanoModal(self.aluno_id, self._salvar_plano)

    def editar_plano(self, plano: tuple) -> None:
        p = {
            "id": plano[0],
            "nome": plano[1],
            "descricao": plano[2],
            "exercicios": plano[3],
        }
        PlanoModal(self.aluno_id, self._salvar_plano, plano=p)

    def _salvar_plano(
        self,
        aluno_id: int,
        nome: str,
        descricao: str,
        exercicios_json: str,
        plano_id: int | None,
    ) -> None:
        def do_save() -> None:
            if plano_id:
                atualizar_plano(plano_id, nome, descricao, exercicios_json)
            else:
                adicionar_plano(aluno_id, nome, descricao, exercicios_json)

        def on_success(_res: object | None = None) -> None:
            self.listar_planos()

        def on_error(err: Exception) -> None:  # pragma: no cover - gui feedback
            messagebox.showerror("Erro", f"Falha ao salvar plano:\n{err}", parent=self)

        run_task(self, do_save, on_success, on_error)

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

        def on_success(_res: object | None = None) -> None:
            pb.stop()
            pb.destroy()
            messagebox.showinfo("PDF", f"Treino exportado como {path}", parent=self)

        def on_error(err: Exception) -> None:  # pragma: no cover - gui feedback
            pb.stop()
            pb.destroy()
            messagebox.showerror("Erro", f"Falha ao gerar PDF:\n{err}", parent=self)

        run_task(
            self,
            lambda: gerar_treino_pdf(f"Treino - {nome}", exs, path),
            on_success,
            on_error,
        )

    def excluir_plano(self, plano_id: int) -> None:
        if messagebox.askyesno("Confirmar", "Excluir plano?", parent=self):
            pb = ttk.Progressbar(self, mode="indeterminate")
            pb.pack(fill="x", pady=5)
            pb.start()
            self.update_idletasks()

            def on_success(_res: object | None = None) -> None:
                pb.stop()
                pb.destroy()
                self.listar_planos()
                messagebox.showinfo("Sucesso", "Plano excluído", parent=self)

            def on_error(err: Exception) -> None:  # pragma: no cover - gui feedback
                pb.stop()
                pb.destroy()
                messagebox.showerror(
                    "Erro", f"Falha ao excluir plano:\n{err}", parent=self
                )

            run_task(self, lambda: remover_plano(plano_id), on_success, on_error)

    def excluir_aluno(self) -> None:
        if messagebox.askyesno("Confirmar", "Excluir aluno?", parent=self):
            pb = ttk.Progressbar(self, mode="indeterminate")
            pb.pack(fill="x", pady=5)
            pb.start()
            self.update_idletasks()

            def on_success(_res: object | None = None) -> None:
                pb.stop()
                pb.destroy()
                self.atualizar_lista()
                self.voltar()
                messagebox.showinfo("Sucesso", "Aluno excluído", parent=self)

            def on_error(err: Exception) -> None:  # pragma: no cover - gui feedback
                pb.stop()
                pb.destroy()
                messagebox.showerror(
                    "Erro", f"Falha ao excluir aluno:\n{err}", parent=self
                )

            run_task(self, lambda: remover_aluno(self.aluno_id), on_success, on_error)


def criar_interface() -> None:
    """Cria e exibe a interface principal."""
    init_app()
    theme = load_theme()
    app = tb.Window(themename=theme)
    app.title("Gestor de Alunos")

    person_img = PhotoImage(data=Icon.icon, master=app)

    style = app.style
    style.configure("TLabel", font=("Segoe UI", 10))
    style.configure("TButton", font=("Segoe UI", 10))
    style.configure("Title.TLabel", font=("Segoe UI", 14, "bold"))
    style.configure("Header.TLabel", font=("Segoe UI", 12, "bold"))
    style.configure("CardTitle.TLabel", font=("Segoe UI", 11, "bold"))
    style.configure("Card.TFrame", borderwidth=1, relief="solid")

    def toggle_theme() -> None:
        new_theme = "superhero" if theme_var.get() else "flatly"
        app.style.theme_use(new_theme)
        save_theme(new_theme)

    app.columnconfigure(0, weight=1)
    app.rowconfigure(1, weight=1)

    header = ttk.Frame(app, padding=DEFAULT_PAD)
    header.grid(row=0, column=0, sticky="ew")
    ttk.Label(header, text="Gestor de Alunos", style="Title.TLabel").pack(side="left")
    theme_var = tk.BooleanVar(value=theme == "superhero")
    tb.Checkbutton(
        header,
        text="Modo Escuro",
        variable=theme_var,
        command=toggle_theme,
        bootstyle="round-toggle",
    ).pack(side="right")

    main = ttk.Frame(app, padding=DEFAULT_PAD)
    main.grid(row=1, column=0, sticky="nsew")
    main.columnconfigure(0, weight=1)
    main.rowconfigure(0, weight=1)

    list_frame = ttk.Frame(main, padding=DEFAULT_PAD)
    list_frame.grid(row=0, column=0, sticky="nsew")
    list_frame.columnconfigure(0, weight=1)
    list_frame.rowconfigure(0, weight=1)

    canvas = tk.Canvas(list_frame)
    scroll = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scroll.set)
    scroll.grid(row=0, column=1, sticky="ns")
    canvas.grid(row=0, column=0, sticky="nsew")

    cards = ttk.Frame(canvas, padding=DEFAULT_PAD)
    canvas.create_window((0, 0), window=cards, anchor="nw")

    detail_container = ttk.Frame(main, padding=DEFAULT_PAD)
    detail_container.grid(row=0, column=0, sticky="nsew")
    detail_container.grid_remove()

    def on_configure(event=None) -> None:
        canvas.configure(scrollregion=canvas.bbox("all"))

    cards.bind("<Configure>", on_configure)

    def show_list() -> None:
        for child in detail_container.winfo_children():
            child.destroy()
        detail_container.grid_remove()
        list_frame.grid()
        atualizar_cards()

    def show_detail(aluno_id: int) -> None:
        list_frame.grid_remove()
        for child in detail_container.winfo_children():
            child.destroy()
        dados = obter_aluno(aluno_id)
        DetalhesFrame(detail_container, dados, show_list, atualizar_cards).pack(
            fill="both", expand=True
        )
        detail_container.grid()

    def atualizar_cards() -> None:
        for child in cards.winfo_children():
            child.destroy()
        alunos = listar_alunos()
        if not alunos:
            ttk.Label(cards, text="Nenhum aluno cadastrado").pack(pady=20)
        for aid, nome, email, data_inicio in alunos:
            card = tb.Frame(cards, padding=10, bootstyle="card")
            card.pack(fill="x", pady=5)
            ttk.Label(
                card,
                text=nome,
                image=person_img,
                compound="left",
                style="CardTitle.TLabel",
            ).pack(anchor="w")
            ttk.Label(card, text=email or "-").pack(anchor="w")
            ttk.Label(card, text=f"Desde {data_inicio}").pack(anchor="w")
            card.bind("<Button-1>", lambda e, i=aid: show_detail(i))
            for w in card.winfo_children():
                w.bind("<Button-1>", lambda e, i=aid: show_detail(i))
            _add_hover_animation(card)

    botoes = ttk.Frame(app, padding=DEFAULT_PAD)
    botoes.grid(row=2, column=0, sticky="ew")
    ttk.Button(
        botoes,
        text="Adicionar Aluno",
        command=lambda: abrir_modal_adicionar(atualizar_cards),
    ).pack()

    atualizar_cards()
    app.mainloop()


if __name__ == "__main__":
    criar_interface()
