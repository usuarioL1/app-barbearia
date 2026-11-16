# Design

## Context

A rota `/admin` usa o console escuro e dourado compartilhado, com indicadores, gráfico mensal e painel de agendamentos recentes. Os dados já são carregados pelo estado Reflex a partir da fonte mockada.

## Goals / Non-Goals

**Goals:**
- Preservar a composição e hierarquia visual do dashboard BarberFlow.
- Apresentar indicadores e gráficos consistentes com os dados do período selecionado.
- Excluir atendimentos não concluídos do faturamento.

**Non-Goals:**
- Conectar o dashboard a endpoints Xano nesta change.
- Afirmar que os dados mockados representam operações persistidas.

## Decisions

- Reutilizar os componentes compartilhados de métricas, gráfico e lista de atendimentos recentes.
- Calcular a receita mensal a partir dos atendimentos concluídos, conforme a regra de negócio do projeto.

## Risks / Trade-offs

- Valores demonstrativos podem parecer financeiros reais; a integração posterior deve substituir a fonte sem alterar a regra do cálculo.
