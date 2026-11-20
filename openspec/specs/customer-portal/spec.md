# customer-portal Specification

## Purpose

O portal permite que clientes acessem suas jornadas de conta, serviços e agendamentos com privacidade e estados de operação claros.

## Requirements

### Requirement: Cliente acessa pela tela de login
A interface SHALL validar as credenciais e apresentar o resultado da autenticação sem expor ou salvar dados sensíveis no modo mockado.

#### Scenario: Credenciais inválidas no formulário
- **WHEN** o visitante envia um e-mail inválido ou deixa a senha vazia
- **THEN** a interface informa o erro de validação sem iniciar autenticação

#### Scenario: Autenticação mockada bem-sucedida
- **WHEN** o visitante envia credenciais de demonstração válidas
- **THEN** a interface apresenta o usuário de cliente e abre o portal, informando que a sessão não foi salva

#### Scenario: Autenticação recusada
- **WHEN** o repositório mockado recusa as credenciais
- **THEN** a interface informa a falha e não apresenta o acesso como bem-sucedido

### Requirement: Cliente acessa e mantém sua conta
A interface SHALL oferecer login, cadastro público de cliente, recuperação de senha e consulta/edição do próprio perfil, sem permitir que o cliente selecione ou altere o próprio papel.

#### Scenario: Cadastro público
- **WHEN** um visitante envia nome, e-mail, telefone e senha válidos no cadastro
- **THEN** a interface cria ou solicita a criação de uma conta com papel `client` e apresenta o resultado real da operação

#### Scenario: Credenciais inválidas
- **WHEN** login, cadastro ou recuperação de senha retorna erro de validação ou de autenticação
- **THEN** a interface identifica o campo ou a ação com erro e mantém os dados não sensíveis preenchidos

#### Scenario: Cliente consulta seu perfil
- **WHEN** um cliente autenticado abre ou edita a própria conta
- **THEN** a interface exibe somente os dados do usuário autenticado e comunica o resultado da atualização

### Requirement: Authentication and recovery use server-controlled identity
The client SHALL use the server-issued session and role, and SHALL NOT submit or choose a business role during public signup.

#### Scenario: Public signup
- **WHEN** a visitor submits valid registration details
- **THEN** the local signup contract creates a client account and the UI presents the server result without accepting a role from the request

#### Scenario: Invalid login
- **WHEN** the authentication service rejects credentials
- **THEN** the UI reports the failure and does not create or retain an authenticated session

#### Scenario: Password recovery
- **WHEN** a user requests and completes password recovery using a valid reset token
- **THEN** the reset token is single-use and expires according to the local XanoScript contract

### Requirement: Cliente descobre serviços e barbeiros disponíveis
A interface SHALL apresentar serviços ativos com descrição, preço em BRL e duração, além de barbeiros ativos e suas especialidades, sem expor dados pessoais de clientes.

#### Scenario: Catálogo disponível
- **WHEN** um cliente abre a tela de serviços
- **THEN** a interface lista os serviços e barbeiros ativos retornados pelo sistema e permite iniciar um agendamento a partir de uma seleção

#### Scenario: Catálogo vazio ou indisponível
- **WHEN** não há itens ativos ou a consulta falha
- **THEN** a interface mostra estado vazio ou erro compreensível e não oferece itens fictícios para agendamento

### Requirement: Profile and initial catalog use validated service responses
The client SHALL obtain the authenticated profile and initial service/barber catalog through the local Xano integration contracts, validate response shapes, and report failures without substituting mock results in Xano mode.

#### Scenario: Load profile and catalog
- **WHEN** a user loads their profile or the initial service/barber catalog
- **THEN** the UI presents the validated data returned by the selected repository

#### Scenario: Invalid or failed response
- **WHEN** an Xano request fails or returns an invalid response
- **THEN** the UI reports the error and does not present demo data as a successful Xano result

### Requirement: Cliente agenda um serviço com disponibilidade atual
A interface SHALL guiar o cliente pela seleção de serviço, barbeiro, data e horário, exibindo horários no fuso `America/Sao_Paulo` e confirmando a reserva somente após sucesso do backend.

#### Scenario: Escolha de horário válido
- **WHEN** o cliente seleciona serviço, barbeiro, data e um horário disponível retornado pelo backend
- **THEN** a interface apresenta o resumo com preço e duração e envia a solicitação de agendamento mediante confirmação explícita do cliente

