# Spec Delta

## Purpose

Define as telas de trabalho do barbeiro para visualizar sua agenda e conduzir atendimentos, mantendo visibilidade e ações limitadas à sua própria equipe e às regras de estado do MVP.

## ADDED Requirements

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
