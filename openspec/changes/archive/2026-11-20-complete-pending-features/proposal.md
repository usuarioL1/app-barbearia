# Proposal

## Why

Partes importantes do portal do cliente ainda aparecem como “Em breve” ou não concluem operações de ponta a ponta, deixando agendamentos, histórico, catálogo, perfil e segurança incompletos. Esta change fecha esses fluxos com persistência e autorização no Xano, sem apresentar sucesso otimista nem substituir falhas por dados demonstrativos.

## What Changes

- Habilitar remarcação de agendamentos próprios até 12 horas antes do início, com nova disponibilidade consultada no backend, prevenção atômica de conflitos e registro auditável.
- Mostrar detalhes completos do agendamento em uma visualização dedicada, carregados do endpoint autorizado pelo backend.
- Completar a navegação de serviços com busca por nome e uma aba “Barbeiros” que lista profissionais reais e inicia o agendamento com o profissional escolhido.
- Adicionar filtros de categoria e período ao histórico e filtros de período aos agendamentos futuros, preservando estados vazios e a origem dos dados.
- Trocar somente as imagens de Sobrancelha e Pezinho / Acabamento por imagens profissionais adequadas; manter inalteradas as imagens de Corte + Barba e Hidratação Capilar.
- Persistir nome, telefone e URL de avatar do cliente autenticado no Xano; a foto será configurada por URL, sem upload.
- Implementar alteração autenticada de senha, 2FA por TOTP e encerramento efetivo de todas as sessões da conta no backend. Uma sessão revogada deverá ser recusada nos pedidos autenticados seguintes.
- Remover os estados “Em breve” dessas ações e só indicar sucesso após confirmação do repositório selecionado.

## Capabilities

### New Capabilities

- `account-security`: alteração autenticada de senha, configuração e validação TOTP, e revogação imediata de todas as sessões do usuário.

### Modified Capabilities

- `customer-portal`: ampliar os fluxos de catálogo, agendamentos, histórico e perfil, incluindo avatar por URL e filtros.
- `appointments`: definir a remarcação segura e auditada sob a janela de 12 horas, com consulta de detalhes e preservação das regras de concorrência e autorização.

## Impact

- Interface e estado Reflex em `app_barbearia/customer_portal.py` e `app_barbearia/state.py`; contratos de repositório em `app_barbearia/xano_repository.py` e `app_barbearia/mock_repository.py`.
- Endpoints, funções e tabelas XanoScript em `xano/`, incluindo autenticação, perfil, TOTP, revogação de sessão, remarcação e auditoria.
- Assets e mapeamento de imagens de serviços; testes de estado, repositório, API e UI.
- Sem dependência de upload de arquivos ou de um serviço externo para TOTP; o segredo TOTP deverá ser protegido no backend e nunca exposto após a ativação.
