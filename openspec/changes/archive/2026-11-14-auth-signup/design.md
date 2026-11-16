# Design

## Context

A aplicação já registra `/cadastro` em `app_barbearia/app_barbearia.py`. `signup_page` em `auth_pages.py` reutiliza os campos públicos e liga os dados a `AppState.signup`; o estado valida a entrada e chama `MockRepository.signup`.

## Goals / Non-Goals

**Goals:**
- Documentar campos, validação, papel fixo `client` e feedback do cadastro simulado.
- Preservar a tela e os componentes Reflex existentes.

**Non-Goals:**
- Alterar código, adicionar etapas de confirmação ou declarar persistência de conta.

## Decisions

1. Manter a rota, o formulário compartilhado e os campos já vinculados ao estado.
2. Tratar o repositório mockado como fonte do resultado da demonstração; ele sempre devolve um cliente e não salva nem envia dados por HTTP.
3. Manter mensagens de validação e resultado no mecanismo de feedback existente.

## Risks / Trade-offs

- A resposta simulada pode ser confundida com uma conta persistida; o texto de sucesso deve continuar identificando a operação como simulada.