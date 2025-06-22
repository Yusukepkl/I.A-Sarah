from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Dict

from ia_sarah.core.use_cases import controllers

app = FastAPI(title="I.A-Sarah API")


class StudentIn(BaseModel):
    nome: str
    email: str


class ThemeIn(BaseModel):
    theme: str


@app.on_event("startup")
def startup() -> None:
    controllers.init_app()


@app.get("/students")
def list_students():
    alunos = controllers.listar_alunos()
    return [
        {"id": a[0], "nome": a[1], "email": a[2], "data_inicio": a[3]} for a in alunos
    ]


@app.get("/students/{aluno_id}")
def get_student(aluno_id: int):
    aluno = controllers.obter_aluno(aluno_id)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno not found")
    (
        _id,
        nome,
        email,
        data_inicio,
        plano,
        pagamento,
        progresso,
        dieta,
        treino,
    ) = aluno
    return {
        "id": _id,
        "nome": nome,
        "email": email,
        "data_inicio": data_inicio,
        "plano": plano,
        "pagamento": pagamento,
        "progresso": progresso,
        "dieta": dieta,
        "treino": treino,
    }


@app.post("/students", status_code=201)
def create_student(student: StudentIn):
    aluno_id = controllers.adicionar_aluno(student.nome, student.email)
    return {"id": aluno_id}


@app.delete("/students/{aluno_id}", status_code=204)
def delete_student(aluno_id: int):
    if controllers.obter_aluno(aluno_id) is None:
        raise HTTPException(status_code=404, detail="Aluno not found")
    controllers.remover_aluno(aluno_id)


@app.get("/theme")
def get_theme():
    """Return saved theme."""
    return {"theme": controllers.load_theme()}


@app.post("/theme", status_code=204)
def set_theme(data: ThemeIn):
    """Persist theme selection."""
    controllers.save_theme(data.theme)


@app.get("/config")
def get_config() -> Dict[str, Any]:
    """Return application configuration."""
    return controllers.load_config()


@app.post("/config", status_code=204)
def update_config(config: Dict[str, Any]):
    """Update and persist configuration values."""
    controllers.update_config(config)


def main() -> None:
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)


if __name__ == "__main__":
    main()
