# Especificação do Projeto: Sistema de Gerenciamento de Barbearia (OpenSpec)

## 1. Visão Geral do Projeto

O objetivo deste projeto é desenvolver uma aplicação completa de gerenciamento para uma barbearia local. O sistema permitirá o agendamento de serviços, gestão de clientes, controle de barbeiros, controle de serviços prestados e visualização de relatórios operacionais.

O MVP atende uma única unidade. O expediente global fixo é de segunda-feira a sábado, das 09h às 18h, no fuso `America/Sao_Paulo`.

A arquitetura do sistema segue a divisão:

* **Frontend:** Reflex (Python/React framework).

* **Backend:** Xano (BaaS - Backend as a Service) integrado via APIs REST.

* **Inteligência Artificial:** GitHub Copilot / Gemini assistidos pelo **Xano Developer MCP** e pelo **XanoScript Language Server**.

## 2. Arquitetura e Tecnologias

```
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND (Reflex)                      │
│   - Interface Web (Página do Cliente e Painel do Barbeiro)   │
│   - Gerenciamento de Estado em Python (rx.State)             │
└──────────────┬──────────────────────────────────────────────┘
               │ Chamadas HTTP REST API
               ▼
┌─────────────────────────────────────────────────────────────┐
│                      BACKEND (Xano)                         │
│   - Banco de dados relacional (PostgreSQL)                  │
│   - Endpoints de Autenticação (JWT)                         │
│   - Lógica de Negócios e Agendamentos em XanoScript (.xs)   │
└─────────────────────────────────────────────────────────────┘

```

## 3. Módulos do Sistema e Requisitos Funcionais

### Módulo 1: Autenticação e Perfis (Auth & Users)

* **Público:** Clientes e Administradores/Barbeiros.

* **Funcionalidades:**

  * Cadastro de novos clientes (Nome, E-mail, Telefone/WhatsApp, Senha).

  * Login com geração de token JWT (gerenciado pelo Xano).

  * Perfis de permissão: `client`, `barber` e `admin`.

  * O cadastro público cria sempre usuários `client`; o papel não é aceito como campo confiável do frontend. O primeiro `admin` e os usuários `barber` são provisionados manualmente na interface administrativa do Xano, usando o mecanismo seguro de credenciais do Xano. Nenhuma operação pública pode atribuir ou promover esses papéis.

  * Clientes podem consultar e alterar os próprios dados e consultar/cancelar os próprios agendamentos. Barbeiros podem consultar a própria agenda e atualizar o status dos próprios atendimentos. Administradores podem gerenciar usuários, equipe, serviços, agenda e relatórios.

  * A senha deve ser armazenada somente com o mecanismo seguro de hash do Xano, nunca em texto puro. O JWT deve ser enviado no cabeçalho HTTP `Authorization` com o esquema `Bearer`. Respostas de endpoints protegidos sem token ou com token inválido/expirado devem ser `401`, e falta de permissão deve ser `403`. Configurar expiração de sessão em 24 horas e exigir novo login após expiração. Não armazenar senha nem token em logs.

### Módulo 2: Catálogo de Serviços e Barbeiros

* **Funcionalidades:**

  * Listagem de serviços oferecidos (ex: Corte de Cabelo, Barba, Sobrancelha, Combo).

  * Informações de cada serviço: Nome, Descrição, Preço e Duração (em minutos).

  * Listagem da equipe de barbeiros com especialidades; todos seguem o expediente global da unidade.

  * Serviços e barbeiros possuem estado ativo/inativo. Somente registros ativos aparecem para novos agendamentos; desativar não remove o histórico associado.

### Módulo 3: Agendamento de Horários (Core)

