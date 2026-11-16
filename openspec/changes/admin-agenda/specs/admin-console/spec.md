# Spec Delta

## ADDED Requirements

### Requirement: Administrador consulta agenda semanal filtrada
A agenda SHALL exibir a semana da data selecionada, os atendimentos demonstrativos e filtros combináveis por barbeiro e estado, usando datas locais de `America/Sao_Paulo`.

#### Scenario: Seleção de semana e filtros
- **WHEN** o administrador seleciona uma data, barbeiro ou estado
- **THEN** a interface exibe a semana correspondente e somente os atendimentos que correspondem aos filtros ativos

#### Scenario: Semana sem resultados
- **WHEN** não há atendimento mock correspondente à semana e aos filtros
- **THEN** a interface apresenta o estado vazio e mantém visível o período consultado

### Requirement: Administrador consulta agenda diária
A agenda SHALL permitir alternar para um dia selecionado e apresentar somente os atendimentos desse dia, mantendo os filtros de barbeiro e estado.

#### Scenario: Visualização diária selecionada
- **WHEN** o administrador escolhe a visualização diária para uma data
- **THEN** a interface apresenta apenas os atendimentos da data selecionada que correspondem aos filtros ativos

### Requirement: Administrador solicita transições simuladas de atendimento
A agenda SHALL permitir as transições administrativas mock válidas entre `pending`, `confirmed`, `cancelled` e `completed`, respeitando as regras de transição e o horário de término.

#### Scenario: Transição aceita
- **WHEN** o administrador solicita uma transição permitida e o repositório mock a aceita
- **THEN** a agenda exibe o estado resultante na sessão e identifica a ação como simulada e não persistida

#### Scenario: Transição recusada
- **WHEN** a transição é inválida ou o repositório mock retorna erro
- **THEN** a agenda preserva os registros exibidos e informa que a operação não foi concluída

### Requirement: Agenda administrativa não persiste operações mock
A agenda SHALL usar somente dados demonstrativos nesta etapa, sem chamadas HTTP ao Xano ou gravação durável de consulta ou transição.

#### Scenario: Atualização da agenda mock
- **WHEN** uma consulta ou transição é concluída
- **THEN** nenhum dado é apresentado como persistido fora da sessão mock