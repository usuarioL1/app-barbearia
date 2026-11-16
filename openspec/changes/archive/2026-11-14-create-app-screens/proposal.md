# Proposal

## Why

O aplicativo precisa implementar as jornadas de cliente, barbeiro e administrador com base nos designs BarberFlow criados pelo usuário. As imagens fornecidas são a especificação visual do produto: as telas devem reproduzir sua composição, hierarquia, proporções e identidade preto/dourado em componentes Reflex, e não apenas adotar sua paleta como inspiração.

## What Changes

- Implementar as telas públicas de login, cadastro de cliente e recuperação de senha conforme os designs fornecidos.
- Implementar o portal do cliente, incluindo perfil, catálogo, equipe, agendamento, próximos atendimentos e histórico, reproduzindo os layouts fornecidos.
- Implementar o espaço do barbeiro com agenda, atendimentos e apresentação dos estados e ações conforme as referências.
- Implementar o console administrativo com dashboard, agenda, clientes, serviços, equipe, relatórios, usuários e configurações conforme as referências.
- Reproduzir em Reflex a navegação lateral, cabeçalhos, fundos, molduras douradas, cartões, tabelas, gráficos, calendário, campos e hierarquia visual das composições.
- Usar arquivos individuais de imagem existentes quando disponíveis; para logo, retratos e fundos não disponíveis individualmente, usar placeholders coerentes em código, sem substituir uma tela inteira por uma captura de tela.
- Manter as ações visuais coerentes com os designs; implementar comportamento com mocks apenas depois da revisão das telas e integrar banco e Xano na etapa final.

## Capabilities

### New Capabilities
- `customer-portal`: Telas e jornadas de autenticação visual, área do cliente, catálogo, perfil, agendamento, consulta e cancelamento dos próprios atendimentos.
- `barber-workspace`: Telas do barbeiro para visualizar sua agenda e apresentar ações de atendimento limitadas às transições permitidas.
- `admin-console`: Telas administrativas de resumo, agenda, cadastros operacionais e relatórios.

### Modified Capabilities

Nenhuma. O repositório não possui especificações de capabilities existentes.

## Impact

- Frontend Reflex em `app_barbearia/`, incluindo páginas, estado de apresentação, navegação e componentes compartilhados.
- As composições visuais fornecidas pelo usuário, mantidas em `assets/`, como referências de layout e aparência, não como telas rasterizadas de produção.
- Componentes Reflex para autenticação, navegação, cartões, agenda, tabelas, dashboard, relatórios e formulários; placeholders de imagens individuais onde não houver arquivos próprios.
- Após a conclusão visual, camada isolada de mocks para desenvolver interações antes da integração real.
- Banco de dados, scripts de autenticação e chamadas reais do Xano ficam adiados para a etapa final; nenhum schema ou conta existente será alterado antes dessa etapa.
- As regras funcionais finais permanecem alinhadas à especificação do projeto, incluindo papéis, estados canônicos, fuso `America/Sao_Paulo`, limites de cancelamento e snapshots de preço e duração.

## Decomposição

As jornadas de tela foram desmembradas em changes independentes por rota. Esta change registra o trabalho original concluído; o planejamento de integração real permanece em `xano-integration`.
