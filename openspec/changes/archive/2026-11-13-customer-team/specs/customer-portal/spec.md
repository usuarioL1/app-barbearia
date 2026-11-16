# Spec Delta

## ADDED Requirements

### Requirement: Cliente consulta barbeiros ativos
A rota de equipe SHALL apresentar barbeiros ativos e suas especialidades conforme os dados mockados, sem expor dados pessoais de clientes.

#### Scenario: Equipe disponível
- **WHEN** a consulta mockada retorna barbeiros ativos
- **THEN** a interface apresenta seus nomes, especialidades e elementos visuais da referência BarberFlow

#### Scenario: Equipe vazia ou indisponível
- **WHEN** a consulta não retorna barbeiros ou falha
- **THEN** a interface apresenta estado vazio ou erro compreensível
