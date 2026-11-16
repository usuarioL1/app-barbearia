# Design

## Context

A rota `/perfil` usa o layout do cliente e apresenta campos controlados para nome, e-mail e telefone em `customer_portal.py`. `AppState.load_profile` carrega o perfil do repositório mockado; `save_profile` valida os campos e chama `MockRepository.update_profile`.

## Goals / Non-Goals

**Goals:**
- Documentar consulta e edição dos três campos existentes.
- Preservar validação, mensagens de resultado e composição atual da tela.

**Non-Goals:**
- Acrescentar alteração de senha, dados de conta não apresentados ou persistência.

## Decisions

1. Manter os campos vinculados ao estado compartilhado do cliente e apresentar o usuário retornado pelo repositório.
2. Validar nome, e-mail e telefone antes da chamada mockada e usar o mecanismo comum de feedback para erros e sucesso.
3. Tratar o retorno como alteração apenas demonstrativa, sem salvar no repositório original.

## Risks / Trade-offs

- O retorno de sucesso atualiza o estado de apresentação; a mensagem deve continuar deixando claro que a alteração é simulada.