# Spec Delta

## ADDED Requirements

### Requirement: Cliente acessa o portal inicial
A rota inicial SHALL apresentar o portal do cliente conforme o design BarberFlow, com navegação para as jornadas disponíveis e conteúdo demonstrativo sem alegação de persistência.

#### Scenario: Cliente abre o portal
- **WHEN** o cliente abre a rota inicial
- **THEN** a interface apresenta a composição do portal e seus atalhos navegáveis

#### Scenario: Portal inicial não pode carregar os dados
- **WHEN** a consulta mockada do portal falha
- **THEN** a interface informa o erro sem apresentar o carregamento como sucesso
