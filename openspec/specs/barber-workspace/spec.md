# barber-workspace Specification

## Purpose

Define as telas de trabalho do barbeiro para visualizar sua agenda e conduzir atendimentos, mantendo visibilidade e ações limitadas à sua própria equipe e às regras de estado do MVP.

## Requirements

### Requirement: Barbeiro visualiza somente a própria agenda
A interface SHALL apresentar ao barbeiro os atendimentos atribuídos a ele, em uma visão diária com data, horário local, serviço, cliente e estado, sem disponibilizar dados de clientes além do necessário para o atendimento.

#### Scenario: Agenda com atendimentos
- **WHEN** um barbeiro autenticado abre a agenda de um dia
- **THEN** a interface mostra apenas os atendimentos atribuídos ao barbeiro para esse dia no fuso `America/Sao_Paulo`

#### Scenario: Agenda sem atendimentos
- **WHEN** o barbeiro abre uma data sem atendimentos
- **THEN** a interface mostra um estado vazio para a data selecionada

### Requirement: Barbeiro atualiza estados permitidos dos atendimentos
A interface SHALL permitir ao barbeiro confirmar ou cancelar atendimentos pendentes e concluir ou cancelar atendimentos confirmados, solicitando ao backend a transição e exibindo o estado resultante.

#### Scenario: Transição permitida confirmada pelo backend
- **WHEN** o barbeiro solicita uma transição permitida para um atendimento próprio e o backend confirma
- **THEN** a interface atualiza o estado apresentado e identifica o resultado em linguagem compreensível

#### Scenario: Transição inválida ou falha
- **WHEN** o backend recusa uma transição, inclusive por horário ou estado incompatível
- **THEN** a interface preserva o estado atual e informa que a operação não foi concluída

#### Scenario: Atendimento de outro barbeiro
- **WHEN** um barbeiro tenta abrir ou alterar um atendimento não atribuído a ele
- **THEN** a interface não expõe os dados nem apresenta a ação como concluída

### Requirement: Espaço do barbeiro reproduz os designs BarberFlow fornecidos
A interface do barbeiro SHALL reconstruir os designs fornecidos como componentes, preservando estrutura, proporções, navegação, hierarquia e aparência preto/dourado. A composição inteira não deve substituir a tela; assets individuais ausentes devem usar placeholders coerentes, sem acrescentar elementos visuais ausentes da referência.

#### Scenario: Barbeiro abre a agenda
- **WHEN** o barbeiro acessa sua agenda
- **THEN** a interface apresenta a navegação, o período, os compromissos, os cartões e a organização visual da referência BarberFlow

#### Scenario: Barbeiro visualiza estados de atendimento
- **WHEN** a agenda exibe atendimentos em diferentes estados
- **THEN** cada estado e as ações correspondentes são apresentados com a hierarquia e o tratamento visual da referência, sem alterar as regras de transição

### Requirement: Barbeiro consulta somente os atendimentos da própria agenda
A interface SHALL listar, para a data selecionada, os atendimentos atribuídos ao barbeiro atual com horário local, serviço, nome do cliente e estado, sem expor identificadores ou e-mail do cliente.

#### Scenario: Agenda diária carregada
- **WHEN** o barbeiro abre sua agenda para uma data com atendimentos
- **THEN** a interface mostra somente os atendimentos atribuídos a ele nessa data e apresenta os horários em `America/Sao_Paulo`

#### Scenario: Data sem atendimentos
- **WHEN** o barbeiro abre uma data sem atendimentos atribuídos
- **THEN** a interface mostra o estado vazio para a data selecionada

### Requirement: Barbeiro navega entre datas da agenda
A interface SHALL permitir consultar datas diferentes sem ampliar o escopo dos atendimentos além do barbeiro atual.

#### Scenario: Consulta de outra data
- **WHEN** o barbeiro navega para o dia anterior ou seguinte
- **THEN** a agenda carrega a data escolhida e apresenta os respectivos atendimentos próprios

#### Scenario: Falha ao carregar outra data
- **WHEN** a consulta da nova data falha
- **THEN** a interface informa a falha e não apresenta a data como carregada com sucesso

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

### Requirement: Barbeiro consulta a apresentação do próprio perfil profissional
A interface SHALL apresentar o resumo profissional do barbeiro com nome, função e especialidade, sem oferecer edição ou confirmar alterações de perfil.

#### Scenario: Perfil exibido
- **WHEN** o barbeiro abre a seção Perfil
- **THEN** a interface mostra o nome, a função profissional e a especialidade disponíveis na apresentação do workspace

#### Scenario: Tentativa de editar o perfil
- **WHEN** o barbeiro consulta a seção Perfil
- **THEN** a interface não apresenta uma operação de edição ou persistência de perfil