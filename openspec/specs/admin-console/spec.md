# admin-console Specification

## Purpose

Define as jornadas administrativas para acompanhar a operação da barbearia, gerir agenda e cadastros e consultar desempenho sem ultrapassar as permissões e regras de negócio do MVP.

## Requirements

### Requirement: Administrador acompanha o resumo operacional
A interface SHALL oferecer um dashboard administrativo com indicadores de agenda, faturamento, clientes e comparecimento, identificando o período consultado e exibindo dados retornados pelo sistema.

#### Scenario: Dashboard carregado
- **WHEN** um administrador autenticado abre o dashboard e os dados são carregados
- **THEN** a interface apresenta os indicadores e o resumo de faturamento do período selecionado, sem substituir dados ausentes por métricas inventadas

#### Scenario: Falha ao carregar o resumo
- **WHEN** a consulta do dashboard falha
- **THEN** a interface indica que os dados não puderam ser carregados e permite tentar novamente

### Requirement: Administrador consulta e opera a agenda da unidade
A interface SHALL oferecer visualização diária e semanal com filtros de barbeiro e estado, usando o fuso `America/Sao_Paulo` e as informações de atendimento necessárias à gestão.

#### Scenario: Agenda filtrada
- **WHEN** um administrador seleciona período, barbeiro ou estado
- **THEN** a interface apresenta somente os atendimentos que correspondem aos filtros e mantém visível o período consultado

#### Scenario: Alteração de estado
- **WHEN** o administrador solicita uma transição de estado permitida e o backend confirma
- **THEN** a interface exibe o estado atualizado e o resultado da operação

#### Scenario: Alteração recusada
- **WHEN** a transição é inválida ou o backend retorna erro
- **THEN** a interface preserva o estado atual e informa que a operação não foi concluída

### Requirement: Administrador gerencia cadastros operacionais sem apagar histórico
A interface SHALL permitir consultar e manter clientes, usuários, serviços e equipe conforme as permissões administrativas, usando desativação para registros com histórico associado.

#### Scenario: Cadastro ou edição confirmados
- **WHEN** o administrador salva um cadastro válido e o backend confirma a operação
- **THEN** a interface apresenta os dados persistidos e comunica o sucesso

#### Scenario: Desativação com histórico
- **WHEN** o administrador desativa um serviço, barbeiro ou usuário associado a histórico
- **THEN** a interface preserva os registros relacionados, remove o item das novas opções aplicáveis e mantém seus dados disponíveis para consulta administrativa

#### Scenario: Falha de validação ou autorização
- **WHEN** o backend recusa um cadastro ou alteração
- **THEN** a interface informa o erro e não apresenta a alteração como persistida

### Requirement: Administrador consulta faturamento por período
A interface SHALL oferecer relatórios diários e mensais que usem os preços snapshot de atendimentos concluídos e agrupem os valores pela data local do início do atendimento.

#### Scenario: Relatório de faturamento
- **WHEN** o administrador seleciona um dia ou mês para consulta
- **THEN** a interface apresenta o total e os dados disponíveis considerando somente atendimentos `completed` no período local selecionado

#### Scenario: Período sem faturamento
- **WHEN** o relatório não encontra atendimentos concluídos no período
- **THEN** a interface apresenta total zero e um estado vazio, sem incluir atendimentos pendentes, confirmados ou cancelados

### Requirement: Console administrativo reproduz os designs BarberFlow fornecidos
A interface administrativa SHALL reconstruir os designs fornecidos como componentes, preservando estrutura, proporções, navegação, hierarquia e aparência preto/dourado. Composições inteiras não devem substituir as telas; assets individuais ausentes devem usar placeholders coerentes, sem acrescentar elementos visuais ausentes da referência.

#### Scenario: Administrador navega pelo console
- **WHEN** o administrador abre dashboard, agenda ou uma seção de gestão
- **THEN** a tela apresenta a navegação lateral, seleção ativa, cabeçalho, cartões, tabelas, indicadores ou gráficos conforme o design BarberFlow correspondente

#### Scenario: Administrador consulta relatórios e configurações
- **WHEN** o administrador abre relatórios ou configurações
- **THEN** a interface preserva a hierarquia, os filtros e os agrupamentos visuais representados no design, sem alterar as regras de autorização e os dados apresentados

### Requirement: Dashboard apresenta um resumo operacional demonstrativo
O dashboard SHALL exibir o período consultado, contagem de agendamentos, faturamento mensal, clientes, comparecimento e agendamentos recentes a partir dos dados mock disponíveis.

#### Scenario: Dashboard carregado
- **WHEN** o administrador abre o dashboard e a consulta mock é concluída
- **THEN** a interface apresenta o período e os indicadores derivados dos registros demonstrativos, sem inventar métricas para dados ausentes

#### Scenario: Período sem registros
- **WHEN** o período consultado não contém agendamentos ou faturamento concluído
- **THEN** a interface apresenta o estado vazio ou valor zero correspondente, sem contar agendamentos não concluídos como faturamento

### Requirement: Dashboard não persiste dados demonstrativos
O dashboard SHALL obter seus dados exclusivamente da fonte mock isolada, sem enviar dados ao cliente HTTP ou gravar alterações em Xano.

