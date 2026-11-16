# Spec Delta

## Purpose

Define as jornadas administrativas do BarberFlow para acompanhar a operação da barbearia, gerenciar agenda e cadastros, e consultar relatórios e configurações.

## ADDED Requirements

### Requirement: Administrador acompanha o dashboard da barbearia
A rota `/admin` SHALL apresentar indicadores de operação, faturamento mensal, série de receita e agendamentos recentes conforme o design BarberFlow, usando os dados mockados sem alegar persistência.

#### Scenario: Dashboard com dados
- **WHEN** as consultas mockadas retornam os dados do período
- **THEN** a interface apresenta os indicadores e agendamentos recentes, contabilizando no faturamento apenas atendimentos concluídos

#### Scenario: Dashboard vazio ou indisponível
- **WHEN** não há agendamentos recentes ou uma consulta falha
- **THEN** a interface apresenta o estado vazio ou erro correspondente sem indicar que dados incompletos foram carregados com sucesso