#### Scenario: Horário deixa de estar disponível
- **WHEN** o backend recusa a criação por conflito ou indisponibilidade
- **THEN** a interface informa que o horário não está mais disponível e permite atualizar as opções sem criar uma confirmação local

#### Scenario: Falha ao consultar disponibilidade
- **WHEN** a disponibilidade não pode ser consultada por falha de rede ou do serviço
- **THEN** a interface apresenta o erro e não permite confirmar um horário baseado em dados desatualizados ou simulados

### Requirement: Cliente consulta e cancela somente seus agendamentos
A interface SHALL separar próximos agendamentos e histórico, exibir estados legíveis dos estados canônicos e respeitar a política de cancelamento do próprio cliente.

#### Scenario: Visualizar agendamentos
- **WHEN** o cliente autenticado abre seus agendamentos
- **THEN** a interface mostra somente registros pertencentes a ele, com data e hora locais, serviço, barbeiro e estado correspondente

#### Scenario: Cancelamento dentro do limite
- **WHEN** o cliente solicita cancelamento até 12 horas antes do início e o backend confirma
- **THEN** a interface atualiza o agendamento como cancelado e comunica o sucesso

#### Scenario: Cancelamento fora do limite ou recusado
- **WHEN** o cliente tenta cancelar depois do limite ou o backend recusa a operação
- **THEN** a interface mantém o estado retornado pelo sistema e explica que a ação não foi concluída

#### Scenario: Nenhum agendamento registrado
- **WHEN** o cliente abre a área de agendamentos sem registros
- **THEN** a interface exibe um estado vazio com acesso ao catálogo e à jornada de agendamento

### Requirement: Telas do cliente reproduzem os designs BarberFlow fornecidos
A interface do cliente SHALL seguir as referências de Dashboard, Serviços, Agendamentos, Histórico e Perfil, mantendo os dados e bindings existentes, layouts responsivos e componentes funcionais em vez de imagens de tela.

#### Scenario: Visitante acessa autenticação
- **WHEN** um visitante abre login, cadastro ou recuperação de senha
- **THEN** a interface preserva os formulários, campos, mensagens e ações existentes dentro da identidade visual BarberFlow

#### Scenario: Cliente usa a navegação compartilhada
- **WHEN** um cliente abre `/`, `/agendamentos`, `/servicos`, `/perfil`, `/historico` ou `/agendar`
- **THEN** a interface mantém links para Início, Meus Agendamentos, Serviços, Meu Perfil, Histórico e Sair, realça a rota ativa com fundo dourado e texto e ícone pretos, e identifica o usuário autenticado no cabeçalho

#### Scenario: Cliente navega pelo portal e catálogo
- **WHEN** um cliente abre o portal, serviços, equipe, perfil ou agendamentos
- **THEN** as telas mantêm a navegação, os dados, campos e ações suportados pelo sistema, organizados segundo a hierarquia visual da rota

#### Scenario: Dashboard apresenta dados do cliente
- **WHEN** um cliente abre `/`
- **THEN** a interface organiza próximo agendamento, chamada para agendar, até quatro serviços ativos, histórico recente e banner em cartões responsivos, usando somente dados carregados para a conta

#### Scenario: Catálogo permite pré-selecionar serviço
- **WHEN** um cliente abre `/servicos` e seleciona um serviço retornado pelo sistema
- **THEN** a interface apresenta os serviços disponíveis em cartões responsivos e inicia `/agendar` com o serviço selecionado pelo binding existente

#### Scenario: Agendamentos preservam ações suportadas
- **WHEN** um cliente alterna entre próximos agendamentos e histórico em `/agendamentos`
- **THEN** a interface usa os filtros existentes, mostra os dados do cliente e mantém o cancelamento sujeito à regra vigente de 12 horas, sem sucesso otimista

#### Scenario: Perfil preserva edição existente
- **WHEN** um cliente consulta e salva seu perfil
- **THEN** a interface apresenta e atualiza somente os campos suportados, usando o binding e o feedback existentes

#### Scenario: Cliente abre o fluxo de agendamento
- **WHEN** um cliente abre `/agendar` e seleciona serviço, barbeiro, data e horário disponível
- **THEN** a interface apresenta escolhas legíveis, calendário e resumo com a ação de confirmação ligada ao handler existente, sem alterar disponibilidade ou regra de negócio

