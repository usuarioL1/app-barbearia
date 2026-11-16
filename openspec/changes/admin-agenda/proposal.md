# Proposal

## Why

A administração precisa consultar a agenda semanal da unidade e acompanhar alterações de estado sem perder os filtros selecionados. Esta mudança registra a tela administrativa existente e o seu comportamento simulado antes de qualquer integração real.

## What Changes

- Definir visualizações diária e semanal com data de referência, navegação entre semanas e filtros por barbeiro e estado.
- Registrar as ações administrativas de transição de estado e a preservação da exibição quando uma operação falha.
- Manter consultas e transições na fonte mock, sem chamadas ao Xano ou persistência.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities
- `admin-console`: Consulta e operações simuladas na agenda administrativa.

## Impact

- `app_barbearia/state.py`, `app_barbearia/mock_repository.py` e `app_barbearia/workspace_pages.py`.
- Testes de filtro, transição e falha da agenda; nenhum endpoint ou schema Xano é alterado.