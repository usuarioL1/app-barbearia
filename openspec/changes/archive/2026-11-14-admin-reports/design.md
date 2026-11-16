# Design

## Context

A página de relatórios lê o período e a data do estado Reflex. O repositório mock agrega por dia ou mês com as datas locais dos registros e soma somente atendimentos `completed`; o estado também calcula contagem e resumo por serviço. Nenhuma consulta chama Xano.

## Goals / Non-Goals

**Goals:**
- Manter os filtros e indicadores sincronizados com uma única consulta simulada.
- Preservar os valores já carregados quando uma nova consulta falha.
- Deixar evidente nos resultados que os dados não são persistidos.

**Non-Goals:**
- Expor números financeiros reais ou integrar uma fonte contábil.
- Alterar preço, duração ou estados dos atendimentos.

## Decisions

- Usar a data local do início do atendimento e os preços snapshot existentes, alinhados à regra de faturamento do projeto.
- Calcular os indicadores e a série visual a partir dos mesmos registros demonstrativos, sem completar lacunas com métricas fabricadas.
- Manter validação de data e período na camada de estado/repositório; em falha, não substituir a seleção ou os totais anteriores.
- Não criar contrato de API neste change; a integração real pertence à etapa posterior do projeto.

## Risks / Trade-offs

- [Dados mockados não representam faturamento real] → Identificar as operações como simuladas e manter a fonte isolada.
- [Datas demonstrativas dependem do formato local do seed] → Na integração, normalizar datas a partir dos timestamps com fuso explícito antes de agrupar.

## Migration Plan

Não há migração. Na etapa de integração, substituir a agregação mock por dados confirmados do serviço, preservando período local e critério de estado concluído.