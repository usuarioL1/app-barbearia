# Design

## Context

A rota `/agendar` renderiza etapas, opções de serviço e barbeiro, calendário, horários e resumo em `customer_portal.py`. `AppState` carrega o catálogo, consulta disponibilidade e processa confirmação via `MockRepository`; nenhuma etapa usa transporte HTTP para a reserva mockada.

## Goals / Non-Goals

**Goals:**
- Documentar seleção, resumo, disponibilidade, confirmação e conflito da tela atual.
- Manter regras demonstrativas alinhadas a `America/Sao_Paulo`, duração do serviço e intervalo de preparação.

**Non-Goals:**
- Alterar o fluxo, conectar serviços externos ou afirmar que a reserva foi persistida.

## Decisions

1. Manter as escolhas e estados transitórios no `AppState` compartilhado pelas telas do cliente.
2. Buscar opções de serviço e barbeiro e horários de `MockRepository`; a confirmação é habilitada apenas quando há um horário disponível selecionado.
3. Em falha de disponibilidade ou conflito, descartar opções antigas; em sucesso simulado, exibir o resumo e a mensagem de não persistência.
4. Apresentar datas e horários no fuso local da barbearia, conforme a regra já usada pelo repositório mockado.

## Risks / Trade-offs

- Disponibilidade simulada pode mudar entre consulta e confirmação; o mock retorna conflito para opções vencidas e a interface exige nova seleção.