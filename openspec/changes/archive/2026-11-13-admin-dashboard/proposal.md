# Proposal

## Why

A rota `/admin` oferece a visão geral operacional da barbearia e precisa registrar separadamente o dashboard BarberFlow já implementado.

## What Changes

- Registrar indicadores de agendamentos, faturamento mensal, clientes e comparecimento.
- Registrar a série mensal de faturamento e a lista de agendamentos recentes alimentadas pelos dados mockados.

## Capabilities

### New Capabilities
- `admin-console`: Jornadas administrativas de dashboard, agenda, cadastros, relatórios, usuários e configurações.

### Modified Capabilities

Nenhuma.

## Impact

- Rota Reflex `/admin`, estado do dashboard e consultas do repositório mockado.
- Faturamento apresentado considera somente atendimentos concluídos e segue as regras do projeto.
