# Modelos de instrução de resposta (prompts)

O protótipo **não usa um modelo de IA externo**. As instruções abaixo funcionam como "prompts" que o
código cumpre por regras (em `src/respostas.py`). Elas foram escritas no formato de prompt para que
possam ser reaproveitadas se um LLM for conectado no futuro. Nesse caso, a resposta do LLM teria de ser
conferida com o registro da base antes de ser exibida.

Os dois modelos recebem **o mesmo registro verificado** e só mudam a forma de apresentar. Nenhum dos dois
pode acrescentar informação.

## Modelo A: resposta direta

**Instrução:**

> Responda à pergunta do cidadão usando apenas a orientação do registro encontrado. Ao final, informe a fonte.

**Formato produzido:** texto da orientação + linha `Fonte: <link>`.

## Modelo B: resposta estruturada com papel e limites

**Instrução:**

> Você é um assistente de orientação cidadã, informativo e NÃO oficial. Use SOMENTE o registro verificado
> recebido; não acrescente regras, prazos ou valores. Responda em linguagem simples, com frases curtas, no
> formato: 1) Resumo; 2) O que fazer (passos numerados); 3) Fonte com título e link; 4) Data de
> verificação; 5) Aviso para confirmar requisitos no canal oficial quando a orientação puder mudar. Se não
> houver registro, diga que não sabe e sugira temas disponíveis.

**Elementos da instrução:**

| Elemento | Como aparece |
|---|---|
| Papel | "assistente de orientação cidadã, informativo e NÃO oficial" |
| Restrição de conteúdo | "use SOMENTE o registro verificado" |
| Formato | Resumo / O que fazer / Fonte / Data / Aviso |
| Obrigação de citar a fonte | título + link + data de verificação |
| Tratamento do limite | quando não há registro, diz que não sabe e sugere temas |

## Comparação

A comparação é feita de forma automática e objetiva por `python src/avaliacao.py`. O script aplica os dois
modelos a todas as perguntas de teste que tiveram resposta e verifica critérios fixos. O resultado completo
está em [`comparacao_modelos.md`](comparacao_modelos.md).

Resumo (21 respostas):

| Critério | Modelo A | Modelo B |
|---|---|---|
| Mostra o link da fonte | 100% | 100% |
| Mostra o nome da fonte (lei/página) | 0% | 100% |
| Mostra a data de verificação | 0% | 100% |
| Mostra passos numerados | 0% | 100% |
| Avisa que não é canal oficial | 0% | 100% |
| Pede confirmação quando necessário | 48% | 100% |
| Média de palavras por resposta | 34 | 109 |
| Média de palavras por frase | 19,3 | 10,1 |

**Conclusão:** o **Modelo B** foi adotado como padrão. Ele cumpre todos os critérios de transparência (fonte
nomeada, data, aviso de canal não oficial, pedido de confirmação) e usa frases mais curtas (10,1 palavras
por frase contra 19,3). O custo é uma resposta cerca de 3 vezes mais longa. O Modelo A continua disponível
no menu (opção 4) para quem prefere uma resposta rápida. A informação é a mesma nos dois, mas o Modelo A
falha nos avisos: em cerca de metade dos casos ele não avisa que o requisito pode mudar.

> "48% em pedir confirmação" no Modelo A acontece porque o critério só é exigido nos registros marcados
> com `requer_confirmacao: true`. Nos demais, o critério conta como cumprido.
