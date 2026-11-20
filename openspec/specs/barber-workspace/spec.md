# barber-workspace Specification

## Purpose

Define as telas de trabalho do barbeiro para visualizar sua agenda e conduzir atendimentos, mantendo visibilidade e ações limitadas à sua própria equipe e às regras de estado do MVP.

## Requirements

### Requirement: Barbeiro visualiza somente a própria agenda
A interface SHALL carregar pelo Xano somente os atendimentos atribuídos ao barbeiro autenticado, sem substituir falhas ou respostas vazias por dados demonstrativos.

#### Scenario: Agenda com atendimentos
- **WHEN** um barbeiro autenticado abre uma data e o Xano retorna atendimentos
- **THEN** a interface mostra apenas os atendimentos atribuídos ao barbeiro para esse dia no fuso `America/Sao_Paulo`

#### Scenario: Agenda sem atendimentos
- **WHEN** o Xano retorna uma lista vazia para a data selecionada
- **THEN** a interface mostra o estado vazio para a data sem inventar atendimentos

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
A interface do barbeiro SHALL aplicar preto `#090909` e dourado `#F2A900` às rotas existentes `/barbeiro`, `/barbeiro/atendimentos` e `/barbeiro/perfil`, refinando navegação e conteúdo sem acrescentar dados, páginas ou operações que o sistema não fornece.

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

### Requirement: Barbeiro preserva o estado exibido quando uma ação falha
A interface SHALL comunicar falhas de transição ou de propriedade sem apresentar o atendimento como atualizado nem expor mensagens técnicas de endpoints indisponíveis, seja no repositório Xano ou no mock.

#### Scenario: Transição inválida
- **WHEN** o repositório selecionado recusa uma transição de estado inválida
- **THEN** a interface informa que a operação não foi concluída e mantém o estado exibido

#### Scenario: Atendimento de outro barbeiro
- **WHEN** o barbeiro solicita uma ação sobre atendimento atribuído a outro barbeiro e o repositório selecionado a recusa
- **THEN** a operação é recusada e nenhum dado do atendimento é apresentado como atualizado

### Requirement: Barbeiro consulta a apresentação do próprio perfil profissional
A interface SHALL apresentar o resumo profissional do barbeiro com nome, função e especialidade, sem oferecer edição ou confirmar alterações de perfil.

#### Scenario: Perfil exibido
- **WHEN** o barbeiro abre a seção Perfil
- **THEN** a interface mostra o nome, a função profissional e a especialidade disponíveis na apresentação do workspace

#### Scenario: Tentativa de editar o perfil
- **WHEN** o barbeiro consulta a seção Perfil
- **THEN** a interface não apresenta uma operação de edição ou persistência de perfil

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

### Requirement: 404 técnico de endpoint não publicado mantém o espaço do barbeiro limpo
Quando o estado da interface do barbeiro contém exatamente a mensagem `Unable to locate request.`, a interface SHALL ocultá-la no feedback global e substituir o conteúdo afetado por um estado de dados indisponíveis, sem renderizar atendimentos antigos ou demonstrativos.

#### Scenario: Endpoint da agenda ainda não publicado
- **WHEN** a consulta da agenda deixa no estado global a mensagem `Unable to locate request.`
- **THEN** a interface não exibe a mensagem no topo, não renderiza os atendimentos anteriores e apresenta um estado neutro de indisponibilidade sem declarar sucesso da consulta

#### Scenario: Outra mensagem de erro
- **WHEN** a consulta deixa no estado global qualquer mensagem diferente de `Unable to locate request.`
- **THEN** a interface preserva o tratamento de erro aplicável e não apresenta a falha como uma consulta vazia bem-sucedida
