# Tasks

## 1. Consulta de relatórios

- [x] 1.1 Conectar seleção diária/mensal e data aos indicadores do relatório; verificar filtros, totais e resumo por serviço com `test_admin_report_uses_only_completed_demo_appointments`.
- [x] 1.2 Calcular faturamento somente com atendimentos concluídos e retornar zero em período vazio; verificar com `test_revenue_counts_only_completed_demo_appointments`.
- [x] 1.3 Preservar os indicadores anteriores quando a consulta falha; verificar com `test_admin_report_failure_preserves_previous_totals`.

## 2. Apresentação

- [x] 2.1 Renderizar filtros, métricas e gráficos na rota de relatórios sem apresentar os dados como persistidos; verificar a página Reflex e executar `reflex compile --dry`.