# Proposal

## Why

A administração precisa visualizar a equipe de barbeiros, suas especialidades e estado operacional na composição BarberFlow. Esta mudança documenta as ações simuladas da tela, mantendo os dados demonstrativos isolados e não persistentes.

## What Changes

- Definir a tabela da equipe com nome, especialidade e estado ativo/inativo.
- Registrar criação, edição e desativação como ações mock, sem afirmar que alteram o registro exibido.
- Manter agendamentos históricos e integração com Xano fora de qualquer operação real desta etapa.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities
- `admin-console`: Consulta e ações simuladas sobre a equipe de barbeiros.

## Impact

- `app_barbearia/state.py`, `app_barbearia/mock_repository.py` e `app_barbearia/workspace_pages.py`.
- Testes do repositório mock e do tratamento de falhas administrativas; nenhuma API, dependência ou schema é alterado.