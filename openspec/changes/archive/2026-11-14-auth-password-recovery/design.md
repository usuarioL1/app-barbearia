# Design

## Context

A aplicação registra `/recuperar-senha` em `app_barbearia/app_barbearia.py`. `password_reset_page` em `auth_pages.py` usa o formulário de autenticação compartilhado, vinculado a `AppState.request_password_reset` e `MockRepository.password_reset`.

## Goals / Non-Goals

**Goals:**
- Documentar a entrada de e-mail, a validação e o feedback da solicitação simulada.
- Preservar navegação de retorno ao login e o layout Reflex existente.

**Non-Goals:**
- Adicionar redefinição de senha, envio de e-mail ou persistência.

## Decisions

1. Reutilizar o formulário secundário de autenticação, variando seus campos para solicitar somente o e-mail cadastrado.
2. Manter validação e feedback no `AppState`, usando o repositório mockado como única fonte do resultado da demonstração.
3. Indicar explicitamente que nenhum link foi enviado quando a chamada mockada é aceita.

## Risks / Trade-offs

- O texto visual menciona um link de redefinição, mas a operação atual é simulada; o feedback de resultado deve evitar uma falsa promessa de envio.