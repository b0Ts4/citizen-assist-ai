# FIAP — Faculdade de Informática e Administração Paulista

## Graduação ON em Ciência da Computação: Global Solution 2026.2

# Citizen Assist AI

Assistente textual de orientação cidadã, do desafio **CitizenTech**.

## Equipe

**Nome da equipe:** _[preencher]_

| Nome | RM |
|---|---|
| _[preencher]_ | _[RM]_ |

**Vídeo de apresentação (YouTube, não listado):** _[colar link]_

---

## 1. Problema, público e temas

Informações sobre documentos, direitos e serviços públicos ficam espalhadas em leis e sites diferentes,
com linguagem difícil. O **Citizen Assist AI** reúne orientações **conferidas em fontes oficiais** e responde
perguntas simples do dia a dia, sempre mostrando a fonte e avisando quando não sabe.

**Público:** qualquer cidadão, com atenção a quem tem pouca familiaridade com serviços digitais (pessoas
idosas, famílias de baixa renda, quem faz o primeiro documento).

**Temas (19 orientações, 4 temas, 18 subtemas):**

| Tema | Subtemas | Registros |
|---|---|---|
| Documentos pessoais | identidade (CIN), CPF, certidões, título de eleitor, carteira de trabalho, conta gov.br | 6 |
| Direitos do consumidor | arrependimento, garantia, cobrança indevida, onde reclamar | 4 |
| Direitos e atendimento prioritário | pessoa idosa, atendimento prioritário, LGPD | 4 |
| Serviços e orientações comunitárias | SAMU, SUS, Cadastro Único, Disque 100/Ligue 180, Defesa Civil | 5 |

## 2. Estrutura do repositório

```
citizen-assist-ai/
├── README.md
├── data/
│   ├── base_conhecimento.json   # 19 orientações verificadas
│   ├── temas.json               # hierarquia tema → subtema e relações entre temas
│   └── perguntas_teste.json     # 34 perguntas de teste com resposta esperada
├── src/
│   ├── sistema.py               # programa principal (menu)
│   ├── base.py                  # leitura e validação do JSON
│   ├── busca.py                 # validação da entrada e algoritmo de busca
│   ├── grafo.py                 # grafo de assuntos e sugestões (BFS)
│   ├── respostas.py             # modelos de resposta A e B, mensagens de limite
│   └── avaliacao.py             # executa os testes e gera os indicadores
├── tests/
│   └── test_sistema.py          # 14 testes unitários
└── docs/
    ├── fontes.md                # fonte e conferência de cada registro
    ├── prompts.md               # modelos de instrução e comparação
    ├── comparacao_modelos.md    # (gerado) comparação A x B
    ├── resultados_testes.md     # (gerado) tabela de testes e indicadores
    ├── resultados_testes.csv    # (gerado) mesmo resultado em CSV
    ├── resultados_testes_v1.md  # resultado da versão 1 da busca (histórico)
    ├── roteiro_video.md         # roteiro da apresentação em vídeo
    ├── usabilidade.md           # roteiro e resultado do teste de uso
    └── uso_ia.md                # uso de IA e validação crítica
```

## 3. Como executar

Requisitos: **Python 3.8+**, sem bibliotecas externas.

```bash
python src/sistema.py
```

```bash
python src/avaliacao.py
```

```bash
python -m unittest discover -s tests -v
```

## 4. Base de conhecimento

Arquivo `data/base_conhecimento.json`, uma lista de registros:

```json
{
  "id": "CON01",
  "tema": "consumidor",
  "subtema": "compras",
  "pergunta": "Posso desistir de uma compra feita pela internet?",
  "palavras_chave": ["arrependimento", "desistir", "compra pela internet", "7 dias"],
  "orientacao": "Em compras feitas fora do estabelecimento ... (CDC, art. 49).",
  "passos": ["Comunique a desistência ...", "Guarde comprovantes ..."],
  "referencia": {"titulo": "Código de Defesa do Consumidor, art. 49", "url": "https://www.planalto.gov.br/..."},
  "data_verificacao": "2026-11-22",
  "requer_confirmacao": false,
  "relacionados": ["CON04", "CON02"]
}
```

- **Obrigatórios:** `id`, `tema`, `pergunta`, `palavras_chave`, `orientacao`, `referencia` (com `titulo` e
  `url`), `data_verificacao` (AAAA-MM-DD).
- **Opcionais:** `subtema`, `passos`, `requer_confirmacao` (padrão: `true`, o mais seguro), `relacionados`.
- **Validação (`base.py`):** arquivo ausente, vazio ou com JSON inválido mostra uma mensagem clara e
  encerra. Registro com campo faltando, id duplicado, tema inexistente ou data fora do formato é
  **ignorado com aviso**, e o resto da base continua funcionando.
