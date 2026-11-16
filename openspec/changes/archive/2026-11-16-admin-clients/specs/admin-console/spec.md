# Spec Delta

## ADDED Requirements

### Requirement: Administrador consulta a lista demonstrativa de clientes
A seção de clientes SHALL exibir, para cada registro disponível, nome, telefone, quantidade de agendamentos e data do último atendimento, preservando o acesso administrativo aos dados mock.

#### Scenario: Lista carregada
- **WHEN** a consulta mock de clientes é concluída
- **THEN** a interface apresenta os campos disponíveis para cada cliente sem expor dados além dos exibidos na tela

#### Scenario: Lista vazia
- **WHEN** a consulta mock não retorna clientes
- **THEN** a interface apresenta um estado vazio, distinguindo-o do carregamento em andamento

### Requirement: Administrador pesquisa a lista de clientes
A lista SHALL filtrar clientes por nome, e-mail ou telefone sem modificar os registros e sem expor o e-mail como uma coluna adicional.

#### Scenario: Busca com correspondências
- **WHEN** o administrador informa um termo que corresponde a um ou mais clientes
- **THEN** a lista apresenta somente os registros correspondentes

#### Scenario: Busca sem correspondências
- **WHEN** o administrador informa um termo sem correspondência
- **THEN** a lista apresenta o estado vazio sem remover ou alterar os registros mock

### Requirement: Ações de cadastro de clientes são apenas simuladas
A seção SHALL permitir informar dados para criar ou editar clientes e oferecer desativação, encaminhando as ações à validação mock sem alterar registros ou apresentá-las como persistidas.

#### Scenario: Ação mock concluída
- **WHEN** o administrador submete dados válidos ou aciona desativação e a validação mock aceita a operação
- **THEN** a interface informa que a ação foi simulada e nenhum registro é gravado ou alterado

#### Scenario: Ação mock inválida ou recusada
- **WHEN** nome ou telefone são inválidos, os dados não passam pela validação mock ou a operação retorna erro
- **THEN** a interface informa a falha sem apresentar sucesso ou mudança persistida