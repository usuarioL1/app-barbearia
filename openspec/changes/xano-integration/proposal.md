# Proposal

## Why

As jornadas por tela já funcionam com dados mockados, mas não persistem alterações nem consultam disponibilidade real. Uma change separada permite confirmar o schema e os contratos do Xano antes de substituir os mocks, sem misturar integração com a conclusão visual das telas.

## What Changes

- Inspecionar schema e papéis de usuário no workspace Xano indicado; confirmar suporte a `phone` e `client` antes de propor qualquer migração.
- Mapear os endpoints reais de autenticação, perfil, catálogo, disponibilidade, agendamentos e administração antes de conectá-los.
- Integrar as jornadas usando autorização, estados, fuso, conflitos e tratamento de erros previstos no contrato do projeto.
- Nesta execução, limitar as mudanças a arquivos locais XanoScript e ao frontend Reflex; não executar push, Meta API de escrita ou outra alteração remota.
- Manter tarefas de migração, implementação e validação pendentes até que os contratos e decisões necessários sejam confirmados.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `customer-portal`: autenticação, perfil, catálogo, disponibilidade e agendamentos deixam de ser apenas mockados após confirmação dos contratos.
- `barber-workspace`: agenda e transições passam a refletir respostas autorizadas do Xano.
- `admin-console`: consultas e operações administrativas passam a usar endpoints reais confirmados.

## Impact

- `app_barbearia/api_client.py`, estado Reflex e adaptadores entre os mocks e os endpoints confirmados.
- Scripts/schema Xano e workspace `149139`; em ambiente live-only, mudanças dependem de validação prévia, aprovação explícita de cada escrita e um caminho autorizado de escrita. Nenhuma conta existente será convertida automaticamente.
- Testes automatizados de contratos, validação, autorização e falhas. Nenhuma conta existente será convertida sem aprovação.
