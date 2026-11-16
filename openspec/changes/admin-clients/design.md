# Design

## Context

A tela lista clientes fornecidos por `MockRepository.clients()` e exibe nome, telefone, quantidade de agendamentos e último atendimento. Os botões de criação/edição/desativação disparam ações mock, sem alterar a lista; o botão de criação usa valores fixos. O campo de busca é apenas visual e não filtra resultados. Ver `proposal.md` e `specs/admin-console/spec.md` para escopo e comportamento.

## Goals / Non-Goals

**Goals:**
- Preservar a listagem existente e encaminhar operações administrativas à fonte mock.
- Acrescentar entradas reais de formulário para criar e editar dados mockados, sem persistir alterações.

**Non-Goals:**
- Consultar Xano, gravar clientes ou alterar dados históricos.
- Expor campos de perfil que não são necessários à tabela administrativa.

## Decisions

- Continuar usando `AppState` para carregar e apresentar `ClientRecord`; isso mantém os dados da tela alinhados às demais seções administrativas.
- Enviar operações de manutenção ao `MockRepository.admin_mutation`, preservando validação e mensagens não persistentes. Não alterar a lista como se houvesse gravação.
- Substituir os payloads fixos por formulários controlados e validar nome e telefone; o repositório já valida telefone, mas os botões atuais não coletam entrada do administrador.

## Risks / Trade-offs

- [Busca e formulários ainda não estão conectados] → manter os requisitos correspondentes pendentes até que os controles usem entrada real e tenham testes.
- [Ações mock podem ser confundidas com gravação] → comunicar em cada resultado que a ação foi simulada e que nada foi salvo.
- [A lista contém dados pessoais] → limitar a exibição aos campos da tabela e não adicionar dados de perfil desnecessários.

## Migration Plan

Não há migração de dados ou endpoint. Completar e testar os formulários mock primeiro; qualquer integração Xano futura requer uma mudança separada e aprovação da etapa final.