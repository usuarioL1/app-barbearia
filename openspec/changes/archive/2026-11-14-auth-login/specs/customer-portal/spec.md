# Spec Delta

## Purpose

O portal permite que clientes acessem suas jornadas de conta, serviços e agendamentos com privacidade e estados de operação claros.

## ADDED Requirements

### Requirement: Cliente acessa pela tela de login
A interface SHALL validar as credenciais e apresentar o resultado da autenticação sem expor ou salvar dados sensíveis no modo mockado.

#### Scenario: Credenciais inválidas no formulário
- **WHEN** o visitante envia um e-mail inválido ou deixa a senha vazia
- **THEN** a interface informa o erro de validação sem iniciar autenticação

#### Scenario: Autenticação mockada bem-sucedida
- **WHEN** o visitante envia credenciais de demonstração válidas
- **THEN** a interface apresenta o usuário de cliente e abre o portal, informando que a sessão não foi salva

#### Scenario: Autenticação recusada
- **WHEN** o repositório mockado recusa as credenciais
- **THEN** a interface informa a falha e não apresenta o acesso como bem-sucedido