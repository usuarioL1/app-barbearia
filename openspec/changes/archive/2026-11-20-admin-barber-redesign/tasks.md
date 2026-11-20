# Tasks

## 1. Tratamento de endpoints indisponíveis

- [x] 1.1 Nas telas Admin e Barbeiro, suprimir na UI somente a mensagem exata `Unable to locate request.` e substituir o conteúdo da tela por um estado neutro sem renderizar registros anteriores; validar o caso exato e outras mensagens.
- [x] 1.2 Preservar o feedback normal para mensagens de autenticação, autorização, rede, respostas inválidas e erros diferentes; validar que esses casos continuam informados e nenhum estado de sucesso é apresentado.

## 2. Operações administrativas e do barbeiro

- [x] 2.1 Remover ou desabilitar controles de operações sem endpoint Xano permitido, mantendo configurações somente leitura e provisionamento manual de papéis privilegiados; validar que nenhum handler simula sucesso.
- [x] 2.2 Preservar as mutações existentes somente após confirmação Xano e sem atualização otimista; validar transições recusadas, estado exibido inalterado e ausência de fallback mock em `BARBERFLOW_MODE=xano`.

## 3. Acabamento visual dos portais

- [x] 3.1 Refinar o layout compartilhado e as telas `/admin/*` e de Barbeiro com preto `#090909`, dourado `#F2A900`, hierarquia, espaçamento e responsividade consistentes; validar compilação Reflex e rotas em desktop e viewport estreita.
- [x] 3.2 Preservar navegação, filtros, estados vazios/carregamento/erro, acessibilidade e ações suportadas durante o refinamento; validar que nenhuma rota ou controle funcional existente foi ocultado indevidamente.

## 4. Verificação de integração

- [x] 4.1 Executar os testes focados e `reflex compile --dry` com `BARBERFLOW_MODE=xano`; confirmar que a aplicação inicia sem trocar o modo de repositório.
- [x] 4.2 Verificar as telas administrativas e do barbeiro com respostas Xano de sucesso, lista vazia e a mensagem técnica exata; confirmar que o texto não aparece no topo e que o portal do cliente permanece inalterado.
