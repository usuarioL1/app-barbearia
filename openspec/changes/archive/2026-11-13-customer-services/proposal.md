# Proposal

## Why

O catálogo de serviços precisa ser acompanhado independentemente das outras rotas do cliente. A rota concluída apresenta os serviços demonstrativos em uma composição própria.

## What Changes

- Registrar a rota `/servicos`, a consulta mockada do catálogo e os estados de vazio/erro como entregues.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `customer-portal`: adicionar o contrato de apresentação do catálogo.

## Impact

- `app_barbearia/customer_portal.py`, `state.py` e `mock_repository.py`; sem chamadas HTTP.
