# Proposal

## Why

O acesso é uma jornada própria e precisa ser acompanhado independentemente das demais telas do cliente. Esta change registra a tela de login implementada, incluindo validação e autenticação por mocks, sem antecipar a integração com Xano.

## What Changes

- Documentar o login BarberFlow, seus estados de validação, carregamento, sucesso e erro.
- Manter credenciais e sessão de demonstração exclusivamente no repositório mockado, sem persistência nem chamadas HTTP.
- Preservar a composição visual preto/dourado e os controles acessíveis da referência.

## Capabilities

### New Capabilities
- `customer-portal`: Jornada de acesso do cliente, incluindo o formulário de login e seu resultado mockado.

### Modified Capabilities
- Nenhuma.

## Impact

- Tela `/login` em `app_barbearia/auth_pages.py`.
- Validação e estado de autenticação em `app_barbearia/state.py`, com dados isolados em `app_barbearia/mock_repository.py`.
- Testes em `tests/test_client_state.py` e `tests/test_mock_repository.py`. Xano permanece fora do escopo.