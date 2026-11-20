# appointments Specification

## Purpose

Define o ciclo de vida persistente dos agendamentos e a disponibilidade da barbearia, aplicando no backend as regras de negócio, autorização, privacidade e prevenção de conflitos.

## Requirements

### Requirement: Disponibilidade respeita expediente, duração e preparação
O sistema SHALL oferecer horários somente para serviço e barbeiro ativos, entre segunda-feira e sábado, das 09h às 18h em `America/Sao_Paulo`, respeitando a duração exata do serviço e 15 minutos de preparação após o atendimento.

#### Scenario: Horários válidos no expediente
- **WHEN** um cliente autenticado consulta horários para serviço, barbeiro e data válidos
- **THEN** a resposta contém somente inícios cuja duração e preparação cabem no expediente e que não conflitam com atendimentos não cancelados

#### Scenario: Dia ou opção indisponível
- **WHEN** a data não é dia útil de atendimento, ou o serviço ou barbeiro está inativo
- **THEN** o sistema não oferece horários para a seleção

#### Scenario: Janela de agendamento
- **WHEN** a data consultada contém horários no passado, com menos de duas horas de antecedência ou além de 30 dias
- **THEN** esses horários não são oferecidos

### Requirement: Criação de agendamento valida o cliente e captura snapshots
O sistema SHALL criar reservas somente para o cliente autenticado, validar as referências e regras de negócio no backend e preservar no agendamento o nome, preço e duração do serviço no momento da reserva.

#### Scenario: Reserva válida
- **WHEN** um cliente autenticado envia barbeiro, serviço e início ISO 8601 com fuso válidos e disponíveis
- **THEN** o sistema cria um agendamento `pending` com fim calculado pela duração snapshot e timestamps persistidos em UTC

#### Scenario: Campos ou referências inválidas
- **WHEN** a solicitação contém referência inexistente/inativa, horário fora das regras ou dado inválido
- **THEN** o sistema recusa a criação com erro apropriado e não cria agendamento nem histórico parcial

#### Scenario: Papel não cliente solicita reserva
- **WHEN** um usuário sem papel `client` tenta criar uma reserva de cliente
- **THEN** o sistema recusa a operação sem aceitar identidade de cliente fornecida no payload

### Requirement: Reservas concorrentes não ocupam o mesmo horário
O sistema SHALL garantir atomicamente que consultas de conflito e gravações não permitam intervalos ocupados sobrepostos para o mesmo barbeiro.

#### Scenario: Duas reservas concorrentes sobrepostas
- **WHEN** solicitações concorrentes tentam reservar intervalos sobrepostos para o mesmo barbeiro
- **THEN** no máximo uma é criada e as demais recebem `400` com o conflito identificável no envelope, sem registros parciais

#### Scenario: Intervalo de preparação
- **WHEN** uma nova reserva começa antes de 15 minutos após o fim de um atendimento existente não cancelado
- **THEN** o backend recusa a reserva como conflito

### Requirement: Criação e histórico inicial são consistentes
O sistema SHALL registrar a criação e seu primeiro evento de estado como uma única operação consistente, sem expor ou registrar credenciais, tokens ou dados desnecessários.

#### Scenario: Reserva registrada com auditoria
- **WHEN** uma reserva é criada com sucesso
- **THEN** o agendamento fica `pending` e seu histórico contém a transição inicial para `pending` com autor autenticado e horário UTC

#### Scenario: Falha ao registrar auditoria
- **WHEN** não é possível registrar o evento inicial de histórico
- **THEN** a criação é desfeita e nenhum agendamento incompleto é retornado como sucesso

### Requirement: Cliente acessa somente seus próprios agendamentos
O sistema SHALL permitir que clientes consultem suas próprias reservas, sem revelar dados ou registros pertencentes a outros clientes.

#### Scenario: Listagem do cliente autenticado
- **WHEN** um cliente consulta sua lista de agendamentos
- **THEN** a resposta contém somente reservas associadas à identidade da sessão e inclui os dados necessários para apresentar serviço, barbeiro, horário local e estado

#### Scenario: Consulta de reserva de outro cliente
- **WHEN** um cliente consulta diretamente uma reserva pertencente a outro usuário
- **THEN** o sistema não revela os dados dessa reserva e retorna acesso negado ou recurso não encontrado

