# Spec Delta

## ADDED Requirements

### Requirement: Barbeiro consulta a apresentação do próprio perfil profissional
A interface SHALL apresentar o resumo profissional do barbeiro com nome, função e especialidade, sem oferecer edição ou confirmar alterações de perfil.

#### Scenario: Perfil exibido
- **WHEN** o barbeiro abre a seção Perfil
- **THEN** a interface mostra o nome, a função profissional e a especialidade disponíveis na apresentação do workspace

#### Scenario: Tentativa de editar o perfil
- **WHEN** o barbeiro consulta a seção Perfil
- **THEN** a interface não apresenta uma operação de edição ou persistência de perfil