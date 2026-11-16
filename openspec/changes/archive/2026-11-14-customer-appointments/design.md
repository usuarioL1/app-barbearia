# Design

## Context

A rota `/agendamentos` em `customer_portal.py` mostra seções de próximos atendimentos e histórico, com filtros no `AppState`. A carga consulta `MockRepository.customer_appointments` para o identificador do cliente corrente; a ação de cancelamento atualiza a exibição somente após sucesso do mock.

## Goals / Non-Goals

**Goals:**
- Documentar consulta, filtros, estados vazios e cancelamento da tela existente.
- Preservar a política de cancelamento e a separação de registros por cliente.

**Non-Goals:**
- Acrescentar visualização administrativa, histórico de auditoria ou persistência.

## Decisions

1. Manter `customer_appointments` como fonte da tela e separar próximos e históricos em estado compartilhado.
2. Expor a ação de cancelamento apenas para estados pendente e confirmado; o repositório mockado valida propriedade e antecedência mínima de 12 horas.
3. Atualizar o estado local apenas após retorno bem-sucedido e preservar os registros em caso de falha.

## Risks / Trade-offs

- A consulta mockada representa somente o cliente corrente configurado no estado e não deve ser apresentada como autorização de uma sessão real.