# Gestor de Alunos para Personal Trainer

Aplicação simples para gerenciamento de alunos em academias ou atendimentos particulares.
Permite registrar alunos e gerenciar planos de treino completos, exportando
as informações em PDF. A interface usa `tkinter` com `ttkbootstrap` e conta com
alternância de tema (claro ou escuro) e exibe os alunos em cartões. Os detalhes
de cada aluno são mostrados na própria janela principal e os PDFs.

O módulo de treinos foi ampliado para aceitar detalhes de cada exercício, como séries, repetições,
peso, tempo de descanso e observações. Cada plano pode ser exportado em PDF mostrando essas
informações de forma estruturada.

## Requisitos
- Python 3.11 ou superior
- Dependências listadas em `requirements.txt`

## Como usar
1. Instale o Python 3.11 ou superior em seu computador.
2. (Opcional) Crie um ambiente virtual com `python -m venv venv` e ative-o.
3. Instale as dependências com `pip install -r requirements.txt`.
4. (Opcional) Rode os testes com `pytest` para garantir que tudo está funcionando.
5. Execute `python src/main.py` para abrir o sistema.

Todo o banco de dados fica salvo localmente em `alunos.db`.

## Licença

Distribuído sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais
informações.
