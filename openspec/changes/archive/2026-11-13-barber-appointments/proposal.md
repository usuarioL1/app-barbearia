# Proposal

## Why

A rota `/barbeiro/atendimentos` reúne os atendimentos ativos e as ações de status do barbeiro em uma tela própria, conforme o design BarberFlow.

## What Changes

- Registrar a listagem de atendimentos ativos, os estados exibidos e as ações de transição disponíveis ao barbeiro.
- Manter as ações ligadas aos mocks existentes, atualizando a interface somente após sucesso.

## Capabilities

### New Capabilities

### Modified Capabilities
- `barber-workspace`: Registrar a gestão mockada dos atendimentos do próprio barbeiro.

## Impact

- Rota Reflex `/barbeiro/atendimentos` e ações de status já conectadas à fonte mockada.
- Regras de estado e autorização da especificação do projeto permanecem aplicáveis.