#### Scenario: Layout estreito
- **WHEN** a largura disponível não comporta a composição desktop
- **THEN** a navegação, os cartões e os campos se reorganizam sem cortar conteúdo funcional ou exigir eventos novos

### Requirement: Campos do cadastro público
A rota `/cadastro` SHALL apresentar nome, e-mail, telefone, senha e confirmação e não oferecer um campo para escolher o papel da conta.

#### Scenario: Formulário de cadastro
- **WHEN** um visitante abre `/cadastro`
- **THEN** a tela apresenta os cinco campos de cadastro e não permite escolher um papel

### Requirement: Validação e submissão do cadastro
A interface SHALL validar os dados do cadastro antes de chamar o repositório mockado e apresentar o resultado como não persistido.

#### Scenario: Dados inválidos ou confirmação divergente
- **WHEN** o visitante envia dados obrigatórios inválidos ou senhas diferentes
- **THEN** a interface informa a validação e não chama o repositório

#### Scenario: Cadastro válido no modo mockado
- **WHEN** o visitante envia dados válidos e o repositório mockado aceita o cadastro
- **THEN** a interface apresenta o usuário com papel `client`, informa que a operação é simulada e não persistida, e segue para o portal

### Requirement: Consulta do perfil do cliente
A rota `/perfil` SHALL apresentar nome, e-mail e telefone do cliente corrente nos campos editáveis.

#### Scenario: Consultar perfil
- **WHEN** o cliente abre a tela de perfil
- **THEN** a interface apresenta os dados pessoais associados ao cliente corrente nos campos editáveis

### Requirement: Atualização mockada do perfil
A interface SHALL validar nome, e-mail e telefone antes de chamar o repositório mockado e apresentar o resultado sem indicar persistência.

#### Scenario: Dados inválidos
- **WHEN** o cliente envia nome vazio, e-mail inválido ou telefone inválido
- **THEN** a interface apresenta erro de validação e não chama a atualização do repositório

#### Scenario: Atualização aceita pelo mock
- **WHEN** o cliente envia dados válidos e o repositório mockado aceita a atualização
- **THEN** a interface atualiza os dados exibidos e comunica que a operação não foi persistida

#### Scenario: Atualização recusada
- **WHEN** o repositório mockado rejeita os dados
- **THEN** a interface informa o erro sem apresentar o salvamento como concluído

### Requirement: Equipe disponível para o cliente
A rota `/equipe` SHALL listar barbeiros ativos com nome e especialidade, sem dados pessoais de clientes.

#### Scenario: Equipe carregada
- **WHEN** a consulta mockada retorna barbeiros ativos
- **THEN** a tela apresenta os profissionais e suas especialidades sem dados de clientes

#### Scenario: Equipe vazia ou em carregamento
- **WHEN** a lista de barbeiros está vazia
- **THEN** a tela distingue o carregamento do estado sem profissionais disponíveis

### Requirement: Seleção de barbeiro para agendamento
A tela SHALL permitir iniciar a jornada `/agendar` com o barbeiro escolhido.

#### Scenario: Selecionar profissional
- **WHEN** o cliente aciona o botão de agendamento de um barbeiro
- **THEN** a interface abre `/agendar` com esse profissional selecionado

### Requirement: Lista de serviços ativos
A rota `/servicos` SHALL listar serviços ativos com nome, preço em BRL e duração e distinguir carregamento de lista vazia.

#### Scenario: Catálogo carregado
- **WHEN** a consulta mockada retorna serviços ativos
- **THEN** cada cartão mostra o nome, preço e duração do serviço

#### Scenario: Catálogo vazio ou em carregamento
- **WHEN** a lista de serviços está vazia
- **THEN** a tela distingue a consulta em andamento do estado sem serviços disponíveis

### Requirement: Busca e seleção de serviço
A tela SHALL filtrar os serviços carregados por texto e permitir iniciar um agendamento a partir do serviço selecionado.

#### Scenario: Busca sem correspondência
- **WHEN** o cliente pesquisa um termo sem correspondência entre os serviços carregados
- **THEN** a tela mostra o estado vazio da busca sem sugerir serviços indisponíveis

#### Scenario: Iniciar agendamento
- **WHEN** o cliente aciona “Agendar” em um serviço
- **THEN** a interface abre a jornada `/agendar` com esse serviço selecionado

