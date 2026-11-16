# Spec Delta

## ADDED Requirements

### Requirement: Administrador consulta a equipe de barbeiros
A seção administrativa SHALL listar os barbeiros mock com nome, especialidade e estado ativo/inativo, mantendo registros inativos disponíveis para consulta administrativa.

#### Scenario: Equipe carregada
- **WHEN** a consulta mock da equipe é concluída
- **THEN** a interface exibe os dados disponíveis e o estado de cada barbeiro

#### Scenario: Barbeiro inativo em novo agendamento
- **WHEN** um barbeiro está inativo e um cliente consulta opções para agendar
- **THEN** esse barbeiro não aparece entre as opções agendáveis

### Requirement: Ações administrativas da equipe não persistem
A seção SHALL permitir informar nome e especialidade para criar ou editar barbeiros e desativar registros, validando no mock sem alterar registros ou apresentar operações como persistidas.

#### Scenario: Criação mock aceita
- **WHEN** o administrador submete nome e especialidade válidos para criação
- **THEN** a validação mock aceita a ação e informa que nada foi salvo

#### Scenario: Dados obrigatórios ausentes
- **WHEN** nome ou especialidade não são informados na criação mock
- **THEN** a interface informa a validação sem apresentar uma alteração persistida

#### Scenario: Edição ou desativação mock
- **WHEN** o administrador aciona editar ou desativar para um barbeiro
- **THEN** a operação permanece simulada e não remove o barbeiro nem seus agendamentos históricos