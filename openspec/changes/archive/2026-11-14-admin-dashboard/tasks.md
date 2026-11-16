# Tasks

## 1. Dashboard demonstrativo

- [x] 1.1 Exibir período, indicadores operacionais e agendamentos recentes a partir do estado mock; verificar que a rota administrativa passa `reflex compile --dry`.
- [x] 1.2 Calcular faturamento somente com atendimentos concluídos e manter a fonte mock isolada da camada HTTP; verificar `test_revenue_counts_only_completed_demo_appointments`, `test_mock_operations_never_call_the_http_client` e a suíte `python -m unittest discover -s tests`.