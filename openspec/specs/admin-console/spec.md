# admin-console Specification

## Purpose

Define as jornadas administrativas para acompanhar a operação da barbearia, gerir agenda e cadastros e consultar desempenho sem ultrapassar as permissões e regras de negócio do MVP.

## Requirements

### Requirement: Administrador acompanha o resumo operacional
A interface SHALL oferecer um dashboard administrativo com indicadores de agenda, faturamento, clientes e comparecimento, identificando o período consultado e exibindo dados retornados pelo sistema.

#### Scenario: Dashboard carregado
- **WHEN** um administrador autenticado abre o dashboard e os dados são carregados
- **THEN** a interface apresenta os indicadores e o resumo de faturamento do período selecionado, sem substituir dados ausentes por métricas inventadas

#### Scenario: Falha ao carregar o resumo
- **WHEN** a consulta do dashboard falha
- **THEN** a interface indica que os dados não puderam ser carregados e permite tentar novamente

### Requirement: Administrador consulta e opera a agenda da unidade
A interface SHALL oferecer visualização diária e semanal com filtros de barbeiro e estado, usando o fuso `America/Sao_Paulo` e as informações de atendimento necessárias à gestão, com os dados do repositório selecionado.

#### Scenario: Agenda filtrada
- **WHEN** um administrador seleciona período, barbeiro ou estado
- **THEN** a interface apresenta somente os atendimentos que correspondem aos filtros e mantém visível o período consultado

#### Scenario: Seleção de semana e filtros
- **WHEN** o administrador seleciona uma data, barbeiro ou estado
- **THEN** a interface exibe a semana correspondente e somente os atendimentos do repositório selecionado que correspondem aos filtros ativos

#### Scenario: Semana sem resultados
- **WHEN** não há atendimento correspondente à semana e aos filtros no repositório selecionado
- **THEN** a interface apresenta o estado vazio e mantém visível o período consultado

#### Scenario: Alteração de estado
- **WHEN** o administrador solicita uma transição de estado permitida e o backend confirma
- **THEN** a interface exibe o estado atualizado e o resultado da operação

#### Scenario: Alteração recusada
- **WHEN** a transição é inválida ou o backend retorna erro
- **THEN** a interface preserva o estado atual e informa que a operação não foi concluída

### Requirement: Administrador gerencia cadastros operacionais sem apagar histórico
A interface SHALL permitir consultar e manter clientes, usuários, serviços e equipe conforme as permissões administrativas, usando desativação para registros com histórico associado.

#### Scenario: Cadastro ou edição confirmados
- **WHEN** o administrador salva um cadastro válido e o backend confirma a operação
- **THEN** a interface apresenta os dados persistidos e comunica o sucesso

#### Scenario: Desativação com histórico
- **WHEN** o administrador desativa um serviço, barbeiro ou usuário associado a histórico
- **THEN** a interface preserva os registros relacionados, remove o item das novas opções aplicáveis e mantém seus dados disponíveis para consulta administrativa

#### Scenario: Falha de validação ou autorização
- **WHEN** o backend recusa um cadastro ou alteração
- **THEN** a interface informa o erro e não apresenta a alteração como persistida

### Requirement: Administrador consulta faturamento por período
A interface SHALL oferecer relatórios diários e mensais que usem os preços snapshot de atendimentos concluídos e agrupem os valores pela data local do início do atendimento.

#### Scenario: Relatório de faturamento
- **WHEN** o administrador seleciona um dia ou mês para consulta
- **THEN** a interface apresenta o total e os dados disponíveis considerando somente atendimentos `completed` no período local selecionado

#### Scenario: Período sem faturamento
- **WHEN** o relatório não encontra atendimentos concluídos no período
- **THEN** a interface apresenta total zero e um estado vazio, sem incluir atendimentos pendentes, confirmados ou cancelados

