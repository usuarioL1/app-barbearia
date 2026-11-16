# Spec Delta

## Purpose

Permite que administradores acompanhem os principais indicadores operacionais e o movimento da barbearia em um dashboard.

## ADDED Requirements

### Requirement: Dashboard apresenta um resumo operacional demonstrativo
O dashboard SHALL exibir o período consultado, contagem de agendamentos, faturamento mensal, clientes, comparecimento e agendamentos recentes a partir dos dados mock disponíveis.

#### Scenario: Dashboard carregado
- **WHEN** o administrador abre o dashboard e a consulta mock é concluída
- **THEN** a interface apresenta o período e os indicadores derivados dos registros demonstrativos, sem inventar métricas para dados ausentes

#### Scenario: Período sem registros
- **WHEN** o período consultado não contém agendamentos ou faturamento concluído
- **THEN** a interface apresenta o estado vazio ou valor zero correspondente, sem contar agendamentos não concluídos como faturamento

### Requirement: Dashboard não persiste dados demonstrativos
O dashboard SHALL obter seus dados exclusivamente da fonte mock isolada, sem enviar dados ao cliente HTTP ou gravar alterações em Xano.

#### Scenario: Consulta demonstrativa
- **WHEN** o dashboard carrega seus indicadores ou agendamentos recentes
- **THEN** os valores permanecem demonstrativos e nenhuma operação é apresentada como persistida