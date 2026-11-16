# Spec Delta

## ADDED Requirements

### Requirement: Visitante cria uma conta de cliente
A interface SHALL oferecer cadastro público com validação dos campos e papel de cliente fixado, sem simular persistência.

#### Scenario: Cadastro válido pela fonte mockada
- **WHEN** o visitante envia nome, e-mail, telefone e senha válidos e confirma a senha
- **THEN** a interface inicia a jornada do cliente e informa que os dados não foram salvos

#### Scenario: Dados inválidos ou senhas diferentes
- **WHEN** algum campo é inválido ou a confirmação não corresponde à senha
- **THEN** a interface identifica o erro e não apresenta o cadastro como concluído
