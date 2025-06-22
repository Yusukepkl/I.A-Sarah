"""Interface de linha de comando para gerenciamento de alunos."""

from __future__ import annotations

import typer

from ia_sarah.core.use_cases import controllers

app = typer.Typer(help="Gerenciar alunos sem a interface grafica")


@app.command()
def listar() -> None:
    """Listar alunos cadastrados."""
    alunos = controllers.listar_alunos()
    for a in alunos:
        typer.echo(f"{a.id}\t{a.nome}\t{a.email}")


@app.command()
def adicionar(nome: str, email: str) -> None:
    """Adicionar um novo aluno."""
    aluno_id = controllers.adicionar_aluno(nome, email)
    typer.echo(f"Aluno criado com id {aluno_id}")


@app.command()
def remover(aluno_id: int) -> None:
    """Remover um aluno pelo id."""
    controllers.remover_aluno(aluno_id)
    typer.echo("Aluno removido")


def main() -> None:
    """Ponto de entrada do CLI."""
    controllers.init_app()
    app()


if __name__ == "__main__":
    main()
