# Design

## Context

`AppState.load_admin_data` carrega barbeiros ativos e inativos via `MockRepository`; a página mostra nome, especialidade, estado e ações. O botão de criação usa valores fixos, enquanto editar/desativar enviam somente o ID. `MockRepository.admin_mutation` valida os campos obrigatórios para criação e não persiste. Ver `proposal.md` e `specs/admin-console/spec.md`.

## Goals / Non-Goals

**Goals:**
- Preservar a visualização de todos os registros da equipe no console.
- Acrescentar formulários mock com entradas reais e validação para manutenção.
- Manter somente barbeiros ativos disponíveis para novos agendamentos.

**Non-Goals:**
- Gravar dados, promover usuários a papéis privilegiados ou chamar Xano.
- Remover registros de barbeiros ou seus atendimentos históricos.

## Decisions

- Continuar usando a coleção `barbers` no estado administrativo e consultar ativos e inativos; o catálogo de agendamento permanece limitado aos barbeiros ativos.
- Encaminhar entradas para `MockRepository.admin_mutation` e apresentar claramente a natureza não persistente das respostas.
- Substituir payloads fixos por formulários para nome e especialidade e validar antes de confirmar a simulação.

## Risks / Trade-offs

- [Os botões atuais não coletam valores editáveis] → manter os formulários pendentes até testes comprovarem submissão, validação e falha.
- [Desativação mock pode ser interpretada como remoção real] → preservar os registros e informar que nada foi salvo.
- [Papéis de usuário não devem ser promovidos pelo console público] → manter qualquer provisionamento de administradores ou barbeiros fora deste fluxo mock.

## Migration Plan

Não há migração ou alteração de API. Completar e testar os formulários mock primeiro. Uma futura integração real deverá preservar os históricos e ser feita em mudança separada após aprovação da etapa Xano.