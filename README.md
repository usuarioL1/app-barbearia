# BarberFlow — Manual de Uso do Aplicativo Web

## 1. Apresentação
O **BarberFlow** é um aplicativo web de agendamento e gestão para barbearias criado para organizar o atendimento diário e facilitar a marcação de horários.
- **Problema que resolve:** Elimina conflitos de horários, agendamentos desorganizados feitos manualmente por mensagens e a falta de visibilidade da agenda do dia pelos barbeiros.
- **Público-alvo:** Clientes de barbearias que buscam praticidade para agendar serviços, barbeiros que precisam acompanhar sua agenda e gestores/administradores do estabelecimento.

---

## 2. Acesso ao Aplicativo
Como esta versão não possui link público na internet (deploy), o acesso é feito localmente após iniciar o sistema:

1. No terminal da pasta do projeto, execute:
   $env:BARBERFLOW_MODE = "xano"; $env:XANO_API_BASE_URL = "https://x8ki-letl-twmt.n7.xano.io/api:5t-IFNmz"; reflex run --frontend-port 3002
2. Abra o navegador e acesse: `http://localhost:3002/login`

### Contas de Teste Disponíveis
| Perfil | E-mail | Senha |
| :--- | :--- | :--- |
| **Cliente** | `cliente@gmail.com` | `1q2w3e4r` |
| **Barbeiro** | `barbeiro2@gmail.com` | `1q2w3e4r` |
| **Administrador** | `adm@gmail.com` | `1q2w3e4r` |

---

## 3. Perfis de Usuários
- **Cliente:** Consulta os serviços disponíveis, escolhe o barbeiro, agenda horários, acompanha seu histórico, remarca ou cancela atendimentos e edita seus dados cadastrais.
- **Barbeiro:** Visualiza sua agenda pessoal de atendimentos filtrada por data para saber exatamente quais clientes e serviços atenderá no dia.
- **Administrador:** Gerencia o catálogo de serviços (nomes, preços e durações), administra os barbeiros cadastrados e acompanha todos os agendamentos da barbearia.

---

## 4. Funcionalidades
- Tela de login com direcionamento automático conforme o perfil do usuário (Cliente, Barbeiro ou Administrador) e verificação em duas etapas.
- Catálogo visual de serviços e preços.
- Agendamento online com escolha de profissional, data e horários livres.
- Histórico de agendamentos do cliente com opção de remarcação e cancelamento.
- Agenda diária organizada para o barbeiro.
- Painel administrativo para controle de serviços, equipe e visão geral dos horários.
- Edição de perfil do usuário.

---

## 5. Manual de Utilização

### Jornada 1: Cliente (Agendar, Consultar e Remarcar)
1. **Entrar no sistema:** Acesse `http://localhost:3002/login`, preencha o e-mail `cliente@gmail.com` e a senha `1q2w3e4r`, e clique em **Entrar**.
2. **Ver serviços:** Na tela inicial do cliente, navegue pelo catálogo para conferir os serviços oferecidos e os respectivos valores.
3. **Fazer um agendamento:** Acesse a área de agendamento, selecione o serviço desejado, escolha o barbeiro, selecione a data e clique em um dos horários disponíveis. Por fim, clique em **Confirmar Agendamento**.
   - *Resultado esperado:* O horário é reservado com sucesso, deixará de aparecer como livre para outros clientes e passará a constar no seu histórico e na agenda do barbeiro.
4. **Consultar ou remarcar:** Abra a aba **Histórico** para ver seus agendamentos marcados. Caso precise alterar, utilize as opções disponíveis no próprio agendamento para remarcar ou cancelar.
   - *Resultado esperado:* A alteração é salva imediatamente e o horário antigo volta a ficar disponível.

### Jornada 2: Barbeiro (Acompanhar Agenda)
1. **Entrar no sistema:** Faça login utilizando `barbeiro2@gmail.com` e a senha `1q2w3e4r`.
2. **Conferir atendimentos:** Na tela principal do barbeiro, utilize o seletor de data para visualizar os compromissos marcados para aquele dia.
   - *Resultado esperado:* O sistema exibe a lista de horários ocupados, o nome do cliente e o serviço que será realizado.

### Jornada 3: Administrador (Gerenciar a Barbearia)
1. **Entrar no sistema:** Faça login utilizando `adm@gmail.com` e a senha `1q2w3e4r`.
2. **Gerenciar serviços e equipe:** Utilize o painel administrativo para adicionar ou editar serviços do catálogo, cadastrar barbeiros e acompanhar a movimentação geral de agendamentos.
   - *Resultado esperado:* Qualquer novo serviço ou alteração de preço feita pelo administrador passa a aparecer imediatamente na tela de agendamento dos clientes.

---

## 6. Exemplos de Utilização
- **Cenário 1 — Marcação rápida pelo cliente:** Um cliente precisa cortar o cabelo no dia seguinte. Ele entra no sistema, escolhe o serviço "Corte", seleciona o barbeiro disponível às 10:00 e confirma. O sistema registra a reserva na hora sem precisar trocar mensagens com a barbearia.
- **Cenário 2 — Trabalho integrado entre cliente e barbeiro:** Logo após o cliente confirmar o horário das 10:00, o barbeiro acessa sua conta no sistema e já visualiza o compromisso na sua agenda diária. Se o cliente remarcar para as 14:00 pelo histórico, a agenda do barbeiro é atualizada automaticamente.

---

## 7. Limitações Conhecidas
- **Hospedagem (Deploy):** O sistema não está publicado em um endereço web público, sendo necessário iniciá-lo localmente para acesso.
- **Verificação em Duas Etapas (2FA):** Para facilitar a demonstração acadêmica sem depender de aplicativos externos no celular, a tela de validação aceita qualquer código numérico de 6 dígitos.
- **Avisos Automáticos:** O sistema não envia notificações externas por e-mail, SMS ou WhatsApp após a confirmação ou cancelamento de um horário.