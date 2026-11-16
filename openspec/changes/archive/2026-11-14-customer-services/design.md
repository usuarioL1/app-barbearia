# Design

## Context

A rota `/servicos` usa a página compartilhada do cliente em `customer_portal.py`. `AppState.load_catalog` carrega serviços e barbeiros ativos do `MockRepository`; a tela de serviços filtra a lista em estado e usa cartões com preço, duração e ação de agendamento.

## Goals / Non-Goals

**Goals:**
- Descrever a descoberta e busca dos serviços disponíveis na interface atual.
- Preservar cartões, navegação Serviços/Barbeiros e ação de início do agendamento.

**Non-Goals:**
- Incluir o catálogo da equipe ou implementar regras de disponibilidade nesta tela.

## Decisions

1. Manter o catálogo em `AppState.services`, com apresentação derivada por `filtered_services`.
2. Exibir os dados de preço e duração fornecidos pelo repositório mockado e encaminhar a seleção para `/agendar`.
3. Distinguir carregamento de lista vazia sem inventar opções.

## Risks / Trade-offs

- A busca opera sobre os dados mockados carregados; a tela não deve ser interpretada como confirmação de disponibilidade para reserva.