# Proposal

## Why

O agendamento concentra uma jornada distinta e precisa de rastreabilidade própria. O fluxo concluído usa serviços, barbeiros, disponibilidade e confirmação exclusivamente mockados.

## What Changes

- Registrar a rota `/agendar`, suas etapas, validação, conflito e confirmação não persistente como entregues.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `customer-portal`: adicionar o contrato do fluxo mockado de agendamento.

## Impact

- `app_barbearia/customer_portal.py`, `state.py` e `mock_repository.py`; a API real permanece adiada.
