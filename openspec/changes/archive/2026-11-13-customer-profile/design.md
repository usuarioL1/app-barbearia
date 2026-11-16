# Design

## Context

A rota `/perfil` apresenta e atualiza os dados do usuário atual com componentes compartilhados e repositório mockado.

## Goals / Non-Goals

**Goals:**
- Validar os campos e manter o resultado atualizado apenas na apresentação local.

**Non-Goals:**
- Salvar alterações no backend nesta etapa.

## Decisions

- Manter a consulta limitada ao identificador do usuário atual e atualizar a interface apenas após sucesso do mock.

## Risks / Trade-offs

- [Alteração local pode parecer permanente] → Reutilizar a mensagem explícita de não persistência.
