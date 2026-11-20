# Spec Delta

## MODIFIED Requirements

### Requirement: Telas do cliente reproduzem os designs BarberFlow fornecidos
A interface do cliente SHALL seguir as referências de Dashboard, Serviços, Agendamentos, Histórico e Perfil, mantendo os dados e bindings existentes, layouts responsivos e componentes funcionais em vez de imagens de tela.

#### Scenario: Visitante acessa autenticação
- **WHEN** um visitante abre login, cadastro ou recuperação de senha
- **THEN** a interface preserva os formulários, campos, mensagens e ações existentes dentro da identidade visual BarberFlow

#### Scenario: Cliente usa a navegação compartilhada
- **WHEN** um cliente abre `/`, `/agendamentos`, `/servicos`, `/perfil`, `/historico` ou `/agendar`
- **THEN** a interface mantém links para Início, Meus Agendamentos, Serviços, Meu Perfil, Histórico e Sair, realça a rota ativa com fundo dourado e texto e ícone pretos, e identifica o usuário autenticado no cabeçalho

#### Scenario: Cliente navega pelo portal e catálogo
- **WHEN** um cliente abre o portal, serviços, equipe, perfil ou agendamentos
- **THEN** as telas mantêm a navegação, os dados, campos e ações suportados pelo sistema, organizados segundo a hierarquia visual da rota

#### Scenario: Dashboard apresenta dados do cliente
- **WHEN** um cliente abre `/`
- **THEN** a interface organiza próximo agendamento, chamada para agendar, até quatro serviços ativos, histórico recente e banner em cartões responsivos, usando somente dados carregados para a conta

#### Scenario: Catálogo permite pré-selecionar serviço
- **WHEN** um cliente abre `/servicos` e seleciona um serviço retornado pelo sistema
- **THEN** a interface apresenta os serviços disponíveis em cartões responsivos e inicia `/agendar` com o serviço selecionado pelo binding existente

#### Scenario: Agendamentos preservam ações suportadas
- **WHEN** um cliente alterna entre próximos agendamentos e histórico em `/agendamentos`
- **THEN** a interface usa os filtros existentes, mostra os dados do cliente e mantém o cancelamento sujeito à regra vigente de 12 horas, sem sucesso otimista

#### Scenario: Perfil preserva edição existente
- **WHEN** um cliente consulta e salva seu perfil
- **THEN** a interface apresenta e atualiza somente os campos suportados, usando o binding e o feedback existentes

#### Scenario: Cliente abre o fluxo de agendamento
- **WHEN** um cliente abre `/agendar` e seleciona serviço, barbeiro, data e horário disponível
- **THEN** a interface apresenta escolhas legíveis, calendário e resumo com a ação de confirmação ligada ao handler existente, sem alterar disponibilidade ou regra de negócio

#### Scenario: Layout estreito
- **WHEN** a largura disponível não comporta a composição desktop
- **THEN** a navegação, os cartões e os campos se reorganizam sem cortar conteúdo funcional ou exigir eventos novos

## ADDED Requirements

### Requirement: Cliente acessa seu histórico em uma rota dedicada
A rota `/historico` SHALL apresentar somente o histórico do cliente autenticado, sem introduzir registros, preços ou resumos não retornados ou derivados dos dados carregados.

#### Scenario: Histórico disponível
- **WHEN** o cliente autenticado abre `/historico` com atendimentos concluídos
- **THEN** a interface lista seus serviços, barbeiros, datas e horários locais, estados e preços disponíveis, com acesso consistente à navegação do portal

#### Scenario: Histórico vazio
- **WHEN** o cliente abre `/historico` sem atendimentos concluídos
- **THEN** a interface apresenta um estado vazio e não inventa registros ou totais

### Requirement: Controles ilustrativos não simulam operações indisponíveis
A interface SHALL desabilitar ou omitir ações de referência que não tenham suporte nos handlers e APIs existentes, sem indicar que uma operação foi realizada.

#### Scenario: Ação sem suporte
- **WHEN** uma referência inclui remarcar, detalhes, upload de foto, autenticação em duas etapas, sair de todos os dispositivos ou filtros sem binding existente
- **THEN** a interface omite o controle ou o apresenta desabilitado sem executar operação ou exibir sucesso

### Requirement: Fotografias locais são decorativas e não identificam usuários
As imagens fotográficas das telas do cliente SHALL ser servidas de assets locais e não apresentar recortes ilustrativos como retratos verificados de usuários ou profissionais nomeados.

#### Scenario: Imagens de serviço e banners
- **WHEN** uma tela do cliente apresenta fotografia de serviço ou ambiente
- **THEN** a imagem carrega de um asset local sem substituir o conteúdo funcional nem representar identidade pessoal verificada
