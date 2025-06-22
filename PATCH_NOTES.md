# Patch Notes

## Versão 1.0 - Primeiro lançamento
- Implementação inicial do gestor de alunos.
- Interface básica e documentação inicial.

## Versão 1.1 - Melhorias de interface
- Atualizações de layout e identidade visual.
- Inclusão de painel lateral e cartões de aluno.
- Ajustes em temas claro/escuro.

## Versão 1.2 - Planos de treino e persistência
- Adição de gerenciamento de planos de treino com salvamento.
- Funcionalidade para edição dos planos.
- Exibição de detalhes do aluno e do plano na mesma janela.

## Versão 1.3 - Experiência do usuário
- Novos estilos de cartão e animações.
- Barra de progresso e feedback para o usuário.
- Execução em background para operações pesadas.
- Correções diversas na interface.

## Versão 1.4 - Testes e empacotamento
- Configuração inicial de testes com pytest.
- Script de empacotamento e instalador para Windows.
- Ajustes de caminho e dependências adicionais.

## Versão 1.5 - Instalador e documentação
- Inclusão de scripts do Inno Setup para gerar instalador.
- Melhoria nas instruções de instalação no README.
- Possibilidade de informar repositório de dados externo.

## Versão 1.6 - Refatorações
- Estrutura modular seguindo padrões de código.
- Organização do projeto com modelo MVC e pacote `ia_sarah`.
- Correções e documentação adicional.

## Versão 2.0 - Plugin system e API
- Implementação de sistema de plugins e pipeline de CI.
- Reestruturação completa com carregamento dinâmico.
- Inclusão de servidor FastAPI para a API.


## Versão 2.1 - Limpeza e organização
- Remoção de arquivos antigos de interfaces e pontos de entrada.
- Criação do arquivo `requirements.txt` para facilitar a instalação.
- Documentação revisada no `README` e novo `AGENTS.md` com instruções de contribuição.

## Versão 2.2 - Interface Qt unificada
- Removidos módulos da interface Tkinter considerados legados.
- Dependências e testes relacionados ao Tkinter foram excluídos.
- Novo script `gestor_exetavel.py` simplifica a execução da aplicação.

## Versão 2.3 - Gestão de planos aprimorada
- Nova página para criar e editar planos de treino por aluno.
- Teste automatizado para a interface de planos.

## Versão 2.4 - Exportadores de treino
- Opções na interface para exportar planos.
- Suporte a formatos PDF, CSV e XLSX através de exportadores registrados.

## Versão 2.5 - Notificações e erros
- Tratamento de exceções nas operações de banco de dados.
- Mensagens de sucesso ou erro exibidas na interface para CRUD e exportações.

## Versão 2.6 - Documentação e licença
- AGENTS.md atualizado com novas diretrizes.
- Licença traduzida para português.
- README atualizado.

## Versão 2.7 - Catálogo de funções
- Nova função `listar_exportadores` exposta em `controllers`.
- README agora possui seção explicando como listar formatos de exportação.
- AGENTS.md orienta documentar novas funções públicas.

## Versão 2.8 - Recarga de plugins
- Função `reload_entrypoints` adicionada para atualizar plugins dinâmicos.
- README demonstra como utilizá-la para recarregar exportadores.

## Versão 2.9 - Melhorias de infraestrutura
- Descoberta automática de plugins na pasta interna.
- Configuração padrão gerada quando ausente e fallback de valores.
- Banco de dados usa `data/db.sqlite` com migrações simples.
- Interface Qt agora exibe erro se inicialização falhar.

## Versão 3.0 - Cadastro completo e backup
- Novo diálogo de aluno permite preencher plano e pagamento com validação.
- Funções `adicionar_aluno_completo` e `backup_dados` expostas em `controllers`.
- Página de configurações oferece seleção de tema, notificações e backup.

## Versão 3.1 - Repaginação visual
- Tema Qt modernizado com novos estilos para botões e tabelas.

## Versão 3.2 - Cadastro premium
- Função `adicionar_aluno_com_plano_pdf` cria aluno, plano e gera PDF.
- Exemplo de uso adicionado na documentação.

## Versão 3.3 - Testes assíncronos
- Dependência `pytest-asyncio` adicionada para executar testes com corrotinas.

## Versão 3.4 - Frontend web
- Adicionada página `web/index.html` para testar a API.

## Versão 3.5 - Orientação de testes
- README atualizado com seção explicando como instalar dependências de teste usando `pip install -r requirements.txt`.

## Versão 3.6 - Estatísticas da API
- Novo endpoint `/stats` retorna total de alunos e planos recentes.
- Função `obter_estatisticas` adicionada aos `controllers`.
- Frontend web exibe estatísticas através do novo botão.

## Versão 3.7 - Integração com VS Code
- Configurações de tarefas e depuração adicionadas em `.vscode/`.
- README atualizado com instruções de uso no Visual Studio Code.

## Versão 3.8 - Dev container
- Diretório `.devcontainer/` permite abrir o projeto em contêiner no VS Code.
- README detalha como utilizar a extensão **Dev Containers**.

## Versão 3.9 - Modal de alunos
- Formulário substituído por modal para cadastro e edição de alunos.
- Endpoint PUT `/students/{id}` adicionado à API.
- Página `web/index.html` atualizada com tabela e validação imediata.

## Versão 4.0 - Melhorias no frontend web
- Confirmação de exclusão com modal.
- Feedback visual de sucesso ou erro após operações.
- Indicador de carregamento para requisições.
- Seleção de tema claro/escuro via menu suspenso.
- Tratamento de JSON inválido com modal de aviso.


## Versão 4.1 - Conformidade flake8
- Correções de estilo e criação do arquivo `.flake8`.

\n## Versão 4.2 - Correção de animações
- Transições entre abas mantêm referências das animações para evitar tela branca.
