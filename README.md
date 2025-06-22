# Gestor de Alunos

Aplicação em Python para organizar alunos de academias ou atendimentos particulares. Cada aluno pode possuir diversos planos de treino e esses planos podem ser exportados em PDF.

## Funcionalidades
- Cadastro de alunos com nome e e‑mail
- Criação de planos de treino com lista de exercícios
- Exportação de planos em PDF
- Interface gráfica com tema claro/escuro

## Estrutura do Projeto
```
src/              Código-fonte principal
scripts/          Scripts para gerar executável e baixar dados
installer/        Arquivos do instalador para Windows
tests/            Testes automatizados com pytest
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
4. Instale o programa:
   ```bash
   pip install .
   ```
5. Inicie a aplicação com:
   ```bash
   gestor-alunos
   ```

### Testes
Para executar os testes:
```bash
pip install .[test]
pytest
```

## Gerar Instalador
Consulte `installer/build_installer.ps1` para criar um executável único e o instalador para Windows.

## Licença
Distribuído sob a licença MIT. Veja o arquivo [LICENSE](LICENSE).
