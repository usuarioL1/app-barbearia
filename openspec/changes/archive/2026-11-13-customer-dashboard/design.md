# Design

## Context

A rota `/` é construída em `customer_portal.py` e usa layout compartilhado, dados mockados e eventos de carregamento em `AppState`.

## Goals / Non-Goals

**Goals:**
- Preservar navegação, composição e estados de carregamento/erro da referência.

**Non-Goals:**
- Integrar a tela a endpoints reais.

## Decisions

- Reutilizar o layout de cliente e carregar o conteúdo pelo evento já registrado na rota.

## Risks / Trade-offs

- [Falha de consulta pode deixar dados desatualizados] → Preservar o estado anterior e exibir o erro.
