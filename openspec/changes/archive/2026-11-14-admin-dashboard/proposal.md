# Proposal

## Why

O console administrativo precisa de um resumo operacional coerente com as telas BarberFlow já reconstruídas. Esta mudança registra o dashboard existente como capability e explicita que seus indicadores vêm de dados demonstrativos, sem integração ou persistência.

## What Changes

- Definir o dashboard administrativo com indicadores de agendamentos, faturamento mensal, clientes e comparecimento, além do resumo de agendamentos e série de faturamento.
- Documentar o período exibido e o comportamento de carregamento/erro dos dados mockados.
- Manter os dados isolados no repositório mock; nenhuma chamada ao Xano ou gravação é feita.

## Capabilities

### New Capabilities
- `admin-console`: Dashboard administrativo e seus indicadores operacionais.

### Modified Capabilities

Nenhuma.

## Impact

- `app_barbearia/state.py`, `app_barbearia/mock_repository.py` e `app_barbearia/workspace_pages.py`.
- Testes de estado e do repositório mock; nenhuma API, dependência ou schema Xano é alterado.