* **Funcionalidades:**

  * Seleção de Barbeiro + Serviço + Data/Hora disponível.

  * Validação de conflito de horários no backend (Xano).

  * Estados canônicos na API e no banco: `pending`, `confirmed`, `cancelled` e `completed`. A interface pode exibir, respectivamente, “Pendente”, “Confirmado”, “Cancelado” e “Concluído”.

  * Visualização dos agendamentos ativos na área do cliente.

  * Horários são apresentados no fuso configurado para a barbearia (padrão: `America/Sao_Paulo`) e persistidos como timestamps UTC. A API recebe e devolve datas ISO 8601 com indicação de fuso.

  * Os inícios disponíveis são calculados pela duração exata do serviço, sem uma grade fixa de 15 minutos. Mantém-se um intervalo de preparação de 15 minutos após cada atendimento. O expediente global é de segunda-feira a sábado, das 09h às 18h. O cliente pode agendar com no mínimo 2 horas de antecedência e até 30 dias no futuro.

  * A disponibilidade é calculada a partir do expediente global, da duração do serviço e dos agendamentos não cancelados. Deve haver intervalo de 15 minutos entre atendimentos. Um serviço só pode ser agendado se a duração do atendimento e o intervalo de preparação couberem no expediente.

  * O backend é a autoridade final de disponibilidade. Para verificar conflito, considerar ocupado cada intervalo desde `start_time` até `end_time + 15 minutos` (intervalo de preparação). Rejeitar sobreposição para o mesmo barbeiro quando `início_existente < fim_ocupado_solicitado` e `fim_ocupado_existente > início_solicitado`. A verificação e a criação precisam ser protegidas por um mecanismo atômico suportado pelo Xano (por exemplo, transação/lock ou estratégia equivalente), para que duas reservas simultâneas não ocupem o mesmo horário. Uma simples checagem imediatamente antes do insert não é suficiente. Em conflito, retornar `409` sem criar o agendamento e informar ao cliente que o horário não está mais disponível.

  * Novos agendamentos começam como `pending`. O barbeiro ou administrador pode confirmar, concluir ou cancelar; o cliente pode cancelar o próprio agendamento até 12 horas antes do início. Administradores podem cancelar a qualquer momento. Agendamentos concluídos não podem voltar a estados anteriores. Cancelamentos registram data/hora e autor.

### Módulo 4: Painel Administrativo / Gestão da Barbearia

* **Funcionalidades:**

  * Agenda diária/semanal dos barbeiros.

  * Alteração manual de status do agendamento (ex: marcar como concluído).

  * Cadastro, edição e remoção de serviços e barbeiros.

  * Relatório simples de faturamento diário/mensal.

  * A agenda permite filtrar por barbeiro e período, e exibe horários no fuso da barbearia. Barbeiros só acessam sua própria agenda; administradores acessam todas.

  * Exclusão de serviços, barbeiros e usuários com histórico deve ser lógica (desativação). Registros referenciados por agendamentos não são apagados fisicamente pela interface.

  * O faturamento contabiliza o preço registrado no agendamento apenas quando o estado for `completed`, agrupado pela data local do início do atendimento. Agendamentos pendentes, confirmados ou cancelados não entram no total. Descontos, taxas, gorjetas e reembolsos ficam fora do escopo inicial.

## 4. Modelagem de Dados (Xano Database)

O backend Xano gerenciará as seguintes tabelas principais:

1. **`user`**:

   * `id` (integer, primary key)

   * `name` (text)

   * `email` (text, unique)

   * `password` (text, hashed)

   * `phone` (text)

   * `role` (enum: `client`, `barber`, `admin`)

   * `created_at` (timestamp)

   * `active` (boolean, padrão `true`)

2. **`service`**:

   * `id` (integer, primary key)

   * `title` (text)

   * `description` (text)

   * `price` (decimal/numeric)

   * `duration_minutes` (integer)

   * `active` (boolean, padrão `true`)

3. **`barber`**:

   * `id` (integer, primary key)

   * `user_id` (table reference -> `user`)

   * `bio` (text)

   * `specialties` (text ou lista de textos)

   * `active` (boolean, padrão `true`)

   * O expediente é global para a unidade: segunda-feira a sábado, das 09h às 18h, no fuso `America/Sao_Paulo`. Não há expediente individual por barbeiro no escopo inicial.

4. **`appointment`**:

   * `id` (integer, primary key)

   * `client_id` (table reference -> `user`)

   * `barber_id` (table reference -> `barber`)

   * `service_id` (table reference -> `service`)

   * `service_title_snapshot` (text)

   * `price_snapshot` (decimal/numeric)

   * `duration_minutes_snapshot` (integer)

   * `start_time` (timestamp)

   * `end_time` (timestamp)

   * `status` (enum: `pending`, `confirmed`, `cancelled`, `completed`)

   * `created_at` (timestamp)

   * `cancelled_at` (timestamp, nullable)

   * `cancelled_by` (table reference -> `user`, nullable)

   * `updated_at` (timestamp)

   * `notes` (text, opcional; não incluir dados sensíveis desnecessários)

   * Os campos `*_snapshot` preservam nome, preço e duração usados na reserva. Alterações posteriores no catálogo não modificam agendamentos existentes.

   * Todos os preços são armazenados em moeda decimal, nunca em ponto flutuante binário. A moeda padrão é BRL (R$).

