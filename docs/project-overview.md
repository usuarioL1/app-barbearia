# BarberFlow — Visão Geral do Projeto

## Visão geral

BarberFlow é uma aplicação web para organizar agendamentos e a operação de uma barbearia de unidade única. O sistema reúne o portal do cliente, o espaço de trabalho do barbeiro e o console administrativo, mantendo o backend como fonte de verdade para autenticação, disponibilidade, autorização e persistência.

O projeto é desenvolvido incrementalmente. As especificações OpenSpec em `openspec/specs/` consolidam os requisitos funcionais e as regras de domínio; mudanças de escopo são propostas, implementadas, verificadas e sincronizadas com essas especificações.

## Problema

Agendamentos, disponibilidade da equipe, alterações de status e acompanhamento operacional precisam permanecer consistentes entre clientes, barbeiros e administração. Processos não integrados podem causar reservas sobrepostas, informações desatualizadas, acesso indevido a dados e divergências entre o serviço realizado e os relatórios.

BarberFlow centraliza essas jornadas e delega ao backend as decisões que exigem integridade e controle de acesso.

## Objetivos

- Permitir que clientes conheçam serviços e barbeiros ativos, consultem horários disponíveis e solicitem agendamentos.
- Dar aos clientes acesso apenas aos próprios dados e agendamentos, inclusive para acompanhar ou solicitar cancelamento.
- Permitir que barbeiros consultem sua própria agenda e atualizem atendimentos dentro das transições autorizadas.
- Permitir que administradores acompanhem a operação, gerenciem cadastros e agenda e consultem relatórios.
- Evitar conflitos de horário, preservar o histórico e apresentar resultados somente quando confirmados pelo backend.
- Fornecer uma interface responsiva e acessível para desktop e dispositivos móveis.

## Públicos-alvo

### Cliente

Cria e acessa a própria conta, consulta o catálogo ativo, agenda um serviço com horário disponível e acompanha ou cancela seus próprios agendamentos de acordo com a política vigente.

### Barbeiro

Consulta somente os atendimentos atribuídos a si, visualiza os dados necessários à execução do serviço e solicita transições de status permitidas.

### Administrador

Acompanha indicadores operacionais, consulta e filtra a agenda da unidade, mantém cadastros sem apagar histórico associado e consulta relatórios de faturamento.

## Escopo do MVP

- Uma única unidade da barbearia.
- Cadastro público restrito ao papel `client`; os papéis `barber` e `admin` são provisionados de forma administrativa no Xano.
- Catálogo de serviços e barbeiros ativos, com preço, duração e especialidades relevantes.
- Consulta de disponibilidade e criação de agendamentos com validação final no backend.
- Consulta de agendamentos próprios do cliente, agenda restrita do barbeiro e agenda administrativa filtrável.
- Cancelamento sujeito a propriedade, papel, estado e prazo aplicável.
- Transições auditáveis de status e preservação dos dados históricos.
- Gestão operacional e relatórios simples de faturamento diário e mensal.
- Modo Xano para operações reais e modo demonstrativo isolado, sem misturar dados de demonstração com resultados Xano.

## Fora do escopo inicial

- Múltiplas unidades e horários de expediente individuais por barbeiro.
- Pagamentos, descontos, taxas, gorjetas e reembolsos.
- Exclusão física de registros que possuam histórico associado.
- Promoção pública de usuários para papéis privilegiados.
- Alterações de configurações operacionais sem endpoint e autorização correspondentes.

## Funcionalidades por portal

### Portal do cliente

- Login, cadastro público de cliente, recuperação de senha e consulta/edição do próprio perfil conforme os endpoints disponíveis.
- Catálogo de serviços e barbeiros ativos.
- Fluxo de agendamento com disponibilidade atual, resumo de preço/duração e confirmação não otimista.
- Próximos agendamentos, histórico e cancelamento de reservas próprias elegíveis.

### Espaço do barbeiro

- Agenda diária limitada ao barbeiro autenticado, com navegação entre datas e estados vazios/erro.
- Exibição das informações necessárias ao atendimento, sem expor dados desnecessários do cliente.
- Solicitação das transições de status permitidas, sem indicar sucesso antes da confirmação.
- Resumo profissional apresentado sem oferecer alterações não suportadas.

### Console administrativo

- Resumo operacional e agenda diária/semanal com filtros disponíveis.
- Consulta e manutenção de clientes, serviços, equipe e usuários conforme permissões e operações publicadas.
- Desativação em vez de remoção física quando houver histórico associado.
- Relatórios que consideram apenas atendimentos concluídos e o preço snapshot.
- Ações sem endpoint ou permissão correspondente permanecem ausentes ou desabilitadas; a interface não simula persistência.

## Regras e restrições principais