### Requirement: Consulta dos próprios agendamentos
A rota `/agendamentos` SHALL apresentar próximos agendamentos e histórico do cliente corrente, oferecer filtros entre todos, próximos e histórico e mostrar estados vazios apropriados.

#### Scenario: Cliente possui registros
- **WHEN** o repositório selecionado retorna agendamentos do cliente corrente
- **THEN** a tela separa próximos atendimentos e histórico e permite alternar a visualização

#### Scenario: Cliente não possui registros
- **WHEN** a consulta do repositório selecionado retorna lista vazia e termina o carregamento
- **THEN** a tela mostra estados vazios e oferece acesso à jornada de agendamento

### Requirement: Cancelamento de agendamento do cliente
A interface SHALL permitir solicitar cancelamento de agendamento próprio pendente ou confirmado somente com pelo menos 12 horas de antecedência e refletir a resposta do repositório selecionado sem sucesso otimista.

#### Scenario: Cancelamento aceito
- **WHEN** o cliente solicita cancelar um de seus agendamentos elegíveis dentro do limite e o repositório selecionado confirma a operação
- **THEN** a tela atualiza o registro para cancelado e indica sucesso persistido em Xano ou simulado no modo mock

#### Scenario: Limite excedido, estado inelegível ou falha
- **WHEN** o cancelamento não é permitido ou o repositório selecionado retorna falha
- **THEN** a tela mantém o estado retornado pelo sistema sem alteração otimista e apresenta a mensagem de erro

### Requirement: Seleção de opções de agendamento
A rota `/agendar` SHALL permitir selecionar serviço e barbeiro ativos, data e horário retornado pela disponibilidade do repositório selecionado, apresentando calendário e resumo com preço e duração.

#### Scenario: Consultar disponibilidade
- **WHEN** o cliente abre o fluxo ou altera serviço, barbeiro ou data
- **THEN** a interface atualiza as opções de horário e o resumo conforme os dados do repositório selecionado e a seleção atual

#### Scenario: Horário disponível
- **WHEN** a consulta retorna horários para a seleção atual
- **THEN** o cliente pode selecionar um deles e revisar serviço, barbeiro, data, hora, preço e duração antes de confirmar

#### Scenario: Consulta de disponibilidade falha
- **WHEN** a consulta do repositório selecionado falha
- **THEN** a interface limpa os horários antigos e impede confirmar com uma opção desatualizada ou simulada em modo Xano

### Requirement: Confirmação simulada de agendamento
A interface SHALL habilitar a confirmação somente para um horário atualmente selecionado e disponível, tratando conflitos sem sucesso otimista.

#### Scenario: Confirmação aceita pelo mock
- **WHEN** o cliente confirma um horário disponível e o repositório mockado aceita a solicitação
- **THEN** a interface mostra os dados da confirmação e informa que nada foi salvo

#### Scenario: Confirmação persistida em Xano
- **WHEN** o cliente confirma um horário disponível e o Xano aceita a solicitação
- **THEN** a interface mostra os dados da reserva e identifica a operação como persistida

#### Scenario: Horário indisponível na confirmação
- **WHEN** o repositório selecionado rejeita a confirmação por conflito
- **THEN** a interface informa a indisponibilidade, limpa o horário selecionado e solicita atualização das opções sem indicar sucesso

### Requirement: Dashboard do cliente
A rota `/` SHALL apresentar a saudação do portal e os próximos agendamentos do cliente corrente, com estados de carregamento ou vazio e atalhos para perfil e lista completa.

#### Scenario: Cliente possui próximos agendamentos
- **WHEN** a consulta do repositório selecionado retorna próximos agendamentos
- **THEN** a tela inicial apresenta esses registros e oferece acesso a todos os agendamentos e ao perfil

#### Scenario: Cliente não possui próximos agendamentos
- **WHEN** a consulta retorna uma lista vazia e não está carregando
- **THEN** a tela apresenta o estado vazio no painel de próximos agendamentos

#### Scenario: Consulta em andamento
- **WHEN** a consulta do portal ainda está carregando
- **THEN** o painel apresenta um estado de carregamento em vez de tratar a ausência temporária como resultado final

### Requirement: Solicitação mockada de recuperação de senha
A rota `/recuperar-senha` SHALL solicitar o e-mail cadastrado, validar sua forma antes de consultar o repositório mockado e distinguir o resultado simulado de um link realmente enviado.

