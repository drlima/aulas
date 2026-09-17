# Guia do professor — Aula 2 ao vivo: Texto vira número (~90 min)

A página publicada é o material dos alunos. Este guia é o seu: tempos, o *setup* de cada
bloco, o *punch* que a página revela e o que fazer ao vivo enquanto a turma pensa. A aula
pressupõe a aula 1 (`ml-intro`): modelo, rótulo, treino e teste, acurácia e k-NN entram
sem reexplicação.

**Regra do formato:** você lança a pergunta em voz alta, pede votos no chat, espera 60–90 s,
comenta duas ou três respostas, e só então diz "agora abram o Revelar".

**Antes de começar (5 min antes):** peça que todos abram o link e, já no bloco 9, apertem
**"Rodar Python"** na primeira caixa. O navegador baixa o Python, o scikit-learn e o nltk
(cerca de 30 MB). Os blocos 1 a 8 não precisam disso: as 4000 avaliações vêm com a página.
Enquanto carrega, peça que escrevam no chat uma avaliação curta de algo que compraram:
você usa essas frases no bloco 8.

**Dois idiomas.** O alternador **PT · EN** fica no canto direito da barra. A versão em
inglês usa outras avaliações (Amazon e Yelp) e outro stemmer (Porter), então os números
dela são diferentes; a estrutura e os punches são os mesmos. Link direto:
https://drlima.github.io/aulas/aulas/nlp-intro/en/

**Cuidado ao vivo na versão en (blocos 5 e 8).** Sem stopwords, "i did not like it" vira
"like", mas **continua negativa (−0,18)**. A frase que inverte é **"i do not recommend it"**
(−2,3 → +0,9). Em pt as duas invertem.

| Bloco da página | Tempo | O que acontece ao vivo |
|---|---|---|
| 1. Parecido | 6 min | Votação nos quatro pares. Lembre as frutas de 150 g e 151 g. Punch: em texto, parecido na forma não é parecido no sentido. Só então diga "NLP". |
| 2. A lista | 7 min | Peça que ajustem as listas e anotem o palpite antes de apertar. A lista de partida acerta 47% e fica sem resposta em 47%. Leia em voz alta duas avaliações "sem resposta". Feche com a ponte: o classificador quer uma tabela. |
| 3. A tabela | 11 min | Peça palpites de colunas no chat (costumam vir centenas). São 9801. Peça que embaralhem a frase: a linha não muda. Nomeie vocabulário, vetor, saco de palavras, esparsa. Guarde "a ordem sumiu" para o bloco 8. |
| 4. Pedaços | 7 min | "ótimo" em quantas colunas? São 19. Ligue os interruptores um a um e mostre o total caindo de 9801 para 5357. Nomeie tokenização e normalização. |
| 5. Palavras vazias | 7 min | Deixe a turma marcar fichas. Depois aperte "Usar a lista pronta" e aponte o "não" riscado. O "não" aparece em 1118 das 2000 negativas. Nomeie stopwords. Não fale ainda de acerto: fica para o bloco 8. |
| 6. A ponta | 10 min | Votação nos oito pares. barato/barata (o inseto) arranca riso: use. Peça que testem palavras na caixa livre. Depois o segundo movimento, "E com dicionário?": pergunte o lema de "fui" antes de mostrar que a ferramenta errou. |
| 7. Quanto puxa | 13 min | **O centro da aula.** Seis cartões: peça votos no chat para "avaliar" e "dentro" antes de abrir. "avaliar" pesa −3,7 (quem ainda não recebeu o produto); "dentro" vem de "dentro do prazo". Ligue com `preço = a × área + b` da aula 1: um "a" por palavra, e aprender é contar. Nomeie peso e Naive Bayes. |
| 8. Sua frase | 12 min | Use as frases que a turma mandou no chat no começo. Depois as fichas-desafio, nesta ordem: "não é ruim" (negativa, −5,3), "a entrega atrasou" (positiva, +0,2; ligue "cortar a ponta" e vira negativa), "não gostei" com "tirar palavras vazias" (vira positiva), "não recomendo" com "pares de palavras" (volta a negativa, −5,0). Aponte o painel de acerto: a média mexe meio ponto enquanto frases trocam de lado. |
| 9. Python | 6 min | Se o download terminou, rode as duas caixas. Peça que achem, no código, a linha de cada bloco. Troque a frase da primeira caixa ao vivo. Os números (0,917, 0,912, 0,919) são os mesmos do bloco 8. |
| 10. Mapa | 4 min | Tabela-resumo e as três perguntas abertas: embeddings, Transformers, domínio e outras línguas. Cada uma foi provocada por um bloco (1, 8 e 7). Quiz de oito perguntas: peça a pontuação no chat. |
| 11. Para continuar | 1 min | Aponte o apêndice B do Jurafsky & Martin para quem quer o classificador a fundo e o CS224n para o próximo passo. |

## Variabilidade de exemplos (por onde passam)

- Corretor do celular (bloco 1)
- Críticas de restaurante (bloco 2)
- Letra de música com versos embaralhados (bloco 3)
- Busca no Google (bloco 4)
- Telegrama (bloco 5)
- Dicionário e palavras cruzadas (bloco 6)
- Comentários na loja de aplicativos (bloco 7)
- Atendimento automático (bloco 8)
- Avaliações de loja online: o fio de dados dos blocos 2 a 9

## Planos B

- **Turma silenciosa:** troque perguntas abertas por votação binária no chat ("1 = mesma
  coluna, 2 = colunas diferentes"). Os blocos 1, 6 e 7 já são votos.
- **Rede bloqueia o jsdelivr:** só o bloco 9 depende dele. A mensagem de erro aparece na
  própria caixa; siga para o mapa. Os blocos 1 a 8 funcionam depois que a página abriu.
- **Sobrou tempo:** no bloco 8, peça que cada um cole no chat a frase que enganou o
  classificador e explique duas delas pela esteira de peças. No bloco 9, troque a frase da
  primeira caixa por uma do chat.
- **Faltou tempo:** o segundo movimento do bloco 6 (lematização) vira leitura, e o bloco 9
  vira tarefa de casa. **Blocos 3, 7 e 8 são inegociáveis.**
