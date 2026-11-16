# Spec Delta

## ADDED Requirements

### Requirement: Administrador consulta usuários demonstrativos
A interface SHALL listar os registros de usuários retornados pela fonte mock, apresentando nome, e-mail e papel sem declarar autenticação ou autorização reais.

#### Scenario: Lista de usuários carregada
- **WHEN** o administrador abre a seção Usuários e a consulta mock é concluída
- **THEN** a interface apresenta os usuários demonstrativos e seus papéis disponíveis

#### Scenario: Lista vazia
- **WHEN** a fonte mock não retorna usuários
- **THEN** a interface apresenta um estado vazio em vez de inventar registros

### Requirement: Ações de usuário são apresentadas como não persistentes
A interface SHALL comunicar como simuladas e não persistentes as ações mockadas de criação, edição ou desativação de usuários.

#### Scenario: Ação mock aceita
- **WHEN** o administrador solicita uma ação de usuário aceita pelo mock
- **THEN** a interface informa que a ação foi simulada e que nenhum dado foi salvo

#### Scenario: Ação mock recusada
- **WHEN** o mock recusa uma ação de usuário por validação ou falha
- **THEN** a interface apresenta o erro sem indicar que o usuário foi alterado