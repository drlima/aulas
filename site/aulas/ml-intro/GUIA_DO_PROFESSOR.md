# Guia do professor — Aula 1 ao vivo (~1h30)

A página publicada é o material dos alunos. Este guia é o seu: tempos, o *setup* de cada
bloco, o *punch* que a página revela e o que fazer ao vivo enquanto a turma pensa.

**Regra do formato:** você lança a pergunta em voz alta, pede votos no chat, espera 60–90 s,
comenta duas ou três respostas, e só então diz "agora abram o Revelar". Os alunos que abrem
antes estragam a própria surpresa, não a dos outros.

**Antes de começar (5 min antes):** peça que todos abram o link e, já no bloco 8, cliquem
em **"Rodar Python"** e em **"Carregar exemplos visuais"**. São dois downloads separados
(~20 MB de Python + scikit-learn, mais ~10 MB de matplotlib) e os dois precisam de
internet. Se a turma esperar chegar no bloco 8 para clicar, você perde uns minutos de aula
olhando barra de progresso. Enquanto carrega, peça que digitem no chat de onde são e o que
fazem: você vai usar isso nos exemplos.

**A aula existe em dois idiomas.** O alternador **PT · EN** fica no canto direito da barra
de navegação. Se houver alguém que não lê português, mande o link direto:
https://drlima.github.io/aulas/aulas/ml-intro/en/

| Bloco da página | Tempo | O que acontece ao vivo |
|---|---|---|
| 1. Regras | 5 min | Pedem regras no chat e testam na caixa. A página derruba cada uma com um contra-exemplo. Punch: ML inverte a lógica. |
| 2. Aprender | 8 min | Cartões de toque. Punch: definição tarefa/experiência/desempenho. Pergunte "qual é o T, E e P do filtro de spam?" |
| 3. Gabarito | 8 min | Frutas cinzas → ligar etiquetas. Peça primeiro "o que vocês enxergam sem etiquetas?" (dois grupos). Só então ligue. |
| 4. Rótulo ou número | 8 min | Régua vs caixas, depois quiz de 6 itens. Peça a pontuação no chat. "Idade pela foto" é o gancho: a entrada não importa. |
| 5. Modelo = fórmula | 15 min | **O centro da aula.** Deixe-os mover a e b tentando reduzir as barras vermelhas por 2 min antes do botão "deixar o computador aprender". Punch: modelo = fórmula com espaços em branco; aprender = preencher. Nomeie parâmetro, erro, treinamento. |
| 6. Vizinhos | 12 min | Tocam no gráfico para colocar a fruta nova. Pergunta-chave: "como chutam sem fórmula?". Depois k e o mapa de decisão com k = 1 (ilhas) vs k = 15. Só então o Revelar. Feche com **Em câmera lenta**, depois do Revelar: o botão anima os três passos que o Revelar acabou de descrever, sobre dez frutas só. Se algum aluno já clicou no gráfico grande, a câmera lenta mostra o caso dele — as dez frutas mais próximas da que ele colocou. Troque o k ali para ver a votação virar. |
| 7. Armadilha | 15 min | Com 0% escondido: "100%, podemos entregar?". Deixe a euforia durar. Punch: o vizinho mais próximo é ele mesmo. Slider de escondidas, depois k. Nomeie generalização, overfitting, hiperparâmetro. |
| 8. Python | 12 min | Clique em "Rodar Python" cedo (download). Mostre que X, y, fit, score são as mesmas palavras dos blocos anteriores. Troque k e o dataset ao vivo. Depois desça para os **exemplos visuais**: o mapa de decisão do Iris com o slider de k (é o mesmo mapa do bloco 6, agora feito por scikit-learn de verdade) e a **árvore de decisão**, que responde ao vivo a terceira pergunta aberta do bloco 9. Suba a profundidade de 1 até 4 e deixe a turma ver as regras se multiplicando. |
| 8b. Árvore vista de cima | 4 min | O jeito de ler o `plot_tree` com a turma. Logo abaixo da árvore, o botão **Ver os cortes** desenha as mesmas duas perguntas sobre o gráfico de frutas do bloco 6: a primeira pergunta corta o gráfico em dois, a segunda corta só o pedaço onde a fruta caiu, e a caixa que sobra já tem a resposta. Faça o pingue-pongue: aponte uma caixa da árvore, pergunte "onde isso está no gráfico?", e só então rode a animação. Este widget não usa Python, então funciona mesmo se o Pyodide não tiver carregado. |
| 9. Mapa | 5 min | Tabela-resumo. As três perguntas abertas são o programa das próximas aulas — mas a terceira você já mostrou: é a árvore do bloco 8. |
| 10. Para continuar | 3 min | Referências com uma linha dizendo por que ler cada uma. Aponte o ISL (gratuito, capítulos 2 e 3) para quem quer profundidade e o Crash Course do Google para quem quer prática. |

## Variabilidade de exemplos (por onde passam)

- Spam / e-mail (bloco 1)
- Recomendação de música, câmera do celular, termostato, corretor, calculadora (bloco 2)
- Churn de operadora de celular, fraude, notícias, segmentação (bloco 3)
- Imóveis, clima, cheques, idade por foto, tumor, internação hospitalar (bloco 4)
- Frutas na feira (blocos 3, 6 e 7), apartamentos (bloco 5), flores/vinhos/exames em Python (bloco 8)
- Iris com pétalas e a árvore de decisão nos exemplos visuais (bloco 8)

## Planos B

- **Turma silenciosa:** substitua perguntas abertas por votação binária no chat ("1 ou 2").
- **Site não carrega para alguém:** compartilhe sua tela; a aula funciona em modo demonstração. O aluno abre o link depois.
- **Rede bloqueia o CDN:** os blocos 1 a 7 e o 9 e 10 funcionam sem internet nenhuma depois que a página carregou. Só o bloco 8 precisa da rede (o Python vem do jsdelivr). Se ele falhar, a página mostra a mensagem de erro no lugar da figura e você pode seguir sem ele — mas teste a rede da sala antes.
- **Sobrou tempo:** abra os painéis **"O mesmo, em Python"** dos blocos 5, 6 e 7 e leia o código em voz alta, amarrando cada slider ao parâmetro correspondente. São 10 linhas cada um.
- **Sobrou tempo:** o desafio de casa (`DecisionTreeClassifier`) vira demonstração ao vivo no bloco 8.
- **Faltou tempo:** corte o bloco 8 (Python vira tarefa de casa). Blocos 5 e 7 são inegociáveis.
