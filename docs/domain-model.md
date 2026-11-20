# BarberFlow — Modelo de Domínio

## Propósito e limites

Este documento descreve os conceitos do domínio BarberFlow, suas relações e invariantes. É um modelo conceitual, não um esquema físico de banco: não define DDL, tipos SQL, índices ou detalhes de implementação de tabelas.

O domínio atende uma única unidade. Xano é a fonte de verdade para identidades, permissões, catálogo, disponibilidade, agendamentos e histórico; Reflex apresenta e coordena as jornadas sem substituir as validações do backend.

## Conceitos

### Usuário e perfis

Representa uma pessoa autenticável e seu acesso ao sistema.

**Atributos conceituais**

- Identificador e identidade de login (e-mail).
- Nome e telefone, quando necessários à operação.
- Papel de negócio: `client`, `barber` ou `admin`.
- Estado ativo/inativo e dados de criação/atualização geridos pelo backend.
- Credencial protegida pelo mecanismo seguro de autenticação do Xano; a senha em texto puro não faz parte dos dados apresentados ou registrados.

**Regras**

- O cadastro público cria somente usuários `client`; o cliente não escolhe nem altera seu papel.
- Usuários `barber` e `admin` são provisionados administrativamente no Xano.
- O backend deriva identidade e papel da sessão autenticada; não confia em identificadores ou papéis enviados como autoridade pelo frontend.
- Sessões protegidas usam o token emitido pelo servidor; ausência ou invalidade resulta em não autenticação, e falta de permissão resulta em acesso negado.
- Usuários desativados não devem obter acesso operacional, sem apagar referências históricas.

### Barbeiro

É a representação profissional associada a um usuário com papel `barber`.

**Atributos conceituais**

- Vínculo com o usuário responsável pela identidade e autenticação.
- Apresentação profissional, como biografia e especialidades.
- Estado ativo/inativo.

**Regras**

- O expediente é global da unidade; não há calendário individual por barbeiro no MVP.
- Somente barbeiros ativos são opções para novas reservas.
- O barbeiro autenticado consulta e opera apenas atendimentos atribuídos ao próprio perfil.
- Desativar o perfil remove-o das novas opções de reserva, sem apagar atendimentos existentes.

### Serviço

Representa uma oferta que pode ser incluída em um agendamento.

**Atributos conceituais**

- Identificador, título e descrição.
- Preço em BRL e duração em minutos.
- Estado ativo/inativo.

**Regras**

- Somente serviços ativos podem ser selecionados em novas reservas.
- Preço e duração são copiados para snapshots quando o agendamento é criado; mudanças futuras no catálogo não modificam esses dados históricos.
- Serviços referenciados por agendamentos devem ser desativados, e não apagados fisicamente pela interface.

### Agendamento

Representa a reserva de um serviço para um cliente, executada por um barbeiro em determinado intervalo.

**Atributos conceituais**

- Identificador da reserva.
- Referências ao cliente, barbeiro e serviço.
- Snapshot do título/nome do serviço, preço e duração no momento da reserva.
- Início e fim do serviço; instantes transferidos em ISO 8601 com fuso e persistidos como UTC.
- Estado canônico: `pending`, `confirmed`, `cancelled` ou `completed`.
- Datas de criação/atualização e, quando cancelado, horário e autor do cancelamento.
- Eventos do histórico de status com estado anterior (quando houver), estado novo, autor e horário UTC.

**Relacionamentos**

- Cada agendamento pertence a um cliente.
- Cada agendamento referencia um barbeiro e um serviço.
- Cada agendamento tem histórico de eventos de estado; a criação registra o primeiro evento como `pending`.

**Regras de ciclo de vida**

- Novas reservas começam em `pending`.
- Transições permitidas: `pending` → `confirmed` ou `cancelled`; `confirmed` → `completed` ou `cancelled`.
- `completed` e `cancelled` são estados finais. Não se reabre um estado final por transição comum.
- Um atendimento só pode ser concluído depois de seu horário de término.
- Cada transição autorizada registra autor e horário; não se altera o histórico silenciosamente.
- O cliente só consulta e cancela reservas próprias. O cancelamento pelo cliente é permitido quando elegível e com pelo menos 12 horas antes do início.
- Barbeiros podem atuar somente sobre atendimentos atribuídos a eles. Administradores podem operar dentro do escopo administrativo, inclusive cancelar sem o limite de 12 horas.
- O cancelamento e a atualização de estado só são apresentados como concluídos depois da confirmação do backend.

### Disponibilidade, bloqueio e concorrência

