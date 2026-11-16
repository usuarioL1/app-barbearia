# Tasks

## 1. Consulta e ações demonstrativas

- [x] 1.1 Exibir nome, especialidade e estado dos barbeiros ativos/inativos no console; verificar a rota com `reflex compile --dry`.
- [x] 1.2 Encaminhar as ações atuais à validação mock, sem persistir alterações nem remover histórico; verificar o fluxo compartilhado com `test_admin_mutation_failure_is_not_reported_as_persisted`, `test_admin_mutation_is_validated_and_not_persisted` e `python -m unittest discover -s tests`.

## 2. Formulários da equipe

- [x] 2.1 Substituir payloads fixos por campos de criação/edição para nome e especialidade; testar campos obrigatórios, falha de validação e resposta simulada não persistente.