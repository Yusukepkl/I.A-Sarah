# Gestor de Alunos

![CI](https://github.com/unknown/I.A-Sarah/actions/workflows/ci.yml/badge.svg)
![Coverage](https://img.shields.io/badge/coverage-90%25-brightgreen)

Aplicação em Python para organizar alunos de academias ou atendimentos particulares. Cada aluno pode possuir diversos planos de treino e esses planos podem ser exportados em PDF, CSV ou Excel.

## Funcionalidades
- Cadastro de alunos com nome e e‑mail
- Criação de planos de treino com lista de exercícios
- Edição dos planos associados a cada aluno
- Exportação de planos em PDF/CSV/XLSX
- Interface gráfica modernizada com seleção de tema claro ou escuro
- Animações suaves, botões com efeito e tela de splash
- Plugins de exportação carregados dinamicamente

### Plugins de exportação

Os formatos disponíveis podem variar conforme plugins instalados. Para listar os
formatos atuais diretamente no Python:

```python
from ia_sarah.core.use_cases import controllers
print(controllers.listar_exportadores())
```

Se novos plugins forem instalados em tempo de execução, é possível atualizar
a lista utilizando:

```python
from ia_sarah.core import plugin_loader
plugin_loader.reload_entrypoints("ia_sarah.exporters")
```

Por padrão estão incluídos os formatos `pdf`, `csv` e `xlsx`.

### Cadastro completo e backup

Para incluir um aluno com todos os campos disponíveis utilize:

```python
id = controllers.adicionar_aluno_completo(
    "Daniel",
    "daniel@email.com",
    plano="Avancado",
    pagamento="Cartao",
)
```

O banco pode ser copiado para um arquivo local com:

```python
controllers.backup_dados("backup.sqlite")
```

### Cadastro com plano e PDF

Para criar um aluno já associado a um plano e gerar o PDF automaticamente:

```python
aluno_id, plano_id = controllers.adicionar_aluno_com_plano_pdf(
    "Maria",
    "maria@email.com",
    plano="Treino A",
    descricao="Plano inicial",
    exercicios_json="[]",
    pdf_dest="treino.pdf",
)
```

### Estatísticas da aplicação

Para saber quantos alunos existem e quais são os planos mais recentes:

```python
print(controllers.obter_estatisticas())
```

A mesma informação está disponível na API pelo endpoint `/stats`.

## Estrutura do Projeto
```
src/
  controllers/    Camada de controle e lógica de apresentação
  services/       Serviços de negócio e plugins
  repositories/   Acesso a dados
  views/          Interfaces gráficas
  utils/          Utilidades e helpers
scripts/          Scripts para gerar executável e baixar dados
installer/        Arquivos do instalador para Windows
tests/            Testes automatizados com pytest
web/              Frontend básico para testar a API
```
O banco de dados é salvo em `~/.gestor_alunos/alunos.db`.

## Instalação rápida
1. Tenha o Python 3.11 ou superior instalado.
2. Clone este repositório e entre na pasta criada:
   ```bash
   git clone <URL do repositorio>
   cd I.A-Sarah
   ```
3. (Opcional) Crie um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
5. Inicie a aplicação com:
   ```bash
   python gestor_exetavel.py
   ```
   ou utilize o script instalado via Poetry:
   ```bash
   iasarah
   ```
6. Para rodar a API FastAPI:
 ```bash
  iasarah-api
  ```
7. Utilize o novo CLI para comandos rápidos:
  ```bash
  iasarah-cli listar
  ```
8. Com a API em execução, abra o arquivo `web/index.html` em seu navegador
   e utilize os botões para listar ou excluir alunos. Todas as ações
   exibem modais de confirmação e feedback. O tema claro/escuro pode
   ser escolhido em um menu suspenso, interagindo com os endpoints
   `/students`, `/theme` e `/config`. O layout utiliza o arquivo
   `web/style.css` para um visual moderno baseado em tema escuro.

### Variáveis de ambiente importantes
* `CONFIG_FILE` - caminho opcional para o arquivo de configuração.
* `METRICS_PORT` - porta utilizada pelo servidor de métricas.
  Certifique-se de instalar `prometheus-client` para habilitar essa funcionalidade.
* `DISABLED_PLUGINS` - lista de plugins separados por vírgula a serem ignorados.
* `PV_KEYWORD_PATH` - caminho do arquivo de palavra‑chave para o Porcupine; se
  vazio, o reconhecimento por voz usa modo dummy.

### Executando os testes
Instale primeiro as dependências de teste:
```bash
pip install -r requirements.txt
pytest -q
```
Para garantir o estilo de código, instale os hooks do pre-commit:
```bash
pre-commit install
pre-commit run --all-files
```

## Gerar Instalador
Consulte `installer/build_installer.ps1` para criar um executável único e o instalador para Windows.
Para Linux e macOS recomenda-se utilizar `pyinstaller`:
```bash
pyinstaller gestor_exetavel.py -n iasarah
```
O binário ficará em `dist/iasarah`.

## Visual Studio Code
Arquivos de configuração em `.vscode/` permitem rodar a aplicação e os testes
diretamente do editor. Use o menu de tarefas para **Rodar aplicacao** ou
**Testes rapidos**. A depuração está disponível pelo launcher
**Python: Gestor de Alunos**.

Para isolar o ambiente de desenvolvimento use a extensão **Dev Containers**.
Abra o repositório no VS Code e escolha **Reabrir em Contêiner**. A
configuração em `.devcontainer/` utiliza o `Dockerfile` do projeto e instala as
dependências automaticamente. Após a criação do contêiner, os comandos de
tarefas e depuração funcionam normalmente.

## Abertura rápida em IDEs
Execute `open_pycharm.py` para abrir o projeto no PyCharm ou `open_vscode.py` para abrir no VS Code. Os comandos `pycharm` e `code` devem estar no PATH.

## Licença
Distribuído sob a Licença MIT em português. Veja o arquivo [LICENSE](LICENSE).
