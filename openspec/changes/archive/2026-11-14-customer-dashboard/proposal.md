# Proposal

## Why

A rota inicial `/` é o ponto de entrada do portal do cliente e já reúne saudação, próximos agendamentos e acesso ao perfil. Seu escopo deve deixar claro que esses dados vêm da apresentação mockada do cliente corrente.

## What Changes

- Definir o conteúdo da tela inicial do cliente em `/`, incluindo próximos agendamentos, estados de carregamento/vazio e navegação relacionada.
- Descrever somente o dashboard; perfil, catálogo e demais jornadas permanecem em suas próprias mudanças.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `customer-portal`: Acrescenta o dashboard inicial do cliente.

## Impact

- Página Reflex em `app_barbearia/customer_portal.py`, estado compartilhado em `app_barbearia/state.py` e consulta a `MockRepository.customer_appointments`.
- Nenhuma alteração de aplicação é proposta.