- **Manutenção:** para incluir ou corrigir orientações basta editar o JSON; nenhuma regra do código muda.
  Veja [`docs/fontes.md`](docs/fontes.md).

### Estruturas de dados

| Estrutura | Tipo | Uso |
|---|---|---|
| `registros` | lista de dicionários | base completa, percorrida pela busca |
| `por_id` | dicionário `id → registro` | busca direta pelo identificador (opção 3 do menu) |
| `por_tema` | dicionário `tema → subtema → lista` | navegação hierárquica pelo menu |
| `grafo` | dicionário `nó → conjunto de vizinhos` | sugestões de continuidade |

### Hierarquia e grafo de assuntos

- **Hierarquia:** `tema → subtema → orientação` (definida em `temas.json` e no campo `subtema`).
- **Grafo (não direcionado):** os nós são os temas (`tema:documentos`...) e as orientações (`DOC01`...).
  As arestas ligam: tema ↔ tema relacionado (`temas.json`), orientação ↔ seu tema, e orientação ↔
  orientações relacionadas (`relacionados`). Exemplo: `CON01` (arrependimento) → `CON04` (onde reclamar),
  porque quem não consegue devolver a compra precisa saber onde reclamar.
- **Navegação:** depois de cada resposta, `sugerir_relacionados` faz uma **busca em largura (BFS)** a
  partir da orientação. Primeiro aparecem os vizinhos diretos, depois os que estão a dois passos (outras
  orientações do mesmo tema). Também são mostrados os temas vizinhos. Assim o usuário sempre tem opções
  para continuar a consulta.

## 5. Estratégia de busca

Implementada em `src/busca.py`:

1. **Validação** da entrada: vazia, só símbolos ou números, curta demais, sem palavras de assunto, ou com
   **dado pessoal** (CPF, e-mail ou telefone, detectados por expressões regulares). Qualquer um desses
   casos gera mensagem explicativa e a busca não é feita.
2. **Normalização:** minúsculas, sem acentos e sem pontuação ("Certidão?" → "certidao").
3. **Remoção de stopwords** ("o", "de", "como", "posso"...).
4. **Radical simples:** retira o plural e mantém as 6 primeiras letras ("documentos" → "docume"), para
   casar variações da mesma palavra.
5. **Pontuação** de cada registro (versão 2), por termo da pergunta:
   - **+3** se é uma palavra-chave própria do registro (ex.: "cpf", "samu");
   - **+2** se aparece solto dentro de uma expressão-chave (ex.: "receita", de "receita federal");
   - **+1** se é um verbo genérico ("tirar", "pedir", "consultar"...) ou aparece só no texto da pergunta
     cadastrada;
   - mais **+2** para cada expressão-chave encontrada inteira (ex.: "compra pela internet").
6. **Decisão:**
   - pontuação máxima **< 3** → *sem resposta confiável* (mostra o limite e sugere temas);
   - 2º colocado com **≥ 80%** da nota do 1º → *ambígua*: o sistema **não escolhe sozinho** e lista até 4
     opções para o usuário (ex.: "prioridade" → pessoa idosa **ou** atendimento prioritário);
   - senão → mostra o 1º colocado. Empates são ordenados pelo id, para que o resultado seja sempre o mesmo.

**Por que essa estratégia?** Ela é simples de explicar e de auditar: dá para dizer exatamente por que uma
resposta foi escolhida. Também é rápida (menos de 1 ms por consulta) e não precisa de bibliotecas nem de
internet. A desvantagem está na seção 8: uma única palavra em comum ainda pode gerar um falso positivo.

**Por que pesos diferentes?** Na versão 1 todo termo encontrado nas palavras-chave valia 3 pontos.
"Como faço para tirar **passaporte**?" recebia 3 pontos por causa de "tirar" (da expressão "tirar cpf"), e
"**receita** de bolo" recebia 3 por causa de "receita federal". Os dois passavam do limiar e eram
respondidos com a orientação do CPF. Na versão 2, palavras soltas de expressões e verbos genéricos valem
menos e não bastam sozinhas para gerar uma resposta.

## 6. Regras de resposta e prompts

- Toda resposta vem de um registro da base. **O sistema não gera texto novo.**
- Toda resposta mostra a **fonte** (título e link) e a **data de verificação**.
- Registros com `requer_confirmacao: true` (taxas, prazos, regras locais) mostram:
  *"ATENÇÃO: requisitos, taxas e prazos podem mudar... Confirme no canal oficial antes de ir."*
- Toda resposta avisa que o assistente **não é canal oficial**.
- Sem correspondência: *"Não encontrei uma orientação confiável na base para essa pergunta. Prefiro não
  responder a arriscar uma informação errada."*, seguido dos temas disponíveis.

