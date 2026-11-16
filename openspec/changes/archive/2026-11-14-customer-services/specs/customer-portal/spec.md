# Spec Delta

## ADDED Requirements

### Requirement: Lista de serviços ativos
A rota `/servicos` SHALL listar serviços ativos com nome, preço em BRL e duração e distinguir carregamento de lista vazia.

#### Scenario: Catálogo carregado
- **WHEN** a consulta mockada retorna serviços ativos
- **THEN** cada cartão mostra o nome, preço e duração do serviço

#### Scenario: Catálogo vazio ou em carregamento
- **WHEN** a lista de serviços está vazia
- **THEN** a tela distingue a consulta em andamento do estado sem serviços disponíveis

### Requirement: Busca e seleção de serviço
A tela SHALL filtrar os serviços carregados por texto e permitir iniciar um agendamento a partir do serviço selecionado.

#### Scenario: Busca sem correspondência
- **WHEN** o cliente pesquisa um termo sem correspondência entre os serviços carregados
- **THEN** a tela mostra o estado vazio da busca sem sugerir serviços indisponíveis

#### Scenario: Iniciar agendamento
- **WHEN** o cliente aciona “Agendar” em um serviço
- **THEN** a interface abre a jornada `/agendar` com esse serviço selecionado