# Spec Delta

## MODIFIED Requirements

### Requirement: Busca e seleção de serviço
A tela SHALL filtrar os serviços carregados por texto e permitir iniciar um agendamento a partir do serviço selecionado.

#### Scenario: Busca sem correspondência
- **WHEN** o cliente pesquisa um termo sem correspondência entre os serviços carregados
- **THEN** a tela mostra o estado vazio da busca sem sugerir serviços indisponíveis

#### Scenario: Iniciar agendamento
- **WHEN** o cliente aciona “Agendar” em um serviço
- **THEN** a interface abre a jornada `/agendar` com esse serviço selecionado

#### Scenario: Busca pelo nome do serviço
- **WHEN** o cliente digita o nome ou parte do nome de um serviço ativo
- **THEN** a tela filtra os serviços carregados sem consultar nem sugerir registros indisponíveis

### Requirement: Consulta dos próprios agendamentos
A rota `/agendamentos` SHALL apresentar o próximo agendamento em destaque, listar todos os próximos agendamentos ativos do cliente corrente e o histórico, oferecer filtros entre todos, próximos e histórico e mostrar estados vazios apropriados.

#### Scenario: Cliente possui registros
- **WHEN** o repositório selecionado retorna agendamentos do cliente corrente
- **THEN** a tela separa próximos atendimentos e histórico, permite alternar a visualização, destaca o agendamento mais próximo e lista todos os agendamentos ativos futuros em ordem cronológica

#### Scenario: Cliente gerencia próximos agendamentos
- **WHEN** um cliente tem vários agendamentos ativos futuros
- **THEN** cada registro aparece na lista completa, incluindo o próximo já destacado, com os dados e controles de cancelamento suportados para aquele registro

#### Scenario: Cliente não possui registros
- **WHEN** a consulta do repositório selecionado retorna lista vazia e termina o carregamento
- **THEN** a tela mostra estados vazios e oferece acesso à jornada de agendamento

#### Scenario: Filtrar agendamentos por período
- **WHEN** o cliente seleciona um período na rota `/agendamentos`
- **THEN** a tela mostra somente os agendamentos correspondentes ao intervalo local selecionado, sem alterar registros ou estados no backend

### Requirement: Xano profile operations are limited to the authenticated user
When Xano mode is active, the profile screen SHALL load and update only the authenticated user's profile through the authenticated profile endpoints.

#### Scenario: Profile is loaded
- **WHEN** an authenticated client opens the profile screen
- **THEN** the application obtains the current profile from `GET /auth/me` and displays only the returned user's permitted profile fields

#### Scenario: Profile is updated
- **WHEN** an authenticated client submits valid editable profile fields
- **THEN** the application sends those fields to `PATCH /auth/me` and presents the returned profile only after the backend confirms the update

#### Scenario: Profile update fails
- **WHEN** Xano rejects the update or the returned profile is invalid
- **THEN** the application preserves the current profile and reports that the update did not complete

#### Scenario: Nome e telefone são persistidos
- **WHEN** o cliente autenticado salva nome e telefone válidos
- **THEN** `PATCH /auth/me` atualiza somente a conta da sessão e a interface exibe os valores retornados pelo backend após sucesso

#### Scenario: URL de avatar é persistida
- **WHEN** o cliente autenticado salva uma URL de avatar HTTPS válida
- **THEN** o backend atualiza a URL somente na conta da sessão e `GET /auth/me` retorna o valor persistido sem aceitar URLs com esquema inseguro

### Requirement: Customer catalog uses active Xano services and barbers
When Xano mode is active, the catalog SHALL load services and barbers from their public Xano endpoints and SHALL NOT offer demo records as available choices.

#### Scenario: Catalog loads
- **WHEN** a customer opens services or team in Xano mode
- **THEN** the application loads services from `GET /services` and barbers from `GET /barbers`, presenting validated active records

#### Scenario: Catalog is empty or unavailable
- **WHEN** an endpoint returns no active records or its request fails
- **THEN** the application shows an empty or error state and does not offer fictitious records for a booking

#### Scenario: Aba Barbeiros no catálogo
- **WHEN** o cliente seleciona a aba “Barbeiros” em `/servicos`
- **THEN** a tela lista os barbeiros ativos retornados pelo repositório selecionado e permite iniciar `/agendar` com o barbeiro escolhido

### Requirement: Cliente acessa seu histórico em uma rota dedicada
A rota `/historico` SHALL apresentar somente o histórico do cliente autenticado, sem introduzir registros, preços ou resumos não retornados ou derivados dos dados carregados.

#### Scenario: Histórico disponível
- **WHEN** o cliente autenticado abre `/historico` com atendimentos concluídos
- **THEN** a interface lista seus serviços, barbeiros, datas e horários locais, estados e preços disponíveis, com acesso consistente à navegação do portal

#### Scenario: Histórico vazio
- **WHEN** o cliente abre `/historico` sem atendimentos concluídos
- **THEN** a interface apresenta um estado vazio e não inventa registros ou totais

#### Scenario: Filtrar por categoria e período
- **WHEN** o cliente seleciona “Todos”, “Cortes”, “Barba” ou “Combos” e um período
- **THEN** a tela filtra somente os registros históricos do cliente autenticado que correspondem aos critérios selecionados

### Requirement: Fotografias locais são decorativas e não identificam usuários
As imagens fotográficas das telas do cliente SHALL ser servidas de assets locais e não apresentar recortes ilustrativos como retratos verificados de usuários ou profissionais nomeados.

#### Scenario: Imagens de serviço e banners
- **WHEN** uma tela do cliente apresenta fotografia de serviço ou ambiente
- **THEN** a imagem carrega de um asset local sem substituir o conteúdo funcional nem representar identidade pessoal verificada

#### Scenario: Imagens distintas de Sobrancelha e Pezinho
- **WHEN** o catálogo apresenta Sobrancelha e Pezinho / Acabamento
- **THEN** cada serviço usa um asset local distinto com fotografia profissional adequada ao serviço, enquanto os assets atuais de Corte + Barba e Hidratação Capilar permanecem inalterados

## ADDED Requirements

### Requirement: Cliente consulta detalhes de um agendamento
A interface SHALL carregar e apresentar os detalhes de um agendamento próprio somente após autorização e resposta válida do repositório selecionado.

#### Scenario: Detalhes carregados
- **WHEN** o cliente solicita “Ver Detalhes” em um de seus agendamentos
- **THEN** a interface apresenta serviço, barbeiro, data, hora, valor e estado retornados pelo backend em uma visualização dedicada

#### Scenario: Detalhes indisponíveis ou não autorizados
- **WHEN** a consulta falha, retorna dados inválidos ou o agendamento não pertence ao cliente
- **THEN** a interface não exibe dados fictícios ou de terceiros e informa que os detalhes não puderam ser carregados

### Requirement: Cliente inicia a remarcação de um agendamento próprio
A interface SHALL permitir que o cliente solicite novo horário para um agendamento próprio elegível, mantendo serviço e barbeiro e aguardando confirmação do repositório.

#### Scenario: Selecionar novo horário disponível
- **WHEN** o cliente inicia a remarcação com pelo menos 12 horas antes do horário atual e seleciona uma opção retornada pela disponibilidade atual
- **THEN** a interface envia a solicitação para o repositório e atualiza o agendamento somente após confirmação

#### Scenario: Remarcação recusada ou indisponível
- **WHEN** o agendamento não é elegível, o horário deixou de estar disponível ou o repositório retorna falha
- **THEN** a interface preserva o horário confirmado anteriormente e informa que a remarcação não foi concluída