5. **`appointment_status_history`**:

   * `id` (integer, primary key)

   * `appointment_id` (table reference -> `appointment`)

   * `from_status` (enum acima, nullable apenas na criação)

   * `to_status` (enum acima)

   * `changed_by` (table reference -> `user`)

   * `changed_at` (timestamp UTC)

   * `notes` (text, opcional)

   * Criar o agendamento e o primeiro evento de histórico na mesma operação. Cada transição de estado permitida cria um evento; o histórico não pode ser editado pelo cliente.

## 5. Regras de negócio e disponibilidade

* Há uma única unidade. O fuso é `America/Sao_Paulo`; o banco armazena instantes em UTC e conversões e agrupamentos de relatórios usam esse fuso.
* A duração efetiva de uma reserva é a duração do serviço. O intervalo de preparação de 15 minutos bloqueia a agenda após o atendimento e é considerado na validação de disponibilidade, mas não altera a duração ou o preço exibidos ao cliente.
* `end_time` representa o fim real do serviço (`start_time + duration_minutes_snapshot`); o intervalo ocupado para conflitos termina 15 minutos depois de `end_time`. O próximo atendimento pode começar nesse limite, mas não antes.
* Não há grade fixa de início em incrementos de 15 minutos: os horários oferecidos são calculados usando a duração exata do serviço escolhido, respeitando o intervalo de preparação e os conflitos existentes.
* A disponibilidade só pode ser oferecida de segunda-feira a sábado, das 09h às 18h, para serviço e barbeiro ativos. A duração do atendimento e o intervalo de preparação devem caber integralmente no expediente. Nenhum horário no passado pode ser reservado.
* Desativar um serviço ou barbeiro o remove imediatamente das opções para novas reservas. Agendamentos futuros já registrados permanecem intactos e visíveis na gestão; cabe ao administrador decidir se serão atendidos ou se entrará em contato com o cliente para remarcar.
* Para alteração de status, transições permitidas:
  * `pending` -> `confirmed` ou `cancelled`.
  * `confirmed` -> `completed` ou `cancelled`.
  * `completed` e `cancelled` são estados finais.
* Um atendimento só pode ser marcado como `completed` após seu horário de término. Administradores podem corrigir dados operacionais por ação administrativa auditada, sem apagar o histórico de estados.
* Cada alteração de status registra usuário responsável e data/hora em UTC. Para auditoria completa, manter histórico de eventos de status; não sobrescrever silenciosamente o histórico.
* A criação ou confirmação que resulte em conflito é recusada pelo backend. A verificação de disponibilidade e a gravação devem ser protegidas por mecanismo atômico suportado pelo Xano (por exemplo, transação/lock ou estratégia equivalente); uma checagem isolada antes do insert, mesmo imediatamente antes, não garante proteção contra concorrência. Em conflito, responder `409` e não criar registros parciais.
* A política padrão de cancelamento do cliente é até 12 horas antes do início. Depois desse limite, somente barbeiro ou administrador pode cancelar. A política pode ser ajustada pela barbearia.

## 6. Contrato das APIs

* A URL base do Xano é configurada por ambiente (desenvolvimento, homologação e produção); não deve ser repetida como literal no código do frontend. O workspace Xano indicado para este projeto é `149139`; endpoints devem ser confirmados nesse workspace antes da integração.
* Endpoints REST mínimos previstos:
  * `POST /auth/signup`, `POST /auth/login`, `GET /auth/me`.
  * `GET /services`, `GET /barbers`, `GET /availability?barber_id=...&service_id=...&date=...`.
  * `POST /appointments`, `GET /appointments/me`, `GET /appointments/{id}`, `POST /appointments/{id}/cancel`.
  * Administração: `GET /admin/appointments?from=...&to=...&barber_id=...`, `PATCH /appointments/{id}/status`, endpoints protegidos `POST`/`PATCH` para criar/editar serviços e barbeiros, `PATCH` para desativá-los e `GET /admin/reports/revenue?period=day|month&date=...`.
