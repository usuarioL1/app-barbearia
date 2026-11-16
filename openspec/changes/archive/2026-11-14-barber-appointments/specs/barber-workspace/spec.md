# Spec Delta

## ADDED Requirements

### Requirement: Barbeiro solicita somente transições permitidas para seus atendimentos
A interface SHALL permitir ao barbeiro solicitar `pending` para `confirmed` ou `cancelled`, e `confirmed` para `completed` ou `cancelled`, somente para atendimentos atribuídos a ele.

#### Scenario: Transição permitida simulada
- **WHEN** o barbeiro solicita uma transição permitida para um atendimento próprio
- **THEN** a interface exibe o resultado retornado pelo mock como simulado e não persistido

#### Scenario: Conclusão antes do término
- **WHEN** o barbeiro tenta concluir um atendimento antes do horário de término
- **THEN** a operação é recusada e o estado exibido permanece inalterado

### Requirement: Barbeiro preserva o estado exibido quando uma ação falha
A interface SHALL comunicar falhas de transição ou de propriedade sem apresentar o atendimento como atualizado.

#### Scenario: Transição inválida
- **WHEN** o mock recusa uma transição de estado inválida
- **THEN** a interface informa que a operação não foi concluída e mantém o estado exibido

#### Scenario: Atendimento de outro barbeiro
- **WHEN** o barbeiro solicita uma ação sobre atendimento atribuído a outro barbeiro
- **THEN** a operação é recusada e nenhum dado do atendimento é apresentado como atualizado