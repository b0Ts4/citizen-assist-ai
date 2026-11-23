# Roteiro do vídeo de apresentação

Duração-alvo: **cerca de 5 minutos**. Ajuste ao limite oficial informado no FIAP ON.
Grave a tela do terminal com o OBS Studio ou a gravação de tela do Windows (Win + Alt + R / Xbox Game
Bar). Aumente a fonte do terminal (Ctrl + roda do mouse) antes de gravar.
Publique no YouTube como **Não listado** e cole o link no README e no `ENTREGA.txt`.

Antes de gravar, abra o terminal **na pasta do projeto** e limpe a tela (`cls`).

| Tempo | O que mostrar | O que falar (sugestão) |
|---|---|---|
| 0:00–0:30 | README aberto no GitHub (topo) | "Sou Arthur Barbosa de Morais, RM573731, projeto individual. Este é o Citizen Assist AI, um assistente textual que responde dúvidas do dia a dia sobre documentos, direitos do consumidor, atendimento prioritário e serviços comunitários, sempre citando a fonte oficial." |
| 0:30–1:15 | `data/base_conhecimento.json` (um registro) e `data/temas.json` | "Cada orientação tem id, tema, palavras-chave, orientação, passos, referência e data de verificação. São 19 orientações em 4 temas, todas conferidas em leis do Planalto ou páginas gov.br. Para acrescentar uma orientação basta editar o JSON." |
| 1:15–2:00 | `python src/sistema.py` → opção 1 → um tema → uma orientação → escolher um assunto relacionado | "Pelo menu navegamos pela hierarquia tema, subtema, orientação. A resposta mostra resumo, passos, fonte, data e um aviso de que não somos canal oficial. Embaixo aparecem assuntos relacionados, escolhidos por uma busca em largura num grafo de assuntos." |
| 2:00–2:45 | Opção 2: `comprei um celular pela internet e me arrependi, consigo devolver?` e depois `prioridade` | "Também dá para perguntar com as próprias palavras. A busca normaliza o texto, tira as palavras vazias e pontua cada orientação. Quando duas opções ficam próximas, como em 'prioridade', o sistema não escolhe sozinho e pergunta ao usuário." |
| 2:45–3:20 | Opção 2: Enter vazio; `meu cpf é 123.456.789-09`; `como tirar passaporte`; menu `9` | "Entrada vazia, dado pessoal, assunto fora da base e opção inexistente geram mensagens claras. Se não há base suficiente, o assistente diz que não sabe em vez de inventar." |
| 3:20–3:40 | Opção 4 e repetir uma pergunta | "Temos dois modelos de resposta: o A, direto, e o B, estruturado. Comparamos os dois e o B cumpre todos os critérios de transparência, por isso é o padrão." |
| 3:40–4:30 | `python src/avaliacao.py` e `docs/resultados_testes.md` | "Testamos 34 perguntas: diretas, reformulações, fora do tema, limitações e exploratórias. A taxa de acerto é de 91,2% e o tempo médio fica abaixo de 1 milissegundo. A versão 1 da busca errava 'tirar passaporte' e 'receita de bolo'; corrigimos com pesos. Nas perguntas exploratórias ainda acertamos só 70%, e mostramos os 3 erros que restam." |
| 4:30–5:00 | README, seção de melhorias e conclusão | "As próximas melhorias são palavras-chave mais específicas, um stemmer de português e uma lista de assuntos fora da base. O assistente não coleta dados pessoais e não se apresenta como canal oficial. Obrigado!" |

## Checklist antes de publicar

- [ ] Áudio audível e fonte do terminal legível.
- [ ] Nenhum dado pessoal real aparece na tela (use o CPF fictício do roteiro).
- [ ] Vídeo como **Não listado**, testado em uma janela anônima.
- [ ] Link colado no README e no `ENTREGA.txt`.