#### Scenario: Consulta demonstrativa
- **WHEN** o dashboard carrega seus indicadores ou agendamentos recentes
- **THEN** os valores permanecem demonstrativos e nenhuma operação é apresentada como persistida

### Requirement: Administrador consulta usuários demonstrativos
A interface SHALL listar os registros de usuários retornados pela fonte mock, apresentando nome, e-mail e papel sem declarar autenticação ou autorização reais.

#### Scenario: Lista de usuários carregada
- **WHEN** o administrador abre a seção Usuários e a consulta mock é concluída
- **THEN** a interface apresenta os usuários demonstrativos e seus papéis disponíveis

#### Scenario: Lista vazia
- **WHEN** a fonte mock não retorna usuários
- **THEN** a interface apresenta um estado vazio em vez de inventar registros

### Requirement: Ações de usuário são apresentadas como não persistentes
A interface SHALL comunicar como simuladas e não persistentes as ações mockadas de criação, edição ou desativação de usuários.

#### Scenario: Ação mock aceita
- **WHEN** o administrador solicita uma ação de usuário aceita pelo mock
- **THEN** a interface informa que a ação foi simulada e que nenhum dado foi salvo

#### Scenario: Ação mock recusada
- **WHEN** o mock recusa uma ação de usuário por validação ou falha
- **THEN** a interface apresenta o erro sem indicar que o usuário foi alterado

### Requirement: Administrador consulta as configurações operacionais apresentadas
A interface SHALL apresentar o expediente, fuso horário e limite padrão de cancelamento como informações somente para leitura, sem confirmar alteração ou persistência dessas configurações.

#### Scenario: Configurações exibidas
- **WHEN** o administrador abre a seção Configurações
- **THEN** a interface apresenta expediente de segunda a sábado das 09h às 18h, fuso `America/Sao_Paulo` e cancelamento até 12 horas antes do atendimento

#### Scenario: Configuração não editável nesta etapa
- **WHEN** o administrador consulta a página de configurações
- **THEN** a interface não oferece um fluxo funcional de edição ou salvamento dos valores exibidos

### Requirement: Administrador consulta relatórios de faturamento por período
A interface SHALL permitir escolher relatório diário ou mensal e apresentar faturamento, quantidade de atendimentos concluídos e indicadores derivados dos registros disponíveis.

#### Scenario: Relatório diário ou mensal
- **WHEN** o administrador seleciona o período e a data do relatório
- **THEN** a interface atualiza os indicadores para o período local selecionado em `America/Sao_Paulo`

#### Scenario: Período sem faturamento
- **WHEN** não há atendimentos concluídos no período selecionado
- **THEN** o relatório apresenta faturamento zero e não inclui atendimentos pendentes, confirmados ou cancelados

### Requirement: Administrador consulta a equipe de barbeiros
A seção administrativa SHALL listar os barbeiros mock com nome, especialidade e estado ativo/inativo, mantendo registros inativos disponíveis para consulta administrativa.

#### Scenario: Equipe carregada
- **WHEN** a consulta mock da equipe é concluída
- **THEN** a interface exibe os dados disponíveis e o estado de cada barbeiro

#### Scenario: Barbeiro inativo em novo agendamento
- **WHEN** um barbeiro está inativo e um cliente consulta opções para agendar
- **THEN** esse barbeiro não aparece entre as opções agendáveis

### Requirement: Ações administrativas da equipe não persistem
A seção SHALL permitir informar nome e especialidade para criar ou editar barbeiros e desativar registros, validando no mock sem alterar registros ou apresentar operações como persistidas.

#### Scenario: Criação mock aceita
- **WHEN** o administrador submete nome e especialidade válidos para criação
- **THEN** a validação mock aceita a ação e informa que nada foi salvo

#### Scenario: Dados obrigatórios ausentes
- **WHEN** nome ou especialidade não são informados na criação mock
- **THEN** a interface informa a validação sem apresentar uma alteração persistida

#### Scenario: Edição ou desativação mock
- **WHEN** o administrador aciona editar ou desativar para um barbeiro
- **THEN** a operação permanece simulada e não remove o barbeiro nem seus agendamentos históricos

### Requirement: Administrador consulta o catálogo de serviços
A seção administrativa SHALL listar os serviços mock com título, descrição, preço, duração e estado ativo/inativo; somente serviços ativos são oferecidos para novos agendamentos.

#### Scenario: Catálogo administrativo carregado
- **WHEN** a consulta mock de serviços é concluída
- **THEN** a interface exibe os campos disponíveis e o estado de cada serviço, incluindo registros inativos para consulta administrativa

#### Scenario: Serviço inativo no agendamento
- **WHEN** um serviço está inativo e um cliente consulta opções para um novo agendamento
- **THEN** esse serviço não aparece entre as opções agendáveis

### Requirement: Ações administrativas de serviço não persistem
A seção SHALL permitir informar título, descrição, preço e duração para criar ou editar serviços e desativar registros, validando no mock e sem alterar registros ou afirmar persistência.

