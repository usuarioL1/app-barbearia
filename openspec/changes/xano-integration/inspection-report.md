# Relatório de inspeção do Xano

## Escopo e reprodução

Inspeção somente leitura do workspace `149139`, branch `v1`, em 15/11/2026.

Comandos executados:

```powershell
xano workspace list --output json
xano workspace pull --workspace 149139 --directory <diretorio-temporario>
```

O primeiro comando identificou `Lucas's Workspace` (`149139`) e a preferência `allow_push: false`. A listagem somente leitura com `xano branch list --workspace 149139 --output json` mostrou apenas a branch `v1`, marcada como live. O pull baixou 17 documentos XanoScript para um diretório temporário, sem solicitar registros, variáveis de ambiente ou estado de sincronização. Nenhuma escrita foi feita no Xano.

O pull não incluiu definições de tabelas/schema. O documento `addon/user.xs` tem referências de tabela vazias. Depois da inspeção, o usuário forneceu a estrutura abaixo para leitura; ela ainda não foi conferida diretamente contra a branch Xano, pois a branch indicada não aparece no CLI.

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

O usuário confirmou que `password_reset` está ausente, embora os scripts de recuperação o leiam e atualizem.

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

Não foram encontrados endpoints para serviços, barbeiros, disponibilidade, agendamentos, agenda, clientes, relatórios ou gestão administrativa. Também não há scripts de negócio correspondentes no pull. O helper `enforce_role` reconhece `admin` e `member`; o cadastro atribui `member`, apesar de o schema informado anotar `client`, `barber` e `admin`.

## Lacunas e riscos que bloqueiam a integração

1. **Papéis e cadastro:** o papel público atual é `member`, divergente de `client`; não há papel `barber` demonstrado. O frontend não deve reinterpretar nem promover esses papéis.
2. **Telefone:** o schema informado inclui `phone` como opcional, mas o cadastro não o aceita; a API precisará exigi-lo conforme a especificação.
3. **Autorização e perfil:** login não devolve papel nem perfil; seria necessário consultar `/auth/me`. Não foi confirmado que o servidor verifica `active` ou limita a sessão ao papel esperado.
4. **Redefinição:** o contrato exige o fluxo `request-reset-link` → `magic-link-login` → `update_password`; o link atual direciona a uma página demo, então não deve ser conectado como se fosse um fluxo pronto da aplicação.
5. **Dados em logs:** `auth/login` inclui `$user` (que seleciona explicitamente `password`) nos metadados do evento; `auth/signup` também registra o objeto criado. A função `Quick Start/log_event` grava os metadados sem sanitização, e `logs/user/my_events` os devolve. Assim, há evidência de que dados de senha podem ser armazenados e expostos pelos logs. O código remoto precisa ser corrigido antes de usar esses fluxos.
6. **Outras jornadas:** sem endpoints confirmados, não é seguro conectar telas de catálogo, reserva, agenda ou administração nem simular sucesso persistido.
7. **Escrita no workspace:** a preferência `allow_push: false` impede push pelo CLI. Após o usuário informar que criou `dev`, `xano branch list --workspace 149139 --output json` ainda mostrou apenas `v1`, e `xano workspace pull --workspace 149139 --branch dev --directory <diretorio-temporario>` retornou `404 Not Found`. Não tentei contornar essa restrição nem alterar o workspace.

## Proposta para decisão — nenhuma migração executada

O usuário inicialmente autorizou mudanças somente após inspeção, em branch não-live, sem conversão automática de contas `member` existentes. Depois confirmou que o plano Free oferece somente `v1` live e pediu que as mudanças fossem feitas diretamente nessa branch. Isso conflita com a tarefa OpenSpec, que exige validar a migração em ambiente seguro antes de aplicar; nenhuma escrita foi feita enquanto esse conflito permanece.

O schema informado contém `phone` opcional e papéis `client`, `barber`, `admin`, mas os scripts divergem. A tabela também não possui `password_reset`, requerido pelo fluxo atual. A proposta para validação segura é:

- alinhar o cadastro/helper às roles informadas (`client`, `barber`, `admin`), preservando administradores e provisionando barbeiros apenas por administração; não converter automaticamente contas `member` existentes;
- aceitar `phone` no cadastro e no perfil, validar como obrigatório no cadastro e definir como tratar contas existentes sem telefone;
- adicionar e validar suporte a `password_reset` usado pelo fluxo de recuperação, ou aprovar outro fluxo que não dependa desse campo;
- retornar apenas os campos necessários e autorizados em `/auth/me`, verificar contas ativas e manter a autorização no backend;
- remover senha, token e outros dados pessoais desnecessários dos metadados de eventos existentes e futuros, e limitar os metadados retornados pelos logs;
- implementar e confirmar os endpoints de catálogo, disponibilidade, agendamento e administração, incluindo autorização, conflito atômico `409`, estados, snapshots e fuso definidos na especificação.

Antes da implementação local descrita abaixo, a recomendação era manter o fluxo demonstrativo mockado até a aprovação da migração e a confirmação dos contratos. Atualmente, o modo `demo` continua mockado; o modo `xano` chama o adaptador real e informa falhas sem fallback, mas suas rotas propostas ainda não foram confirmadas ou implantadas.

## Implementação local posterior à inspeção — sem deploy

Por solicitação do usuário, foram editados apenas arquivos locais. Não foi executado `xano push`, Meta API de escrita ou qualquer operação que altere o workspace. Portanto, os achados sobre a branch `v1` continuam descrevendo o estado remoto observado anteriormente; em particular, os riscos de logs e as divergências de schema continuam existentes no Xano até uma futura aplicação autorizada.

Scripts locais alterados ou adicionados:

- Login, cadastro e `/auth/me`: respostas explícitas sem senha, cadastro exige telefone e cria `client`, conta inativa não autentica.
- Perfil: endpoint PATCH com campos permitidos somente (nome, e-mail e telefone).
- Recuperação: tabela local `password_reset` com token do tipo `password`, validade de uma hora e uso único; endpoints POST para solicitar e concluir a redefinição. O envio de e-mail usa Resend.
- Logs: a função local não persiste metadados e o endpoint local de eventos não retorna a coluna `metadata`.
- Catálogo: endpoints locais somente leitura para serviços e barbeiros ativos.
- Tabelas locais propostas para serviços, barbeiros, agendamentos e histórico de status; a definição `user` não foi reconstruída porque o pull não trouxe seu schema.

`XANO_API_BASE_URL` deve conter a base do grupo `Authentication`, incluindo `/api:5t-IFNmz`. O modo Xano não volta a mocks se a chamada falhar. O modo demonstrativo é selecionado separadamente por `BARBERFLOW_MODE=demo`; em produção, usar `BARBERFLOW_MODE=xano` e configurar a URL. Para recuperação, o Xano também precisa das variáveis `APP_BASE_URL`, `RESEND_API_KEY` e `RESEND_FROM_EMAIL`. Essas variáveis não foram criadas nem configuradas.

O adaptador Reflex define contratos para as jornadas restantes, mas não foram encontrados nem criados scripts locais para disponibilidade, criação/cancelamento de agendamentos, agenda de barbeiros, relatórios e operações administrativas. Essas chamadas falham explicitamente em Xano mode enquanto não houver endpoints. A proteção atômica contra reservas simultâneas também não foi executada nem comprovada. A validação XanoScript abaixo cobre apenas sintaxe, não deploy, schema remoto, permissões ou comportamento runtime.

Verificações locais após essas edições:

- Validador XanoScript: 27 arquivos válidos, 0 inválidos.
- Testes Python: 57 testes aprovados.
- `python -m reflex compile --dry`: compilação aprovada.

As tarefas OpenSpec 1.2, 2.1, 2.2 e 3.1 permanecem pendentes: nenhuma das validações locais confirma que os scripts foram implantados ou que o contrato remoto funciona; os endpoints de negócio e a atomicidade ainda não foram validados.
