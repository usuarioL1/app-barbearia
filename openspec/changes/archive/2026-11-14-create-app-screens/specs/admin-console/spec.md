# Spec Delta

## Purpose

Define as jornadas administrativas para acompanhar a operação da barbearia, gerir agenda e cadastros e consultar desempenho sem ultrapassar as permissões e regras de negócio do MVP.

## ADDED Requirements

### Requirement: Administrador acompanha o resumo operacional
A interface SHALL oferecer um dashboard administrativo com indicadores de agenda, faturamento, clientes e comparecimento, identificando o período consultado e exibindo dados retornados pelo sistema.

#### Scenario: Dashboard carregado
- **WHEN** um administrador autenticado abre o dashboard e os dados são carregados
- **THEN** a interface apresenta os indicadores e o resumo de faturamento do período selecionado, sem substituir dados ausentes por métricas inventadas

#### Scenario: Falha ao carregar o resumo
- **WHEN** a consulta do dashboard falha
- **THEN** a interface indica que os dados não puderam ser carregados e permite tentar novamente

### Requirement: Administrador consulta e opera a agenda da unidade
A interface SHALL oferecer visualização diária e semanal com filtros de barbeiro e estado, usando o fuso `America/Sao_Paulo` e as informações de atendimento necessárias à gestão.

#### Scenario: Agenda filtrada
- **WHEN** um administrador seleciona período, barbeiro ou estado
- **THEN** a interface apresenta somente os atendimentos que correspondem aos filtros e mantém visível o período consultado

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
A interface administrativa SHALL reconstruir os designs fornecidos como componentes, preservando estrutura, proporções, navegação, hierarquia e aparência preto/dourado. Composições inteiras não devem substituir as telas; assets individuais ausentes devem usar placeholders coerentes, sem acrescentar elementos visuais ausentes da referência.

#### Scenario: Administrador navega pelo console
- **WHEN** o administrador abre dashboard, agenda ou uma seção de gestão
- **THEN** a tela apresenta a navegação lateral, seleção ativa, cabeçalho, cartões, tabelas, indicadores ou gráficos conforme o design BarberFlow correspondente

#### Scenario: Administrador consulta relatórios e configurações
- **WHEN** o administrador abre relatórios ou configurações
- **THEN** a interface preserva a hierarquia, os filtros e os agrupamentos visuais representados no design, sem alterar as regras de autorização e os dados apresentados
