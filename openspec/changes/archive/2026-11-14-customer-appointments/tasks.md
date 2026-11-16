# Tasks

- [x] Exibir próximos atendimentos e histórico de `/agendamentos` com filtros, estados vazios e acesso à jornada de reserva.
- [x] Consultar apenas registros do cliente corrente; `test_customer_appointments_are_scoped_to_the_requested_client` verifica o escopo por cliente.
- [x] Restringir cancelamento a registros pendentes/confirmados dentro do limite de 12 horas e atualizar somente após sucesso; testes existentes verificam preservação em falha e resultado mockado não persistente.