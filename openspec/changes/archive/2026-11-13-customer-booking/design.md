# Design

## Context

A rota `/agendar` reúne seleções, calendário, horários, resumo e confirmação em `customer_portal.py`; estado e regras são mockados.

## Goals / Non-Goals

**Goals:**
- Manter as etapas visuais coerentes e impedir confirmação com disponibilidade obsoleta.

**Non-Goals:**
- Fazer reserva real ou chamar Xano.

## Decisions

- Usar o repositório mockado como fonte única das opções; limpar horários antigos quando a consulta falhar ou ocorrer conflito.

## Risks / Trade-offs

- [A confirmação simulada pode ser interpretada como persistida] → Informar que a ação não salvou dados.