### Requirement: Barbeiro e administrador acessam agendas conforme seu papel
O sistema SHALL restringir a agenda do barbeiro aos seus próprios atendimentos e permitir ao administrador consultar a agenda da unidade pelo período e filtros solicitados.

#### Scenario: Barbeiro consulta a própria agenda
- **WHEN** um barbeiro autenticado consulta uma data
- **THEN** a resposta contém somente atendimentos atribuídos ao seu perfil e expõe ao barbeiro apenas os dados do cliente necessários ao atendimento

#### Scenario: Barbeiro tenta consultar agenda alheia
- **WHEN** um barbeiro solicita atendimentos atribuídos a outro barbeiro
- **THEN** o sistema não revela esses registros

#### Scenario: Administrador consulta período filtrado
- **WHEN** um administrador autenticado consulta a agenda com período e filtros opcionais de barbeiro ou estado
- **THEN** a resposta contém somente registros correspondentes ao intervalo e aos filtros em `America/Sao_Paulo`

#### Scenario: Papel sem autorização consulta agenda administrativa
- **WHEN** um cliente ou barbeiro tenta consultar a agenda administrativa da unidade
- **THEN** o sistema recusa a solicitação sem expor registros fora de sua autorização

### Requirement: Cliente cancela somente reserva própria elegível
O sistema SHALL permitir ao cliente cancelar somente seu agendamento `pending` ou `confirmed` com pelo menos 12 horas antes do início, registrando autor, horário UTC e histórico.

#### Scenario: Cancelamento permitido
- **WHEN** o cliente autenticado cancela uma reserva própria elegível dentro do limite
- **THEN** o estado torna-se `cancelled` e o sistema grava `cancelled_at`, `cancelled_by` e o evento de histórico

#### Scenario: Cancelamento fora do prazo ou estado inelegível
- **WHEN** o cliente tenta cancelar depois do limite de 12 horas ou uma reserva em estado final
- **THEN** o sistema recusa a operação e mantém o estado e histórico inalterados

#### Scenario: Cliente tenta cancelar reserva alheia
- **WHEN** o cliente solicita cancelamento de uma reserva de outro usuário
- **THEN** o sistema recusa sem alterar ou revelar a reserva

### Requirement: Transições de estado são autorizadas e auditadas
O sistema SHALL permitir somente transições de estado válidas, autorizadas pelo papel e pela atribuição, e registrar cada transição com autor e horário UTC.

#### Scenario: Barbeiro ou administrador altera estado
- **WHEN** o barbeiro responsável ou um administrador solicita `pending` para `confirmed` ou `cancelled`, ou `confirmed` para `completed` ou `cancelled`
- **THEN** o sistema aplica a transição permitida e grava o evento correspondente no histórico

#### Scenario: Conclusão antes do término ou transição final
- **WHEN** o solicitante tenta concluir antes de `end_time`, reabrir um estado final ou executar outra transição não permitida
- **THEN** o sistema recusa a operação e preserva estado e histórico

#### Scenario: Barbeiro altera atendimento alheio
- **WHEN** um barbeiro tenta alterar atendimento que não está atribuído ao seu perfil
- **THEN** o sistema recusa a operação sem revelar dados não autorizados

### Requirement: API de agendamentos usa contratos e erros previsíveis
As operações de agendamento SHALL usar campos JSON estáveis em `snake_case`, horários ISO 8601 com fuso e erros coerentes com validação, autenticação, permissão, inexistência e conflito.

#### Scenario: Contratos de disponibilidade e reserva
- **WHEN** um cliente consulta disponibilidade ou confirma uma reserva
- **THEN** `GET /availability` recebe `barber_id`, `service_id` e `date` e retorna `{ "items": ["09:00", "..."] }`; `POST /appointments` recebe `barber_id`, `service_id` e `start_time` e, em sucesso, retorna `id`, `client_id`, `barber_id`, `service_id`, `service_title_snapshot`, `price_snapshot`, `duration_minutes_snapshot`, `start_time`, `end_time` e `status`
- **AND** os campos JSON permanecem em `snake_case`, os horários de reserva incluem o offset de `America/Sao_Paulo` e as respostas não incluem senha, token ou dados pessoais desnecessários

