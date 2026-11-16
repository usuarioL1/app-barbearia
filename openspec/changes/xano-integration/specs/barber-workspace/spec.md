# Spec Delta

## ADDED Requirements

### Requirement: Barbeiro acessa somente sua agenda real
A integração SHALL restringir consultas e transições aos atendimentos do barbeiro autenticado, usando os contratos e os dados confirmados pelo Xano.

#### Scenario: Consulta da agenda própria
- **WHEN** um barbeiro autenticado abre a agenda para uma data
- **THEN** a interface exibe somente os atendimentos autorizados para esse barbeiro

#### Scenario: Acesso a atendimento alheio
- **WHEN** o servidor recusa acesso a um atendimento atribuído a outro barbeiro
- **THEN** a interface não expõe os dados nem apresenta a ação como concluída

### Requirement: Transições do barbeiro refletem o resultado do servidor
A interface SHALL atualizar estados somente após o Xano confirmar uma transição permitida e SHALL preservar o estado exibido em caso de falha.

#### Scenario: Transição autorizada
- **WHEN** o barbeiro solicita uma transição permitida para atendimento próprio
- **THEN** a interface apresenta o novo estado retornado pelo Xano

#### Scenario: Transição recusada ou indisponível
- **WHEN** a transição é inválida, não autorizada ou falha por erro de serviço
- **THEN** a interface mantém o estado anterior e informa que a operação não foi concluída
