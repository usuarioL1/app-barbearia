# Design

## Context

Veja `proposal.md` e `specs/customer-portal/spec.md`. O login já é composto em `auth_pages.py`; estado e credenciais mockadas ficam fora da página. A URL `/login` não deve iniciar chamadas ao Xano.

## Goals / Non-Goals

**Goals:**
- Manter apresentação da marca e campos de autenticação coerentes com a referência BarberFlow.
- Expor validação, carregamento, sucesso e erro através do estado compartilhado.
- Preservar navegação por teclado, foco visível, autocomplete e rótulos acessíveis.

**Non-Goals:**
- Persistir sessão, senha ou credenciais.
- Alterar contratos de API ou integrar autenticação real.

## Decisions

- Manter componentes de autenticação compartilhados em `auth_pages.py`, evitando uma implementação isolada para o login.
- Delegar validação e autenticação ao estado e ao repositório mockado, em vez de guardar regra de domínio na função visual.
- Redirecionar ao portal somente após resposta mockada bem-sucedida; falhas não devem ter formato de sucesso.
- Reproduzir a composição em componentes Reflex, sem usar uma captura de tela como interface.

## Risks / Trade-offs

- [O login de demonstração pode ser confundido com sessão persistida] → Informar explicitamente que nenhuma sessão foi salva.
- [A composição desktop pode não caber em telas estreitas] → Manter o layout responsivo e os controles utilizáveis em viewport móvel.