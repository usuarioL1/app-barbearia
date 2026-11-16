# Proposal

## Why

O cadastro público precisa de rastreabilidade própria, separado do login e da recuperação. A rota já está implementada com validação mockada, atribuindo sempre o papel de cliente.

## What Changes

- Registrar a tela `/cadastro`, validações e resultado mockado não persistente como entregues.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `customer-portal`: adicionar o contrato do cadastro público de cliente.

## Impact

- `app_barbearia/auth_pages.py` e eventos mockados de cadastro. A integração real fica em `xano-integration`.
