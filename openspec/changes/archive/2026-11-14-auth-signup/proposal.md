# Proposal

## Why

A rota `/cadastro` já apresenta o formulário de criação de conta, mas sua jornada de cliente precisa de um contrato explícito para campos, validação e resultado. Esta mudança documenta somente o cadastro público existente, que nunca permite escolher um papel privilegiado.

## What Changes

- Definir o comportamento do formulário de cadastro de cliente em `/cadastro`, incluindo nome, e-mail, telefone, senha e confirmação.
- Registrar validação local e resposta do repositório mockado, sem afirmar persistência ou envio a um serviço externo.

## Capabilities

### New Capabilities

- `customer-portal`: Inicializa a jornada de cadastro público de cliente.

### Modified Capabilities

Nenhuma.

## Impact

- Tela Reflex em `app_barbearia/auth_pages.py`, handlers em `app_barbearia/state.py` e dados mockados em `app_barbearia/mock_repository.py`.
- Nenhuma alteração de aplicação é proposta; este change descreve a tela já implementada.