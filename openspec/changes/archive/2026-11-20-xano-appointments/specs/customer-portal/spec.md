# Spec Delta

## MODIFIED Requirements

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