#### Scenario: Horário recebido ou devolvido pela API
- **WHEN** a API recebe ou retorna horário de agendamento
- **THEN** o valor inclui indicação de fuso e representa o mesmo instante que o timestamp UTC armazenado

#### Scenario: Solicitação sem sessão ou sem permissão
- **WHEN** uma operação protegida recebe sessão ausente/inválida ou papel não autorizado
- **THEN** a API retorna `401` ou `403`, respectivamente, sem indicar sucesso

#### Scenario: Erro de conflito
- **WHEN** uma solicitação de reserva colide com a agenda
- **THEN** a API retorna `400` no envelope `{"code":"ERROR_CODE_BAD_REQUEST","message":"appointment_conflict: ...","payload":""}` e não cria registros nem histórico parcial

### Requirement: Cliente remarca somente reserva própria elegível
O sistema SHALL permitir que um cliente altere data e horário de sua própria reserva `pending` ou `confirmed` com pelo menos 12 horas de antecedência, mantendo serviço e barbeiro.

#### Scenario: Remarcação autorizada
- **WHEN** o cliente autenticado solicita novo horário para reserva própria elegível
- **THEN** o backend valida a titularidade, a janela de 12 horas e as regras vigentes de disponibilidade antes de alterar a reserva

#### Scenario: Reserva inelegível ou fora do prazo
- **WHEN** a reserva pertence a outro cliente, está em estado final ou começa em menos de 12 horas
- **THEN** o backend recusa a remarcação e mantém a reserva inalterada

#### Scenario: Novo horário fora das regras
- **WHEN** o novo horário está no passado, fora da janela de agendamento, do expediente ou não corresponde a um horário atualmente disponível
- **THEN** o backend recusa a remarcação sem alterar serviço, barbeiro, horário ou estado da reserva

### Requirement: Remarcação preserva concorrência e histórico
O sistema SHALL aplicar a troca de horário como operação atômica, protegendo a agenda do barbeiro contra conflitos e registrando a alteração para auditoria.

#### Scenario: Remarcação válida sem conflito
- **WHEN** o novo intervalo permanece disponível após revalidação atômica
- **THEN** a reserva mantém seu estado, serviço, barbeiro e snapshots, recebe os novos horários de início e fim e registra autor, horário da alteração e horários anterior e novo

#### Scenario: Remarcações concorrentes
- **WHEN** duas solicitações concorrentes tentam ocupar intervalos sobrepostos para o mesmo barbeiro
- **THEN** no máximo uma é aplicada e as demais retornam conflito sem mudança parcial na reserva ou no histórico

#### Scenario: Conflito ou falha durante a operação
- **WHEN** a nova janela conflita com outra reserva ou não é possível concluir a auditoria
- **THEN** o backend preserva integralmente a reserva original e retorna erro sem sucesso

### Requirement: API de remarcação usa contrato seguro
A API SHALL aceitar remarcação somente com sessão autorizada e horário ISO 8601 com fuso, retornando um registro validado ou erro previsível.

#### Scenario: Remarcação por API
- **WHEN** o cliente envia `PATCH /appointments/{id}/reschedule` com `start_time` ISO 8601 e offset válido
- **THEN** a resposta de sucesso contém os campos canônicos do agendamento, usa `snake_case` e representa o horário local de `America/Sao_Paulo`

#### Scenario: Falta de sessão, permissão ou conflito
- **WHEN** a sessão é inválida, a reserva não pertence ao cliente ou o horário entra em conflito
- **THEN** a API retorna `401`, `403` ou erro `400` com código `appointment_conflict`, sem expor dados de terceiros ou indicar sucesso

### Requirement: Cliente consulta detalhes autorizados de uma reserva
O sistema SHALL fornecer os detalhes de uma reserva apenas ao cliente titular, ao barbeiro atribuído ou ao administrador autorizado.

#### Scenario: Consulta de detalhes própria
- **WHEN** um cliente autenticado solicita `GET /appointments/{id}` para sua própria reserva
- **THEN** a resposta apresenta os snapshots de serviço, valor e duração, barbeiro, início, fim e estado canônico necessários para exibir os detalhes

#### Scenario: Consulta de reserva alheia
- **WHEN** um cliente tenta consultar diretamente uma reserva de outro cliente
- **THEN** o backend nega ou não encontra o recurso sem revelar seus dados
