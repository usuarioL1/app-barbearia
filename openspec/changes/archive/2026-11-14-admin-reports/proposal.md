# Proposal

## Why

Administradores precisam consultar o faturamento e o volume de atendimentos concluídos por dia ou mês sem incluir operações ainda não finalizadas. Esta mudança registra os relatórios apresentados pela aplicação com dados demonstrativos, sem confundi-los com resultados financeiros persistidos.

## What Changes

- Definir filtros diários e mensais e a apresentação de faturamento, contagem, ticket médio e resumo por serviço.
- Somar apenas preços snapshot de atendimentos concluídos no período local selecionado.
- Tratar dados vazios e falhas sem inventar métricas nem substituir resultados anteriores por sucesso.
- Manter a fonte mock, sem integração Xano ou persistência.

## Capabilities

### New Capabilities
- `admin-console`: Consulta administrativa de relatórios de faturamento e atendimentos concluídos.

### Modified Capabilities

Nenhuma.

## Impact

- Página de relatórios em `app_barbearia/workspace_pages.py`, consultas no estado e repositório mock.
- Testes em `tests/test_client_state.py` e `tests/test_mock_repository.py`.
- Nenhuma API ou dependência externa é alterada; os totais são demonstrativos.