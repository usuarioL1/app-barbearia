# Design

## Context

A rota do perfil do barbeiro já é renderizada como um cartão estático em `workspace_pages.py`, com nome, função, especialidade e avatar de apresentação. Ela não usa formulário, evento de gravação ou estado de perfil editável.

## Goals / Non-Goals

**Goals:**
- Descrever com precisão a página informativa já existente.
- Manter a separação visual do perfil em relação às operações de atendimento.

**Non-Goals:**
- Adicionar edição de dados pessoais ou profissionais.
- Introduzir fonte de dados remota, sincronização ou persistência.

## Decisions

- Manter a apresentação como leitura somente; não conectar os controles de perfil do cliente nem criar handlers para a página do barbeiro, pois isso ampliaria o comportamento implementado.
- Tratar nome e especialidade exibidos como conteúdo de demonstração, não como atributos autenticados ou confirmados por um backend.

## Risks / Trade-offs

- [O conteúdo de demonstração pode não refletir o usuário autenticado] → Não apresentar a tela como perfil editável ou como fonte autoritativa.
- [A falta de edição pode limitar o uso real da rota] → Qualquer edição exige decisão e mudança separadas, com especificação própria.

## Migration Plan

Não há migração nem alteração de dados. Uma eventual edição de perfil deve ser planejada separadamente antes de conectar a rota a uma API.