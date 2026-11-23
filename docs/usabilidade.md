# Teste de facilidade de uso

## Roteiro de tarefas

O participante recebe só o objetivo de cada tarefa, sem instruções de quais teclas usar. Para cada tarefa
registramos: concluiu (sim/não), número de passos (escolhas ou digitações), tempo aproximado e dificuldades.

| # | Tarefa | Caminho ideal | Passos mínimos |
|---|---|---|---|
| U1 | Descobrir o número para chamar uma ambulância usando os temas | 1 → 4 (Serviços) → 1 (SAMU) | 3 |
| U2 | Perguntar se é possível devolver uma compra feita pela internet | 2 → digitar pergunta | 2 |
| U3 | Perguntar só "prioridade" e chegar à orientação certa | 2 → "prioridade" → escolher opção | 3 |
| U4 | Depois de uma resposta, abrir um assunto relacionado | escolher número da lista de continuidade | 1 |
| U5 | Pressionar Enter sem digitar nada e voltar a usar o sistema | Enter → ler a mensagem → nova opção | 2 |
| U6 | Trocar para o modelo de resposta curto | 4 | 1 |

## Verificação do roteiro (22/11/2026)

O roteiro foi executado com entradas automatizadas no terminal, para confirmar que cada caminho funciona
e quantos passos exige.

| # | Concluiu | Passos usados | Observação |
|---|---|---|---|
| U1 | Sim | 3 | Lista de temas com descrição ajudou a achar "Serviços e orientações comunitárias". |
| U2 | Sim | 2 | Resposta direta (CON01) com fonte e passos. |
| U3 | Sim | 3 | O sistema mostrou 2 opções (SOC01 e SOC04) em vez de chutar. |
| U4 | Sim | 1 | Lista de continuidade mostra 3 orientações e os temas vizinhos. |
| U5 | Sim | 2 | Mensagem: "Você não digitou nada. Escreva uma pergunta, por exemplo...". |
| U6 | Sim | 1 | A opção 4 alterna entre os modelos. |

**Indicador:** 6 de 6 tarefas concluídas (100%), em média 2,0 passos por tarefa, sempre igual ao caminho
mínimo. Esse resultado tem viés: quem executou conhece o sistema e o caminho ideal.

## Teste com usuário externo

Um teste informal com uma usuária externa foi feito durante o desenvolvimento, mas os resultados não foram
registrados na hora e a participante não estava mais disponível para repetir. Por isso eles **não**
constam aqui, e o indicador acima não representa um usuário que não conhece o sistema. Repetir as tarefas
U1–U6 com pessoas de fora, registrando passos, tempo e dificuldades, é a primeira melhoria da avaliação.

## Dificuldades e limitações já percebidas

- A interface é só texto: quem não usa terminal pode estranhar o "digite o número".
- Respostas do Modelo B são longas (cerca de 105 palavras), e em telas pequenas é preciso rolar.
- O participante precisa saber ler; não há leitura em voz alta (melhoria possível).
