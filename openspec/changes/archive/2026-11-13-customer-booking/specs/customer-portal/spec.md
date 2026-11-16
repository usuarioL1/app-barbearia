# Spec Delta

## ADDED Requirements

### Requirement: Cliente percorre o fluxo mockado de agendamento
A rota de agendamento SHALL guiar a seleção de serviço, barbeiro, data e horário usando opções mockadas, mostrando resumo com preço e duração e sem persistir a reserva.

#### Scenario: Seleção válida e confirmação explícita
- **WHEN** o cliente seleciona opções disponíveis e confirma o resumo
- **THEN** a interface apresenta a confirmação simulada e informa que nada foi salvo

#### Scenario: Disponibilidade falha ou ocorre conflito
- **WHEN** a consulta de horários falha ou a reserva simulada encontra conflito
- **THEN** a interface informa o erro, descarta horários obsoletos e não apresenta confirmação
