# Tasks

## 1. Catálogo e ações mock

- [x] 1.1 Exibir título, descrição, preço, duração e estado dos serviços ativos/inativos no console; verificar a rota com `reflex compile --dry`.
- [x] 1.2 Validar no mock os dados de criação e manter serviços inativos fora das opções de novos agendamentos, sem persistir alterações; verificar `test_admin_mutation_is_validated_and_not_persisted`, `test_mock_operations_never_call_the_http_client` e `python -m unittest discover -s tests`.

## 2. Formulários administrativos

- [x] 2.1 Substituir payloads fixos por campos de criação/edição para título, descrição, preço e duração; testar campos obrigatórios, preço/duração positivos, rejeição de entradas inválidas e resposta mock não persistente.