# Spec Delta

## Purpose

Definir a jornada pública de cadastro de cliente no portal, com validação dos dados exigidos e papel de cliente fixo.

## ADDED Requirements

### Requirement: Campos do cadastro público
A rota `/cadastro` SHALL apresentar nome, e-mail, telefone, senha e confirmação e não oferecer um campo para escolher o papel da conta.

#### Scenario: Formulário de cadastro
- **WHEN** um visitante abre `/cadastro`
- **THEN** a tela apresenta os cinco campos de cadastro e não permite escolher um papel

### Requirement: Validação e submissão do cadastro
A interface SHALL validar os dados do cadastro antes de chamar o repositório mockado e apresentar o resultado como não persistido.

#### Scenario: Dados inválidos ou confirmação divergente
- **WHEN** o visitante envia dados obrigatórios inválidos ou senhas diferentes
- **THEN** a interface informa a validação e não chama o repositório

#### Scenario: Cadastro válido no modo mockado
- **WHEN** o visitante envia dados válidos e o repositório mockado aceita o cadastro
- **THEN** a interface apresenta o usuário com papel `client`, informa que a operação é simulada e não persistida, e segue para o portal