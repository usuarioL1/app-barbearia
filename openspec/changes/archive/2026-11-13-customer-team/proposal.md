# Proposal

## Why

A tela pública da equipe é uma rota própria e deve manter seu registro separado. A interface concluída apresenta barbeiros ativos e suas especialidades sem dados pessoais desnecessários.

## What Changes

- Registrar a rota `/equipe` e sua consulta mockada de barbeiros como entregues.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `customer-portal`: adicionar a apresentação da equipe ao portal.

## Impact

- `app_barbearia/customer_portal.py`, `state.py` e `mock_repository.py`; sem chamadas HTTP.
