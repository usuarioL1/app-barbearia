# Spec Delta

## Purpose

Define as jornadas visuais e os comportamentos de acesso do cliente BarberFlow, incluindo a apresentação do login e os estados temporários de autenticação.

## ADDED Requirements

### Requirement: Visitante entra pela tela de login BarberFlow
A interface SHALL reconstruir a tela de login conforme o design fornecido e apresentar estados de validação e autenticação simulada sem alegar persistência.

#### Scenario: Login com credenciais aceitas pelo mock
- **WHEN** o visitante envia as credenciais válidas definidas pela fonte mockada
- **THEN** a interface inicia a jornada do cliente e informa que a autenticação não criou uma sessão persistida

#### Scenario: Login com entrada inválida ou credenciais recusadas
- **WHEN** os campos são inválidos ou a fonte mockada recusa as credenciais
- **THEN** a interface mostra uma mensagem de erro e não apresenta o acesso como bem-sucedido
