# Relatório de inspeção do Xano

## Escopo e reprodução

Inspeção somente leitura do workspace `149139`, branch `v1`, em 15/11/2026.

Comandos executados:

```powershell
xano workspace list --output json
xano workspace pull --workspace 149139 --directory <diretorio-temporario>
xano branch list --workspace 149139 --output json
```

O workspace indicou `allow_push: false`; a única branch listada foi `v1`, marcada como live. O pull baixou 17 documentos XanoScript, sem solicitar registros, variáveis de ambiente ou estado de sincronização. Não foi feita nenhuma escrita no Xano.

O pull não incluiu definições de tabelas/schema. O documento `addon/user.xs` tem referências de tabela vazias. A estrutura de usuário informada pelo usuário, ainda não conferida diretamente contra a branch remota, foi:

| Campo informado | Tipo | Obrigatório | Default/restrição informada |
|---|---|---:|---|
| `id` | integer | sim | único; chave primária |
| `name` | text | sim | — |
| `email` | email | sim | único |
| `password` | password | sim | hash |
| `phone` | text | não | — |
| `role` | text | sim | default `client`; valores anotados: `client`, `barber`, `admin` |
| `created_at` | timestamp | sim | — |
| `active` | boolean | sim | default `true` |

O usuário confirmou que `password_reset` está ausente no workspace, embora scripts de recuperação existentes no pull a leiam e atualizem.

## Contratos encontrados

| Método e rota | Autenticação | Entrada e resposta observadas |
|---|---|---|
| `POST /auth/signup` | Não requerida | Recebe `name`, `email`, `password`; cria papel `member`; responde `authToken` e `user_id`. Não recebe `phone`. |
| `POST /auth/login` | Não requerida | Recebe `email`, `password`; responde `authToken` e `user_id`. Expiração do token: 86.400 segundos. |
| `GET /auth/me` | Requer token | Responde `id`, `created_at`, `name`, `email`, `role`; não responde `phone`. |
| `GET /reset/request-reset-link?email=...` | Não requerida | Gera e envia link de redefinição; o link gerado aponta para a página demo `1_start_here_demo_page`. |
| `POST /reset/magic-link-login` | Não requerida | Recebe `magic_token`, `email`; responde `authToken` e `user_id`. Token de sessão com validade de 86.400 segundos. |
| `POST /reset/update_password` | Requer token | Recebe `password`, `confirm_password`; atualiza a senha da conta autenticada. |
| `GET /logs/user/my_events` | Requer token | Retorna eventos associados ao usuário autenticado. |

As rotas foram confirmadas nos arquivos sob `api/authentication/` e `api/event_logs/`; não foram inferidas a partir das rotas propostas na especificação.

Não foram encontrados endpoints para serviços, barbeiros, disponibilidade, agendamentos, agenda, clientes, relatórios ou gestão administrativa. Também não há scripts de negócio correspondentes no pull. O helper `enforce_role` reconhece `admin` e `member`; o cadastro atribui `member`, apesar de a estrutura de usuário informada anotar `client`, `barber` e `admin`.

## Lacunas remotas e trabalho futuro

1. **Papéis e cadastro:** o papel público observado é `member`, divergente de `client`; não há papel `barber` demonstrado. O frontend não deve reinterpretar nem promover esses papéis.
2. **Telefone:** a estrutura informada inclui `phone` opcional, mas o cadastro remoto não o aceita.
3. **Perfil:** `/auth/me` remoto não responde telefone; login não devolve perfil/papel e exige consulta separada.
4. **Redefinição:** o fluxo remoto direciona para página demo e pressupõe `password_reset`, que foi confirmado ausente.
5. **Dados em logs:** `auth/login` inclui `$user` (que seleciona explicitamente `password`) nos metadados do evento; `auth/signup` também registra o objeto criado. A função `Quick Start/log_event` grava os metadados sem sanitização e `logs/user/my_events` os devolve, indicando risco de exposição de senha nos logs remotos.
6. **Catálogo e demais jornadas:** não foram encontrados endpoints de negócio no pull. Disponibilidade, operações de agendamento e proteção concorrente, agendas e administração permanecem para changes futuras e confirmação de contratos.
7. **Escrita no workspace:** a preferência `allow_push: false` e a ausência de branch de desenvolvimento impediram uma implantação apropriada. A tentativa read-only de pull da branch `dev` retornou `404 Not Found`; não houve tentativa de contornar esse bloqueio.

## Recorte desta change — somente local

Por solicitação do usuário, `xano-integration` cobre apenas a fatia local de autenticação/recuperação, perfil, catálogo inicial de serviços/barbeiros e definições de tabelas presentes em `xano/table/`. Os arquivos de tabelas locais são `appointment.xs`, `appointment_status_history.xs`, `barber.xs`, `password_reset.xs` e `service.xs`. Essas definições são artefatos locais; não representam schema confirmado nem aplicado no Xano remoto. A inclusão das definições de agendamento não implementa disponibilidade, criação/cancelamento de reservas ou regras de concorrência.

Os scripts locais incluem autenticação, perfil, recuperação, catálogo e alterações de privacidade de logs. O código local não foi publicado, e os achados remotos acima permanecem válidos. O modo Xano do Reflex informa falhas sem fallback para sucesso simulado; os contratos locais não foram validados em runtime contra a branch remota.

Disponibilidade, ciclo de vida de agendamentos, conflito atômico, agendas de barbeiros, administração e relatórios foram explicitamente excluídos desta fatia e devem ser tratados em changes futuras. Nenhum `xano push`, escrita pela Meta API ou outra operação remota foi executada.

## Verificações locais registradas

- Validador XanoScript: 27 arquivos válidos, 0 inválidos, 0 avisos.
- Testes Python: 57 testes aprovados por `python -m unittest discover -s tests -q`.
- `venv\\Scripts\\reflex.exe compile --dry`: compilação aprovada.
- `openspec validate xano-integration --strict --json`: validação aprovada após a revisão dos artefatos.

Essas verificações atestam somente a sintaxe, testes e compilação locais; não confirmam deploy, schema remoto, permissões nem comportamento em runtime. As tarefas listadas em `tasks.md` estão concluídas para este recorte local, não para as jornadas futuras nem para implantação no Xano.