### Requirement: Console administrativo reproduz os designs BarberFlow fornecidos
A interface administrativa SHALL aplicar preto `#090909` e dourado `#F2A900` às rotas existentes `/admin/*`, refinando navegação, filtros e conteúdo sem substituir componentes por capturas de tela nem inventar indicadores, registros ou ações.

#### Scenario: Administrador navega pelo console
- **WHEN** o administrador abre dashboard, agenda, clientes, serviços, equipe ou usuários
- **THEN** a interface mantém navegação lateral com rota ativa, cabeçalho e cartões, tabelas ou agenda adequados aos dados e às ações existentes

#### Scenario: Administrador consulta relatórios e configurações
- **WHEN** o administrador abre relatórios ou configurações
- **THEN** a interface mantém a hierarquia, os filtros e os agrupamentos visuais correspondentes, sem alterar permissões, métricas disponíveis ou o caráter informativo das configurações

#### Scenario: Administrador usa o console em uma tela estreita
- **WHEN** a largura disponível não comporta o layout desktop
- **THEN** a navegação, os filtros, os cartões e as tabelas se reorganizam sem ocultar controles, dados, mensagens ou ações existentes

### Requirement: Administrador consulta as configurações operacionais apresentadas
A interface SHALL apresentar o expediente, fuso horário e limite padrão de cancelamento como informações somente para leitura, sem confirmar alteração ou persistência dessas configurações.

#### Scenario: Configurações exibidas
- **WHEN** o administrador abre a seção Configurações
- **THEN** a interface apresenta expediente de segunda a sábado das 09h às 18h, fuso `America/Sao_Paulo` e cancelamento até 12 horas antes do atendimento

#### Scenario: Configuração não editável nesta etapa
- **WHEN** o administrador consulta a página de configurações
- **THEN** a interface não oferece um fluxo funcional de edição ou salvamento dos valores exibidos

### Requirement: Administrador consulta relatórios de faturamento por período
A interface SHALL permitir escolher relatório diário ou mensal e apresentar faturamento, quantidade de atendimentos concluídos e indicadores derivados dos registros disponíveis.

#### Scenario: Relatório diário ou mensal
- **WHEN** o administrador seleciona o período e a data do relatório
- **THEN** a interface atualiza os indicadores para o período local selecionado em `America/Sao_Paulo`

#### Scenario: Período sem faturamento
- **WHEN** não há atendimentos concluídos no período selecionado
- **THEN** o relatório apresenta faturamento zero e não inclui atendimentos pendentes, confirmados ou cancelados

### Requirement: Administrador pesquisa a lista de clientes
A lista SHALL filtrar clientes por nome, e-mail ou telefone sem modificar os registros e sem expor o e-mail como uma coluna adicional.

#### Scenario: Busca com correspondências
- **WHEN** o administrador informa um termo que corresponde a um ou mais clientes
- **THEN** a lista apresenta somente os registros correspondentes

#### Scenario: Busca sem correspondências
- **WHEN** o administrador informa um termo sem correspondência
- **THEN** a lista apresenta o estado vazio sem remover ou alterar os registros

### Requirement: Faturamento considera somente atendimentos concluídos
O relatório SHALL somar o preço snapshot de cada atendimento concluído cuja data local de início pertença ao período selecionado.

#### Scenario: Soma do faturamento
- **WHEN** existem atendimentos concluídos e não concluídos no período
- **THEN** o total usa somente os preços snapshot dos atendimentos concluídos com datas locais dentro do período

#### Scenario: Falha ao carregar o relatório
- **WHEN** a consulta do relatório falha
- **THEN** a interface informa a falha e preserva os indicadores anteriormente carregados

### Requirement: Dados operacionais administrativos usam respostas do Xano
Quando `BARBERFLOW_MODE=xano`, as telas administrativas SHALL apresentar somente dados e métricas retornados com sucesso pelo Xano, sem substituir falhas ou respostas vazias por dados demonstrativos; no modo mock, SHALL usar somente dados mock sem chamadas HTTP ao Xano.

