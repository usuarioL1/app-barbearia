# Design

## Context

A rota `/equipe` usa componentes de `customer_portal.py` e consulta a equipe ativa pela fonte mockada.

## Goals / Non-Goals

**Goals:**
- Apresentar nomes e especialidades na composição visual fornecida.

**Non-Goals:**
- Expor dados pessoais de clientes ou administrar barbeiros nesta rota.

## Decisions

- Compartilhar o carregamento do catálogo e manter a projeção de equipe mínima para exibição ao cliente.

## Risks / Trade-offs

- [Uma consulta vazia pode parecer falha] → Apresentar estado vazio separado de erro.