- Expediente global: segunda-feira a sábado, das 09h às 18h, em `America/Sao_Paulo`.
- A disponibilidade usa a duração exata do serviço, considera 15 minutos de preparação após cada atendimento e exige que o serviço e esse intervalo caibam no expediente.
- O agendamento deve ocorrer com pelo menos duas horas de antecedência e no máximo 30 dias no futuro.
- A criação deve ser protegida contra reservas concorrentes sobrepostas para o mesmo barbeiro; uma checagem isolada antes da gravação não é suficiente.
- Agendamentos começam como `pending`. Transições permitidas: `pending` para `confirmed` ou `cancelled`; `confirmed` para `completed` ou `cancelled`. `completed` e `cancelled` são finais.
- O cliente pode cancelar a própria reserva elegível até 12 horas antes do início. Administradores podem cancelar a qualquer momento, respeitando o registro de auditoria.
- Preço, nome do serviço e duração são preservados como snapshots da reserva. Alterações posteriores no catálogo não reescrevem o histórico.
- Instantes são persistidos em UTC; a apresentação e agrupamentos de relatório usam `America/Sao_Paulo`.
- Falhas de Xano, rede, configuração ou resposta inválida não podem produzir sucesso aparente nem fallback para dados demonstrativos.

## Arquitetura tecnológica

- **Frontend exclusivo:** Reflex em Python. As páginas e o estado da aplicação ficam no pacote `app_barbearia/`; não há um segundo frontend independente.
- **Ambiente Python:** o ambiente virtual local do projeto é `venv/`. Dependências e execução devem usar esse ambiente conforme a configuração local do repositório.
- **Backend:** Xano como serviço de API e persistência. A aplicação Reflex integra-se ao backend por API REST.
- **Lógica de backend:** endpoints e regras específicos podem ser mantidos em XanoScript (`.xs`), validados contra o contrato e as capacidades publicadas no Xano.
- **Integração:** `app_barbearia/api_client.py` implementa chamadas HTTP; `app_barbearia/xano_repository.py` mapeia operações e respostas; `app_barbearia/mock_repository.py` mantém o modo demonstrativo isolado; `app_barbearia/state.py` coordena o estado da aplicação.
- **Configuração:** a URL da API é fornecida por ambiente (`XANO_API_BASE_URL`); `BARBERFLOW_MODE` seleciona o comportamento de runtime. Endpoints e credenciais não devem ser embutidos no frontend.

## Princípios de desenvolvimento incremental com OpenSpec

1. Consultar as especificações consolidadas em `openspec/specs/` antes de mudar comportamento.
2. Descrever mudanças funcionais como changes OpenSpec, com requisitos, cenários e tarefas verificáveis.
3. Implementar apenas o escopo aprovado, preservando compatibilidade com os portais e regras existentes.
4. Verificar mudanças com testes direcionados, validação OpenSpec e compilação aplicável.
5. Sincronizar deltas com as especificações principais antes de arquivar changes concluídas.
6. Tratar documentação de visão geral como orientação do projeto; em caso de divergência, investigar e corrigir a fonte normativa OpenSpec, sem inventar regras.

## Segurança e integridade

- Xano é a autoridade de identidade, permissões, disponibilidade e persistência; validação no frontend não substitui controles no backend.
- Senhas são tratadas pelo mecanismo seguro do Xano. Tokens de sessão são enviados apenas em chamadas protegidas com `Bearer`.
- Senhas, tokens e dados pessoais desnecessários não devem aparecer em logs ou mensagens para o usuário.
- Clientes acessam somente os próprios registros; barbeiros, somente atendimentos atribuídos; administradores, os recursos autorizados de unidade.
- Operações administrativas privilegiadas não podem ser habilitadas por cadastro público.
- Criação, cancelamento e transições de status devem preservar histórico e evitar registros parciais.
- Uma falha ou resposta inválida deve permanecer explícita. Em modo Xano, nunca substituir silenciosamente o resultado por dados mock.

## Referências normativas

- `AGENTS.md` — instruções de trabalho e requisito de consultar a especificação do projeto.
- `openspec/config.yaml` — nome, domínio, fuso, stack e entidades centrais.
- `openspec/specs/especifica_o_do_projeto.md` — especificação geral e critérios de aceite do MVP.
- `openspec/specs/appointments/spec.md` — disponibilidade, criação, autorização, concorrência, cancelamento e transições.
- `openspec/specs/customer-portal/spec.md` — jornadas e regras do cliente.
- `openspec/specs/barber-workspace/spec.md` — escopo e operações do barbeiro.
- `openspec/specs/admin-console/spec.md` — gestão e relatórios administrativos.
- `openspec/specs/xano-runtime-client/spec.md` — configuração, autenticação e isolamento do runtime Xano.
