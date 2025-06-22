# Gestor de Alunos para Personal Trainer

Aplicação simples para gerenciamento de alunos em academias ou atendimentos
particulares. Permite registrar alunos e gerenciar planos de treino completos,
exportando as informações em PDF. A interface usa `tkinter` com o plugin de
temas `ttkbootstrap`, permitindo alternância entre modo claro e escuro. Cada
aluno é exibido em cartões, e seus detalhes aparecem na janela principal e nos
PDFs gerados.

O módulo de treinos foi ampliado para aceitar detalhes de cada exercício, como séries, repetições,
peso, tempo de descanso e observações. Cada plano pode ser exportado em PDF mostrando essas
informações de forma estruturada.

## Requisitos
- Python 3.11 ou superior
- `git` para clonar o repositório
- Ambiente com suporte a interface gráfica (para testes em servidores sem
  interface utilize `PyVirtualDisplay`)

## Instalação
1. Instale o Python 3.11 ou superior e verifique se o comando `python` está disponível em seu terminal.
2. Clone este repositório:
   ```bash
   git clone <URL do seu repositorio>
   cd I.A-Sarah
   ```
3. (Opcional) Crie um ambiente virtual e ative-o:
   ```bash
   python -m venv venv
   # Linux/macOS
   source venv/bin/activate
   # Windows
   venv\Scripts\activate
   ```
4. Instale o aplicativo e suas dependências. Caso prefira instalar
   manualmente, utilize o arquivo `requirements.txt`:
   ```bash
   pip install .
   # ou
   pip install -r requirements.txt
   ```
5. Para executar o programa use:
   ```bash
   gestor-alunos
   ```
6. Para rodar a suíte de testes (opcional):
   ```bash
   pip install .[test]
   pytest
   ```

O banco de dados é salvo em `~/.gestor_alunos/alunos.db`, garantindo que os dados permaneçam
mesmo ao executar o programa em diretórios diferentes.

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
4. Execute `installer\build_installer.ps1` para gerar o instalador apontando para o caminho onde o repositório está clonado.

É possível personalizar o tema da interface editando o arquivo
`src/config.json` ou utilizando a opção de troca de tema na própria aplicação.

O script `scripts/setup_data.ps1` faz o download ou atualização do conteúdo do
repositório via `git`, garantindo que o usuário receba os arquivos atuais ao
instalar o aplicativo.
