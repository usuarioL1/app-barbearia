# Spec Delta

## ADDED Requirements

### Requirement: Cliente consulta o catálogo de serviços
A rota de serviços SHALL apresentar os registros ativos retornados pela fonte mockada, com descrição, preço e duração, sem oferecer itens fictícios após erro ou resultado vazio.

#### Scenario: Catálogo com serviços ativos
- **WHEN** a consulta mockada retorna serviços ativos
- **THEN** a interface apresenta os serviços e permite iniciar o agendamento a partir de uma seleção

#### Scenario: Catálogo vazio ou indisponível
- **WHEN** a consulta não retorna itens ou falha
- **THEN** a interface apresenta estado vazio ou erro e não declara sucesso
