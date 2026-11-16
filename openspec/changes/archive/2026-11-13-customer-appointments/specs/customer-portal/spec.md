# Spec Delta

## ADDED Requirements

### Requirement: Cliente consulta e cancela os próprios agendamentos mockados
A rota SHALL separar próximos atendimentos e histórico do cliente autenticado, oferecendo cancelamento simulado apenas quando permitido pela regra de antecedência.

#### Scenario: Consulta de registros do cliente
- **WHEN** o cliente abre seus agendamentos
- **THEN** a interface apresenta apenas registros atribuídos a ele, com estado e horário local

#### Scenario: Cancelamento permitido ou recusado
- **WHEN** o cliente solicita cancelamento dentro do limite ou a fonte mockada o recusa
- **THEN** a interface atualiza somente após sucesso simulado ou preserva o estado exibido e informa o erro
