# Design

## Context

O dashboard administrativo já está montado em `workspace_pages.py` e consome estado carregado por `AppState`. `MockRepository` fornece os agendamentos, clientes e faturamento demonstrativos; o relógio e as datas seguem `America/Sao_Paulo`. A motivação e os comportamentos estão em `proposal.md` e `specs/admin-console/spec.md`.

## Goals / Non-Goals

**Goals:**
- Preservar a composição BarberFlow e os indicadores derivados da fonte mock.
- Não confundir valores demonstrativos com operações persistidas.

**Non-Goals:**
- Consultar Xano, alterar schema, autenticação ou introduzir métricas não definidas.
- Implementar relatórios ou gestão cadastral nesta mudança.

## Decisions

- Manter a consulta e a apresentação no fluxo existente `AppState` → `MockRepository` → componentes de página, em vez de criar uma camada paralela; isso reutiliza o isolamento e os estados de carregamento/erro já usados pelas telas.
- Calcular faturamento apenas com agendamentos `completed` e preço snapshot, agrupando pela data local; usar outra base de cálculo divergiría das regras do projeto.
- Exibir valores, período e agendamentos recentes como dados mock. Não introduzir cliente HTTP ou persistência antes da etapa Xano.

## Risks / Trade-offs

- [Os dados podem parecer reais] → manter mensagens das ações mock explícitas e evitar indicar persistência.
- [Indicadores podem mudar com as fixtures] → derivar os totais das fixtures, sem duplicar valores fixos na interface.

## Migration Plan

Não há migração ou alteração de API nesta etapa. A futura substituição da fonte mock por Xano é feita apenas na etapa de integração aprovada, mantendo o contrato visual e validando os cálculos com respostas reais.