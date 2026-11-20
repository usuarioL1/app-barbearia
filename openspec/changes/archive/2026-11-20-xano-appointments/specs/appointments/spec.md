# Spec Delta

## Purpose

Define o ciclo de vida persistente dos agendamentos e a disponibilidade da barbearia, aplicando no backend as regras de negócio, autorização, privacidade e prevenção de conflitos.

## ADDED Requirements

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
