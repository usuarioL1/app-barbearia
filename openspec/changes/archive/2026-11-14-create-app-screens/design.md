# Design

## Context

O frontend usa Reflex (`0.10.1`) e possui rotas iniciais para as jornadas pública, do cliente, do barbeiro e administrativa. O código atual oferece uma estrutura responsiva escura/dourada, mas várias telas são simples placeholders e não reproduzem as composições visuais fornecidas pelo usuário. A implementação deve usar os PNGs em `assets/` como referência para reconstruir as telas com componentes Reflex, sem exibir as imagens compostas como interface final.

O inventário atual de `assets/` inclui as composições BarberFlow enviadas e o favicon; não há arquivos individuais de logo, retratos dos barbeiros nem fundo fotográfico. O usuário autorizou placeholders em código para esses elementos enquanto a estrutura, composição, proporções e cores são reproduzidas. Os scripts Xano existem, mas o schema da tabela `user` não está versionado e a compatibilidade de telefone e do papel `client` não foi confirmada. Nenhuma alteração ou integração real com Xano será feita antes da etapa final.

## Goals / Non-Goals

**Goals:**
- Reproduzir as telas de referência com a estrutura, hierarquia, alinhamento, densidade, proporções e aparência preto/dourado definidas nos designs.
- Construir a interface com componentes Reflex, CSS e recursos locais; manter cada tela navegável e responsiva.
- Usar placeholders locais coerentes para logo, fotos e fundos que não estejam disponíveis individualmente, sem inventar uma direção visual alternativa.
- Revisar a fidelidade visual antes de iniciar as interações mockadas.
- Manter a sequência de trabalho: reprodução visual, funcionalidades com mocks, integração e banco Xano por último.

**Non-Goals:**
- Usar uma composição completa como imagem de fundo, tela rasterizada ou substituto dos componentes de interface.
- Acrescentar faixas ou selos “demonstração”, conteúdos de indisponibilidade, seções ou controles ausentes nos designs.
- Conectar formulários, agendamentos, agenda, cadastros ou relatórios a endpoints reais durante as fases visual e de mocks.
- Alterar ou migrar dados, contas ou schema Xano antes da etapa final.

## Decisions

1. **Tratar as composições fornecidas como especificação visual.** Elas definem o resultado esperado, não apenas uma paleta inspiracional. Recriar as telas em Reflex, mantendo barra lateral de marca, navegação e item ativo, cabeçalhos, fundos escuros, detalhes dourados, cartões, bordas, tabelas, gráficos, calendário e densidade visual. A alternativa de manter os placeholders atuais ou apresentar as composições como imagens foi descartada porque não implementa a interface do aplicativo.

2. **Organizar as telas pelos grupos representados nas referências.** Implementar login; cadastro e recuperação de senha; portal e histórico do cliente; catálogo e equipe; fluxo de agendamento com etapas, calendário, horários e resumo; agenda diária e ações do barbeiro; dashboard e agenda administrativa; gestão de clientes, serviços, equipe e usuários; e relatórios e configurações. A navegação e os estados ativos devem acompanhar a tela atual como mostrado nas composições.

3. **Construir elementos visuais como componentes Reflex.** Usar módulos e componentes compartilhados para sidebar, cabeçalho, cartão, linha de tabela, indicador, estado de atendimento, formulário, gráfico e calendário. Reaproveitar os tokens existentes de fundo, superfície e dourado, refinando suas medidas, proporções, bordas, espaçamentos e tipografia para aproximar a referência. Não criar uma dependência visual nova sem necessidade demonstrada.

4. **Usar assets individuais disponíveis e placeholders para os demais.** Os PNGs completos ficam como referência visual, não são renderizados como páginas. Para logo individual, retratos e fundos ainda ausentes, usar temporariamente ícones nativos, avatares neutros e fundos sólidos/texturas CSS compatíveis com o design. Não introduzir fotos de banco nem substituir a identidade visual por imagens não aprovadas.

5. **Separar reprodução visual de interações.** Na primeira etapa, as telas reproduzem a aparência de estados representados nas referências; componentes e controles não chamam Xano. A fase seguinte implementa interações com uma fonte mockada isolada. Dados demonstrativos podem compor a aparência sem selos, avisos ou banners extras não presentes nos designs; a interface real e os estados de operação serão integrados depois.

6. **Preservar os contratos de domínio para a integração posterior.** Estados de agendamento mantêm os valores `pending`, `confirmed`, `cancelled` e `completed`; datas e horários visíveis usam `America/Sao_Paulo`. A fidelidade visual não substitui regras de autorização, disponibilidade, cancelamento e faturamento da especificação do projeto.

## Risks / Trade-offs

- [Placeholders de logo, retratos e fundo não terão os mesmos detalhes dos assets finais] → Reproduzir primeiro forma, dimensões, contraste e posicionamento; substituir os placeholders quando os arquivos individuais estiverem disponíveis.
- [Uma composição de referência contém várias telas e pode não definir todos os estados] → Implementar apenas os estados visíveis e os já descritos nas specs; não acrescentar variações de produto sem confirmação.
- [Fidelidade no desktop pode comprometer leitura em celular] → Preservar a hierarquia e a identidade, adaptando tabelas e sidebars para apresentação móvel e verificando os dois tamanhos.
- [Dados estáticos de apresentação podem parecer reais] → Não afirmar persistência ou conclusão de operações; os comportamentos e estados reais ficam para as etapas posteriores, sem adicionar marcações visuais ausentes da referência.
- [O schema Xano pode não aceitar telefone ou papel `client`, ou conter contas `member`] → Não alterar o schema nem migrar contas antes da etapa final e de uma decisão explícita sobre a compatibilidade.

## Migration Plan

1. As telas e os comportamentos mockados concluídos ficam registrados em changes independentes por rota, preservando a sequência visual antes de comportamento.
2. Consultar a change específica da tela ao revisar sua interface, estado, testes ou acessibilidade; manter os PNGs como referência visual, não como interface rasterizada.
3. Manter a integração real fora desta change; inspecionar schema, contratos e migrações na change `xano-integration`.
4. Não alterar Xano nem substituir mocks até confirmar contratos, aprovar migrações necessárias e validar os fluxos integrados.
