# Proposal

## Why

A rota `/agendar` reúne as escolhas de serviço, barbeiro, data e horário e só deve mostrar uma confirmação simulada após uma solicitação válida. Registrar esse contrato mantém explícitos os estados de disponibilidade e conflito já tratados pelo portal.

## What Changes

- Definir o fluxo de seleção e resumo do agendamento na tela `/agendar`, incluindo consulta mockada de horários e confirmação.
- Limitar o escopo à jornada de reserva do cliente, sem descrever as agendas de barbeiro ou administração.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `customer-portal`: Acrescenta a jornada de agendamento do cliente.

## Impact

- Tela Reflex em `app_barbearia/customer_portal.py`, handlers em `app_barbearia/state.py` e regras demonstrativas em `app_barbearia/mock_repository.py`.
- Nenhuma alteração de aplicação é proposta.