# Spec Delta

## MODIFIED Requirements

### Requirement: Console administrativo reproduz os designs BarberFlow fornecidos
A interface administrativa SHALL aplicar a identidade preto, carvão e dourado às rotas administrativas existentes, organizando navegação, filtros e conteúdo de cada tela segundo a referência correspondente, sem substituir componentes por capturas de tela nem inventar indicadores, registros ou ações.

#### Scenario: Administrador navega pelo console
- **WHEN** o administrador abre dashboard, agenda, clientes, serviços, equipe ou usuários
- **THEN** a interface apresenta a navegação lateral com rota ativa, cabeçalho e cartões, tabelas ou agenda adequados aos dados e às ações existentes

#### Scenario: Administrador consulta relatórios e configurações
- **WHEN** o administrador abre relatórios ou configurações
- **THEN** a interface mantém a hierarquia, os filtros e os agrupamentos visuais correspondentes, sem alterar permissões, métricas disponíveis ou o caráter informativo das configurações

#### Scenario: Administrador usa o console em uma tela estreita
- **WHEN** a largura disponível não comporta o layout desktop
- **THEN** a navegação, os filtros, os cartões e as tabelas se reorganizam sem ocultar controles, dados, mensagens ou ações existentes
