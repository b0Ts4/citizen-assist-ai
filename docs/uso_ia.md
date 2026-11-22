# Uso de Inteligência Artificial

## Onde a IA foi usada

| Etapa | Ferramenta | Uso |
|---|---|---|
| Estrutura do código e da documentação | Claude (Anthropic), assistente de programação | Sugestão da arquitetura (base/busca/grafo/respostas), rascunho do código Python, dos testes e deste repositório. |
| Redação dos modelos de prompt | Claude | Rascunho dos Modelos A e B, revisados pela equipe. |
| Conferência das fontes | Claude com acesso à web | Abertura das páginas oficiais para conferir se apoiam cada orientação. |

**O protótipo em si não usa IA em tempo de execução.** Todas as respostas vêm da base verificada em JSON,
por regras determinísticas. Isso foi uma escolha: evita que um modelo invente prazos, valores ou requisitos.

## Validação crítica realizada

1. **Fontes:** cada orientação foi comparada com o texto da lei ou da página oficial (ver
   [`fontes.md`](fontes.md)). Dois exemplos de correção que vieram dessa conferência:
   - A primeira versão dizia que a 1ª via da Carteira de Identidade Nacional é gratuita. Essa regra **não**
     aparece no Decreto 10.977/2022 nem na página oficial consultada, então foi retirada. Agora a
     orientação manda confirmar a taxa no órgão estadual.
   - O link da página da CIN estava quebrado (erro 404) e foi trocado pelo endereço correto.
   - A informação dos alertas por SMS (40199) não estava na página citada no início, então a referência
     foi trocada pela página específica de alertas.
   - Duas orientações (CadÚnico e consumidor.gov.br) tiveram o texto ajustado ao que a fonte diz de fato
     ("CPF, de preferência, ou título de eleitor"; "até 10 dias para responder").
2. **Testes:** o comportamento foi medido com 34 perguntas e 14 testes unitários. Os erros da versão 1
   (T13 e T21) foram registrados ([`resultados_testes_v1.md`](resultados_testes_v1.md)) e corrigidos
   com uma regra geral (pesos), não com exceções para cada pergunta. A correção causou uma regressão (T16)
   que também foi registrada. Depois disso foram criadas perguntas **exploratórias** só para procurar
   falhas. Os 3 erros encontrados (T28, T29, T33) foram mantidos no relatório.
3. **Entendimento:** a equipe deve conseguir explicar cada função: a pontuação da busca, o limiar, a regra
   de ambiguidade e a BFS no grafo de assuntos. Todas estão comentadas no código.

## Limites do uso de IA

- A IA pode errar ao resumir uma lei. Por isso toda orientação cita o artigo e o link para conferência.
- A página do TSE bloqueou o acesso automatizado; por isso a fonte de DOC04 é a Constituição (art. 14).
