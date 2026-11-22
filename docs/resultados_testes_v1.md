# Resultados dos testes

Arquivo gerado automaticamente por `python src/avaliacao.py`.

| ID | Tipo | Pergunta | Esperado | Obtido | Detalhe | Resultado | Tempo (ms) |
|---|---|---|---|---|---|---|---|
| T01 | direta | Como tirar o CPF? | DOC02 | DOC02 | pontos: 6 | ACERTO | 0.9333 |
| T02 | direta | A certidão de nascimento é gratuita? | DOC03 | DOC03 | pontos: 9 | ACERTO | 1.0824 |
| T03 | direta | Qual o número do SAMU? | COM01 | COM01 | pontos: 4 | ACERTO | 1.0061 |
| T04 | direta | Onde posso reclamar de uma empresa? | CON04 | CON04 | pontos: 6 | ACERTO | 1.0266 |
| T05 | reformulacao | comprei um celular pela internet e me arrependi, consigo devolver? | CON01 | CON01 | pontos: 12 | ACERTO | 1.1675 |
| T06 | reformulacao | minha avó tem 67 anos, ela paga ônibus? | SOC02 | SOC02 | pontos: 6 | ACERTO | 1.0772 |
| T07 | reformulacao | quero fazer a nova identidade que usa o número do cpf | DOC01 | DOC01 | pontos: 9 | ACERTO | 1.1553 |
| T08 | reformulacao | a geladeira quebrou depois de um mês, ainda dá pra reclamar? | CON02 | CON02 | pontos: 4 | ACERTO | 1.2953 |
| T09 | reformulacao | como ganho o selo ouro na minha conta do governo | DOC06 | DOC06 | pontos: 6 | ACERTO | 1.2577 |
| T10 | reformulacao | a empresa pode apagar meus dados se eu pedir? | SOC03 | SOC03 | pontos: 8 | ACERTO | 1.0562 |
| T11 | reformulacao | quero receber aviso de enchente por SMS | COM05 | COM05 | pontos: 7 | ACERTO | 1.0397 |
| T12 | reformulacao | com 16 anos sou obrigado a votar? | DOC04 | DOC04 | pontos: 6 | ACERTO | 1.0296 |
| T13 | fora_do_tema | Como faço para tirar passaporte? | SEM_RESPOSTA | DOC02 | pontos: 3 | ERRO | 0.9794 |
| T14 | fora_do_tema | Qual a previsão do tempo para amanhã? | SEM_RESPOSTA | SEM_RESPOSTA | sem_resposta | ACERTO | 1.0373 |
| T15 | limitacao_vazia | (vazia) | ENTRADA_INVALIDA | ENTRADA_INVALIDA | vazia | ACERTO | 0.0002 |
| T16 | limitacao_ambigua | prioridade | AMBIGUA | AMBIGUA | opções: SOC01, SOC04 | ACERTO | 0.9209 |
| T17 | limitacao_invalida | ???!!! | ENTRADA_INVALIDA | ENTRADA_INVALIDA | invalida | ACERTO | 0.0023 |
| T18 | limitacao_dados_pessoais | meu cpf é 123.456.789-09, está regular? | ENTRADA_INVALIDA | ENTRADA_INVALIDA | dados_pessoais | ACERTO | 0.0008 |
| T19 | limitacao_sem_base | Quanto custa a segunda via da identidade no meu estado? | DOC01 | DOC01 | pontos: 3 | ACERTO | 1.1882 |
| T20 | reformulacao | fui cobrado duas vezes no cartão, devolvem em dobro? | CON03 | CON03 | pontos: 7 | ACERTO | 1.1537 |
| T21 | fora_do_tema | receita de bolo de chocolate | SEM_RESPOSTA | DOC02 | pontos: 3 | ERRO | 1.0349 |

## Indicadores

- Perguntas testadas: **21**
- Acertos: **19** | Erros: **2**
- Taxa de acerto: **90.5%**
- Tempo médio de consulta: **0.9259 ms** (mediana 1.0373 ms; máximo 1.2953 ms; média de 50 repetições por pergunta)

### Acerto por tipo de pergunta

| Tipo | Acertos | Total | Taxa |
|---|---|---|---|
| direta | 4 | 4 | 100.0% |
| reformulacao | 9 | 9 | 100.0% |
| fora_do_tema | 1 | 3 | 33.3% |
| limitacao | 5 | 5 | 100.0% |
