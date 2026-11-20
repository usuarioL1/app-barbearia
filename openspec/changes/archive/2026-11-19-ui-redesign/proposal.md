# Proposal

## Why

O portal do cliente ainda não reproduz fielmente as cinco referências BarberFlow fornecidas para Dashboard, Agendamentos, Serviços, Perfil e Histórico. A revisão completa essa experiência sem confundir dados ilustrativos das imagens com dados reais nem transformar controles sem suporte em operações funcionais.

## What Changes

- Harmonizar os tokens visuais e os layouts compartilhados: fundo preto, superfícies escuras, dourado de destaque, tipografia sem serifa de alto contraste, navegação por papel, cabeçalhos, cartões, campos, botões e estados.
- Aproximar o portal do cliente às cinco composições fornecidas, incluindo shell compartilhado, Dashboard, Agendamentos, Serviços, Perfil e uma rota `/historico`.
- Incorporar recortes locais de fotografias presentes nas referências como imagens ilustrativas, sem usar uma composição inteira como tela nem apresentar retratos-placeholder como identidade verificada de um profissional.
- Melhorar a composição responsiva do agendamento, incluindo espaçamento dos cartões, calendário e resumo, preservando a confirmação existente.
- Usar dados reais já carregados e ações já disponíveis; controles sem suporte no estado/repositório ficam desabilitados ou são omitidos, nunca simulados como sucesso.
- Manter intactos `state.py` e `xano_repository.py`, o modo `BARBERFLOW_MODE=xano`, contratos e autorização, fuso horário, estados de agendamento e a política de cancelamento de 12 horas.

## Capabilities

### New Capabilities

### Modified Capabilities
- `customer-portal`: especificar o shell e as cinco telas de referência do cliente, incluindo `/historico`, preservando fluxos existentes e tratando controles sem suporte como indisponíveis.

## Impact

- UI Reflex: `app_barbearia/customer_portal.py`, `app_barbearia/ui.py` e o registro da rota em `app_barbearia/app_barbearia.py`.
- Recortes de imagens locais em `assets/`, extraídos das referências fornecidas.
- Contrato OpenSpec de `customer-portal`.
- Nenhuma alteração prevista em `app_barbearia/state.py`, `app_barbearia/xano_repository.py`, APIs ou regras de negócio.
