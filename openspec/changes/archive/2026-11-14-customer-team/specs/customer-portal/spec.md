# Spec Delta

## ADDED Requirements

### Requirement: Equipe disponível para o cliente
A rota `/equipe` SHALL listar barbeiros ativos com nome e especialidade, sem dados pessoais de clientes.

#### Scenario: Equipe carregada
- **WHEN** a consulta mockada retorna barbeiros ativos
- **THEN** a tela apresenta os profissionais e suas especialidades sem dados de clientes

#### Scenario: Equipe vazia ou em carregamento
- **WHEN** a lista de barbeiros está vazia
- **THEN** a tela distingue o carregamento do estado sem profissionais disponíveis

### Requirement: Seleção de barbeiro para agendamento
A tela SHALL permitir iniciar a jornada `/agendar` com o barbeiro escolhido.

#### Scenario: Selecionar profissional
- **WHEN** o cliente aciona o botão de agendamento de um barbeiro
- **THEN** a interface abre `/agendar` com esse profissional selecionado