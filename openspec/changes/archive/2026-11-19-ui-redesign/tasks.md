# Tasks

## 1. Sistema visual e navegação compartilhados

- [x] 1.1 Harmonizar tokens de cor, tipografia, cartões, campos, botões e badges em `ui.py`; verificar que `reflex compile --dry` passa e que os rótulos acessíveis continuam presentes.
- [x] 1.2 Reorganizar os layouts compartilhados cliente/roles para navegação desktop e responsiva sem novo handler; verificar as rotas e os links ativos com inspeção visual em larguras desktop e móvel.

## 2. Telas do cliente

- [x] 2.1 Recompor portal, catálogo, equipe, perfil, agendamentos e agendamento em `customer_portal.py` conforme o mapa; comparar cada ação interativa antes/depois e confirmar que os mesmos handlers, argumentos, estados e feedbacks continuam vinculados.
- [x] 2.2 Harmonizar login, cadastro e recuperação em `auth_pages.py` com o sistema visual compartilhado sem trocar campos nem eventos; verificar visualmente as três rotas e compilar o app.

## 3. Telas do barbeiro e administração

- [x] 3.1 Reorganizar dashboard, atendimentos e perfil do barbeiro em `workspace_pages.py` usando somente informações existentes; verificar navegação de datas, ações de estado e estados vazio/erro sem alterar handlers ou escopo de dados.
- [x] 3.2 Reorganizar as rotas administrativas existentes em `workspace_pages.py` conforme o mapa, mantendo formulários, filtros, permissões e configurações somente de leitura; verificar a compilação e cada binding interativo.

## 4. Verificação integrada do redesign

- [x] 4.1 Executar `reflex compile --dry` e conferir o diff final; confirmar que `state.py` e `xano_repository.py` não foram alterados e que nenhuma regra de cancelamento, estado ou fuso mudou.
- [x] 4.2 Inspecionar visualmente rotas representativas dos três papéis e autenticação em desktop e viewport estreito; verificar contraste, navegação por teclado, foco visível, conteúdo sem cortes e ausência de dados/ações inventados.

## 5. Assets e shell do cliente

- [x] 5.1 Extrair recortes fotográficos individuais das referências para `assets/` e verificar que os arquivos são locais, carregam nas telas e não substituem composições funcionais nem identificam falsamente profissionais.
- [x] 5.2 Atualizar o shell do cliente com a navegação exata, item ativo dourado com texto/ícone pretos, cabeçalho autenticado e detalhes de fundo; verificar todos os links nas rotas do cliente sem alterar `state.py` ou `xano_repository.py`.

## 6. Dashboard e catálogo do cliente

- [x] 6.1 Recompor `/` com próximo agendamento, chamada de agendamento, até quatro serviços reais, histórico recente e banner; verificar estados vazios e que nenhum dado ilustrativo é apresentado como real.
- [x] 6.2 Recompor `/servicos` com hero, cartões responsivos e selos visuais; verificar que Selecionar mantém o pré-selecionamento pelo binding existente e que só serviços retornados são exibidos.
- [x] 6.3 Registrar `/historico` e apresentar somente o histórico do cliente autenticado; verificar navegação, estado vazio e datas/valores provenientes dos dados carregados.

## 7. Agendamentos e perfil do cliente

- [x] 7.1 Recompor `/agendamentos` com abas, lista principal e resumo derivado; verificar filtros e cancelamento existentes, incluindo resposta dentro/fora do limite de 12 horas, sem ação de sucesso otimista.
- [x] 7.2 Recompor `/perfil` em grade responsiva com campos existentes e resumo de histórico; verificar que salvar usa o binding atual e que controles sem suporte ficam desabilitados ou ausentes.
- [x] 7.3 Apresentar filtros de categoria/período do histórico somente se houver binding existente; verificar que controles sem suporte não alteram dados nem simulam uma filtragem.

## 8. Agendamento e validação integrada do portal

- [x] 8.1 Melhorar espaçamento de serviços e barbeiros, calendário e resumo em `/agendar`; verificar legibilidade e que confirmação continua ligada ao handler existente.
- [x] 8.2 Compilar e inspecionar as rotas do cliente em desktop e viewport estreito; confirmar `BARBERFLOW_MODE=xano`, integridade inalterada de `state.py` e `xano_repository.py` e resposta do servidor reiniciado em `localhost:3001`.
