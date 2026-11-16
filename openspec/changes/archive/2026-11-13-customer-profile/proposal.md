# Proposal

## Why

O perfil do cliente tem uma rota e um fluxo de edição próprios. A tela concluída consulta e atualiza uma cópia mockada dos dados do usuário atual.

## What Changes

- Registrar a rota `/perfil`, validação e atualização não persistente do perfil como entregues.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `customer-portal`: adicionar a consulta e edição mockada do próprio perfil.

## Impact

- `app_barbearia/customer_portal.py`, `state.py` e `mock_repository.py`; sem chamadas reais.
