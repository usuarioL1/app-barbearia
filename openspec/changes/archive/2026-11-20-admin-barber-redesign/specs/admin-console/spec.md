# Spec Delta

## MODIFIED Requirements

### Requirement: Console administrativo reproduz os designs BarberFlow fornecidos
A interface administrativa SHALL aplicar preto `#090909` e dourado `#F2A900` às rotas existentes `/admin/*`, refinando navegação, filtros e conteúdo sem substituir componentes por capturas de tela nem inventar indicadores, registros ou ações.

#### Scenario: Administrador navega pelo console
- **WHEN** o administrador abre dashboard, agenda, clientes, serviços, equipe ou usuários
- **THEN** a interface mantém navegação lateral com rota ativa, cabeçalho e cartões, tabelas ou agenda adequados aos dados e às ações existentes

#### Scenario: Administrador consulta relatórios e configurações
- **WHEN** o administrador abre relatórios ou configurações
- **THEN** a interface mantém a hierarquia, os filtros e os agrupamentos visuais correspondentes, sem alterar permissões, métricas disponíveis ou o caráter informativo das configurações

#### Scenario: Administrador usa o console em uma tela estreita
- **WHEN** a largura disponível não comporta o layout desktop
- **THEN** a navegação, os filtros, os cartões e as tabelas se reorganizam sem ocultar controles, dados, mensagens ou ações existentes

### Requirement: Administrador pesquisa a lista de clientes
A lista SHALL filtrar clientes por nome, e-mail ou telefone sem modificar os registros e sem expor o e-mail como uma coluna adicional.

#### Scenario: Busca com correspondências
- **WHEN** o administrador informa um termo que corresponde a um ou mais clientes
- **THEN** a lista apresenta somente os registros correspondentes

#### Scenario: Busca sem correspondências
- **WHEN** o administrador informa um termo sem correspondência
- **THEN** a lista apresenta o estado vazio sem remover ou alterar os registros

## ADDED Requirements

### Requirement: Dados operacionais administrativos usam respostas do Xano
Quando `BARBERFLOW_MODE=xano`, as telas administrativas SHALL apresentar somente dados e métricas retornados com sucesso pelo Xano, sem substituir falhas ou respostas vazias por dados demonstrativos.

#### Scenario: Dados operacionais carregados
- **WHEN** o administrador abre uma tela com dados operacionais e as consultas Xano têm sucesso
- **THEN** a interface apresenta os registros e métricas retornados para a tela e o período selecionados

#### Scenario: Consulta sem registros
- **WHEN** uma consulta Xano bem-sucedida não retorna registros para a tela ou filtros atuais
- **THEN** a interface apresenta o estado vazio correspondente, sem inventar registros ou totais

#### Scenario: Modo Xano sem resposta válida
- **WHEN** uma consulta falha ou retorna uma resposta inválida
- **THEN** a interface não apresenta dados demonstrativos como resultado Xano nem indica que a consulta foi concluída com sucesso

### Requirement: Ações administrativas dependem de operações Xano disponíveis
As telas administrativas SHALL oferecer somente ações que tenham operação Xano correspondente e permitida, refletindo alterações apenas após confirmação do backend.

#### Scenario: Ação suportada confirmada
- **WHEN** o administrador solicita uma ação com endpoint disponível e o Xano confirma a alteração
- **THEN** a interface apresenta o resultado confirmado pelo backend sem simulação ou sucesso otimista

#### Scenario: Ação sem endpoint ou sem permissão
- **WHEN** uma ação não possui endpoint disponível ou é incompatível com as permissões e o provisionamento manual exigido
- **THEN** a interface omite ou desabilita o controle e não apresenta a ação como realizada

#### Scenario: Ação suportada recusada
- **WHEN** o Xano recusa uma ação ou sua resposta não confirma a alteração
- **THEN** a interface preserva os dados atuais e informa que a operação não foi concluída

### Requirement: 404 técnico de endpoint não publicado mantém o console limpo
Quando o estado da interface administrativa contém exatamente a mensagem `Unable to locate request.`, a interface SHALL ocultá-la no feedback global e substituir o conteúdo afetado por um estado de dados indisponíveis, sem renderizar registros antigos ou demonstrativos.