#### Scenario: Dados operacionais carregados
- **WHEN** o administrador abre uma tela com dados operacionais e as consultas Xano têm sucesso
- **THEN** a interface apresenta os registros e métricas retornados para a tela e o período selecionados

#### Scenario: Consulta sem registros
- **WHEN** uma consulta Xano bem-sucedida não retorna registros para a tela ou filtros atuais
- **THEN** a interface apresenta o estado vazio correspondente, sem inventar registros ou totais

#### Scenario: Modo Xano sem resposta válida
- **WHEN** uma consulta falha ou retorna uma resposta inválida
- **THEN** a interface não apresenta dados demonstrativos como resultado Xano nem indica que a consulta foi concluída com sucesso

#### Scenario: Atualização da agenda mock
- **WHEN** uma consulta ou transição é concluída no modo mock
- **THEN** nenhum dado é apresentado como persistido fora da sessão mock

#### Scenario: Consulta ou transição em Xano
- **WHEN** uma consulta ou transição é confirmada pelo Xano
- **THEN** a agenda apresenta os dados retornados sem substituí-los por registros demonstrativos
#### Scenario: Consulta ou transição em Xano
- **WHEN** uma consulta ou transição é confirmada pelo Xano
- **THEN** a agenda apresenta os dados retornados sem substituí-los por registros demonstrativos

### Requirement: Ações administrativas dependem de operações Xano disponíveis
As telas administrativas SHALL oferecer somente ações com operação correspondente permitida, respeitando as transições de `pending` para `confirmed` ou `cancelled` e de `confirmed` para `completed` ou `cancelled`, além do horário de término, e refletindo alterações somente após confirmação do Xano ou identificando explicitamente a simulação no modo mock.

#### Scenario: Transição aceita
- **WHEN** o administrador solicita uma transição permitida e o repositório selecionado a aceita
- **THEN** a agenda exibe o estado resultante e identifica a ação como persistida em Xano ou simulada no modo mock

#### Scenario: Transição recusada
- **WHEN** a transição é inválida ou o repositório selecionado retorna erro
- **THEN** a agenda preserva os registros exibidos e informa que a operação não foi concluída

#### Scenario: Ação suportada confirmada
- **WHEN** o administrador solicita uma ação com endpoint disponível e o Xano confirma a alteração
- **THEN** a interface apresenta o resultado confirmado pelo backend sem simulação ou sucesso otimista

#### Scenario: Ação sem endpoint ou sem permissão
- **WHEN** uma ação não possui endpoint disponível ou é incompatível com as permissões e o provisionamento manual exigido
- **THEN** a interface omite ou desabilita o controle e não apresenta a ação como realizada

#### Scenario: Ação suportada recusada
- **WHEN** o Xano recusa uma ação ou sua resposta não confirma a alteração
- **THEN** a interface preserva os dados atuais e informa que a operação não foi concluída

### Requirement: 404 técnico de endpoint não publicado mantém o console limpo
Quando o estado da interface administrativa contém exatamente a mensagem `Unable to locate request.`, a interface SHALL ocultá-la no feedback global e substituir o conteúdo afetado por um estado de dados indisponíveis, sem renderizar registros antigos ou demonstrativos.

#### Scenario: Endpoint de leitura ainda não publicado
- **WHEN** uma consulta de dados operacionais deixa no estado global a mensagem `Unable to locate request.`
- **THEN** a interface não exibe a mensagem no topo, não renderiza os dados anteriores dessa tela e apresenta um estado neutro de indisponibilidade sem declarar sucesso da consulta

#### Scenario: Outra mensagem de erro
- **WHEN** a consulta deixa no estado global qualquer mensagem diferente de `Unable to locate request.`
- **THEN** a interface preserva o tratamento de erro aplicável e não oculta a falha como se fosse uma consulta bem-sucedida
