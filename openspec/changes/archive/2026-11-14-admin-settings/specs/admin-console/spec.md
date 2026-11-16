# Spec Delta

## ADDED Requirements

### Requirement: Administrador consulta as configurações operacionais apresentadas
A interface SHALL apresentar o expediente, fuso horário e limite padrão de cancelamento como informações somente para leitura, sem confirmar alteração ou persistência dessas configurações.

#### Scenario: Configurações exibidas
- **WHEN** o administrador abre a seção Configurações
- **THEN** a interface apresenta expediente de segunda a sábado das 09h às 18h, fuso `America/Sao_Paulo` e cancelamento até 12 horas antes do atendimento

#### Scenario: Configuração não editável nesta etapa
- **WHEN** o administrador consulta a página de configurações
- **THEN** a interface não oferece um fluxo funcional de edição ou salvamento dos valores exibidos