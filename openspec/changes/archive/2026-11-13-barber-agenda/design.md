# Design

## Context

A página `/barbeiro` usa o layout compartilhado do espaço profissional e a agenda diária carregada pelo estado Reflex a partir do repositório mockado. A implementação já está concluída; esta change registra seu escopo individual.

## Goals / Non-Goals

**Goals:**
- Preservar a composição BarberFlow escura e dourada para o painel do barbeiro.
- Manter navegação de data, lista diária, indicadores e resumo do próximo atendimento coerentes entre si.
- Evitar exposição de campos de cliente que não sejam necessários ao atendimento.

**Non-Goals:**
- Integrar a agenda a endpoints reais do Xano nesta change.
- Criar ou alterar dados persistidos.

## Decisions

- Reutilizar o layout profissional e a projeção restrita de agendamentos existentes.
- Representar estados de carregamento, vazio e erro sem substituir falhas por dados demonstrativos de sucesso.
- Exibir datas e horários no fuso local da barbearia.

## Risks / Trade-offs

- Dados mockados podem ser confundidos com dados persistidos; as ações e mensagens devem continuar identificando operações como simuladas.
