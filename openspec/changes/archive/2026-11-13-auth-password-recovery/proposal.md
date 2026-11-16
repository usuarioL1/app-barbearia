# Proposal

## Why

A recuperação de senha é uma rota pública própria e deve ficar rastreável sem se confundir com login ou cadastro. A interface concluída valida o e-mail e simula a solicitação sem enviar mensagens.

## What Changes

- Registrar a tela `/recuperar-senha` e a resposta não persistente do fluxo mockado como entregues.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `customer-portal`: adicionar o contrato da recuperação visual de senha.

## Impact

- `app_barbearia/auth_pages.py` e estado mockado. O envio real de e-mail permanece fora desta change.
