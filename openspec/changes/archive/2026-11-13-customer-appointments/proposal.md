# Proposal

## Why

Consulta e cancelamento de agendamentos formam uma rota independente do agendamento inicial. A tela concluída usa registros mockados e mantém as regras de propriedade e antecedência.

## What Changes

- Registrar a rota `/agendamentos`, separação entre próximos/histórico e cancelamento mockado como entregues.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `customer-portal`: adicionar consulta e cancelamento mockados dos próprios atendimentos.

## Impact

- `app_barbearia/customer_portal.py`, `state.py` e `mock_repository.py`; sem persistência ou HTTP.
