# Spec Delta

## Purpose

Esta capability permite que administradores acompanhem a operação da barbearia por meio de telas de gestão e indicadores. Nesta etapa, os relatórios usam dados demonstrativos e não representam valores financeiros persistidos.

## ADDED Requirements

### Requirement: Administrador consulta relatórios de faturamento por período
A interface SHALL permitir escolher relatório diário ou mensal e apresentar faturamento, quantidade de atendimentos concluídos e indicadores derivados dos registros disponíveis.

#### Scenario: Relatório diário ou mensal
- **WHEN** o administrador seleciona o período e a data do relatório
- **THEN** a interface atualiza os indicadores para o período local selecionado em `America/Sao_Paulo`

#### Scenario: Período sem faturamento
- **WHEN** não há atendimentos concluídos no período selecionado
- **THEN** o relatório apresenta faturamento zero e não inclui atendimentos pendentes, confirmados ou cancelados

### Requirement: Faturamento considera somente atendimentos concluídos
O relatório SHALL somar o preço snapshot de cada atendimento concluído cuja data local de início pertença ao período selecionado.

#### Scenario: Soma do faturamento
- **WHEN** existem atendimentos concluídos e não concluídos no período
- **THEN** o total usa somente os preços snapshot dos atendimentos concluídos com datas locais dentro do período

#### Scenario: Falha ao carregar o relatório
- **WHEN** a consulta do relatório falha
- **THEN** a interface informa a falha e preserva os indicadores anteriormente carregados