Há **dois modelos de instrução** (Modelo A direto e Modelo B estruturado, com papel, formato e obrigação
de citar a fonte), documentados e comparados em [`docs/prompts.md`](docs/prompts.md). O **Modelo B** é o
padrão porque cumpre 100% dos critérios de transparência e tem frases mais curtas (10,1 contra 19,3
palavras por frase).

## 7. Exemplos de uso

**Pergunta direta**
```
> comprei um celular pela internet e me arrependi, consigo devolver?
[CON01] Posso desistir de uma compra feita pela internet?
RESUMO
  Em compras feitas fora do estabelecimento comercial (internet, telefone, catálogo), o consumidor pode
  desistir em até 7 dias, contados da assinatura ou do recebimento do produto, ... (CDC, art. 49).
O QUE FAZER
  1. Comunique a desistência ao fornecedor por escrito ... dentro dos 7 dias.
  ...
FONTE
  Código de Defesa do Consumidor (Lei nº 8.078/1990), art. 49
  https://www.planalto.gov.br/ccivil_03/leis/l8078compilado.htm
  Informação conferida em: 2026-11-22
(Este assistente é um protótipo educacional e NÃO é canal oficial de nenhum órgão público.)

Quer continuar por um assunto relacionado?
  1. Onde posso reclamar de uma empresa? [CON04]
  ...
```

**Consulta ambígua**
```
> prioridade
Sua pergunta pode se referir a mais de um assunto.
  1. Quais são os direitos de prioridade da pessoa idosa? [SOC01]
  2. Quem tem direito a atendimento prioritário? [SOC04]
```

**Fora da base**
```
> Qual a previsão do tempo para amanhã?
Não encontrei uma orientação confiável na base para essa pergunta. Prefiro não responder a arriscar uma
informação errada.
Temas disponíveis: Documentos pessoais, Direitos do consumidor, ...
```

**Entradas inválidas**
```
> (Enter)                    → Você não digitou nada. Escreva uma pergunta, por exemplo: 'como tirar o CPF?'.
> ???!!!                     → Não entendi a entrada. Use palavras, por exemplo: ...
> meu cpf é 123.456.789-09   → Parece que você digitou um dado pessoal ... A consulta não foi feita nem registrada.
Menu: 9                      → Opção '9' não existe. Escolha entre 0 e 5.
Identificador: XYZ           → Não existe orientação com o identificador 'XYZ'. Exemplos válidos: ...
```

## 8. Testes e indicadores

**Plano:** 34 perguntas em `data/perguntas_teste.json`:

| Grupo | Qtd. | O que testa |
|---|---|---|
| Diretas | 4 | pergunta igual ou parecida com a cadastrada |
| Reformulações | 11 | mesma dúvida com outras palavras ("minha avó tem 67 anos, ela paga ônibus?") |
| Fora do tema | 4 | passaporte, previsão do tempo, receita de bolo, CNH |
| Limitações | 5 | entrada vazia, ambígua ("prioridade"), só símbolos, com CPF, detalhe que não está na base (valor da taxa) |
| Exploratórias | 10 | perguntas novas feitas para **procurar falhas**, com resposta esperada definida antes de rodar |

Cada consulta é repetida 50 vezes para medir o tempo. Resultado completo, gerado pelo script:
[`docs/resultados_testes.md`](docs/resultados_testes.md) e `docs/resultados_testes.csv`.

### Evolução: versão 1 → versão 2 da busca

| | Versão 1 | Versão 2 (atual) |
|---|---|---|
| Perguntas | 21 | 34 (21 originais + 3 de validação + 10 exploratórias) |
| Acerto nas 21 originais | 19/21 (90,5%) | 21/21 (100%) |
| Erros | T13 passaporte → CPF; T21 receita de bolo → CPF | ver abaixo |

Resultado da versão 1 guardado em [`docs/resultados_testes_v1.md`](docs/resultados_testes_v1.md). Ao
mudar os pesos houve uma **regressão**: "prioridade" deixou de ser ambígua, porque a orientação SOC01 só
tinha "prioridade" dentro de uma expressão. Corrigimos a base (palavra-chave "prioridade" no SOC01), sem
mudar o código. Depois disso escrevemos 3 perguntas de validação novas (T22–T24), que acertaram.

### Indicadores atuais

| Indicador | Resultado |
|---|---|
| Perguntas testadas | 34 |
| Acertos | 31 |
| **Taxa de acerto geral** | **91,2%** |
| Taxa nas exploratórias (as mais difíceis) | 7/10 (70%) |
| **Tempo médio de consulta** | **≈ 0,9 ms** |
| Facilidade de uso (roteiro, 6 tarefas) | 6/6 concluídas, média de 2 passos ([`docs/usabilidade.md`](docs/usabilidade.md)) |

