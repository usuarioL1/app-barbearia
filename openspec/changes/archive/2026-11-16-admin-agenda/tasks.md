# Tasks

## 1. Agenda semanal e operações mock

- [x] 1.1 Exibir a grade semanal com navegação e filtros combináveis de barbeiro/estado; verificar `test_admin_filter_success_updates_period_filter_and_results_together`, `test_admin_filter_failure_keeps_previous_filter_and_results` e `reflex compile --dry`.
- [x] 1.2 Aplicar transições mock permitidas sem sucesso otimista e preservar resultados em falhas; verificar `test_admin_transition_removes_appointment_outside_active_filter`, `test_admin_mutation_failure_is_not_reported_as_persisted` e a suíte `python -m unittest discover -s tests`.

## 2. Visualização diária

- [x] 2.1 Adicionar alternância entre a grade semanal e a agenda de um dia, mantendo data e filtros; verificar que a visualização diária exibe somente registros da data selecionada e testar combinações de barbeiro/estado e período vazio.