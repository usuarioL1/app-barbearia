# Proposal

## Why

O espaço do barbeiro inclui uma rota de perfil que precisa apresentar de forma clara a identidade profissional exibida pelo workspace. Esta mudança registra o escopo efetivamente implementado: uma visualização informativa, sem edição ou gravação de dados.

## What Changes

- Documentar a página de perfil do barbeiro com nome, função e especialidade exibidos.
- Manter a página como apresentação somente leitura, sem alegar edição de perfil.
- Registrar que os dados apresentados não são atualizados nem persistidos por integração com Xano.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities
- `barber-workspace`: Acrescenta o comportamento de apresentação do perfil profissional.

## Impact

- Página de perfil em `app_barbearia/workspace_pages.py`.
- Nenhuma API, estado de edição ou dependência externa é alterada.