| Tipo | Acerto |
|---|---|
| Diretas | 4/4 (100%) |
| Reformulações | 11/11 (100%) |
| Fora do tema | 4/4 (100%) |
| Limitações | 5/5 (100%) |
| Exploratórias | 7/10 (70%) |

**Interpretação:**
- O assistente vai bem no que está na base, inclusive quando a pergunta usa outras palavras.
- Todas as entradas inválidas, a consulta ambígua e as perguntas fora do tema foram tratadas
  corretamente. Para CNH, INSS e seguro-desemprego ele disse "não sei" em vez de inventar.
- **Os 100% nos grupos 1 a 4 estão inflados:** as perguntas foram escritas por quem conhece as
  palavras-chave. Os **70% das exploratórias** mostram melhor o desempenho com perguntas reais. Os 3 erros:
  - T33 "qual o **telefone** dos bombeiros" → respondeu com arrependimento de compra (CON01), porque
    "telefone" é palavra-chave de CON01 (compra por telefone). **Falso positivo**: o erro mais grave.
  - T28 "segunda via da **certidão de casamento**" → respondeu com a certidão de nascimento (DOC03). A
    resposta é parecida, mas não trata do documento pedido.
  - T29 "o banco **cobrou** tarifa" → "não sei", mas devia achar cobrança indevida (CON03). O radical de
    "cobrou" ("cobrou") é diferente do de "cobrado" ("cobrad"). **Falso negativo.**
- O tempo (< 1 ms) é desprezível para o usuário. Ele foi medido só na busca, sem contar o tempo de leitura
  da pessoa.

**Melhorias possíveis:**
1. **Palavras-chave mais específicas:** trocar "telefone" por "compra por telefone" em CON01 (resolve
   T33) e acrescentar ao CON03 variações como "cobrou" e "tarifa" (resolve T29). Isso é só manutenção da
   base, sem mudar o código.
2. **Radical melhor:** usar um *stemmer* de português (ex.: RSLP) para que "cobrou", "cobrado" e
   "cobrança" caiam no mesmo radical.
3. **Assuntos conhecidos fora da base** (passaporte, CNH, INSS, bombeiros 193) com resposta "esse assunto
   ainda não está na base, procure o órgão X". Isso é melhor que um "não sei" genérico.
4. **Busca por similaridade (TF-IDF ou embeddings)** para reformulações mais distantes, sempre conferindo a
   resposta com a base verificada.
5. **Acessibilidade:** leitura em voz alta e versão web com fonte ampliável.

**Limitações da avaliação:** a maioria das perguntas foi escrita pela equipe. São só 34 perguntas. O
teste de usabilidade com usuário externo ainda precisa ser feito (roteiro pronto). O critério de acerto
verifica o registro escolhido, não a qualidade do texto. O tempo medido não inclui a leitura da resposta
pela pessoa.

## 9. Clareza, acessibilidade, privacidade e informação não oficial

- **Clareza:** frases curtas, passos numerados, termos técnicos explicados ("CIN – substitui o antigo RG").
- **Acessibilidade:** menu numerado (sem comandos para decorar), mensagens de erro que dizem o que fazer,
  sempre há opção "0. Voltar", só texto (compatível com leitores de tela do terminal).
- **Privacidade:** o sistema **não pede nenhum dado pessoal**. Se a pessoa digitar um CPF, e-mail ou
  telefone, a consulta é bloqueada e não é registrada. Nenhum histórico é salvo.
- **Informação não oficial:** todas as telas avisam que é um protótipo educacional e **não** um canal
  oficial. O sistema não promete atendimento nem integração com órgãos públicos.
- **Fontes:** só leis e páginas oficiais (planalto.gov.br, gov.br), com data de verificação. Todas as 19
  fontes foram abertas e conferidas; o detalhe está em [`docs/fontes.md`](docs/fontes.md).

## 10. Uso de IA

Ver [`docs/uso_ia.md`](docs/uso_ia.md). O protótipo não usa IA em tempo de execução. A IA foi usada no
desenvolvimento e todas as orientações foram conferidas nas fontes.

## 11. Conclusões

O protótipo mostra que listas, dicionários, um grafo simples e uma busca por pontuação já bastam para um
assistente que **responde com fonte, admite quando não sabe e pede esclarecimento em caso de dúvida**. A
taxa de acerto de 91,2% (70% nas perguntas exploratórias) e o tempo abaixo de 1 ms são bons para um
protótipo. A versão 2 da busca eliminou os falsos positivos da versão 1, mas os testes exploratórios
mostram que o risco principal continua: uma coincidência de palavra virar uma resposta confiante (T33).
Esse é o próximo ponto a melhorar (seção 8). A base é pequena (19 orientações) e precisa de revisão periódica, porque leis e
procedimentos mudam.
