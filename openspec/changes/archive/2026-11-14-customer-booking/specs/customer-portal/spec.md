# Spec Delta

## ADDED Requirements

### Requirement: Seleção de opções de agendamento
A rota `/agendar` SHALL permitir selecionar serviço e barbeiro ativos, data e horário retornado pela disponibilidade mockada, apresentando calendário e resumo com preço e duração.

#### Scenario: Consultar disponibilidade
- **WHEN** o cliente abre o fluxo ou altera serviço, barbeiro ou data
- **THEN** a interface atualiza as opções de horário e o resumo conforme os dados selecionados

#### Scenario: Horário disponível
- **WHEN** a consulta retorna horários para a seleção atual
- **THEN** o cliente pode selecionar um deles e revisar serviço, barbeiro, data, hora, preço e duração antes de confirmar

#### Scenario: Consulta de disponibilidade falha
- **WHEN** a consulta mockada falha
- **THEN** a interface limpa os horários antigos e impede confirmar com uma opção desatualizada

### Requirement: Confirmação simulada de agendamento
A interface SHALL habilitar a confirmação somente para um horário atualmente selecionado e disponível, tratando conflitos sem apresentar sucesso nem persistir uma reserva.

#### Scenario: Confirmação aceita pelo mock
- **WHEN** o cliente confirma um horário disponível e o repositório mockado aceita a solicitação
- **THEN** a interface mostra os dados da confirmação e informa que nada foi salvo

#### Scenario: Horário indisponível na confirmação
- **WHEN** o repositório mockado rejeita a confirmação por conflito
- **THEN** a interface informa a indisponibilidade, limpa o horário selecionado e solicita atualização das opções