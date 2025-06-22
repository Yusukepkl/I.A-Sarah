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
async def startup() -> None:
    controllers.init_app()


@app.get("/students")
async def list_students():
    alunos = controllers.listar_alunos()
    return [
        {
            "id": a.id,
            "nome": a.nome,
            "email": a.email,
            "data_inicio": a.data_inicio,
        }
        for a in alunos
    ]


@app.get("/students/{aluno_id}")
async def get_student(aluno_id: int):
    aluno = controllers.obter_aluno(aluno_id)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno not found")
    return {
        "id": aluno.id,
        "nome": aluno.nome,
        "email": aluno.email,
        "data_inicio": aluno.data_inicio,
    }


@app.post("/students", status_code=201)
async def create_student(student: StudentIn):
    aluno_id = controllers.adicionar_aluno(student.nome, student.email)
    return {"id": aluno_id}


@app.put("/students/{aluno_id}", status_code=204)
async def update_student(aluno_id: int, student: StudentIn):
    """Update an existing student."""
    if controllers.obter_aluno(aluno_id) is None:
        raise HTTPException(status_code=404, detail="Aluno not found")
    controllers.atualizar_aluno(aluno_id, "nome", student.nome)
    controllers.atualizar_aluno(aluno_id, "email", student.email)


@app.delete("/students/{aluno_id}", status_code=204)
async def delete_student(aluno_id: int):
    if controllers.obter_aluno(aluno_id) is None:
        raise HTTPException(status_code=404, detail="Aluno not found")
    controllers.remover_aluno(aluno_id)


@app.get("/theme")
async def get_theme():
    """Return saved theme."""
    return {"theme": controllers.load_theme()}


@app.post("/theme", status_code=204)
async def set_theme(data: ThemeIn):
    """Persist theme selection."""
    controllers.save_theme(data.theme)


@app.get("/config")
async def get_config() -> Dict[str, Any]:
    """Return application configuration."""
    return controllers.load_config()


@app.post("/config", status_code=204)
async def update_config(config: Dict[str, Any]):
    """Update and persist configuration values."""
    controllers.update_config(config)


@app.get("/stats")
async def get_stats(limit: int = 5):
    """Return basic application statistics."""
    return controllers.obter_estatisticas(limit)


def main() -> None:
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)


if __name__ == "__main__":
    main()
