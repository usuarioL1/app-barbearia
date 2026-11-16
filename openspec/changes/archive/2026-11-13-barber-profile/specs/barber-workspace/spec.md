# Spec Delta

## ADDED Requirements

### Requirement: Barbeiro consulta o próprio perfil profissional
A rota `/barbeiro/perfil` SHALL apresentar a identidade profissional, função e especialidade do barbeiro atual, usando somente dados de apresentação e sem alegar persistência.

#### Scenario: Perfil profissional apresentado
- **WHEN** o barbeiro abre sua rota de perfil
- **THEN** a interface mostra as informações profissionais e o avatar de apresentação sem expor dados de outro usuário
