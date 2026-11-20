# Tasks

## 1. Backend Xano: disponibilidade e reserva

- [x] 1.1 Implementar e registrar lock nativo por barbeiro via `barber_booking_lock`/`db.add_or_edit` dentro de transação; comprovar com teste concorrente e bloquear a reserva se a atomicidade não puder ser validada no plano Xano alvo.
- [x] 1.2 Implementar `GET /availability` com expediente, timezone, duração exata, preparação, antecedência, horizonte e itens ativos; adicionar testes para limites, dias fechados, conflitos e conversão ISO 8601/UTC.
- [x] 1.3 Implementar `POST /appointments` com identidade derivada da sessão, validação de papel, snapshots e histórico inicial dentro da garantia atômica; verificar no Xano que uma solicitação válida persiste uma única reserva e conflito retorna `400` identificável sem registros parciais.
- [x] 1.4 Documentar no contrato OpenSpec/API os envelopes de disponibilidade e reserva e verificar que campos e erros publicados permanecem em `snake_case` e não expõem dados sensíveis.

## 2. Backend Xano: consultas, cancelamento e transições

- [x] 2.1 Implementar `GET /appointments/me` e `GET /appointments/{id}` com autorização por propriedade; testar que clientes só consultam dados próprios e que uma tentativa alheia não revela registros.
- [x] 2.2 Implementar `GET /barber/appointments` e `GET /admin/appointments` com filtros de data/período e autorização por papel; testar agenda própria do barbeiro, período administrativo e campos pessoais mínimos.
- [x] 2.3 Implementar `POST /appointments/{id}/cancel` com limite de 12 horas, estados elegíveis, autor/data de cancelamento e histórico; testar cancelamento permitido, fora do prazo, estado final e propriedade.
- [x] 2.4 Implementar `PATCH /appointments/{id}/status` com transições permitidas, autorização, conclusão após `end_time` e gravação do histórico; testar cada papel, transição inválida e falha sem sucesso parcial.

## 3. Integração Reflex: cliente

- [x] 3.1 Atualizar o mapeamento do `XanoRepository` para os envelopes reais, conflitos `400` normalizados como `appointment_conflict`, consultas por período e horários ISO 8601; verificar chamadas HTTP e Bearer com testes de contrato direcionados.
- [x] 3.2 Conectar disponibilidade, confirmação, lista/dashboard e cancelamento do cliente ao repositório Xano sem sucesso otimista; verificar estados atualizados somente após sucesso e limpeza de horários obsoletos em conflito/falha.
- [x] 3.3 Preservar o modo mock nas jornadas do cliente e executar testes de estado para mock e Xano, cobrindo carregamento, vazio, sucesso, erro e cancelamento.

## 4. Integração Reflex: barbeiro e administrador

- [x] 4.1 Conectar a agenda e as transições do barbeiro aos endpoints Xano, mantendo o escopo do barbeiro autenticado; verificar testes para agenda própria, data sem registros, falha e transições permitidas/recusadas.
- [x] 4.2 Conectar a agenda administrativa a filtros de período, barbeiro e estado e persistir transições somente após confirmação Xano; verificar filtros combinados, erros e isolamento do modo mock.

## 5. Validação ponta a ponta

- [x] 5.1 Executar a suíte de testes relacionada a API, repositórios e estado e corrigir regressões; registrar o resultado do comando executado.
- [x] 5.2 Validar no branch Xano alvo as respostas reais de disponibilidade, listagem por papel, criação, cancelamento e transições; verificar concorrência, histórico, autorização e contagens sem usar dados de usuários reais.
- [x] 5.3 Executar compilação Reflex e smoke test dos fluxos de agendamento de cliente, barbeiro e administrador com Xano configurado; confirmar que falhas não recorrem a dados mock.
