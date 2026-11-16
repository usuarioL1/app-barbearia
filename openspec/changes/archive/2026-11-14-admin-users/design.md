# Design

## Context

A rota lê a lista do repositório mock e apresenta nome, e-mail e papel. Os controles visuais de criar, editar e desativar chamam a operação mock, que valida a entrada e retorna uma mensagem não persistente; ela não altera a fonte de usuários. O campo de busca não está conectado a um filtro.

## Goals / Non-Goals

**Goals:**
- Descrever a listagem de demonstração e deixar explícito o resultado não persistente das ações.
- Evitar que as permissões ilustrativas da tela sejam confundidas com controles de acesso efetivos.

**Non-Goals:**
- Persistir usuários ou implementar autenticação, autorização ou auditoria.
- Prometer busca, edição efetiva ou desativação que atualize os registros exibidos.

## Decisions

- Manter a lista como cópia dos dados mock, sem mutar o conjunto de origem após uma ação.
- Reutilizar o resultado e a mensagem da operação mock para informar sucesso simulado ou falha, sem feedback de persistência.
- Tratar os rótulos de papel e o quadro de permissões como conteúdo de apresentação, não como enforcement.

## Risks / Trade-offs

- [Ações e campo de busca podem parecer funcionais além do que são] → Especificar somente o feedback mock e registrar a busca funcional como lacuna.
- [A lista não reflete alterações simuladas] → Não apresentar ações mock como modificações dos registros nem como dados salvos.
- [Papéis exibidos não concedem permissões] → Implementar autorização no backend quando a integração real for planejada.

## Migration Plan

Não há migração. Para gestão real de usuários, definir antes contratos, papéis autorizáveis, validação, auditoria e regras de desativação.