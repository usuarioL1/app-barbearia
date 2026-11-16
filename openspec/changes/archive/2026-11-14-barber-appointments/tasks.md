# Tasks

## 1. Transições do barbeiro

- [x] 1.1 Conectar as ações da página ao estado e atualizar o registro somente após aceitação do mock; verificar com `test_barber_agenda_is_scoped_and_failed_transition_preserves_state`.
- [x] 1.2 Validar transições canônicas, atribuição ao barbeiro e horário de término, sem persistir alterações; verificar com `test_barber_status_update_enforces_ownership_and_is_not_persistent` e a suíte de testes do repositório.

## 2. Feedback de falhas

- [x] 2.1 Preservar o estado exibido e apresentar mensagem em caso de recusa; verificar o estado anterior e a mensagem no teste do handler de agenda do barbeiro.