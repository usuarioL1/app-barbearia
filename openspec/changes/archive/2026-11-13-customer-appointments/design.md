# Design

## Context

A rota `/agendamentos` separa próximos atendimentos e histórico usando o estado carregado para o cliente atual.

## Goals / Non-Goals

**Goals:**
- Preservar escopo do cliente, estados legíveis e resposta não otimista às ações.

**Non-Goals:**
- Consultar dados de outras contas ou persistir cancelamentos.

## Decisions

- Reutilizar as consultas mockadas com filtragem por proprietário e aplicar mudanças apenas após retorno bem-sucedido.

## Risks / Trade-offs

- [Falha em cancelar pode remover indevidamente um item] → Preservar a lista exibida quando o mock recusar a ação.
