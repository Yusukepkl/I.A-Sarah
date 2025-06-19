# Gestor de Alunos para Personal Trainer

Aplicação simples para gerenciamento de alunos em academias ou atendimentos particulares.
Permite registrar alunos, controlar planos, pagamentos, progresso, dietas e treinos, além de exportar
informações em PDF. A interface foi renovada e utiliza `tkinter` com `ttkbootstrap` no tema `superhero`.
Os detalhes do aluno aparecem em um painel lateral integrado, e os PDFs
gerados recebem o nome do aluno e o tipo (treino ou dieta).

## Requisitos
- Python 3.13 para Windows
- Dependências listadas em `requirements.txt`

## Como usar
1. Instale o Python 3.13 em seu computador.
2. Instale as dependências com `pip install -r requirements.txt`.
3. Execute `python src/main.py` para abrir o sistema.

Todo o banco de dados fica salvo localmente em `alunos.db`.
