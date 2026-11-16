# Proposal

## Why

O login é a entrada da jornada BarberFlow e precisa ter rastreabilidade própria, separada das demais rotas. A tela já foi implementada conforme a referência visual e usa autenticação mockada até a futura integração com Xano.

## What Changes

- Registrar a tela `/login`, seus estados de validação e a resposta não persistente da autenticação mockada como entregues.

## Capabilities

### New Capabilities

- `customer-portal`: Jornada de autenticação visual e acesso do cliente.

### Modified Capabilities

Nenhuma.

## Impact

- Página Reflex em `app_barbearia/auth_pages.py` e estado de autenticação mockada.
- Esta mudança registra a entrega existente; a autenticação real permanece na change `xano-integration`.
