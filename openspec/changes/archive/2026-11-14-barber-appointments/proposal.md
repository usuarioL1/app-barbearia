# Proposal

## Why

Os atendimentos do barbeiro precisam refletir transições de estado permitidas e não podem parecer atualizados quando uma operação é recusada. Esta mudança registra as ações simuladas, as restrições de propriedade e a confirmação explícita de que nenhuma alteração é persistida.

## What Changes

- Documentar as transições disponíveis para atendimentos pendentes e confirmados, incluindo a restrição de conclusão após o término.
- Preservar o estado exibido em caso de falha e limitar as operações aos atendimentos do barbeiro selecionado.
- Manter as operações na camada mock, sem chamadas Xano e sem persistência.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities
- `barber-workspace`: Regras observáveis para ações de status e tratamento de falhas na agenda do barbeiro.

## Impact

- Ações de atendimento em `app_barbearia/workspace_pages.py`, `app_barbearia/state.py` e `app_barbearia/mock_repository.py`.
- Testes em `tests/test_client_state.py` e `tests/test_mock_repository.py`.
- Nenhuma API ou dependência externa é alterada; os resultados são simulados e não persistidos.