# Proposal

## Why

O barbeiro precisa consultar os atendimentos do dia sem depender de uma agenda genérica que exponha dados desnecessários dos clientes. Esta mudança registra o comportamento já implementado para a agenda diária, sua navegação por data e os estados sem resultados.

## What Changes

- Definir a visualização diária dos atendimentos atribuídos ao barbeiro atual.
- Apresentar horário local, serviço, nome do cliente e estado, sem expor identificadores ou e-mail do cliente.
- Permitir consultar outras datas e apresentar carregamento, falha e agenda vazia.
- Registrar que os dados vêm de mocks locais, sem chamadas Xano ou persistência.

## Capabilities

### New Capabilities
- `barber-workspace`: Consulta diária e restrita da agenda de trabalho do barbeiro.

### Modified Capabilities

Nenhuma.

## Impact

- Interface da agenda em `app_barbearia/workspace_pages.py`, estado em `app_barbearia/state.py` e dados em `app_barbearia/mock_repository.py`.
- Testes de estado e repositório em `tests/`.
- Nenhuma API ou dependência externa é alterada; os mocks não salvam dados.