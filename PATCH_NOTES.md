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
