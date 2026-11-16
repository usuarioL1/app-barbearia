# Tasks

## 1. Base já concluída

- [x] 1.1 Criar a estrutura inicial de páginas públicas e layouts compartilhados por papel, com navegação responsiva, tokens de tema escuro/dourado e componentes acessíveis; verificar a estrutura no app Reflex.
- [x] 1.2 Implementar a configuração da URL base e a camada HTTP compartilhada; manter essa base sem novas conexões com Xano durante as etapas visuais e de mocks, e confirmar que os testes existentes passam.

## 2. Etapa visual: finalizar todas as telas

- [x] 2.1 Reconstruir login, cadastro e recuperação de senha como componentes Reflex, comparando composição, proporções, tipografia, campos, botões e paleta preto/dourado com os designs fornecidos; não adicionar rótulos de demonstração ausentes das referências.
- [x] 2.2 Reconstruir portal, perfil, catálogo, equipe, próximos atendimentos e histórico do cliente conforme os designs, incluindo navegação, seleção ativa, cabeçalhos, cartões e densidade visual; usar componentes, não capturas de tela.
- [x] 2.3 Reconstruir o fluxo de agendamento conforme a referência, incluindo etapas, seleção de serviço e barbeiro, calendário, horários, resumo e confirmação visual; manter os controles sem integração real nessa etapa.
- [x] 2.4 Reconstruir agenda, cartões de atendimento, estados e ações visuais do barbeiro conforme a referência, preservando a hierarquia de informações e sem executar transições reais.
- [x] 2.5 Reconstruir dashboard, agenda, clientes, serviços, equipe, relatórios, usuários e configurações administrativas conforme as referências, incluindo navegação, tabelas, cartões, filtros e gráficos apresentados.
- [x] 2.6 Comparar cada rota visualmente com as referências em desktop e celular; usar placeholders coerentes para logo, retratos e fundos individuais ausentes, sem renderizar composições completas como telas ou acrescentar banners e selos; verificar navegação por teclado, foco, rótulos, acessibilidade e build Reflex.

## 3. Etapa de comportamento: mocks somente após revisão visual

- [x] 3.1 Após a revisão e aprovação visual das telas, criar uma fonte de mocks isolada; testar que os dados simulados não são enviados à camada HTTP nem apresentados como operações persistidas.
- [x] 3.2 Implementar com mocks os fluxos do cliente de autenticação visual, perfil, catálogo, agendamento, consulta e cancelamento; testar estados de carregamento, vazio, sucesso, validação, conflito e erro sem sucesso otimista.
- [x] 3.3 Implementar com mocks a agenda e as transições do barbeiro, além das consultas e operações administrativas; testar filtros, permissões de apresentação, falhas sem perda do estado exibido e relatórios calculados apenas com os dados demonstrativos definidos.

## 4. Integração real com Xano (desmembrada)

As tarefas de inspeção do schema, confirmação de contratos, integração e validação foram transferidas para [xano-integration](../xano-integration/tasks.md). Permanecem pendentes nessa change; não fazem parte do trabalho concluído registrado aqui.
