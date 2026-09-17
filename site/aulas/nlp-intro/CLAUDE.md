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
  peso, Naive Bayes 7 · n-grama, bigrama 8 · embeddings, Transformers só no 10. Conferir
  com `scripts/nlp-intro/gating.py` ou com um grep por termo nas seções anteriores.
- **Menu do topo: "6 A ponta" e "7 Quanto puxa"** (en: "6 The ending", "7 How hard").
  O menu fica visível desde o começo da página, e "radical"/"peso" (en: "stem"/"weight")
  só podem aparecer a partir dos blocos 6 e 7. **Não "consertar" para "6 Radical" e
  "7 Pesos":** isso entrega os termos antes da hora e quebra o gating.
- **Nuance da en no bloco 5.** Sem stopwords, "i did not like it" vira "like", mas
  **continua negativa (−0,18)**. A frase que inverte é "i do not recommend it"
  (−2,26 → +0,91). Não escrever, nem na página nem no guia, que "i did not like it" vira
  positiva. Em pt as duas invertem ("não gostei" −0,89 → +1,05).
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

## Regenerar a amostra

Os scripts ficam em `scripts/nlp-intro/`, fora de `site/`. O `README.md` de lá diz de onde
baixar os dados originais, que não entram no repositório.

1. Critérios, todos no topo de `scripts/nlp-intro/gerar_amostra.py`:
   - **pt (B2W):** notas 1 e 2 são negativas (rótulo 0), notas 4 e 5 positivas
     (rótulo 1), e a nota 3 fica de fora. Entram avaliações de 3 a 20 palavras separadas
     por espaço, sem texto duplicado e sem o filtro de `filtros.py`. Sorteio de 2000 por
     classe com `random_state=7`, e o conjunto é embaralhado com a mesma semente.
   - **en (UCI):** Amazon e Yelp, sem duplicatas, com filtro e embaralhamento pela
     semente 7.
   - **Divisões:** 20 divisões com `train_test_split` (`random_state` de 0 a 19, 25% de
     teste, estratificadas).
2. `./env.sh gerar_amostra.py --conferir` precisa dizer "identico ao publicado: True"
   nas duas línguas. Se disser False, a amostra mudou: o motivo pode ser a versão de
   pandas, numpy ou scikit-learn, ou o próprio CSV.
3. Para mudar a amostra de propósito, altere as constantes e rode
   `./env.sh gerar_amostra.py`, depois `./env.sh build_assets.py`. Em seguida
   `./env.sh v12_final.py pt` e `en` e `./env.sh v21_revelar_en.py` para refazer os
   números dos Revelar, `harness.py pt` e `en` para conferir o JS e `v13_robustez.py`
   para os punches de frase.

## Números que sustentam os punches

Medidos contra os JSON publicados, com o classificador e as 20 divisões da página.
Todos são regenerados, e comparados com o texto da página, por:

- pt: `cd scripts/nlp-intro && ./env.sh v22_revelar_pt.py` (saída em `saida-v22-pt.txt`)
- en: `cd scripts/nlp-intro && ./env.sh v21_revelar_en.py` (saída em `saida-v21-en.txt`)

Cada linha termina com "sim" ou "NAO", e o script termina com "TUDO BATE" ou com a lista
do que não bate. O download do bloco 9 sai do `prod2.py` (`saida-prod2.txt`).

| Bloco · punch | pt | en |
|---|---|---|
| 1 · forma não é sentido (letras que mudam) | é ruim/não é ruim 4 · ótimo/excelente 9 · metades trocadas 20 | bad/not bad 4 · great/excellent 7 · metades 26 |
| 2 · a lista fica muda | certas 47,15% · erradas 5,97% · sem resposta 46,88% | 34,1% · 3,5% · 62,4% |
| 3 · tabela esparsa e sem ordem | 9801 colunas · 12,55 palavras por avaliação · 99,87% de zeros · 67,6% das colunas numa avaliação só | 4977 · 10,15 · 99,80% · 66,7% |
| 4 · uma palavra, muitas colunas | "ótimo" em 19 colunas (122/101/28/15/13/11/7) · 9801 → 5357 (−45%) · 5145 sem acento | "great" em 11 (69/46/22/11/6/1) · 4977 → 3187 (−36%) · 3185 |
| 5 · stopwords apagam a negação | 52.138 palavras, 39,2% stopwords, 131 colunas · "não" é a 4ª, em 1118 negativas e 136 positivas | 20.957, 49,2%, 150 · "not" é a 11ª, em 189 negativas e 32 positivas |
| 6 · o corte junta demais e de menos | barato = barata, casa = casamento · bom ≠ boa, amei ≠ amo · 5357 → 3195 (−40%) | liked = likely, general = generous, news = new · good ≠ better, went ≠ go · 3187 → 2554 (−20%) |
| 6 · lema depende do contexto (spaCy 3.8.7) | fui → ser · Amei → Amei | better → well |
| 7 · o peso vem de onde a palavra apareceu | avaliar −3,70 (131 neg, 2 pos; 111 das 131 de quem não recebeu, contagem conservadora) · dentro 59 pos, 15 neg (40 das 59 com "dentro do prazo") · produto 886/857, +0,12 · acerto 91,7% | money −2,47 (24 neg, 1 pos) · town 7 pos, 0 neg · the +0,07 · acerto 81,3% |
| 8 · a soma não sabe negar | não −2,01 + ruim −3,48: "não é ruim" −5,33 · "a entrega atrasou" +0,24, com radical −1,22 · ironia −2,31, com radical +3,04 · "não gostei" −0,89, sem stopwords +1,05 | not −1,69 + bad −3,41: "not bad" −5,10 · "the delivery was late" +0,08 · "oh great, it broke…" −0,41, com radical +0,18 · "i do not recommend it" −2,26, sem stopwords +0,91 |
| 8 · a média quase não se mexe | sem stopwords 91,2% (pior em 16 de 20) · pares 92,7% (melhor em 20 de 20), 5357 → 29.509 colunas (5,5×) | 79,3% (pior em 18 de 20) · 82,4% (melhor em 15 de 20), 3187 → 15.264 (4,8×) |
| 9 · nada era de brinquedo | 0,917 · 0,912 · 0,919 | 0,813 · 0,793 · 0,819 |

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
