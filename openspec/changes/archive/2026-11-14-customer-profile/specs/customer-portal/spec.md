# Spec Delta

## ADDED Requirements

### Requirement: Consulta do perfil do cliente
A rota `/perfil` SHALL apresentar nome, e-mail e telefone do cliente corrente nos campos editáveis.

#### Scenario: Consultar perfil
- **WHEN** o cliente abre a tela de perfil
- **THEN** a interface apresenta os dados pessoais associados ao cliente corrente nos campos editáveis

### Requirement: Atualização mockada do perfil
A interface SHALL validar nome, e-mail e telefone antes de chamar o repositório mockado e apresentar o resultado sem indicar persistência.

#### Scenario: Dados inválidos
- **WHEN** o cliente envia nome vazio, e-mail inválido ou telefone inválido
- **THEN** a interface apresenta erro de validação e não chama a atualização do repositório

#### Scenario: Atualização aceita pelo mock
- **WHEN** o cliente envia dados válidos e o repositório mockado aceita a atualização
- **THEN** a interface atualiza os dados exibidos e comunica que a operação não foi persistida

#### Scenario: Atualização recusada
- **WHEN** o repositório mockado rejeita os dados
- **THEN** a interface informa o erro sem apresentar o salvamento como concluído