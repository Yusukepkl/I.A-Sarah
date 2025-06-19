# Gestor de Alunos para Personal Trainer

Aplicação simples para gerenciamento de alunos em academias ou atendimentos particulares.
Permite registrar alunos, controlar planos, pagamentos, progresso, dietas e treinos, além de exportar
informações em PDF. A interface usa `tkinter` com `ttkbootstrap` e agora conta com alternância de tema
(claro ou escuro) e exibe os alunos em cartões. Os detalhes de cada aluno abrem em uma janela e os PDFs
gerados recebem o nome do aluno e o tipo (treino ou dieta).

## Requisitos
- Python 3.11 ou superior
- Dependências listadas em `requirements.txt`

## Como usar
1. Instale o Python 3.11 ou superior em seu computador.
2. (Opcional) Crie um ambiente virtual com `python -m venv venv` e ative-o.
3. Instale as dependências com `pip install -r requirements.txt`.
4. Execute `python src/main.py` para abrir o sistema.

Todo o banco de dados fica salvo localmente em `alunos.db`.
