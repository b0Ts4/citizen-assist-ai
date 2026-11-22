# Uso de Inteligência Artificial

O enunciado permite usar IA, desde que a equipe **compreenda, teste e justifique** a solução e registre aqui
o uso e a validação crítica. Este arquivo descreve com honestidade o que foi feito com apoio de IA e o que
foi feito pela equipe.

## Divisão do trabalho

| Parte do projeto | Feito com apoio de IA (Claude, Anthropic) | Feito pela equipe |
|---|---|---|
| Requisitos e escopo | Organização dos requisitos do enunciado em um plano | Leitura do enunciado, definição do que entregar, aprovação das decisões |
| Base de conhecimento (19 orientações) | Rascunho dos textos e primeira busca das fontes | _[descrever: revisão das orientações, novas orientações acrescentadas, fontes conferidas no navegador]_ |
| Código Python (`src/`) | Rascunho da arquitetura e do código | _[descrever: leitura e entendimento de cada módulo, alterações feitas pela equipe]_ |
| Busca versão 2 | Proposta de pesos diferentes para corrigir T13 e T21 | _[descrever: correções da equipe, ex.: palavras-chave de CON01/CON03 para T33/T29]_ |
| Perguntas de teste | Rascunho das perguntas T01–T34 | _[descrever: perguntas criadas pela equipe]_ |
| Modelos de prompt A e B | Rascunho das instruções e da comparação automática | _[descrever: revisão / escolha do modelo padrão]_ |
| Teste de usabilidade | Roteiro de tarefas | Aplicação do teste com usuário externo e registro em `usabilidade.md` |
| Vídeo | Roteiro sugerido | Gravação, narração e publicação |
| Publicação | Criação do repositório no GitHub, a pedido da equipe | Revisão final do repositório e envio no FIAP ON |

> Preencha os campos _[descrever]_ só com o que a equipe fez de fato. Apague as linhas que não se aplicarem.

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
2. **Testes:** o comportamento foi medido com 34 perguntas e 14 testes unitários. Os erros da versão 1
   (T13 e T21) foram registrados ([`resultados_testes_v1.md`](resultados_testes_v1.md)) e corrigidos
   com uma regra geral (pesos), não com exceções para cada pergunta. A correção causou uma regressão (T16)
   que também foi registrada. Depois disso foram criadas perguntas **exploratórias** só para procurar
   falhas. Os erros encontrados (T28, T29, T33) foram mantidos no relatório.
3. **Entendimento:** _[descrever como a equipe estudou o código: ex.: cada integrante explicou um módulo,
   rodou o sistema e os testes, alterou algo e viu o efeito]_.

## Limites do uso de IA

- A IA pode errar ao resumir uma lei. Por isso toda orientação cita o artigo e o link para conferência.
- A página do TSE bloqueou o acesso automatizado; por isso a fonte de DOC04 é a Constituição (art. 14).
