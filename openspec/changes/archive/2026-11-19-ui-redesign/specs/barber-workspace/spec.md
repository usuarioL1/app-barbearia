# Spec Delta

## MODIFIED Requirements

### Requirement: Espaço do barbeiro reproduz os designs BarberFlow fornecidos
A interface do barbeiro SHALL aplicar a identidade preto, carvão e dourado às rotas existentes `/barbeiro`, `/barbeiro/atendimentos` e `/barbeiro/perfil`, preservando a hierarquia de agenda, estados e ações disponíveis e sem acrescentar dados, páginas ou operações que o sistema não fornece.

#### Scenario: Barbeiro abre a agenda
- **WHEN** o barbeiro acessa `/barbeiro`
- **THEN** a interface organiza data, atendimentos do dia e resumo visual em painéis legíveis, usando somente os dados retornados pelo estado atual

#### Scenario: Barbeiro visualiza estados de atendimento
- **WHEN** a agenda exibe atendimentos em diferentes estados
- **THEN** cada estado e as ações já permitidas são apresentados com distinção visual consistente, sem alterar as regras de transição ou confirmar ações antes do resultado do sistema

#### Scenario: Barbeiro acessa atendimentos ou perfil
- **WHEN** o barbeiro abre `/barbeiro/atendimentos` ou `/barbeiro/perfil`
- **THEN** a tela mantém a navegação do papel e a hierarquia visual das referências, mostrando apenas a lista de atendimentos ou o resumo profissional que já existem

#### Scenario: Barbeiro usa a interface em uma tela estreita
- **WHEN** a largura disponível não comporta o layout desktop
- **THEN** os painéis e a navegação se reorganizam sem ocultar atendimentos, ações permitidas ou estados vazios e de erro
