# Proposal

## Why

O frontend já possui a jornada de agendamento e o repositório Xano aponta para operações de disponibilidade, reserva, consultas e transições, mas os endpoints correspondentes não existem no código Xano do projeto. Assim, os fluxos continuam sem persistência confiável no runtime real, impedindo validar o principal objetivo operacional da barbearia.

## What Changes

- Criar contratos e endpoints Xano para disponibilidade, criação, consulta e cancelamento de agendamentos, além de consultas das agendas de barbeiro e administrador e transições de estado.
- Validar autorização por papel e propriedade no backend, aplicar as regras de expediente, antecedência, horizonte de agendamento, intervalo de preparação, cancelamento e transições, e evitar reservas conflitantes simultâneas por mecanismo atômico suportado pelo Xano.
- Preservar snapshots do serviço e histórico auditável de cada transição, sem criar registros parciais em caso de falha.
- Conectar os fluxos Reflex existentes a operações persistidas quando Xano estiver configurado, mantendo o modo demonstrativo isolado e comunicando erros sem sucesso otimista.
- Adicionar testes de contrato, regras de negócio, autorização, concorrência e comportamento de estado; validar os endpoints publicados antes de declarar a integração real concluída.

## Capabilities

### New Capabilities
- `appointments`: disponibilidade e ciclo de vida persistente de agendamentos, com regras de domínio, autorização, auditoria e prevenção de conflitos.

### Modified Capabilities
- `customer-portal`: substituir as afirmações de simulação para seleção, criação, listagem e cancelamento por comportamento persistido em modo Xano, preservando a experiência demonstrativa em modo mock.
- `barber-workspace`: consultar a agenda real do barbeiro autenticado e persistir transições permitidas, sem ampliar acesso a dados de outros barbeiros.
- `admin-console`: consultar e operar a agenda real da unidade com filtros e persistir transições administrativas, mantendo dados de demonstração isolados no modo mock.

## Impact

- Xano: grupo `Authentication`, tabelas existentes `appointment` e `appointment_status_history`, nova tabela técnica `barber_booking_lock` com chave única por barbeiro e novos endpoints protegidos para disponibilidade, reservas, consultas e mudanças de estado.
- Reflex: métodos já presentes em `app_barbearia/xano_repository.py`, seleção de repositório e estados em `app_barbearia/state.py`, e interfaces do cliente, barbeiro e administrador.
- Testes: contratos de `XanoRepository`, regras existentes do repositório mock, estado Reflex e autorização/integração dos endpoints Xano.
- Sem mudança de dependências prevista. A estratégia atômica de prevenção de conflitos deverá ser confirmada contra os recursos disponíveis no Xano antes da implementação.
