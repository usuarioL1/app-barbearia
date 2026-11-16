# Spec Delta

## ADDED Requirements

### Requirement: Barbeiro atualiza os próprios atendimentos
A rota `/barbeiro/atendimentos` SHALL listar os atendimentos do barbeiro atual e oferecer somente as transições permitidas pela regra de negócio, sem persistir alterações na fase mockada.

#### Scenario: Transição permitida pela fonte mockada
- **WHEN** o barbeiro solicita uma transição de status permitida e a fonte mockada a confirma
- **THEN** a interface atualiza o atendimento correspondente e informa que a operação foi simulada

#### Scenario: Transição recusada ou operação indisponível
- **WHEN** a fonte mockada recusa a transição ou falha
- **THEN** a interface preserva o estado exibido e informa o erro sem apresentar sucesso
