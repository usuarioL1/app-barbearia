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

### Requirement: Cliente descobre serviços e barbeiros disponíveis
A interface SHALL apresentar serviços ativos com descrição, preço em BRL e duração, além de barbeiros ativos e suas especialidades, sem expor dados pessoais de clientes.

#### Scenario: Catálogo disponível
- **WHEN** um cliente abre a tela de serviços
- **THEN** a interface lista os serviços e barbeiros ativos retornados pelo sistema e permite iniciar um agendamento a partir de uma seleção

#### Scenario: Catálogo vazio ou indisponível
- **WHEN** não há itens ativos ou a consulta falha
- **THEN** a interface mostra estado vazio ou erro compreensível e não oferece itens fictícios para agendamento

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
A interface do cliente SHALL reconstruir os designs fornecidos como componentes, preservando estrutura, proporções, navegação, hierarquia e aparência preto/dourado. Composições inteiras não devem substituir as telas; assets individuais ausentes devem usar placeholders coerentes, sem acrescentar elementos visuais ausentes da referência.

#### Scenario: Visitante acessa autenticação
- **WHEN** um visitante abre login, cadastro ou recuperação de senha
- **THEN** a tela apresenta a composição, os campos, a navegação, os controles e a hierarquia visual correspondentes ao design BarberFlow fornecido

#### Scenario: Cliente navega pelo portal e catálogo
- **WHEN** o cliente abre o portal, o catálogo, seu perfil ou seus agendamentos
- **THEN** as telas mantêm a navegação lateral, cartões, informações e organização visual representadas nos designs correspondentes

#### Scenario: Cliente abre o fluxo de agendamento
- **WHEN** o cliente abre a jornada de agendamento
- **THEN** a interface apresenta as etapas, seleções de serviço e barbeiro, calendário, horários e resumo na composição visual fornecida, mantendo esses elementos como componentes da aplicação

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
- **WHEN** o repositório mockado retorna agendamentos do cliente corrente
- **THEN** a tela separa próximos atendimentos e histórico e permite alternar a visualização

#### Scenario: Cliente não possui registros
- **WHEN** a consulta retorna listas vazias e termina o carregamento
- **THEN** a tela mostra estados vazios e oferece acesso à jornada de agendamento

### Requirement: Cancelamento de agendamento do cliente
A interface SHALL permitir solicitar cancelamento de agendamento próprio pendente ou confirmado somente com pelo menos 12 horas de antecedência e refletir a resposta do repositório mockado sem sucesso otimista.

#### Scenario: Cancelamento aceito
- **WHEN** o cliente solicita cancelar um de seus agendamentos elegíveis dentro do limite e o mock aceita
- **THEN** a tela atualiza o registro para cancelado e identifica a operação como simulada

#### Scenario: Limite excedido, estado inelegível ou falha
- **WHEN** o cancelamento não é permitido ou o repositório retorna falha
- **THEN** a tela mantém o registro exibido sem alteração e apresenta a mensagem de erro

### Requirement: Seleção de opções de agendamento
A rota `/agendar` SHALL permitir selecionar serviço e barbeiro ativos, data e horário retornado pela disponibilidade mockada, apresentando calendário e resumo com preço e duração.

#### Scenario: Consultar disponibilidade
- **WHEN** o cliente abre o fluxo ou altera serviço, barbeiro ou data
- **THEN** a interface atualiza as opções de horário e o resumo conforme os dados selecionados

#### Scenario: Horário disponível
- **WHEN** a consulta retorna horários para a seleção atual
- **THEN** o cliente pode selecionar um deles e revisar serviço, barbeiro, data, hora, preço e duração antes de confirmar

#### Scenario: Consulta de disponibilidade falha
- **WHEN** a consulta mockada falha
- **THEN** a interface limpa os horários antigos e impede confirmar com uma opção desatualizada

### Requirement: Confirmação simulada de agendamento
A interface SHALL habilitar a confirmação somente para um horário atualmente selecionado e disponível, tratando conflitos sem apresentar sucesso nem persistir uma reserva.

#### Scenario: Confirmação aceita pelo mock
- **WHEN** o cliente confirma um horário disponível e o repositório mockado aceita a solicitação
- **THEN** a interface mostra os dados da confirmação e informa que nada foi salvo

#### Scenario: Horário indisponível na confirmação
- **WHEN** o repositório mockado rejeita a confirmação por conflito
- **THEN** a interface informa a indisponibilidade, limpa o horário selecionado e solicita atualização das opções

### Requirement: Dashboard do cliente
A rota `/` SHALL apresentar a saudação do portal e os próximos agendamentos do cliente corrente, com estados de carregamento ou vazio e atalhos para perfil e lista completa.

#### Scenario: Cliente possui próximos agendamentos
- **WHEN** a consulta mockada do portal retorna próximos agendamentos
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