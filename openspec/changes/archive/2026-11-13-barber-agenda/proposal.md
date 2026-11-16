# Proposal

## Why

A rota `/barbeiro` é o ponto principal de consulta da agenda diária do profissional e precisa preservar a composição BarberFlow já implementada.

## What Changes

- Registrar a agenda diária do barbeiro, navegação por data, indicadores de atendimentos e o resumo do próximo atendimento.
- Manter os dados demonstrativos ligados à fonte mockada existente, sem alegar persistência.

## Capabilities

### New Capabilities
- `barber-workspace`: Jornadas do barbeiro para consultar a própria agenda, atendimentos e perfil.

### Modified Capabilities

Nenhuma.

## Impact

- Rota Reflex `/barbeiro` e estado de apresentação da agenda do barbeiro.
- Dados mockados projetados para expor somente os dados necessários à agenda.
