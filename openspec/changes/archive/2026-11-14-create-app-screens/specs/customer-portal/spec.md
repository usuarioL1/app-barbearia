# Spec Delta

## Purpose

Define as jornadas visuais e os comportamentos da interface do cliente BarberFlow, desde o acesso à conta até a descoberta de serviços e o gerenciamento dos próprios agendamentos.

## ADDED Requirements

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
