# Proposal

## Why

O console administrativo precisa apresentar as configurações operacionais que orientam os horários e cancelamentos da barbearia. Esta mudança registra a tela informativa existente sem sugerir que os controles visuais alteram ou salvam configurações.

## What Changes

- Documentar a apresentação do expediente, fuso horário e política de cancelamento.
- Restringir o comportamento desta etapa à consulta visual; edição e persistência não são incluídas.
- Manter os valores alinhados à especificação do projeto e sem integração Xano.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities
- `admin-console`: Acrescenta a apresentação de configurações operacionais somente para leitura.

## Impact

- Página de configurações em `app_barbearia/workspace_pages.py`.
- Nenhuma API, estado de edição ou dependência externa é alterada; os valores são apresentados pela interface.