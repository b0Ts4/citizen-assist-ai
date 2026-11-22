# Resultados dos testes

Arquivo gerado automaticamente por `python src/avaliacao.py`.

| ID | Tipo | Pergunta | Esperado | Obtido | Detalhe | Resultado | Tempo (ms) |
|---|---|---|---|---|---|---|---|
| T01 | direta | Como tirar o CPF? | DOC02 | DOC02 | pontos: 4 | ACERTO | 0.8921 |
| T02 | direta | A certidão de nascimento é gratuita? | DOC03 | DOC03 | pontos: 8 | ACERTO | 0.9983 |
| T03 | direta | Qual o número do SAMU? | COM01 | COM01 | pontos: 4 | ACERTO | 0.9291 |
| T04 | direta | Onde posso reclamar de uma empresa? | CON04 | CON04 | pontos: 5 | ACERTO | 0.9641 |
| T05 | reformulacao | comprei um celular pela internet e me arrependi, consigo devolver? | CON01 | CON01 | pontos: 11 | ACERTO | 1.1053 |
| T06 | reformulacao | minha avó tem 67 anos, ela paga ônibus? | SOC02 | SOC02 | pontos: 5 | ACERTO | 1.0426 |
| T07 | reformulacao | quero fazer a nova identidade que usa o número do cpf | DOC01 | DOC01 | pontos: 8 | ACERTO | 1.0892 |
| T08 | reformulacao | a geladeira quebrou depois de um mês, ainda dá pra reclamar? | CON02 | CON02 | pontos: 4 | ACERTO | 1.1255 |
| T09 | reformulacao | como ganho o selo ouro na minha conta do governo | DOC06 | DOC06 | pontos: 4 | ACERTO | 1.0355 |
| T10 | reformulacao | a empresa pode apagar meus dados se eu pedir? | SOC03 | SOC03 | pontos: 6 | ACERTO | 1.0306 |
| T11 | reformulacao | quero receber aviso de enchente por SMS | COM05 | COM05 | pontos: 7 | ACERTO | 0.9961 |
| T12 | reformulacao | com 16 anos sou obrigado a votar? | DOC04 | DOC04 | pontos: 5 | ACERTO | 0.9864 |
| T13 | fora_do_tema | Como faço para tirar passaporte? | SEM_RESPOSTA | SEM_RESPOSTA | sem_resposta | ACERTO | 0.9990 |
| T14 | fora_do_tema | Qual a previsão do tempo para amanhã? | SEM_RESPOSTA | SEM_RESPOSTA | sem_resposta | ACERTO | 1.0248 |
| T15 | limitacao_vazia | (vazia) | ENTRADA_INVALIDA | ENTRADA_INVALIDA | vazia | ACERTO | 0.0002 |
| T16 | limitacao_ambigua | prioridade | AMBIGUA | AMBIGUA | opções: SOC01, SOC04 | ACERTO | 0.8521 |
| T17 | limitacao_invalida | ???!!! | ENTRADA_INVALIDA | ENTRADA_INVALIDA | invalida | ACERTO | 0.0024 |
| T18 | limitacao_dados_pessoais | meu cpf é 123.456.789-09, está regular? | ENTRADA_INVALIDA | ENTRADA_INVALIDA | dados_pessoais | ACERTO | 0.0009 |
| T19 | limitacao_sem_base | Quanto custa a segunda via da identidade no meu estado? | DOC01 | DOC01 | pontos: 3 | ACERTO | 1.0766 |
| T20 | reformulacao | fui cobrado duas vezes no cartão, devolvem em dobro? | CON03 | CON03 | pontos: 5 | ACERTO | 1.0894 |
| T21 | fora_do_tema | receita de bolo de chocolate | SEM_RESPOSTA | SEM_RESPOSTA | sem_resposta | ACERTO | 0.9797 |
| T22 | reformulacao | meu filho nasceu, preciso pagar o cartório? | DOC03 | DOC03 | pontos: 3 | ACERTO | 1.0550 |
| T23 | reformulacao | a loja não quer trocar meu produto estragado | CON02 | CON02 | pontos: 5 | ACERTO | 1.0475 |
| T24 | fora_do_tema | como tirar a carteira de motorista | SEM_RESPOSTA | SEM_RESPOSTA | sem_resposta | ACERTO | 0.9756 |
| T25 | exploratoria | como renovar minha cnh | SEM_RESPOSTA | SEM_RESPOSTA | sem_resposta | ACERTO | 0.9259 |
| T26 | exploratoria | quero me aposentar pelo inss | SEM_RESPOSTA | SEM_RESPOSTA | sem_resposta | ACERTO | 0.9600 |
| T27 | exploratoria | perdi meu rg o que faço | DOC01 | DOC01 | pontos: 3 | ACERTO | 0.9708 |
| T28 | exploratoria | segunda via da certidão de casamento | SEM_RESPOSTA | DOC03 | pontos: 3 | ERRO | 1.0135 |
| T29 | exploratoria | o banco cobrou tarifa que eu não autorizei | CON03 | SEM_RESPOSTA | sem_resposta | ERRO | 1.0368 |
| T30 | exploratoria | como pedir seguro desemprego | SEM_RESPOSTA | SEM_RESPOSTA | sem_resposta | ACERTO | 0.9594 |
| T31 | exploratoria | tem vacina no posto de saúde? | COM02 | COM02 | pontos: 6 | ACERTO | 0.9867 |
| T32 | exploratoria | meu vizinho maltrata o cachorro | SEM_RESPOSTA | SEM_RESPOSTA | sem_resposta | ACERTO | 0.9518 |
| T33 | exploratoria | qual o telefone dos bombeiros | SEM_RESPOSTA | CON01 | pontos: 3 | ERRO | 0.9529 |
| T34 | exploratoria | como consultar meu título | DOC04 | DOC04 | pontos: 3 | ACERTO | 0.9350 |

## Indicadores

- Perguntas testadas: **34**
- Acertos: **31** | Erros: **3**
- Taxa de acerto: **91.2%**
- Tempo médio de consulta: **0.9115 ms** (mediana 0.9866 ms; máximo 1.1255 ms; média de 50 repetições por pergunta)

### Acerto por tipo de pergunta

| Tipo | Acertos | Total | Taxa |
|---|---|---|---|
| direta | 4 | 4 | 100.0% |
| reformulacao | 11 | 11 | 100.0% |
| fora_do_tema | 4 | 4 | 100.0% |
| limitacao | 5 | 5 | 100.0% |
| exploratoria | 7 | 10 | 70.0% |
