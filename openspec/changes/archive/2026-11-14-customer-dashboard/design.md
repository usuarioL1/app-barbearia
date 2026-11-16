# Design

## Context

A página inicial Reflex em `customer_portal.py` exibe saudação, painel de próximos agendamentos e links para `/perfil` e `/agendamentos`. A rota carrega `AppState.load_client_portal`, que consulta o repositório mockado e separa os registros do cliente corrente.

## Goals / Non-Goals

**Goals:**
- Documentar o dashboard e seus estados de carregamento e vazio.
- Manter os atalhos e a composição visual atualmente usados pelo portal.

**Non-Goals:**
- Acrescentar métricas, recomendações, autenticação ou dados de outras jornadas.

## Decisions

1. Preservar a rota inicial e os componentes de portal existentes.
2. Usar `AppState.next_appointments` como apresentação dos próximos atendimentos, derivada da consulta mockada de agendamentos do cliente corrente.
3. Manter os estados de carregamento e vazio dentro do painel, sem inserir itens fictícios.

## Risks / Trade-offs

- O conjunto atual de demonstração depende do identificador de cliente mantido pelo estado compartilhado; os dados não representam uma consulta persistida de sessão.