# Design

## Context

A página apresenta as ações de atendimento por meio do estado Reflex. O repositório mock aplica as transições canônicas, valida a atribuição do atendimento e impede conclusão antes do horário de término; seu resultado nunca persiste nem chama o cliente HTTP.

## Goals / Non-Goals

**Goals:**
- Manter interface e estado em sincronia somente após uma transição simulada aceita.
- Preservar informações já exibidas e mostrar erro quando a operação falhar.

**Non-Goals:**
- Registrar histórico durável, identidade autenticada ou auditoria de status.
- Implementar chamadas reais ao Xano ou alegar persistência da transição.

## Decisions

- Centralizar a validação de estado, escopo do barbeiro e horário de término no repositório mock; a página não decide por conta própria que a mudança foi concluída.
- Atualizar a lista local apenas depois de um resultado bem-sucedido e projetá-la novamente para omitir campos pessoais desnecessários.
- Usar os estados canônicos definidos pela especificação do projeto, sem inventar estados adicionais a partir dos rótulos visuais.

## Risks / Trade-offs

- [O mock não substitui autorização e transação no servidor] → Tratar a validação local somente como comportamento demonstrativo; a integração futura deve repetir as regras no backend.
- [O horário fixo dos dados simulados não representa o relógio de produção] → Não considerar as verificações mock como garantia operacional.

## Migration Plan

Não há migração. Na etapa de integração, conectar a operação a um endpoint autorizado e manter o estado anterior quando o servidor recusar a transição.