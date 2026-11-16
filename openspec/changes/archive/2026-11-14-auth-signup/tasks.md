# Tasks

- [x] Expor em `/cadastro` nome, e-mail, telefone, senha e confirmação sem seletor de papel; a tela existente fornece os cinco campos.
- [x] Validar campos e confirmação antes do envio e aceitar apenas papel `client` no mock; `test_public_signup_cannot_choose_a_privileged_role` verifica essa restrição.
- [x] Exibir o resultado simulado sem persistência nem chamada HTTP; `test_mock_operations_never_call_the_http_client` cobre o caminho de cadastro do repositório.