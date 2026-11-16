# Tasks

- [x] Renderizar seleção de serviço, barbeiro, calendário, horários e resumo com preço e duração na rota `/agendar`.
- [x] Consultar disponibilidade mockada e descartar opções antigas em falha; `test_booking_availability_failure_discards_stale_slots` verifica esse comportamento.
- [x] Confirmar somente horário disponível e tratar conflito sem sucesso otimista; `test_booking_conflict_is_not_reported_as_success` e `test_booking_success_is_explicitly_non_persistent` cobrem os resultados e a não persistência.