#### Scenario: Endpoint de leitura ainda não publicado
- **WHEN** uma consulta de dados operacionais deixa no estado global a mensagem `Unable to locate request.`
- **THEN** a interface não exibe a mensagem no topo, não renderiza os dados anteriores dessa tela e apresenta um estado neutro de indisponibilidade sem declarar sucesso da consulta

#### Scenario: Outra mensagem de erro
- **WHEN** a consulta deixa no estado global qualquer mensagem diferente de `Unable to locate request.`
- **THEN** a interface preserva o tratamento de erro aplicável e não oculta a falha como se fosse uma consulta bem-sucedida

## REMOVED Requirements

### Requirement: Dashboard apresenta um resumo operacional demonstrativo
**Reason**: O dashboard em modo Xano deve refletir consultas reais; dados demonstrativos conflitam com esse contrato.
**Migration**: Usar os requisitos de dados operacionais administrativos e de tratamento de endpoint indisponível definidos nesta mudança.

### Requirement: Dashboard não persiste dados demonstrativos
**Reason**: O requisito descreve uma fonte mock que não corresponde ao modo Xano solicitado.
**Migration**: Carregar métricas e registros pelos endpoints Xano existentes e apresentar somente resultados confirmados.

### Requirement: Administrador consulta usuários demonstrativos
**Reason**: Usuários administrativos devem vir da resposta Xano, e não de registros demonstrativos.
**Migration**: A listagem permanece somente leitura e usa dados Xano; o provisionamento de papéis privilegiados continua manual.

### Requirement: Ações de usuário são apresentadas como não persistentes
**Reason**: Ações simuladas de usuário conflitam com o requisito de não oferecer operações sem endpoint permitido.
**Migration**: Omitir ou desabilitar ações sem endpoint Xano e não oferecer provisionamento público de papéis privilegiados.

### Requirement: Administrador consulta a equipe de barbeiros
**Reason**: O requisito atual limita a origem a uma lista mock, incompatível com o modo Xano.
**Migration**: Consultar a equipe pela fonte Xano e manter as regras de atividade já definidas.

### Requirement: Ações administrativas da equipe não persistem
**Reason**: Ações simuladas não correspondem à operação Xano, embora algumas mutações possam ter endpoints reais.
**Migration**: Oferecer somente ações com endpoint disponível e refletir mudanças após confirmação do Xano.

### Requirement: Administrador consulta o catálogo de serviços
**Reason**: A listagem deve apresentar os registros da fonte Xano em modo Xano, não um catálogo mock.
**Migration**: Consultar serviços pela fonte Xano e preservar a distinção entre ativos e inativos.

### Requirement: Ações administrativas de serviço não persistem
**Reason**: O contrato proíbe persistência mesmo quando há endpoints Xano disponíveis.
**Migration**: Usar apenas ações de serviço com endpoint disponível; manter a tela sem ações para operações não suportadas.

### Requirement: Administrador consulta a lista demonstrativa de clientes
**Reason**: A lista demonstrativa conflita com a origem Xano da gestão administrativa.
**Migration**: Apresentar somente registros retornados pela consulta Xano, respeitando os campos permitidos.

### Requirement: Ações de cadastro de clientes são apenas simuladas
**Reason**: A simulação pode sugerir uma alteração que não foi persistida no Xano.
**Migration**: Enviar somente operações com endpoint disponível e mostrar sucesso apenas após confirmação do backend.

### Requirement: Administrador consulta agenda semanal filtrada
**Reason**: A agenda deve representar registros Xano, não atendimentos demonstrativos.
**Migration**: Manter período, filtros e fuso local usando a resposta Xano; apresentar estado vazio quando não houver registros.

### Requirement: Administrador solicita transições simuladas de atendimento
**Reason**: Alterações de estado não podem ser simuladas nem exibidas como persistidas.
**Migration**: Solicitar transições permitidas ao endpoint Xano e atualizar a interface somente após confirmação.

### Requirement: Agenda administrativa não persiste operações mock
**Reason**: O requisito exclui chamadas Xano, incompatível com a operação real solicitada.
**Migration**: Preservar a agenda baseada em Xano e não oferecer transições sem endpoint disponível.