Disponibilidade é o conjunto de horários oferecidos para a combinação atual de serviço, barbeiro e data. Ela é derivada de regras de expediente, duração, preparação, horizonte de agendamento e reservas não canceladas.

**Regras estruturais**

- Expediente global: segunda-feira a sábado, das 09h às 18h em `America/Sao_Paulo`.
- A duração do serviço é exata, sem grade fixa de inícios de 15 minutos.
- Após cada serviço há 15 minutos de preparação bloqueados na agenda; esse intervalo não altera a duração ou o preço apresentados ao cliente.
- O serviço e o período de preparação precisam caber integralmente no expediente.
- Reservas novas exigem no mínimo duas horas de antecedência e não podem ultrapassar 30 dias no futuro.
- Reservas não canceladas ocupam o intervalo do início até 15 minutos depois do fim do serviço. Reservas do mesmo barbeiro não podem sobrepor esse intervalo.
- O backend recalcula e valida a disponibilidade no momento da criação; um horário apresentado anteriormente não garante que continue livre.

**Bloqueio de concorrência**

O mecanismo de bloqueio por barbeiro é um recurso técnico para serializar ou proteger operações concorrentes de reserva. Não representa um atendimento, não é exibido como agendamento e não substitui as regras de disponibilidade.

Uma verificação de conflito isolada, seguida de uma gravação desprotegida, não garante integridade. A verificação e a persistência precisam ocorrer sob uma estratégia atômica suportada pelo Xano. Em conflito, a tentativa é recusada com código `appointment_conflict` e não deixa reserva ou histórico parcial.

### Configurações da barbearia

Representam parâmetros operacionais comuns à unidade no MVP.

**Configurações conceituais**

- Fuso horário: `America/Sao_Paulo`.
- Expediente global: segunda-feira a sábado, das 09h às 18h.
- Intervalo de preparação: 15 minutos.
- Antecedência mínima para agendar: duas horas.
- Horizonte máximo de agendamento: 30 dias.
- Janela padrão de cancelamento do cliente: até 12 horas antes do início.
- Moeda padrão: BRL.

**Regras**

- Datas e horas são apresentadas no fuso da barbearia; persistência e auditoria usam instantes UTC.
- As configurações apresentadas no console não implicam que possam ser editadas. A interface só oferece alteração quando existir operação backend autorizada.
- O MVP não define configurações individuais por barbeiro nem múltiplas unidades.

## Isolamento de permissões

| Papel | Escopo de acesso |
|---|---|
| `client` | Próprio perfil e próprios agendamentos; consulta catálogo ativo e solicita reservas próprias. |
| `barber` | Agenda e transições permitidas somente para atendimentos atribuídos ao perfil autenticado; dados pessoais limitados ao necessário para o serviço. |
| `admin` | Operações administrativas autorizadas sobre agenda, catálogo, equipe, usuários e relatórios da unidade. |

O frontend pode ocultar ou desabilitar controles não disponíveis, mas a autorização deve ser imposta pelo Xano. O cliente não pode adquirir privilégios alterando campos locais ou payloads.

## Integridade, privacidade e auditoria

- O Xano é a autoridade final para autenticação, propriedade, permissões, disponibilidade e transições.
- Uma reserva e seu evento inicial de histórico são consistentes: falha na auditoria não pode deixar uma reserva parcial apresentada como sucesso.
- Conflitos e falhas não devem ser convertidos em sucesso nem em dados demonstrativos quando o modo Xano está selecionado.
- Preços e durações históricos vêm dos snapshots do agendamento, não do catálogo atual.
- Relatórios contam apenas reservas `completed`, usando o preço snapshot e a data local do início do atendimento.
- Dados de clientes são limitados por papel e propriedade; identificadores, e-mails, tokens e credenciais não são expostos sem necessidade.
- Logs e mensagens não devem conter senhas ou tokens.

## Referências

- `openspec/config.yaml` — domínio, fuso, stack e entidades centrais.
- `openspec/specs/especifica_o_do_projeto.md` — regras gerais e critérios de aceite.
- `openspec/specs/appointments/spec.md` — disponibilidade, reservas, concorrência, autorização e ciclo de vida.
- `openspec/specs/customer-portal/spec.md` — operações do cliente.
- `openspec/specs/barber-workspace/spec.md` — escopo e ações do barbeiro.
- `openspec/specs/admin-console/spec.md` — gestão administrativa e relatórios.
- `openspec/specs/xano-runtime-client/spec.md` — integração e falhas do runtime Xano.
