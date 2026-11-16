# Tasks

## 1. Consulta e ações demonstrativas

- [x] 1.1 Carregar clientes mock e exibir nome, telefone, quantidade de agendamentos e último atendimento; verificar a rota com `reflex compile --dry`.
- [x] 1.2 Encaminhar os controles atuais ao mock sem alterar registros ou afirmar persistência; verificar o contrato genérico com `test_admin_mutation_is_validated_and_not_persisted`, `test_admin_mutation_failure_is_not_reported_as_persisted` e `python -m unittest discover -s tests`.

## 2. Interação da lista e formulários

- [x] 2.1 Conectar a busca por nome, e-mail ou telefone à lista; testar correspondências, resultado vazio e confirmação de que a consulta não altera os registros.
- [x] 2.2 Substituir payloads fixos por formulários de criação/edição e validação de nome/telefone; testar entradas válidas, telefone inválido e resposta não persistente do mock.