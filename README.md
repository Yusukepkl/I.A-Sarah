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
- `pip` recente para instalar o pacote

## Como usar
1. Instale o Python 3.11 ou superior em seu computador.
2. (Opcional) Crie um ambiente virtual com `python -m venv venv` e ative-o.
3. Instale o Gestor de Alunos executando `pip install .` dentro do diretório do projeto.
4. (Opcional) Rode os testes com `pip install .[test]` e em seguida `pytest`.
5. Após a instalação, rode `gestor-alunos` para abrir o sistema.

O banco de dados agora fica salvo em `~/.gestor_alunos/alunos.db`,
garantindo que os dados permaneçam mesmo ao executar o programa
em diretórios diferentes.

## Licença

Distribuído sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais
informações.

## Gerar executável e instalador

Para distribuir o programa como aplicativo de desktop, você pode gerar um
executável único e um instalador simples. Siga estes passos:

1. Instale o PyInstaller com `pip install pyinstaller`.
2. Execute o script `scripts/build_exe.ps1` no PowerShell para criar o
   executável em `dist/gestor-alunos.exe`.
3. Opcionalmente, utilize o script `installer/installer.iss` com o Inno Setup
   para montar um instalador. Esse instalador inclui o executável e rodará o
   script `setup_data.ps1` na primeira execução, baixando os dados mais recentes
   do repositório.

O script `scripts/setup_data.ps1` faz o download ou atualização do conteúdo do
repositório via `git`, garantindo que o usuário receba os arquivos atuais ao
instalar o aplicativo.
