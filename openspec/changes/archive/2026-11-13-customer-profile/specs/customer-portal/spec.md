# Spec Delta

## ADDED Requirements

### Requirement: Cliente consulta e edita o próprio perfil mockado
A rota SHALL apresentar somente os dados do cliente atual, validar alterações e manter os resultados não persistentes.

#### Scenario: Perfil carregado
- **WHEN** o cliente abre a rota de perfil
- **THEN** a interface apresenta os dados do usuário atual sem expor o perfil de outra pessoa

#### Scenario: Atualização confirmada ou recusada
- **WHEN** o cliente envia dados válidos ou a operação mockada falha
- **THEN** a interface apresenta a cópia atualizada com aviso de não persistência ou preserva os dados exibidos e informa o erro
