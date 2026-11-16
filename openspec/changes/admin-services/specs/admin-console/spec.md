# Spec Delta

## ADDED Requirements

### Requirement: Administrador consulta o catálogo de serviços
A seção administrativa SHALL listar os serviços mock com título, descrição, preço, duração e estado ativo/inativo; somente serviços ativos são oferecidos para novos agendamentos.

#### Scenario: Catálogo administrativo carregado
- **WHEN** a consulta mock de serviços é concluída
- **THEN** a interface exibe os campos disponíveis e o estado de cada serviço, incluindo registros inativos para consulta administrativa

#### Scenario: Serviço inativo no agendamento
- **WHEN** um serviço está inativo e um cliente consulta opções para um novo agendamento
- **THEN** esse serviço não aparece entre as opções agendáveis

### Requirement: Ações administrativas de serviço não persistem
A seção SHALL permitir informar título, descrição, preço e duração para criar ou editar serviços e desativar registros, validando no mock e sem alterar registros ou afirmar persistência.

#### Scenario: Criação mock válida
- **WHEN** o administrador submete título, preço positivo e duração positiva
- **THEN** a validação mock aceita a ação e informa que nada foi salvo

#### Scenario: Criação mock inválida
- **WHEN** o título obrigatório está ausente ou preço ou duração não são valores positivos válidos
- **THEN** a interface informa a validação sem apresentar uma alteração persistida

#### Scenario: Edição ou desativação mock
- **WHEN** o administrador aciona editar ou desativar para um serviço
- **THEN** a operação permanece simulada, sem remover registros de serviço ou histórico associado