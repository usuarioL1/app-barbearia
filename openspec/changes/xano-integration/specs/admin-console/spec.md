# Spec Delta

## ADDED Requirements

### Requirement: Administração opera somente endpoints confirmados e autorizados
A integração administrativa SHALL usar apenas endpoints existentes e confirmados, e SHALL apresentar o resultado real de cada consulta ou mutação.

#### Scenario: Consulta ou alteração autorizada
- **WHEN** um administrador autenticado consulta ou altera um cadastro ou agendamento por endpoint confirmado
- **THEN** a interface apresenta os dados ou o resultado retornado pelo Xano

#### Scenario: Erro de validação, autorização ou serviço
- **WHEN** o Xano recusa a consulta ou alteração, ou retorna uma resposta inválida
- **THEN** a interface informa a falha e não exibe dados ou alterações como sucesso persistido

### Requirement: Relatórios administrativos usam resultados reais concluídos
A integração SHALL calcular relatórios com os snapshots de preço dos agendamentos concluídos, agrupados pela data local do início do atendimento.

#### Scenario: Consulta de faturamento
- **WHEN** um administrador seleciona um período de relatório
- **THEN** o total considera somente atendimentos `completed` retornados pelo endpoint confirmado, respeitando o fuso da barbearia

#### Scenario: Relatório sem faturamento
- **WHEN** não há atendimentos concluídos no período ou a consulta falha
- **THEN** a interface diferencia total zero de erro de consulta e não usa dados mockados como resultado real
