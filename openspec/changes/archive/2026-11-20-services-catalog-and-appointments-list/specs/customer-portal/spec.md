# Spec Delta

## MODIFIED Requirements

### Requirement: Lista de serviços ativos
A rota `/servicos` SHALL listar serviços ativos com nome, preço em BRL, duração e imagem semanticamente adequada, distinguindo carregamento de lista vazia.

#### Scenario: Catálogo carregado
- **WHEN** a consulta do repositório selecionado retorna serviços ativos
- **THEN** cada cartão mostra o nome, preço, duração e uma imagem adequada ao serviço, sem reutilizar para Corte + Barba a imagem de Corte Masculino

#### Scenario: Serviços solicitados no catálogo
- **WHEN** o cliente consulta o catálogo após a inclusão dos novos serviços
- **THEN** Sobrancelha aparece com 15 minutos e R$ 20,00, Pezinho / Acabamento com 15 minutos e R$ 15,00, e Hidratação Capilar com 30 minutos e R$ 40,00, com serviços anteriores preservados

#### Scenario: Catálogo vazio ou em carregamento
- **WHEN** a lista de serviços está vazia
- **THEN** a tela distingue a consulta em andamento do estado sem serviços disponíveis

### Requirement: Consulta dos próprios agendamentos
A rota `/agendamentos` SHALL apresentar o próximo agendamento em destaque e listar todos os próximos agendamentos ativos do cliente corrente, além do histórico, oferecendo filtros e estados vazios apropriados.

#### Scenario: Cliente possui registros
- **WHEN** o repositório selecionado retorna agendamentos do cliente corrente
- **THEN** a tela separa próximos atendimentos e histórico, permite alternar a visualização, destaca o agendamento mais próximo e lista todos os agendamentos ativos futuros em ordem cronológica

#### Scenario: Cliente gerencia próximos agendamentos
- **WHEN** um cliente tem vários agendamentos ativos futuros
- **THEN** cada registro aparece na lista completa, incluindo o próximo já destacado, com os dados e controles de cancelamento suportados para aquele registro

#### Scenario: Cliente não possui registros
- **WHEN** a consulta do repositório selecionado retorna lista vazia e termina o carregamento
- **THEN** a tela mostra estados vazios e oferece acesso à jornada de agendamento