#### Scenario: Criação mock válida
- **WHEN** o administrador submete título, preço positivo e duração positiva
- **THEN** a validação mock aceita a ação e informa que nada foi salvo

#### Scenario: Criação mock inválida
- **WHEN** o título obrigatório está ausente ou preço ou duração não são valores positivos válidos
- **THEN** a interface informa a validação sem apresentar uma alteração persistida

#### Scenario: Edição ou desativação mock
- **WHEN** o administrador aciona editar ou desativar para um serviço
- **THEN** a operação permanece simulada, sem remover registros de serviço ou histórico associado

### Requirement: Administrador consulta a lista demonstrativa de clientes
A seção de clientes SHALL exibir, para cada registro disponível, nome, telefone, quantidade de agendamentos e data do último atendimento, preservando o acesso administrativo aos dados mock.

#### Scenario: Lista carregada
- **WHEN** a consulta mock de clientes é concluída
- **THEN** a interface apresenta os campos disponíveis para cada cliente sem expor dados além dos exibidos na tela

#### Scenario: Lista vazia
- **WHEN** a consulta mock não retorna clientes
- **THEN** a interface apresenta um estado vazio, distinguindo-o do carregamento em andamento

### Requirement: Administrador pesquisa a lista de clientes
A lista SHALL filtrar clientes por nome, e-mail ou telefone sem modificar os registros e sem expor o e-mail como uma coluna adicional.

#### Scenario: Busca com correspondências
- **WHEN** o administrador informa um termo que corresponde a um ou mais clientes
- **THEN** a lista apresenta somente os registros correspondentes

#### Scenario: Busca sem correspondências
- **WHEN** o administrador informa um termo sem correspondência
- **THEN** a lista apresenta o estado vazio sem remover ou alterar os registros mock

### Requirement: Ações de cadastro de clientes são apenas simuladas
A seção SHALL permitir informar dados para criar ou editar clientes e oferecer desativação, encaminhando as ações à validação mock sem alterar registros ou apresentá-las como persistidas.

#### Scenario: Ação mock concluída
- **WHEN** o administrador submete dados válidos ou aciona desativação e a validação mock aceita a operação
- **THEN** a interface informa que a ação foi simulada e nenhum registro é gravado ou alterado

#### Scenario: Ação mock inválida ou recusada
- **WHEN** nome ou telefone são inválidos, os dados não passam pela validação mock ou a operação retorna erro
- **THEN** a interface informa a falha sem apresentar sucesso ou mudança persistida

### Requirement: Administrador consulta agenda semanal filtrada
A agenda SHALL exibir a semana da data selecionada, os atendimentos demonstrativos e filtros combináveis por barbeiro e estado, usando datas locais de `America/Sao_Paulo`.

#### Scenario: Seleção de semana e filtros
- **WHEN** o administrador seleciona uma data, barbeiro ou estado
- **THEN** a interface exibe a semana correspondente e somente os atendimentos que correspondem aos filtros ativos

#### Scenario: Semana sem resultados
- **WHEN** não há atendimento mock correspondente à semana e aos filtros
- **THEN** a interface apresenta o estado vazio e mantém visível o período consultado

### Requirement: Administrador consulta agenda diária
A agenda SHALL permitir alternar para um dia selecionado e apresentar somente os atendimentos desse dia, mantendo os filtros de barbeiro e estado.

#### Scenario: Visualização diária selecionada
- **WHEN** o administrador escolhe a visualização diária para uma data
- **THEN** a interface apresenta apenas os atendimentos da data selecionada que correspondem aos filtros ativos

### Requirement: Administrador solicita transições simuladas de atendimento
A agenda SHALL permitir as transições administrativas mock válidas entre `pending`, `confirmed`, `cancelled` e `completed`, respeitando as regras de transição e o horário de término.

#### Scenario: Transição aceita
- **WHEN** o administrador solicita uma transição permitida e o repositório mock a aceita
- **THEN** a agenda exibe o estado resultante na sessão e identifica a ação como simulada e não persistida

#### Scenario: Transição recusada
- **WHEN** a transição é inválida ou o repositório mock retorna erro
- **THEN** a agenda preserva os registros exibidos e informa que a operação não foi concluída

### Requirement: Agenda administrativa não persiste operações mock
A agenda SHALL usar somente dados demonstrativos nesta etapa, sem chamadas HTTP ao Xano ou gravação durável de consulta ou transição.

#### Scenario: Atualização da agenda mock
- **WHEN** uma consulta ou transição é concluída
- **THEN** nenhum dado é apresentado como persistido fora da sessão mock

### Requirement: Faturamento considera somente atendimentos concluídos
O relatório SHALL somar o preço snapshot de cada atendimento concluído cuja data local de início pertença ao período selecionado.

#### Scenario: Soma do faturamento
- **WHEN** existem atendimentos concluídos e não concluídos no período
- **THEN** o total usa somente os preços snapshot dos atendimentos concluídos com datas locais dentro do período

#### Scenario: Falha ao carregar o relatório
- **WHEN** a consulta do relatório falha
- **THEN** a interface informa a falha e preserva os indicadores anteriormente carregados