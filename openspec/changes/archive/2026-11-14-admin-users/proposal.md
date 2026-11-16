# Proposal

## Why

O console administrativo precisa apresentar os usuários demonstrativos e os papéis atribuídos sem sugerir que ações de manutenção alteram uma base real. Esta mudança registra a listagem e o feedback das ações mockadas, mantendo explícita a ausência de persistência.

## What Changes

- Documentar a listagem de usuários demonstrativos com nome, e-mail e papel.
- Registrar as ações visuais de criação, edição e desativação como simulações que informam que nada foi salvo.
- Não declarar busca funcional, alteração persistente de usuário ou autorização real.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities
- `admin-console`: Acrescenta a consulta demonstrativa de usuários e o feedback não persistente das ações.

## Impact

- Página de usuários em `app_barbearia/workspace_pages.py`, estado em `app_barbearia/state.py` e repositório mock.
- Testes em `tests/test_client_state.py` e `tests/test_mock_repository.py`.
- Nenhuma API ou dependência externa é alterada; nenhuma ação mock persiste dados.