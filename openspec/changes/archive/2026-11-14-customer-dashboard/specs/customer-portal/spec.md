# Spec Delta

## ADDED Requirements

### Requirement: Dashboard do cliente
A rota `/` SHALL apresentar a saudação do portal e os próximos agendamentos do cliente corrente, com estados de carregamento ou vazio e atalhos para perfil e lista completa.

#### Scenario: Cliente possui próximos agendamentos
- **WHEN** a consulta mockada do portal retorna próximos agendamentos
- **THEN** a tela inicial apresenta esses registros e oferece acesso a todos os agendamentos e ao perfil

#### Scenario: Cliente não possui próximos agendamentos
- **WHEN** a consulta retorna uma lista vazia e não está carregando
- **THEN** a tela apresenta o estado vazio no painel de próximos agendamentos

#### Scenario: Consulta em andamento
- **WHEN** a consulta do portal ainda está carregando
- **THEN** o painel apresenta um estado de carregamento em vez de tratar a ausência temporária como resultado final