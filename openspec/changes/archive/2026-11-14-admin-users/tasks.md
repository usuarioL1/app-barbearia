# Tasks

## 1. Consulta demonstrativa

- [x] 1.1 Carregar usuários da fonte mock e apresentar nome, e-mail e papel na tabela; verificar a página `admin_users_page` e compilar com `reflex compile --dry`.

## 2. Ações mockadas

- [x] 2.1 Conectar as ações de usuário ao validador mock e exibir mensagens de simulação ou falha sem alterar os registros; verificar com `test_admin_mutation_is_validated_and_not_persisted` e `test_admin_mutation_failure_is_not_reported_as_persisted`.