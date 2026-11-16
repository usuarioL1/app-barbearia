# Design

## Context

`AppState.load_admin_data` consulta os serviços ativos e inativos em `MockRepository`; a página mostra título, descrição, preço, duração e estado. A criação envia valores fixos e as ações de edição/desativação enviam apenas o identificador, sem alterar a lista. A validação mock de criação exige título, preço e duração positivos. Ver `proposal.md` e `specs/admin-console/spec.md`.

## Goals / Non-Goals

**Goals:**
- Preservar a visualização administrativa de todos os serviços, inclusive inativos.
- Permitir inserir e validar valores de criação/edição no fluxo mock, sem persistência.
- Manter somente serviços ativos disponíveis em novos agendamentos.

**Non-Goals:**
- Alterar registros reais, apagar histórico, chamar Xano ou modificar schema.
- Alterar regras de preço snapshot ou de faturamento.

## Decisions

- Manter a consulta administrativa com `active_only=False`, enquanto as opções de novos agendamentos continuam restritas a `active_only=True`; isso conserva o histórico visível sem oferecer serviço inativo para reserva.
- Reutilizar `MockRepository.admin_mutation` para validar entradas e manter respostas explicitamente não persistentes.
- Substituir payloads fixos por campos de formulário para título, descrição, preço e duração. Preservar a validação de preço e duração positivos antes de emitir sucesso mock.

## Risks / Trade-offs

- [Os botões atuais não coletam valores editáveis] → deixar os formulários como tarefa pendente até haver testes de submissão, validação e falha.
- [Desativação mock pode ser confundida com retirada real do catálogo] → não atualizar o estado do registro e informar que nada foi salvo.
- [Um serviço inativo pode aparecer em consulta de agendamentos antigos] → manter o registro administrativo e o histórico; excluir da seleção de novos agendamentos.

## Migration Plan

Não há migração ou mudança de API. Completar e testar os formulários mock primeiro. Qualquer integração real com Xano e preservação persistente de histórico pertence à etapa aprovada de integração.