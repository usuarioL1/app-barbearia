# Design

## Context

A tela atual representa a semana iniciada na segunda-feira da data selecionada, com uma grade de sete dias. `AppState` aplica os filtros por barbeiro e estado à consulta `MockRepository`, atualiza a grade após transições mock e preserva os resultados quando uma solicitação falha. A motivação e os comportamentos estão em `proposal.md` e `specs/admin-console/spec.md`.

## Goals / Non-Goals

**Goals:**
- Manter período, filtros e transições coerentes com os estados demonstrativos e com `America/Sao_Paulo`.
- Acrescentar uma apresentação diária reutilizando a consulta e os filtros já existentes.

**Non-Goals:**
- Mudar regras de disponibilidade, horários de funcionamento ou conectar a agenda ao Xano.
- Persistir transições ou atribuir dados privados fora do escopo administrativo.

## Decisions

- Manter uma única consulta de agenda e derivar as apresentações diária e semanal da data selecionada e dos filtros combinados; duplicar fontes de estado criaria resultados inconsistentes.
- Reutilizar as transições já validadas pelo repositório mock. A interface atualiza a sessão somente após sucesso e remove da lista o registro que deixa de corresponder ao filtro ativo.
- Tratar os registros e as mutações como demonstrativos, sem enviar ao cliente HTTP nem alegar que alterações foram salvas.

## Risks / Trade-offs

- [A tela existente só apresenta a grade semanal] → implementar e testar uma seleção explícita de visualização diária antes de considerar a agenda pronta para o requisito completo.
- [Falha ao trocar filtros poderia misturar período e resultados] → atualizar filtros e dados juntos após consulta bem-sucedida e preservar a seleção anterior em caso de erro.
- [Datas podem ser interpretadas em outro fuso] → apresentar as datas locais do domínio em `America/Sao_Paulo`.

## Migration Plan

Não há migração ou alteração de API nesta etapa. A visualização diária pode ser entregue junto da grade semanal sem modificar os registros mock; a integração real é posterior e fora deste change.