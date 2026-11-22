# Fontes e verificação da base

Cada registro de `data/base_conhecimento.json` cita uma fonte pública identificável. As páginas foram
abertas em **22/11/2026** para confirmar que o conteúdo apoia a orientação resumida.

| Registro | Fonte | Situação da conferência |
|---|---|---|
| DOC01 | gov.br – Carteira de Identidade Nacional (CIN) + Decreto 10.977/2022, art. 3º | Confirmado: CPF como número único. **Não** foi encontrada regra de gratuidade, então a orientação manda confirmar a taxa no órgão estadual. |
| DOC02 | Receita Federal – Meu CPF | Confirmado: inscrição e consulta on-line, sem custo. |
| DOC03 | Lei 9.534/1997 | Confirmado: registro de nascimento e primeira certidão gratuitos. |
| DOC04 | Constituição Federal, art. 14, §1º | Confirmado: obrigatório para maiores de 18; facultativo para analfabetos, maiores de 70 e de 16 a 18 anos. A página do TSE recusou acesso automatizado (HTTP 403), por isso não foi usada como fonte principal. |
| DOC05 | gov.br – Obter a Carteira de Trabalho | Confirmado: a partir do CPF, pelo app ou web, gratuito. |
| DOC06 | Governo Digital – Conta gov.br | Confirmado: três níveis (bronze, prata, ouro). |
| CON01 | CDC, art. 49 | Confirmado: 7 dias para compras fora do estabelecimento. |
| CON02 | CDC, art. 26 | Confirmado: 30 dias (não duráveis) e 90 dias (duráveis) para reclamar de vícios aparentes. |
| CON03 | CDC, art. 42, parágrafo único | Confirmado: devolução em dobro do valor pago indevidamente. |
| CON04 | consumidor.gov.br (página principal) | Confirmado: a empresa participante tem até 10 dias para responder; acesso com conta gov.br prata ou ouro. |
| SOC01 | Estatuto da Pessoa Idosa, arts. 1º e 3º | Confirmado: 60+ e prioridade especial para maiores de 80. |
| SOC02 | Estatuto da Pessoa Idosa, art. 39 | Confirmado: gratuidade para maiores de 65; de 60 a 64 depende da lei local. |
| SOC03 | LGPD, art. 18 | Confirmado: acesso, correção, eliminação etc. |
| SOC04 | Lei 10.048/2000, art. 1º | Confirmado na redação atual (inclui TEA, mobilidade reduzida e doadores de sangue). |
| COM01 | Ministério da Saúde – SAMU 192 | Confirmado: 192, gratuito, 24 h. |
| COM02 | Lei 8.080/1990, arts. 2º e 7º | Confirmado: acesso universal e igualitário. |
| COM03 | gov.br – Inscrever-se no Cadastro Único | Confirmado: inscrição pessoal em posto de atendimento da cidade, como o CRAS; responsável familiar leva CPF (de preferência) ou título de eleitor. (A página do MDS citada antes não trazia esses detalhes e foi substituída.) |
| COM04 | MDHC – Ouvidoria Nacional de Direitos Humanos | Confirmado: Disque 100 e Ligue 180. |
| COM05 | MIDR – Alertas de desastres | Confirmado: "Envie um SMS com seu CEP para o número 40199". |

## Como manter a base

1. Para corrigir uma orientação, edite o registro no JSON e atualize `data_verificacao`.
2. Para acrescentar uma orientação, copie um registro, troque o `id` (único) e preencha os campos
   obrigatórios. Se for um tema novo, cadastre-o antes em `data/temas.json`.
3. Rode `python -m unittest discover -s tests` e `python src/avaliacao.py`. Registros inválidos são
   listados como `[aviso]` e ignorados, sem derrubar o programa.
