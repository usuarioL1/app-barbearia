# Proposal

## Why

A rota `/servicos` permite descobrir serviços ativos e iniciar um agendamento a partir do catálogo. Documentar essa tela esclarece os dados exibidos e o comportamento da busca sem misturar a jornada da equipe ou a seleção de horário.

## What Changes

- Definir a listagem e busca de serviços na tela `/servicos`, incluindo preço, duração, estado vazio e ação de agendar.
- Limitar o escopo ao catálogo de serviços do cliente.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `customer-portal`: Acrescenta a descoberta e busca de serviços.

## Impact

- Página Reflex em `app_barbearia/customer_portal.py`; `AppState.load_catalog` e `MockRepository.services` fornecem os dados da tela.
- Nenhuma alteração de aplicação é proposta.