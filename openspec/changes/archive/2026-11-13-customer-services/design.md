# Design

## Context

A rota `/servicos` apresenta o catálogo em `customer_portal.py`; `AppState` carrega registros do repositório mockado.

## Goals / Non-Goals

**Goals:**
- Exibir serviços ativos e seus dados de preço e duração mantendo a identidade BarberFlow.

**Non-Goals:**
- Criar, editar ou persistir serviços nesta tela de cliente.

## Decisions

- Reutilizar o carregamento mockado do catálogo e os componentes visuais existentes.

## Risks / Trade-offs

- [Catálogo indisponível não pode parecer completo] → Diferenciar erro, vazio e dados retornados.