* As rotas são uma proposta de contrato lógico; os caminhos reais devem ser mapeados aos endpoints existentes/criados no Xano, documentados e mantidos consistentes no frontend.
* Respostas JSON devem usar nomes de campos estáveis em `snake_case`; listas devem retornar estrutura previsível e paginação quando aplicável (`items`, `page`, `page_size`, `total`).
* Erros devem ter formato uniforme, por exemplo `{"error":{"code":"...","message":"...","details":{}}}`. Usar `400` para entrada inválida, `401` para ausência/invalidade de autenticação, `403` para falta de permissão, `404` para recurso inexistente, `409` para conflito de agenda e `5xx` para falhas inesperadas. Não retornar sucesso se a operação falhou.
* Validar no backend todos os campos, referências, regras de papel, disponibilidade e transições de estado. O frontend não é uma fronteira de segurança.

## 7. Requisitos não funcionais e privacidade

* Interface responsiva para celular e desktop, com rótulos acessíveis, navegação por teclado e mensagens de erro compreensíveis.
* Não expor segredos ou credenciais no frontend ou no repositório. URLs e configurações não secretas podem variar por ambiente; chaves privadas permanecem em configuração segura do servidor.
* Coletar somente dados necessários. Restringir acesso a dados pessoais por papel e propriedade do registro; não expor telefone, e-mail ou dados de clientes na agenda pública.
* Registrar eventos operacionais relevantes (criação/cancelamento de agendamento, mudanças de status e alterações administrativas) sem gravar senhas, tokens ou conteúdo sensível.
* Tratar falhas de rede e respostas inesperadas sem perder dados já confirmados; mostrar claramente quando a disponibilidade precisa ser atualizada.

## 8. Critérios de aceite do MVP

1. Um visitante pode criar conta de cliente e entrar; não pode atribuir a si mesmo papel de barbeiro ou administrador.
2. Um cliente autenticado pode consultar serviços/barbeiros ativos, obter horários disponíveis e criar um agendamento válido.
3. Duas solicitações concorrentes para horários sobrepostos do mesmo barbeiro não podem resultar em duas reservas; a segunda recebe conflito `409`.
4. Um cliente só consulta/cancela os próprios agendamentos e não pode cancelar fora do limite de 12 horas; barbeiro e administrador seguem as permissões definidas.
5. Barbeiro só consulta sua própria agenda e só atualiza estados permitidos; administrador pode gerenciar a agenda e os cadastros. Cada transição fica registrada no histórico com autor e horário.
6. Desativar serviço/barbeiro remove-o imediatamente das opções para novas reservas e preserva os agendamentos futuros já registrados; o administrador decide se serão atendidos ou se o cliente será contatado para remarcar.
7. Alterar preço ou duração do serviço não modifica os snapshots de agendamentos existentes.
8. Relatórios diários e mensais somam apenas atendimentos `completed`, usando o preço snapshot e o fuso da barbearia.
9. Datas exibidas respeitam o fuso configurado, enquanto timestamps persistidos e transferidos têm referência explícita de fuso.
10. Falhas de validação, autenticação, autorização e conflito apresentam códigos HTTP e mensagens consistentes, sem criar registros parciais.

## 9. Instruções Específicas para o GitHub Copilot (Prompt de Contexto)

Ao solicitar assistência ao Copilot para implementar partes deste projeto, utilize a seguinte orientação no chat:

> **Instrução para a IA:**
> "Estamos desenvolvendo um sistema de gerenciamento de barbearia com frontend em Reflex (Python) e backend no Xano.
>
> 1. Para código XanoScript (`.xs`), consulte a documentação e valide a sintaxe utilizando o **Xano Developer MCP**.
>
> 2. Para componentes de interface no Reflex, siga as convenções do Reflex (Python), criando páginas modularizadas dentro do diretório `app_barbearia/` e gerenciando estados com `rx.State`.
>
> 3. Certifique-se de que todas as chamadas de API do Reflex apontem para os endpoints correspondentes do Xano no workspace `149139`, usando configuração por ambiente em vez de URLs embutidas no código.
>
> 4. Use os estados `pending`, `confirmed`, `cancelled` e `completed`, aplique autorização no backend e nunca confie somente na validação do frontend.
>
> 5. Preserve o preço e a duração no snapshot do agendamento, use UTC para persistência e o fuso configurado para exibição e relatórios."