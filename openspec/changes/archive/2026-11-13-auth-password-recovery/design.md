# Design

## Context

A rota `/recuperar-senha` reutiliza a estrutura Reflex de autenticação e delega a solicitação simulada ao repositório mockado.

## Goals / Non-Goals

**Goals:**
- Manter validação de e-mail e comunicação clara do resultado simulado.

**Non-Goals:**
- Enviar e-mail, criar token ou alterar credenciais.

## Decisions

- Não introduzir dependências; a solicitação permanece em memória e não usa HTTP.

## Risks / Trade-offs

- [A mensagem pode ser confundida com um link enviado] → Informar explicitamente que nenhum link foi enviado.
