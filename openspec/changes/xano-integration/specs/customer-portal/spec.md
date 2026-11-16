# Spec Delta

## ADDED Requirements

### Requirement: Autenticação real respeita o papel atribuído pelo servidor
A interface SHALL autenticar pelo contrato confirmado do Xano e usar o papel retornado pelo servidor, sem aceitar escolha ou promoção de papel pelo cliente.

#### Scenario: Cadastro público confirmado
- **WHEN** um visitante conclui um cadastro válido
- **THEN** a conta é criada como cliente segundo as regras do servidor e a interface apresenta o resultado real da operação

#### Scenario: Login com credenciais inválidas
- **WHEN** o Xano recusa as credenciais
- **THEN** a interface informa a falha sem criar ou manter uma sessão autenticada

### Requirement: Dados da conta e catálogo vêm de respostas confirmadas
A interface SHALL obter o perfil autenticado e as opções de catálogo das respostas reais do Xano, sem substituir falhas por dados mockados.

#### Scenario: Consulta de perfil e catálogo
- **WHEN** um cliente autenticado abre o perfil, os serviços ou a equipe
- **THEN** a interface apresenta somente os dados autorizados retornados pelos endpoints confirmados

#### Scenario: Falha de consulta
- **WHEN** uma consulta real falha ou retorna uma resposta inválida
- **THEN** a interface informa o erro e não apresenta dados demonstrativos como resultado do sistema

### Requirement: Agendamento usa disponibilidade e resultado autoritativos
A interface SHALL consultar horários atuais e confirmar ou cancelar agendamentos somente após resposta bem-sucedida do Xano.

#### Scenario: Conflito de disponibilidade
- **WHEN** o Xano recusa uma reserva com conflito `409`
- **THEN** a interface informa que o horário não está mais disponível e não apresenta confirmação local

#### Scenario: Falha na disponibilidade
- **WHEN** o Xano não consegue fornecer horários
- **THEN** a interface descarta opções desatualizadas e impede confirmar um horário simulado

#### Scenario: Cancelamento recusado
- **WHEN** o Xano recusa o cancelamento por prazo, propriedade ou estado
- **THEN** a interface mantém o estado retornado e explica que a operação não foi concluída
