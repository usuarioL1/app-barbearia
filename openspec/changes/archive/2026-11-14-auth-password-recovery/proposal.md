# Proposal

## Why

A rota `/recuperar-senha` já oferece um formulário de solicitação por e-mail. Documentar sua validação e resposta simulada deixa explícito o que a tela faz sem sugerir que um link real foi enviado.

## What Changes

- Definir o formulário de recuperação de senha em `/recuperar-senha`, sua validação de e-mail e o resultado informado ao visitante.
- Limitar o escopo à solicitação mockada de recuperação, sem descrever redefinição efetiva de credenciais.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `customer-portal`: Acrescenta a tela de solicitação de recuperação de senha.

## Impact

- Tela e rota Reflex em `app_barbearia/auth_pages.py` e handler em `app_barbearia/state.py`, usando `MockRepository.password_reset`.
- Nenhuma alteração de aplicação é proposta.