# Design

## Context

A rota `/cadastro` reutiliza os campos e a composição de autenticação em `auth_pages.py`; `AppState` delega ao repositório mockado.

## Goals / Non-Goals

**Goals:**
- Preservar a composição visual e validar dados sem atribuição de papel pelo visitante.

**Non-Goals:**
- Criar uma conta persistida ou chamar endpoints reais.

## Decisions

- Manter o formulário em componentes compartilhados e gerar sempre papel `client` no mock.

## Risks / Trade-offs

- [O resultado pode parecer persistido] → Exibir a mensagem mockada de que nada foi salvo.
