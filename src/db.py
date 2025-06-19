import sqlite3
from contextlib import closing

DB_NAME = 'alunos.db'

def init_db():
    with closing(sqlite3.connect(DB_NAME)) as conn:
        with conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS alunos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                plano TEXT,
                pagamento TEXT,
                progresso TEXT,
                dieta TEXT,
                treino TEXT
            )
            """)

def listar_alunos():
    with closing(sqlite3.connect(DB_NAME)) as conn:
        cur = conn.execute("SELECT id, nome FROM alunos ORDER BY nome")
        return cur.fetchall()

def obter_aluno(aluno_id: int):
    with closing(sqlite3.connect(DB_NAME)) as conn:
        cur = conn.execute(
            "SELECT id, nome, plano, pagamento, progresso, dieta, treino FROM alunos WHERE id=?",
            (aluno_id,)
        )
        return cur.fetchone()

def adicionar_aluno(nome: str):
    with closing(sqlite3.connect(DB_NAME)) as conn:
        with conn:
            cur = conn.execute("INSERT INTO alunos (nome) VALUES (?)", (nome,))
            return cur.lastrowid

def atualizar_aluno(aluno_id: int, campo: str, valor: str):
    with closing(sqlite3.connect(DB_NAME)) as conn:
        with conn:
            conn.execute(f"UPDATE alunos SET {campo}=? WHERE id=?", (valor, aluno_id))

def remover_aluno(aluno_id: int):
    with closing(sqlite3.connect(DB_NAME)) as conn:
        with conn:
            conn.execute("DELETE FROM alunos WHERE id=?", (aluno_id,))
