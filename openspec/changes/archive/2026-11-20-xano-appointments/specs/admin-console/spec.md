# Spec Delta

## MODIFIED Requirements

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
