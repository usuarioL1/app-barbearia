# Proposal

## Why

A rota `/agendamentos` reúne os próximos atendimentos e o histórico do cliente, com filtros e ações de cancelamento. Seu contrato deve especificar que a consulta é restrita ao cliente corrente e que erros não alteram o estado apresentado.

## What Changes

- Definir separação e filtros de próximos agendamentos e histórico em `/agendamentos`.
- Documentar cancelamento mockado de registros próprios elegíveis, incluindo o limite de 12 horas e feedback de falha.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `customer-portal`: Acrescenta consulta e cancelamento dos agendamentos do cliente.

## Impact

- Tela em `app_barbearia/customer_portal.py`, estado compartilhado em `app_barbearia/state.py` e operações em `MockRepository`.
- Nenhuma alteração de aplicação é proposta.