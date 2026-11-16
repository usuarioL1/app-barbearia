# Design

## Context

A rota `/login` usa componentes compartilhados de `auth_pages.py` e eventos de `AppState`. A autenticação fica isolada no repositório mockado até a futura mudança de integração Xano.

## Goals / Non-Goals

**Goals:**
- Preservar a composição, os campos e a paleta do design BarberFlow.
- Manter os estados de validação claros e as operações explicitamente não persistentes.

**Non-Goals:**
- Criar uma sessão real, armazenar credenciais ou conectar a rota a endpoints.

## Decisions

- Manter a tela em componentes Reflex existentes e reutilizar os campos, botões e feedback comuns.
- Manter validação e autenticação no estado e repositório mockados; uma chamada HTTP foi descartada até a change de Xano.

## Risks / Trade-offs

- [O usuário pode interpretar o acesso simulado como persistido] → Informar explicitamente que nenhuma sessão foi salva.
