# account-security Specification

## Purpose
Permite que clientes controlem credenciais, autenticação em duas etapas e sessões com verificação no servidor, privacidade e estados de operação explícitos.

## Requirements

### Requirement: Cliente altera a própria senha com reautenticação
O sistema SHALL permitir que um cliente autenticado altere a própria senha após validar a senha atual e a nova senha, sem expor credenciais ou indicar sucesso antes da confirmação do servidor.

#### Scenario: Alteração de senha confirmada
- **WHEN** o cliente fornece senha atual válida e nova senha que atende à política vigente
- **THEN** o servidor atualiza a senha da conta autenticada e a interface informa sucesso somente após a confirmação

#### Scenario: Senha atual ou nova senha inválida
- **WHEN** a senha atual não confere ou a nova senha não atende à política vigente
- **THEN** o servidor recusa a alteração, a conta mantém a senha anterior e a interface apresenta erro sem revelar qual credencial de terceiros é válida

### Requirement: Cliente configura autenticação TOTP
O sistema SHALL permitir que um cliente habilite ou desabilite TOTP por meio de verificação no servidor, sem expor segredo TOTP após a ativação.

#### Scenario: Ativação de TOTP
- **WHEN** o cliente autenticado inicia a configuração e confirma um código TOTP válido para o segredo de configuração
- **THEN** o servidor ativa o segundo fator, confirma o estado habilitado e a interface não mantém nem exibe novamente o segredo

#### Scenario: Código de configuração inválido
- **WHEN** o cliente confirma um código TOTP inválido ou expirado
- **THEN** o segundo fator permanece desabilitado e a interface informa que a configuração não foi concluída

#### Scenario: Desativação de TOTP
- **WHEN** o cliente solicita desativar TOTP e confirma a identidade com credenciais válidas e um código TOTP atual
- **THEN** o servidor remove o segundo fator e confirma o estado desabilitado

### Requirement: Login exige o segundo fator TOTP quando habilitado
O sistema SHALL exigir uma prova TOTP válida antes de emitir uma sessão autenticada para uma conta com segundo fator habilitado.

#### Scenario: Senha correta com TOTP habilitado
- **WHEN** o cliente informa a senha correta de uma conta protegida por TOTP
- **THEN** o servidor retorna somente um desafio temporário e não concede acesso a endpoints protegidos até validar o código TOTP

#### Scenario: Código TOTP válido no desafio de login
- **WHEN** o cliente apresenta um código TOTP válido para um desafio de login vigente
- **THEN** o servidor invalida o desafio e emite uma sessão autenticada com as permissões da conta

#### Scenario: Desafio ou código inválido
- **WHEN** o desafio expirou, já foi consumido ou o código TOTP é inválido
- **THEN** o servidor não emite sessão autenticada e a interface mantém o usuário fora das áreas protegidas

### Requirement: Cliente encerra todas as próprias sessões
O sistema SHALL permitir que o cliente revogue todas as sessões da própria conta no servidor, incluindo a sessão usada para solicitar a operação.

#### Scenario: Revogação confirmada
- **WHEN** o cliente autenticado confirma sair de todos os dispositivos e o servidor confirma a revogação
- **THEN** todas as sessões emitidas anteriormente são recusadas nos pedidos autenticados seguintes, e a interface limpa a sessão local e retorna ao login

#### Scenario: Sessão antiga tenta acessar a API
- **WHEN** uma sessão revogada envia uma solicitação a qualquer endpoint protegido
- **THEN** o servidor responde como não autenticado e não executa nem revela o recurso solicitado

#### Scenario: Falha ao revogar sessões
- **WHEN** o servidor não confirma a revogação de todas as sessões
- **THEN** a interface informa a falha e não comunica que outros dispositivos foram desconectados
