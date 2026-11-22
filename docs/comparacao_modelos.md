# Comparação dos modelos de resposta

Arquivo gerado por `python src/avaliacao.py`. Os dois modelos foram aplicados às 21 perguntas de teste que retornaram uma orientação.

| Critério | Modelo A – Resposta direta | Modelo B – Resposta estruturada com papel e limites |
|---|---|---|
| Mostra o link da fonte | 100% | 100% |
| Mostra o nome da fonte (lei/página) | 0% | 100% |
| Mostra a data de verificação | 0% | 100% |
| Mostra passos numerados | 0% | 100% |
| Avisa que não é canal oficial | 0% | 100% |
| Pede confirmação quando necessário | 48% | 100% |
| Média de palavras por resposta | 34 | 109 |
| Média de palavras por frase | 19.3 | 10.1 |

## Exemplo (DOC02)

**Modelo A**

```
A inscrição e a consulta da situação do CPF podem ser feitas gratuitamente pelo site da Receita Federal. O CPF também é o número usado na nova Carteira de Identidade Nacional.
Fonte: https://www.gov.br/receitafederal/pt-br/assuntos/meu-cpf
```

**Modelo B**

```
RESUMO
  A inscrição e a consulta da situação do CPF podem ser feitas gratuitamente pelo site da Receita Federal. O CPF também é o número usado na nova Carteira de Identidade Nacional.
O QUE FAZER
  1. Acesse a página 'Meu CPF' da Receita Federal.
  2. Escolha 'Inscrever-se no CPF' ou 'Consultar CPF'.
  3. Desconfie de sites ou pessoas que cobram por esse serviço.
FONTE
  Receita Federal – Meu CPF
  https://www.gov.br/receitafederal/pt-br/assuntos/meu-cpf
  Informação conferida em: 2026-11-22
(Este assistente é um protótipo educacional e NÃO é canal oficial de nenhum órgão público.)
```
