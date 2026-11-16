# Design

## Context

A rota `/barbeiro/perfil` usa o layout profissional compartilhado e apresenta as informações do profissional em um cartão visual com avatar de placeholder.

## Goals / Non-Goals

**Goals:**
- Preservar o visual BarberFlow e a identificação clara do profissional.
- Limitar o conteúdo às informações profissionais previstas na tela.

**Non-Goals:**
- Implementar edição de perfil ou persistência nesta change.
- Expor informações pessoais ou dados de clientes.

## Decisions

- Manter o avatar como elemento de apresentação local enquanto não houver asset individual aprovado.
- Apresentar nome, função e especialidade no cartão do perfil.

## Risks / Trade-offs

- O conteúdo demonstrativo não é uma fonte de identidade real; a integração futura deverá carregar o perfil autenticado.
