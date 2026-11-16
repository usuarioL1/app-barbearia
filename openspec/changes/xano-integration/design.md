# Design

## Context

Veja `proposal.md` e as specs delta. O frontend tinha um cliente HTTP genérico, mas as jornadas usavam `MockRepository`. A inspeção somente leitura do workspace `149139` não confirmou contratos de negócio suficientes para deploy. O escopo desta execução é estritamente local: editar e validar XanoScript e integrar o frontend, sem `xano push`, Meta API de escrita ou alteração no workspace remoto.

## Goals / Non-Goals

**Goals:**
- Descobrir schema, papéis, endpoints e formatos de resposta antes de conectar cada fluxo.
- Preservar separação entre UI/estado e transporte HTTP, com validação explícita de respostas.
- Manter autorização, propriedade dos registros, fuso, conflitos e não persistência de senhas/tokens em logs.
- Selecionar explicitamente o modo Xano por configuração; quando selecionado, falhas não devem voltar para dados mockados.
- Manter os mocks como modo de demonstração separado enquanto os contratos remotos e o deploy não forem confirmados.

**Non-Goals:**
- Supor que as rotas propostas na especificação já existem no Xano.
- Alterar schema, converter contas existentes ou publicar endpoints sem decisão explícita.
- Remover a fonte mockada antes da validação dos fluxos integrados.

## Decisions

- Fazer inspeção read-only no workspace Xano `149139` antes de editar tabelas ou scripts; verificar `phone`, papéis e relações e apresentar qualquer migração necessária para aprovação.
- Mapear cada endpoint existente para os fluxos do app e documentar lacunas antes de implementar. Caminhos inferidos ou sugestões do projeto não serão tratados como contratos confirmados.
- Manter `api_client.py` como transporte e usar `xano_repository.py` para adaptar respostas, erros e autenticação aos tipos do estado Reflex.
- `XANO_API_BASE_URL` deve apontar para a URL-base do grupo Xano `Authentication` (incluindo `/api:5t-IFNmz`). `BARBERFLOW_MODE=xano` seleciona Xano; sem endpoint configurado em produção, a integração falha explicitamente. O modo `demo` é separado e não é fallback de erros Xano.
- A sessão JWT, senhas e token de recuperação ficam em variáveis privadas do estado Reflex, não serializadas como estado público. O cadastro não envia papel; o servidor atribui `client`.
- O código local inclui scripts de autenticação, perfil, recuperação e leitura do catálogo, além de propostas locais de tabelas. Esses arquivos ainda não foram aplicados nem confirmados no workspace.
- A recuperação local usa `password_reset` e requer as variáveis Xano `APP_BASE_URL`, `RESEND_API_KEY` e `RESEND_FROM_EMAIL`; nenhuma foi configurada nem enviada.
- Usar respostas do Xano como autoridade; não aplicar sucesso otimista e não apresentar fallback mockado quando uma chamada real falhar.
- Exigir aprovação do usuário antes de migrações, conversão de contas ou qualquer alteração de schema já existente.
- Não executar push nem usar outro caminho de escrita remota nesta change. A validação XanoScript confirma sintaxe, não compatibilidade com tabelas, execução, permissões ou comportamento do workspace.
- Não converter contas `member` existentes. O retorno do papel `member` não é aceito pelo frontend como papel de negócio válido até decisão/migração aprovada.

## Risks / Trade-offs

- [Schema ou papel de usuário pode divergir da especificação] → As tabelas `service`, `barber`, `appointment`, `appointment_status_history` e `password_reset` são apenas propostas locais; não são evidência do schema remoto.
- [Endpoints reais podem divergir dos caminhos propostos] → Rotas locais de catálogo e autenticação não foram implantadas nem verificadas contra a branch remota.
- [Concorrência de agendamento] → Não há evidência runtime de mecanismo atômico Xano que proteja a verificação de sobreposição; não declarar reserva concorrente segura nem concluir a integração de agendamento sem essa validação.
- [Workspace sem branch de desenvolvimento] → A execução local não publica nada. A implantação permanece separada e bloqueada pelo escopo atual e pelo `allow_push: false` observado.
- [Fallbacks podem mascarar indisponibilidade] → Manter falhas explícitas e preservar somente dados previamente confirmados, sem declarar persistência quando não houve sucesso.
- [Sessões ou logs podem expor credenciais] → Usar o mecanismo seguro do Xano, Bearer somente no cabeçalho e testes que garantam ausência de senha/token nos logs.

## Migration Plan

1. Preservar o relatório de inspeção read-only e os contratos ainda ausentes.
2. Escrever localmente scripts Xano e adaptadores Reflex; validar sintaxe XanoScript, testes automatizados e compilação Reflex.
3. Manter as tarefas OpenSpec pendentes quando dependerem de deploy, confirmação do schema remoto, testes de contrato ou validação de concorrência.
4. Não fazer push, Meta API de escrita nem outras alterações remotas nesta execução.
