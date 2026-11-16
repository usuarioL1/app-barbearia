# Spec Delta

## ADDED Requirements

### Requirement: Solicitação mockada de recuperação de senha
A rota `/recuperar-senha` SHALL solicitar o e-mail cadastrado, validar sua forma antes de consultar o repositório mockado e distinguir o resultado simulado de um link realmente enviado.

#### Scenario: E-mail inválido
- **WHEN** o visitante envia um e-mail sem formato válido
- **THEN** a interface apresenta erro de validação e não consulta o repositório

#### Scenario: Solicitação aceita no modo mockado
- **WHEN** o visitante envia um e-mail conhecido e o repositório mockado aceita a solicitação
- **THEN** a interface informa que a solicitação foi simulada e que nenhum link foi enviado

#### Scenario: Conta não encontrada
- **WHEN** o repositório mockado não encontra o e-mail informado
- **THEN** a interface apresenta a falha sem indicar que a recuperação foi concluída