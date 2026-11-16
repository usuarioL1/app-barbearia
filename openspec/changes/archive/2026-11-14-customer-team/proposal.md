# Proposal

## Why

A rota `/equipe` ajuda o cliente a conhecer os profissionais ativos e iniciar um agendamento com um barbeiro selecionado. Seu contrato deve permanecer restrito à apresentação da equipe, sem expor dados de clientes.

## What Changes

- Definir a listagem de barbeiros ativos em `/equipe`, com nome, especialidade e ação de agendamento.
- Manter a seleção de horários e demais etapas na jornada própria de agendamento.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `customer-portal`: Acrescenta a descoberta da equipe pelo cliente.

## Impact

- Página Reflex em `app_barbearia/customer_portal.py` e dados carregados por `AppState.load_catalog` de `MockRepository.barbers`.
- Nenhuma alteração de aplicação é proposta.