# Design

## Context

A agenda do barbeiro usa o estado da aplicação e `MockRepository`; a projeção de cada atendimento omite `client_id` e `client_email`. A data é consultada como dia local e a navegação altera a seleção somente quando a consulta simulada é concluída.

## Goals / Non-Goals

**Goals:**
- Manter a agenda diária escopada ao barbeiro selecionado no estado.
- Preservar campos mínimos de apresentação e mensagens de carregamento, vazio e falha.

**Non-Goals:**
- Autenticar ou autorizar usuários contra um servidor.
- Persistir consultas ou alterações, nem conectar a agenda ao Xano.

## Decisions

- Manter o repositório mock como fonte da agenda nesta etapa; assim os cenários podem ser exercitados sem rede ou dados persistidos.
- Projetar os registros para a agenda do barbeiro sem identificadores e e-mail do cliente, em vez de reutilizar diretamente o registro administrativo completo.
- Usar a data local selecionada para filtrar os registros e exibir horários segundo `America/Sao_Paulo`, alinhado à especificação do projeto.
- Em falha, preservar a data e os atendimentos previamente carregados, em vez de simular uma consulta bem-sucedida.

## Risks / Trade-offs

- [Os registros demonstrativos podem ser confundidos com dados reais] → Manter o repositório isolado e não indicar persistência.
- [A identidade do barbeiro ainda é controlada pelo estado de demonstração] → Não tratar essa seleção como fronteira de autorização; a autorização real fica para integração posterior.

## Migration Plan

Não há migração nesta etapa. Ao integrar o backend, substituir a fonte mockada por consulta autenticada, mantendo a projeção restrita e a apresentação local.