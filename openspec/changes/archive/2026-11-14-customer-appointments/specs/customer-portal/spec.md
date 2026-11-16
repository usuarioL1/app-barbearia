# Spec Delta

## ADDED Requirements

### Requirement: Consulta dos próprios agendamentos
A rota `/agendamentos` SHALL apresentar próximos agendamentos e histórico do cliente corrente, oferecer filtros entre todos, próximos e histórico e mostrar estados vazios apropriados.

#### Scenario: Cliente possui registros
- **WHEN** o repositório mockado retorna agendamentos do cliente corrente
- **THEN** a tela separa próximos atendimentos e histórico e permite alternar a visualização

#### Scenario: Cliente não possui registros
- **WHEN** a consulta retorna listas vazias e termina o carregamento
- **THEN** a tela mostra estados vazios e oferece acesso à jornada de agendamento

### Requirement: Cancelamento de agendamento do cliente
A interface SHALL permitir solicitar cancelamento de agendamento próprio pendente ou confirmado somente com pelo menos 12 horas de antecedência e refletir a resposta do repositório mockado sem sucesso otimista.

#### Scenario: Cancelamento aceito
- **WHEN** o cliente solicita cancelar um de seus agendamentos elegíveis dentro do limite e o mock aceita
- **THEN** a tela atualiza o registro para cancelado e identifica a operação como simulada

#### Scenario: Limite excedido, estado inelegível ou falha
- **WHEN** o cancelamento não é permitido ou o repositório retorna falha
- **THEN** a tela mantém o registro exibido sem alteração e apresenta a mensagem de erro