# Design

## Context

A rota do console administrativo apresenta cartões estáticos com expediente, fuso e política de cancelamento. Os botões de edição são elementos visuais sem fluxo de alteração conectado; não há estado de configurações nem gravação no repositório mock.

## Goals / Non-Goals

**Goals:**
- Registrar a exibição dos valores operacionais já presentes na interface.
- Evitar que a tela sugira uma alteração salva quando não existe fluxo de edição.

**Non-Goals:**
- Criar formulários, handlers ou armazenamento para as configurações.
- Alterar horário da unidade, fuso ou política definida no projeto.

## Decisions

- Manter os valores visíveis como informação estática alinhada à especificação do projeto.
- Descrever explicitamente o limite de somente leitura; não conectar os botões visuais a mutações administrativas mockadas, pois elas não oferecem suporte a validação e estado de configurações.
- Deixar persistência e autorização de alterações para uma mudança futura com contratos confirmados.

## Risks / Trade-offs

- [Os botões visuais podem sugerir edição disponível] → A especificação deste escopo não promete edição nem salvamento; revisar a affordance em uma mudança futura.
- [Valores estáticos não acompanham alterações de operação] → Confirmar qualquer mudança de negócio e sua fonte antes de introduzir edição.

## Migration Plan

Não há migração. Uma futura edição de configurações exige definir valores editáveis, validação, autorização e persistência antes de alterar o comportamento.