# Design

## Context

A rota `/barbeiro/atendimentos` compartilha o layout profissional, apresenta a lista de atendimentos ativos e mantém uma legenda visual para os estados. As ações já usam o repositório mockado e aplicam a visão restrita do barbeiro.

## Goals / Non-Goals

**Goals:**
- Preservar a hierarquia BarberFlow entre lista de atendimentos e legenda de status.
- Atualizar a apresentação somente após retorno bem-sucedido da operação mockada.
- Respeitar o escopo do próprio barbeiro e as transições canônicas permitidas.

**Non-Goals:**
- Persistir transições ou integrar endpoints Xano nesta change.
- Criar novos estados de agendamento diferentes dos estados canônicos.

## Decisions

- Reutilizar os componentes de linha, badge e ações já presentes no painel.
- Manter o estado anterior e apresentar erro explícito quando a operação mockada falhar.

## Risks / Trade-offs

- O estado local simulado não equivale a uma atualização persistida; a interface deve deixar isso explícito.
