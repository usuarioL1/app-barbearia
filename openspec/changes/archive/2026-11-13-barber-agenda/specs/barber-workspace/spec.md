# Spec Delta

## Purpose

Define as jornadas do espaço de trabalho do barbeiro, incluindo a consulta restrita da própria agenda, os atendimentos e a apresentação de seu perfil profissional.

## ADDED Requirements

### Requirement: Barbeiro consulta a agenda diária
A rota `/barbeiro` SHALL apresentar a agenda do dia do barbeiro atual, com navegação entre datas, indicadores do dia e resumo do próximo atendimento, usando dados mockados sem alegar persistência.

#### Scenario: Agenda com atendimentos
- **WHEN** a fonte mockada retorna atendimentos para a data selecionada
- **THEN** a interface mostra horários, serviços, estados, indicadores e o próximo atendimento sem expor dados pessoais desnecessários do cliente

#### Scenario: Agenda vazia, carregando ou indisponível
- **WHEN** a agenda está sendo consultada, não possui registros ou a consulta falha
- **THEN** a interface apresenta o estado de carregamento, vazio ou erro correspondente sem inventar atendimentos nem indicar sucesso
