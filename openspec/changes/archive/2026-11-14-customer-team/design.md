# Design

## Context

A rota `/equipe` usa o layout compartilhado do cliente em `customer_portal.py`. `AppState.load_catalog` consulta barbeiros ativos pelo repositório mockado, e cada cartão exibe nome, especialidade e um controle que inicia o agendamento.

## Goals / Non-Goals

**Goals:**
- Documentar somente a descoberta dos profissionais e a escolha inicial de barbeiro.
- Reutilizar os cartões e a navegação já existentes no portal.

**Non-Goals:**
- Apresentar agenda individual, dados pessoais de clientes ou transições de atendimento.

## Decisions

1. Manter a consulta da equipe junto à carga do catálogo compartilhado, apresentando apenas registros ativos.
2. Guardar a seleção em `AppState.selected_barber_id` e encaminhar o cliente à rota `/agendar`.
3. Exibir estados de carregamento e lista vazia no próprio painel da equipe.

## Risks / Trade-offs

- Os dados demonstrativos de especialidade e disponibilidade não substituem a confirmação de horário na jornada de agendamento.