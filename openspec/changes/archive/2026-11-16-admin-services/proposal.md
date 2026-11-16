# Proposal

## Why

A tela de serviços precisa apresentar o catálogo administrativo e os controles de manutenção conforme a referência BarberFlow, preservando a distinção entre demonstração e alteração persistida. Esta mudança formaliza o comportamento já conectado à fonte mock.

## What Changes

- Definir a tabela de serviços com descrição, preço, duração e estado ativo/inativo.
- Registrar criação, edição e desativação como operações simuladas com validação mock.
- Não integrar endpoints, gravar cadastros nem remover serviços ou histórico nesta etapa.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities
- `admin-console`: Consulta e ações simuladas sobre serviços.

## Impact

- `app_barbearia/state.py`, `app_barbearia/mock_repository.py` e `app_barbearia/workspace_pages.py`.
- Testes do repositório mock e do tratamento de falhas administrativas; nenhuma API, dependência ou schema é alterado.