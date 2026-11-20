# Design

## Context

Ver [proposal.md](./proposal.md) para a motivação e [specs/appointments/spec.md](./specs/appointments/spec.md) para os contratos de domínio. As tabelas `appointment` e `appointment_status_history` já existem. O `XanoRepository` já chama rotas de disponibilidade, reserva, listagens e transições, mas os arquivos de API Xano do projeto atualmente cobrem autenticação, catálogo e logs, não agendamentos. As jornadas de cliente, barbeiro e administrador já têm estados e operações mock.

## Goals / Non-Goals

**Goals:**
- Manter os contratos do cliente Reflex compatíveis com o grupo de API configurado e com as regras da especificação.
- Concentrar autorização, validação temporal, conflitos, snapshots e histórico no backend Xano.
- Preservar a separação entre modo Xano e modo demonstrativo.
- Exigir prova de atomicidade antes de habilitar a criação de reservas.

**Non-Goals:**
- Alterar o modelo de autenticação ou provisionamento de papéis.
- Implementar gestão de catálogo, relatórios financeiros ou novas políticas administrativas.
- Introduzir outra fonte de dados ou dependência de runtime.

## Decisions

1. **Manter uma API de domínio de agendamentos no grupo Xano existente.** Implementar `GET /availability`, `POST /appointments`, `GET /appointments/me`, `GET /barber/appointments`, `GET /admin/appointments`, `GET /appointments/{id}`, `POST /appointments/{id}/cancel` e `PATCH /appointments/{id}/status`, alinhados às chamadas existentes e às rotas lógicas documentadas. A consulta administrativa aceitará intervalo `from`/`to` e filtros opcionais. Alternativas: criar outro grupo ou renomear os caminhos no cliente; ambas aumentariam divergência e risco de quebra sem benefício funcional.

2. **Derivar identidade e autorização do token em todas as mutações e consultas protegidas.** O cliente não escolhe `client_id`; o barbeiro é resolvido pelo usuário autenticado; operações administrativas exigem `admin`. O backend verifica propriedade e papel em cada endpoint. Alternativa: confiar nos identificadores enviados pelo frontend; rejeitada por permitir acesso ou alteração de dados alheios.

3. **Calcular horários no domínio usando `America/Sao_Paulo` e persistir instantes UTC.** A disponibilidade combina expediente, duração exata, preparação, horizonte, antecedência e reservas não canceladas. Ao encontrar uma colisão, o cálculo avança para o fim do último intervalo ocupado conflitante e volta a procurar a partir desse limite, em vez de descartar o horário e continuar numa grade fixa. Respostas usam ISO 8601 com offset. As alterações mantêm os snapshots já previstos no modelo. Alternativa: calcular disponibilidade só no frontend; rejeitada porque o estado pode mudar e o cliente não é autoridade.

4. **Serializar reservas por barbeiro com lock de linha nativo.** Criar a tabela técnica `barber_booking_lock` com índice único por `barber_id`. Dentro de `db.transaction`, executar `db.add_or_edit` nessa chave antes de consultar conflitos e manter a transação aberta até gravar o agendamento e o histórico. O Xano Free retornou `403` (“Not supported. Please upgrade your Xano instance”) ao executar o caminho com `db.direct_query`; por isso, a alternativa nativa só será aceita após validar transação/upsert e provar a exclusão mútua em chamadas concorrentes no branch alvo. Conflitos usarão `badrequest` (`400`), distinto de erros comuns de entrada (`inputerror`), e o `XanoRepository` normalizará o envelope específico como `appointment_conflict`. Se a estratégia nativa não for suportada ou o teste admitir duas reservas, bloquear a criação e reportar a limitação.

5. **Centralizar as transições e sua auditoria no backend.** Cancelamento e mudanças de estado validam o estado anterior, papel, atribuição e horário de término e gravam evento em `appointment_status_history` junto com a atualização. A operação não retorna sucesso se qualquer gravação necessária falhar. Alternativa: atualizar estado diretamente na interface ou em endpoints desconectados; rejeitada por permitir divergência e perda de auditoria.

6. **Preservar os adaptadores e a UX existentes, atualizando o estado apenas com respostas confirmadas.** O `XanoRepository` envia a sessão apenas em chamadas protegidas e valida os envelopes retornados; conflitos invalidam a opção de horário e pedem nova consulta. Erros de Xano permanecem explícitos, sem fallback ao mock. O modo mock continua isolado e rotulado como não persistente. Alternativa: manter confirmações otimistas ou fazer fallback após falha; rejeitada porque aparentaria reservas inexistentes.

## Risks / Trade-offs

- [O Xano pode não oferecer uma primitiva atômica adequada para exclusão de conflitos concorrentes] → comprovar a estratégia antes da implementação/publicação; bloquear reservas reais se a prova falhar.
- [Diferenças de timezone ou horário de verão podem deslocar horários apresentados] → converter com `America/Sao_Paulo`, trafegar ISO 8601 com offset e testar limites de expediente e conversões UTC.
- [A API publicada pode diferir do código local ou dos envelopes esperados pelo Reflex] → testar contratos no workspace/branch alvo e ajustar o mapeamento sem aceitar respostas incompletas como sucesso.
- [Falha parcial entre estado e histórico pode comprometer auditoria] → gravar ambos sob a mesma garantia transacional e testar falhas antes da publicação.
- [A mudança substitui dados mock nas jornadas operacionais quando Xano está configurado] → manter o modo demo isolado e nunca ocultar erro real com dados de demonstração.

## Migration Plan

1. Confirmar no Xano a disponibilidade de mecanismo atômico, verificar as tabelas existentes e implantar as APIs sem habilitar reserva até passar os testes de concorrência.
2. Implementar o mapeamento do `XanoRepository` e conectar as jornadas Reflex, preservando o caminho mock em modo demo.
3. Validar permissões por papel, limites temporais, snapshots, histórico, conflitos concorrentes e respostas reais de cada endpoint no branch alvo.
4. Habilitar `XANO_API_BASE_URL` somente após os testes de contrato e concorrência passarem. Em caso de falha, reverter a implantação das APIs e manter a interface sem sucesso de reserva; não trocar automaticamente para o mock.