#### Scenario: E-mail inválido
- **WHEN** o visitante envia um e-mail sem formato válido
- **THEN** a interface apresenta erro de validação e não consulta o repositório

#### Scenario: Solicitação aceita no modo mockado
- **WHEN** o visitante envia um e-mail conhecido e o repositório mockado aceita a solicitação
- **THEN** a interface informa que a solicitação foi simulada e que nenhum link foi enviado

#### Scenario: Conta não encontrada
- **WHEN** o repositório mockado não encontra o e-mail informado
- **THEN** a interface apresenta a falha sem indicar que a recuperação foi concluída

### Requirement: Xano authentication uses server-controlled identity
When Xano mode is active, the account screens SHALL authenticate through Xano and use only the session token and user profile returned or confirmed by the server.

#### Scenario: Login succeeds
- **WHEN** a visitor submits valid credentials and `POST /auth/login` succeeds
- **THEN** the application establishes the session from the returned token and server profile, obtaining the profile from `GET /auth/me` when it is not included in the response

#### Scenario: Public signup succeeds
- **WHEN** a visitor submits valid name, email, phone, and password and `POST /auth/signup` succeeds
- **THEN** the application establishes the returned server session and presents the account as a client without sending or selecting a role

#### Scenario: Login or signup is rejected
- **WHEN** Xano rejects login or signup
- **THEN** the application reports the failure and does not retain an authenticated session or present the operation as successful

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

### Requirement: Password recovery uses Xano's public reset endpoints
When Xano mode is active, the recovery screens SHALL request and confirm password changes through the public Xano reset endpoints without sending the current session token.

#### Scenario: Reset is requested
- **WHEN** a visitor submits a valid email address
- **THEN** the application sends it to `POST /auth/password-reset` and displays only the response returned by the service

#### Scenario: Reset token is confirmed
- **WHEN** a visitor submits the email, one-time reset token, and a valid new password
- **THEN** the application sends them to `POST /auth/password-reset/confirm` and reports success only after Xano confirms the change

#### Scenario: Reset request or confirmation fails
- **WHEN** Xano rejects a reset request or confirmation
- **THEN** the application reports the failure without presenting a password change as completed

### Requirement: Customer catalog uses active Xano services and barbers
When Xano mode is active, the catalog SHALL load services and barbers from their public Xano endpoints and SHALL NOT offer demo records as available choices.

#### Scenario: Catalog loads
- **WHEN** a customer opens services or team in Xano mode
- **THEN** the application loads services from `GET /services` and barbers from `GET /barbers`, presenting validated active records

#### Scenario: Catalog is empty or unavailable
- **WHEN** an endpoint returns no active records or its request fails
- **THEN** the application shows an empty or error state and does not offer fictitious records for a booking

### Requirement: Cliente acessa seu histórico em uma rota dedicada
A rota `/historico` SHALL apresentar somente o histórico do cliente autenticado, sem introduzir registros, preços ou resumos não retornados ou derivados dos dados carregados.

#### Scenario: Histórico disponível
- **WHEN** o cliente autenticado abre `/historico` com atendimentos concluídos
- **THEN** a interface lista seus serviços, barbeiros, datas e horários locais, estados e preços disponíveis, com acesso consistente à navegação do portal

#### Scenario: Histórico vazio
- **WHEN** o cliente abre `/historico` sem atendimentos concluídos
- **THEN** a interface apresenta um estado vazio e não inventa registros ou totais

### Requirement: Controles ilustrativos não simulam operações indisponíveis
A interface SHALL desabilitar ou omitir ações de referência que não tenham suporte nos handlers e APIs existentes, sem indicar que uma operação foi realizada.

#### Scenario: Ação sem suporte
- **WHEN** uma referência inclui remarcar, detalhes, upload de foto, autenticação em duas etapas, sair de todos os dispositivos ou filtros sem binding existente
- **THEN** a interface omite o controle ou o apresenta desabilitado sem executar operação ou exibir sucesso

### Requirement: Fotografias locais são decorativas e não identificam usuários
As imagens fotográficas das telas do cliente SHALL ser servidas de assets locais e não apresentar recortes ilustrativos como retratos verificados de usuários ou profissionais nomeados.

#### Scenario: Imagens de serviço e banners
- **WHEN** uma tela do cliente apresenta fotografia de serviço ou ambiente
- **THEN** a imagem carrega de um asset local sem substituir o conteúdo funcional nem representar identidade pessoal verificada