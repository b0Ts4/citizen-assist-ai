# Uso de Inteligência Artificial

O enunciado permite usar IA, desde que a equipe **compreenda, teste e justifique** a solução e registre aqui
o uso e a validação crítica. Este arquivo descreve com honestidade o que foi feito com apoio de IA e o que
foi feito pelo autor. O projeto foi desenvolvido individualmente (equipe de 1 pessoa).

## Divisão do trabalho

| Parte do projeto | Feito com apoio de IA (Claude, Anthropic) | Feito pelo autor |
|---|---|---|
| Requisitos e escopo | Organização dos requisitos do enunciado em um plano | Leitura do enunciado, definição do que entregar, aprovação das decisões |
| Base de conhecimento (19 orientações) | Rascunho dos textos e primeira busca das fontes | Conferência das fontes das orientações |
| Código Python (`src/`) | Rascunho da arquitetura e do código | Verificação do código e entendimento do funcionamento |
| Busca versão 2 | Proposta de pesos diferentes para corrigir T13 e T21 | Testes do comportamento da busca, repetidos várias vezes |
| Perguntas de teste | Rascunho das perguntas T01–T34 | Execução dos testes e conferência dos resultados |
| Modelos de prompt A e B | Rascunho das instruções e da comparação automática | Revisão das instruções dos Modelos A e B |
| Teste de usabilidade | Roteiro de tarefas e execução automatizada da verificação do roteiro | Teste informal com uma usuária externa (resultados não registrados) |
| Vídeo | Roteiro sugerido e gravação automatizada da tela (a IA executou a demonstração no VS Code e no terminal) | Narração, edição e publicação |
| Publicação | Criação do repositório no GitHub, a pedido da equipe | Revisão final do repositório e envio no FIAP ON |

**O protótipo em si não usa IA em tempo de execução.** Todas as respostas vêm da base verificada em JSON,
por regras determinísticas. Isso foi uma escolha: evita que um modelo invente prazos, valores ou requisitos.

## Validação crítica realizada

1. **Fontes:** cada orientação foi comparada com o texto da lei ou da página oficial (ver
   [`fontes.md`](fontes.md)). A conferência mudou o conteúdo gerado pela IA em vários pontos:
   - A primeira versão dizia que a 1ª via da Carteira de Identidade Nacional é gratuita. Essa regra **não**
     aparece no Decreto 10.977/2022 nem na página oficial consultada, então foi retirada. Agora a
     orientação manda confirmar a taxa no órgão estadual.
   - O link da página da CIN estava quebrado (erro 404) e foi trocado pelo endereço correto.
   - A informação dos alertas por SMS (40199) não estava na página citada no início, então a referência
     foi trocada pela página específica de alertas.
   - Duas orientações (CadÚnico e consumidor.gov.br) tiveram o texto ajustado ao que a fonte diz de fato
     ("CPF, de preferência, ou título de eleitor"; "até 10 dias para responder").
2. **Testes:** o comportamento foi medido com 34 perguntas e 13 testes unitários. Os erros da versão 1
   (T13 e T21) foram registrados ([`resultados_testes_v1.md`](resultados_testes_v1.md)) e corrigidos
   com uma regra geral (pesos), não com exceções para cada pergunta. A correção causou uma regressão (T16)
   que também foi registrada. Depois disso foram criadas perguntas **exploratórias** só para procurar
   falhas. Os erros encontrados (T28, T29, T33) foram mantidos no relatório.
3. **Entendimento:** o autor conferiu as fontes, verificou o código, entendeu o funcionamento do sistema
   e o testou diversas vezes, rodando o assistente, os testes unitários e a avaliação.

## Limites do uso de IA

- A IA pode errar ao resumir uma lei. Por isso toda orientação cita o artigo e o link para conferência.
- A página do TSE bloqueou o acesso automatizado; por isso a fonte de DOC04 é a Constituição (art. 14).
