# Spec Delta

## Purpose

Esta capability permite que o barbeiro consulte a própria agenda diária com as informações necessárias ao atendimento, preservando a privacidade dos clientes e o horário local da barbearia.

## ADDED Requirements

### Requirement: Barbeiro consulta somente os atendimentos da própria agenda
A interface SHALL listar, para a data selecionada, os atendimentos atribuídos ao barbeiro atual com horário local, serviço, nome do cliente e estado, sem expor identificadores ou e-mail do cliente.

#### Scenario: Agenda diária carregada
- **WHEN** o barbeiro abre sua agenda para uma data com atendimentos
- **THEN** a interface mostra somente os atendimentos atribuídos a ele nessa data e apresenta os horários em `America/Sao_Paulo`

#### Scenario: Data sem atendimentos
- **WHEN** o barbeiro abre uma data sem atendimentos atribuídos
- **THEN** a interface mostra o estado vazio para a data selecionada

### Requirement: Barbeiro navega entre datas da agenda
A interface SHALL permitir consultar datas diferentes sem ampliar o escopo dos atendimentos além do barbeiro atual.

#### Scenario: Consulta de outra data
- **WHEN** o barbeiro navega para o dia anterior ou seguinte
- **THEN** a agenda carrega a data escolhida e apresenta os respectivos atendimentos próprios

#### Scenario: Falha ao carregar outra data
- **WHEN** a consulta da nova data falha
- **THEN** a interface informa a falha e não apresenta a data como carregada com sucesso