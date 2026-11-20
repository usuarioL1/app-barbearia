# Spec Delta

## MODIFIED Requirements

### Requirement: Barbeiro oferece somente transições permitidas com endpoint Xano
A interface SHALL oferecer somente transições permitidas para atendimentos atribuídos ao barbeiro, encaminhando a operação ao repositório selecionado e refletindo alterações somente após a confirmação do Xano ou identificando explicitamente a simulação no modo mock.

#### Scenario: Transição permitida confirmada pelo Xano
- **WHEN** o barbeiro solicita uma transição permitida para um atendimento próprio e o Xano confirma
- **THEN** a interface atualiza o estado apresentado e identifica o resultado em linguagem compreensível

#### Scenario: Transição permitida simulada
- **WHEN** o barbeiro solicita uma transição permitida para atendimento próprio e o mock aceita
- **THEN** a interface exibe o resultado como simulado e não persistido

#### Scenario: Conclusão antes do término
- **WHEN** o barbeiro tenta concluir um atendimento antes do horário de término
- **THEN** a operação é recusada e o estado exibido permanece inalterado

#### Scenario: Transição sem endpoint disponível
- **WHEN** a transição solicitada não possui endpoint disponível no Xano
- **THEN** a interface não oferece a ação ou a apresenta desabilitada e não indica que houve uma alteração

### Requirement: Barbeiro preserva o estado exibido quando uma ação falha
A interface SHALL comunicar falhas de transição ou de propriedade sem apresentar o atendimento como atualizado nem expor mensagens técnicas de endpoints indisponíveis, seja no repositório Xano ou no mock.

#### Scenario: Transição inválida
- **WHEN** o repositório selecionado recusa uma transição de estado inválida
- **THEN** a interface informa que a operação não foi concluída e mantém o estado exibido

#### Scenario: Atendimento de outro barbeiro
- **WHEN** o barbeiro solicita uma ação sobre atendimento atribuído a outro barbeiro e o repositório selecionado a recusa
- **THEN** a operação é recusada e nenhum dado do atendimento é apresentado como atualizado
