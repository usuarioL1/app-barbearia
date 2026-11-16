# Spec Delta

## ADDED Requirements

### Requirement: Visitante solicita recuperação de senha
A interface SHALL validar o e-mail informado e apresentar o resultado da solicitação mockada sem enviar e-mail ou alegar que a conta foi alterada.

#### Scenario: E-mail válido
- **WHEN** o visitante envia um endereço de e-mail válido
- **THEN** a interface informa que a solicitação foi simulada e nenhum link foi enviado

#### Scenario: E-mail inválido
- **WHEN** o endereço informado não é válido
- **THEN** a interface mostra uma mensagem de validação e não simula sucesso
