# CLAUDE.md — aula `nlp-intro` (Texto vira número)

Introdução a NLP que termina num classificador de sentimento que o aluno consegue
explicar. Ao vivo, ~90 min, sucede `ml-intro` e pressupõe o vocabulário dela.
Publicada em https://drlima.github.io/aulas/aulas/nlp-intro/ (pt-BR) e
https://drlima.github.io/aulas/aulas/nlp-intro/en/ (en-US). As regras do repositório
estão no `CLAUDE.md` da raiz. `ROTEIRO.md` é o roteiro aprovado; `PESQUISA.md`, o dossiê;
`GUIA_DO_PROFESSOR.md`, os tempos ao vivo.

| id | Bloco | Ideia |
|---|---|---|
| s1 | Parecido | forma não é sentido |
| s2 | A lista | a lista à mão fica muda; o classificador quer uma tabela |
| s3 | A tabela | saco de palavras: 9801 colunas, quase tudo zero, sem ordem |
| s4 | Pedaços | "ótimo" em 19 colunas: tokenização e normalização |
| s5 | Palavras vazias | a lista de stopwords apaga o "não" |
| s6 | A ponta | stemming corta demais e de menos; lematização precisa de contexto |
| s7 | Quanto puxa | **centro:** peso = contagem; a nota é a soma |
| s8 | Sua frase | pouso: a frase do aluno, os erros explicados pelos números |
| s9 | Python | nltk + scikit-learn no Pyodide (único bloco que precisa de rede) |
| s10 | Mapa | resumo, três perguntas abertas, quiz |
| s11 | Referências | links conferidos |

## Regras firmes

- **Gating de vocabulário.** Cada termo só aparece a partir do bloco indicado; antes, a
  paráfrase. classificador 2 · vocabulário, vetor, saco de palavras, esparsa 3 ·
  token, normalização 4 · stopwords 5 · stemming, radical, lematização, lema 6 ·
  peso, Naive Bayes 7 · n-grama, bigrama 8 · embeddings, Transformers só no 10. O menu
  do topo conta como texto visível desde o início (por isso "6 A ponta", "7 Quanto
  puxa"). Conferir com `rascunhos/nlp-intro/verif/gating.py` (fora do repositório) ou
  com um grep por termo nas seções anteriores.
- **Classificador: Naive Bayes multinomial sobre presença (0/1), alpha = 1.** O peso se
  explica por contagem, que é o centro da aula. Não trocar por regressão logística nem
  por contagem de ocorrências.
- **Acurácia sempre como média das 20 divisões gravadas no JSON** (`divisoes`, geradas
  pelo `train_test_split` com `random_state` 0 a 19). Uma divisão só engana: com
  `random_state=7` o radical parecia ganhar 1,8 ponto.
- **Fio de dados.** pt: 4000 avaliações do B2W-Reviews01 (notas 1–2 negativa, 4–5
  positiva, 3 fora; 3 a 20 palavras; 2000 de cada; sorteio `random_state=7`; filtro de
  palavrão forte, acusação e dado pessoal antes do sorteio). en: 1984 frases do UCI
  Sentiment Labelled Sentences (Amazon + Yelp). Mudar a amostra muda todos os números
  dos Revelar; refaça-os.
- **Punches vetados** por não se sustentarem em outras amostras: "atrasou só aparece
  em 'não atrasou'" e "encontrei uma barata dentro da caixa sai positiva".
- **Stemmers em JS têm de bater com o nltk 3.8.1**: RSLP (regras em `assets/rslp.json`,
  exportadas do próprio nltk) e Porter em `mode="ORIGINAL_ALGORITHM"` (não o default).
  Tokenizador pt `[^\W\d_]+`; en `[^\W\d_]+(?:'[^\W\d_]+)?`. Qualquer divergência de
  radical, de coluna ou de acerto por sorteio bloqueia o push.
- **Lematização só com exemplos pré-calculados** (spaCy 3.8.7), e a página diz isso.
- **Dados em JSON, nunca em `.js`** (regra de acentos). `avaliacoes-pt.json` leva
  `fonte` e `licenca` (CC BY-NC-SA 4.0, a amostra sai com a mesma licença); o bloco 11
  dá o crédito. Só texto e rótulo entram na amostra.
- **Bloco 9** baixa `rslp.zip` e `stopwords.zip` do nltk_data pelo jsdelivr e o JSON do
  corpus do próprio site. `nltk.download()` não funciona no Pyodide.

## Contrato de ids

| Bloco | ids |
|---|---|
| seções | `s1` a `s11` |
| s1 | `pairCards`, `pairOut` |
| s2 | `listPos`, `listNeg`, `listGuess`, `vListGuess`, `listBtn`, `listBars`, `listOut`, `listMute` |
| s3 | `tabGuess`, `tabText`, `tabShuffle`, `tabGrid`, `tabOut` |
| s4 | `tokSearch`, `tokLower`, `tokLetters`, `tokAccents`, `tokList`, `tokOut` |
| s5 | `stopChips`, `stopBtn`, `stopSamples`, `stopOut` |
| s6 | `stemCards`, `stemInput`, `stemOut`, `lemmaTable` |
| s7 | `pullCards`, `sumText`, `svgSum`, `sumOut`, `accOut` |
| s8 | `frText`, `frChips`, `frStop`, `frStem`, `frPairs`, `frBelt`, `svgFrase`, `frVerdict`, `frAcc` |
| s9 | `pyStatus`, `py1`, `run1`, `pyOut1`, `py2`, `run2`, `pyOut2` |
| s10 | `quiz10`, `quiz10Out` |

## Widgets a conferir antes do push

Pares (s1), "Testar nas 4000 avaliações" (s2), frase e "Embaralhar" (s3), busca e três
interruptores (s4), fichas e "lista pronta" (s5), cartões e caixa livre (s6), cartões
de peso e frase (s7), frase, fichas-desafio e três interruptores (s8), as duas células
de Python (s9, exigem rede), quiz (s10). Números esperados: `ROTEIRO.md`, seção do bloco 8.
