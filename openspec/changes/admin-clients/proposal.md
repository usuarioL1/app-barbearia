# Proposal

## Why

A equipe administrativa precisa consultar os registros demonstrativos de clientes e avaliar os controles de manutenção apresentados na tela BarberFlow. Esta mudança documenta a listagem e as ações simuladas sem sugerir que um cadastro foi realmente gravado.

## What Changes

- Definir a tabela de clientes com nome, telefone, quantidade de agendamentos e último atendimento, além da busca da lista.
- Registrar criação, edição e desativação como operações mock não persistentes, sem alterar cadastros.
- Excluir desta etapa alteração durável de cadastro e chamadas ao Xano.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities
- `admin-console`: Consulta e ações simuladas sobre clientes.

## Impact

- `app_barbearia/state.py`, `app_barbearia/mock_repository.py` e `app_barbearia/workspace_pages.py`.
- Testes do repositório mock e do tratamento de erros administrativos; nenhuma API, dependência ou schema é alterado.