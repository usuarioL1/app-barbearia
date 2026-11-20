# Spec Delta

## ADDED Requirements

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
