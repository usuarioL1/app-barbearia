# Tasks

## 1. Contratos e compatibilidade

- [x] 1.1 Inspecionar schema `user`, papéis e scripts no workspace Xano; registrar contratos reais de endpoints e verificar sanitização de logs, sem alterar schema ou converter contas; entregar relatório reproduzível da inspeção.
- [ ] 1.2 Se `phone`, `client` ou outro requisito não for suportado, propor a mudança necessária e obter aprovação explícita do escopo de cada escrita; antes de cada escrita, guardar snapshot somente leitura dos scripts relevantes e validar XanoScript e testes locais. Quando só houver a branch live, aplicar uma alteração estreita por vez apenas por caminho autorizado, sem contornar bloqueios de escrita e sem converter contas existentes sem decisão separada.

## 2. Integração por jornada

- [ ] 2.1 Conectar login, cadastro, recuperação, perfil e `/auth/me` somente aos endpoints confirmados; testar validação, autorização, erros e que o frontend não envia nem escolhe papel.
- [ ] 2.2 Conectar catálogo, barbeiros, disponibilidade, agendamentos, agenda e administração aos endpoints confirmados; documentar contratos ausentes e testar que falhas não são exibidas como sucesso.

## 3. Validação integrada

- [ ] 3.1 Validar fluxos críticos, regras de papel, conflito `409`, cancelamento, fuso, estados de erro e ausência de dependência de mocks; executar testes automatizados e `reflex compile --dry`.
