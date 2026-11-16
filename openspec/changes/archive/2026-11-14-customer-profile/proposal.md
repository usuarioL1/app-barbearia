# Proposal

## Why

A rota `/perfil` permite que o cliente revise e edite nome, e-mail e telefone. Documentar essa tela deixa claros os campos editáveis, validação e o caráter temporário das alterações no repositório mockado.

## What Changes

- Definir consulta e edição do perfil do cliente em `/perfil`, incluindo validação e feedback de salvamento.
- Limitar o escopo aos dados pessoais da tela de perfil.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `customer-portal`: Acrescenta a edição do próprio perfil do cliente.

## Impact

- Página Reflex em `app_barbearia/customer_portal.py`, estado em `app_barbearia/state.py` e atualização demonstrativa em `MockRepository.update_profile`.
- Nenhuma alteração de aplicação é proposta.