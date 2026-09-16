# Pesquisa — Texto vira número: introdução a NLP e análise de sentimentos

Dossiê da fase 1 da aula `nlp-intro`. Todo número marcado com **[v]** foi produzido em
shell pelos scripts de verificação (`verif/`, fora do repositório), com as versões do
Pyodide 0.27.5: nltk 3.8.1,
scikit-learn 1.6.1, numpy 2.0.2, scipy 1.14.1, pandas 2.2.3 (`verif/env.sh`).

O notebook de NLP do projeto do claude.ai não foi acessível a partir do Claude Code; o autor
autorizou seguir sem ele. Os três punches do brief que vieram dele (`não` sobrevive ao RSLP;
barato/barata, casa/casamento, livro/livre colidem) foram reverificados **[v]**.

## Recorte

- Público: iniciante absoluto em NLP que fez `ml-intro` (modelo, rótulo, treino/teste,
  acurácia, k-NN, parâmetro, overfitting e hiperparâmetro já liberados; "modelo = fórmula
  com espaços em branco; aprender = preencher").
- Ao vivo, online, ~90 min. Termina com o aluno escrevendo uma frase, vendo o classificador
  decidir e explicando a decisão pela tabela de números em que a frase virou.
- Fora: embeddings densos, Transformers, treino de redes, multilíngue (só no mapa).

## Fontes de referência

Links abertos em 2026-09-16.

| Fonte | Seção | Por que ler |
|---|---|---|
| Jurafsky & Martin, *Speech and Language Processing*, 3ª ed., rascunho de 19 ago. 2026 — https://web.stanford.edu/~jurafsky/slp3/ | Cap. 2 "Words and Tokens" (https://web.stanford.edu/~jurafsky/slp3/2.pdf); Apêndice B "Naive Bayes, Text Classification, and Sentiment" (https://web.stanford.edu/~jurafsky/slp3/B.pdf), B.4 "Optimizing for Sentiment Analysis"; Cap. 4 "Logistic Regression and Text Classification" (https://web.stanford.edu/~jurafsky/slp3/4.pdf) | O livro de referência. B.1–B.4 é, quase passo a passo, o classificador desta aula |
| CS224n, Stanford, Winter 2026 — https://web.stanford.edu/class/cs224n/ | Aula 2 "Word Vectors", slides 7–8 (https://web.stanford.edu/class/cs224n/slides_w26/cs224n-2026-lecture02-wordvecs.pdf) | "motel" e "hotel" em one-hot são ortogonais: a porta para embeddings (bloco de mapa) |
| scikit-learn, 8.2.3 "Text feature extraction" — https://scikit-learn.org/stable/modules/feature_extraction.html | 8.2.3.1 Bag of Words, 8.2.3.2 Sparsity, 8.2.3.4 Using stop words, 8.2.3.8 Limitations | Documentação oficial do `CountVectorizer`; já avisa que listas de stopwords podem apagar palavras informativas |
| NLTK Book, cap. 3 "Processing Raw Text", §3.6 "Normalizing Text" — https://www.nltk.org/book/ch03.html | stemmers vs lematizador | Mostra stem e lema lado a lado ("women" → "wom" / "woman") |
| NLTK HOWTO português — https://www.nltk.org/howto/portuguese_en.html | RSLP e stopwords em pt | Exemplos prontos em português |
| Orengo & Huyck (2001), "A Stemming Algorithm for the Portuguese Language", SPIRE — https://www.inf.ufrgs.br/~viviane/rslp/index.htm | página do RSLP | A origem do stemmer que a aula usa |
| Pang, Lee & Vaithyanathan (2002), "Thumbs up? Sentiment Classification using Machine Learning Techniques", EMNLP — https://aclanthology.org/W02-1011/ | Fig. 1–3 | O experimento "lista de palavras escolhida por gente vs aprendizado" que o bloco 2 refaz |
| Google, Text Classification Guide, Step 3 — https://developers.google.com/machine-learning/guides/text-classification/step-3 | n-gramas, contagem, tamanho do vocabulário | Curto e prático; pares de palavras (bloco 8) |
| d2l.ai, 16.1 "Sentiment Analysis and the Dataset" — https://d2l.ai/chapter_natural-language-processing-applications/sentiment-analysis-and-dataset.html | vocabulário com `min_freq` | Pipeline real, para quem quer ir para redes depois |
| B2W-Reviews01 — https://github.com/americanas-tech/b2w-reviews01 ; Real, Oshiro & Mafra (2019), STIL | corpus e artigo | Fonte do corpus pt (licença abaixo) |
| UCI Sentiment Labelled Sentences (Kotzias et al., KDD 2015) — https://archive.ics.uci.edu/dataset/331/sentiment+labelled+sentences | — | Fonte do corpus en, CC BY 4.0 |
| Camacho-Collados & Pilehvar (2018), "On the Role of Text Preprocessing in Neural Network Architectures" — https://arxiv.org/abs/1707.01780 | resultados | Evidência de que lematizar/limpar "does not help in general" |
| Wilson, Wiebe & Hoffmann (2005) — https://aclanthology.org/H05-1044/ ; Turney (2002) — https://aclanthology.org/P02-1053/ | concordância; domínio | Teto humano (~82% de concordância em polaridade); "unpredictable" muda de sinal por domínio |

`scikit-learn "Working With Text Data"` foi removido depois da 1.4 (só existe arquivado em
https://scikit-learn.org/1.4/tutorial/text_analytics/working_with_text_data.html); não
entra nas referências da página.

## Como as boas introduções abrem o tema

- **SLP3, Apêndice B.** Abre com trechos de reviews ("awesome caramel sauce", "awful pizza
  and ridiculously overpriced"), diz que regras à mão "can be fragile" e chega ao
  supervisionado. Ordem: bag of words como "unordered set of words" → treino (vocabulário,
  palavras desconhecidas, stopwords) → exemplo resolvido → ajustes para sentimento (binary
  NB, truque do `NOT_`, léxicos). Tokenização e normalização vêm **antes**, em capítulo
  próprio.
- **SLP3, Cap. 4.** Abre com uma regra à mão que a negação quebra ("if 'love' appears and
  it's not preceded by 'don't'"). Exemplo central: 6 features com pesos, soma, decisão.
- **scikit-learn.** Dados → bag of words → contagem → classificador → pipeline. Não fala de
  stemming; stopwords só como aviso.
- **CS224n.** Abre pelo significado, derruba o one-hot ("no natural notion of similarity")
  e vai para vetores densos.
- **Onde divergem, e a decisão que isso impõe ao roteiro:**
  1. *Preparo antes ou depois da tabela?* Livros põem tokenização antes da classificação,
     como pré-requisito. O pedido do autor é o inverso (preparo como consequência do custo
     da tabela), e os dados o sustentam: cada técnica tem um custo mensurável que ela ataca.
  2. *Stemming importa?* O NLTK (2009) o trata como passo central; o SLP3 de 2026 **tirou**
     a seção de stemming do cap. 2 (sobrou nas notas históricas) e foi para subpalavras. Os
     nossos números concordam com o SLP3: stemming corta colunas, quase não mexe na nota.

## Equívocos comuns

1. **"Remover stopwords sempre ajuda."** SLP3 B.2: "using a stop word list doesn't improve
   performance". scikit-learn 8.2.3.4 avisa sobre a própria lista. As listas padrão contêm a
   negação **[v]**: NLTK pt tem `não, nem, mais, muito, sem` (não tem `nunca`); NLTK en tem
   `not, no, nor, very, too, don't, didn't, wasn't, isn't, but, against`; a lista do
   scikit-learn tem `not, no, never, nothing` — e também `cry, fire, bill, amount`.
2. **"Stemming/lematização sempre melhoram."** Pang 2002 chegou a 82,9% sem stemming nem
   stoplist; Camacho-Collados 2018; nossos números abaixo.
3. **"O saco de palavras guarda a ordem."** SLP3, scikit-learn 8.2.3.8.
4. **"O modelo entende o significado."** O peso de uma palavra vem de onde ela apareceu, não
   do que ela quer dizer (punches P9, P10).
5. **"Mais pré-processamento é sempre melhor"** — a "receita completa" piora (P12).
6. **"Stem e lema são a mesma coisa"** — NLTK book; P7.
7. **"Contar quantas vezes é melhor que marcar presença."** Pang 2002: presença 82,9% vs
   frequência 72,8% (SVM); SLP3 B.4 binary NB. A aula usa presença (0/1).
8. **"Negação e ironia o modelo resolve sozinho."** SLP3 B.4 (truque do `NOT_`); Pang 2002
   ("thwarted expectations").

## Números verificados que sustentam os punches

> **Atenção — números exploratórios.** Esta seção e os candidatos a punch usam a amostra de
> exploração (1000 por classe, antes do filtro de conteúdo). A configuração final (2000 por
> classe em pt, filtro aplicado, Porter no modo original) mudou vários valores; **os números
> que valem estão no `ROTEIRO.md`** e em `verif/saida-v12-*.txt`. Dois punches não
> sobreviveram à troca de amostra e foram descartados: P9 na versão "atrasou só aparece em
> 'não atrasou'" e P11 na frase "encontrei uma barata dentro da caixa" (teste de 10 amostras
> em `verif/v13_robustez.py`).

Corpus pt: B2W, reviews de 3 a 20 palavras, sem duplicatas, 1000 com nota 1–2 (negativas)
e 1000 com nota 4–5 (positivas), amostra `random_state=7`; 158 KB de texto. Corpus en: UCI,
Amazon + Yelp, 1986 frases após tirar duplicatas (992 positivas, 994 negativas); 111 KB.
Classificador: Naive Bayes multinomial sobre presença (0/1), `alpha=1` (= `CountVectorizer(binary=True)` + `MultinomialNB()`).
Acurácias: média de 20 divisões treino/teste (25% teste, estratificadas, `random_state` 0–19).

| Etapa (a partir de "minúsculas + tokens") | pt colunas | pt acurácia | pt vs base | en colunas | en acurácia | en vs base |
|---|---|---|---|---|---|---|
| texto cru, separado por espaço | 5058 | 0,890 | −1,5 pt, pior 20/20 | 4104 | 0,764 | −4,9 pt, pior 20/20 |
| **base: minúsculas + só letras** | 3107 | 0,906 | — | 2705 | 0,813 | — |
| + tirar acentos | 3016 | 0,908 | +0,2, melhor 14/20 | 2704 | 0,814 | 0 |
| + stopwords (lista NLTK) | 2991 | 0,891 | −1,5, pior 20/20 | 2559 | 0,791 | −2,2, pior 19/20 |
| + stopwords, mantendo negações | 2994 | 0,906 | 0 (9 × 9) | 2571 | 0,815 | +0,2 (9 × 7) |
| + stemming (RSLP / Porter) | 2020 | 0,909 | +0,4 (12 × 6) | 2203 | 0,817 | +0,4 (13 × 6) |
| + pares de palavras | 14069 | 0,913 | +0,8 (15 × 4) | 12259 | 0,823 | +0,9 (14 × 6) |
| + stemming + pares | 12161 | 0,919 | +1,3 (18 × 1) | 11483 | 0,831 | +1,7 (17 × 3) |
| "receita completa": acento + stopwords + stemming | 1897 | 0,898 | −0,7, pior 13/20 | 2065 | 0,792 | −2,2, pior 19/20 |

Atenção: **uma divisão só engana.** Com `random_state=7` isolado, em pt o stemming aparece
com +1,8 pt e as stopwords com só −0,2. O widget precisa mostrar a média das 20 divisões
(ver Riscos).

Outros números **[v]** (corpus inteiro, pipeline base):

- Tamanho: pt 26 158 palavras, 3696 colunas; en 20 976 palavras, 3191 colunas.
- Palavras que aparecem **uma vez só**: pt 58% do vocabulário (2152); en 56% (1781).
- As 10 palavras mais comuns cobrem 25% (pt) / 24% (en) de todo o texto. Em pt: produto, o,
  e, **não** (4ª), de, a, muito, do, que, com.
- Stopwords: 39% das palavras do texto em pt, mas só 122 colunas; en 49% e 150 colunas.
- Uma review tem em média 12,4 palavras distintas (pt) / 10,0 (en): 99,67% / 99,69% de zeros.
- Variantes cruas de "ótimo" no corpus pt: **18** colunas diferentes (Ótimo 47, ótimo 44,
  otimo 10, "ótimo," 8, "ótimo." 6, Otimo 3, OTIMO 3, …). Em en, "great": 11.
- Lista de palavras escrita à mão **antes** de olhar os pesos (13 positivas, 12 negativas;
  lista em `verif/v04_pareado_zipf_lista.py`): pt acerta 46,9%, erra 6,6% e fica **muda em
  46,6%** (nenhuma palavra da lista, ou saldo zero); en acerta 34,1%, erra 3,5%, muda em
  62,4%. Pang 2002 (Fig. 1): humanos 58% e 64%, com 75% e 39% de empates.
- Presença por classe (em quantas das 1000 positivas / 1000 negativas a palavra aparece):
  `não` 65 / 546; `produto` 447 / 448; `dentro` 33 / 2 ("dentro do prazo"); **`atrasou` 2 /
  0 — as duas são "não atrasou"**; `avaliar` 2 / 72 ("não posso avaliar, não recebi");
  `dinheiro` 1 / 38; `hoje` 1 / 31; `top` 11 / 0; `ótimo` 118 / 2; `otimo` 18 / 0; `ruim` 1 /
  34; `bom` 205 / 36; `nem` 3 / 40; `quebrado` 0 / 15.
  en (992 / 994): `not` 32 / 189; `the` 413 / 408; `town` 7 / 0 ("best … in town"); `spot` 8
  / 0; `money` 1 / 24 ("waste of money"); `minutes` 2 / 20; **`disappoint` 2 / 1 — as duas
  positivas são "did not / won't disappoint"**; `great` 150 / 5; `bad` 0 / 31.
- Stemmer RSLP (nltk 3.8.1) **[v]**: `Não/NÃO → não`; gostei, gosto, gosta, gostaria,
  gostoso → `gost`; barato, barata, baratinho → `barat`; casa, casamento → `cas`; livro,
  livre, livraria → `livr`; paisagem → `pais`; pais → `pal`; pior → `pi`. Corta de menos:
  bom → `bom` mas boa → `boa`; amei → `ame`, amo → `amo`, amor → `am`, amava → `am`; demora →
  `dem` mas demorou → `demor`; recomendo → `recom` mas recomendação → `recomend`; rápido →
  `rápid` mas rapidez → `rapid`. fui, vou, ir, foi, era, sou, é: todos intocados.
- Porter, modo `ORIGINAL_ALGORITHM` **[v]**: liked, like, likes, likely → `like`; general,
  generous, generate → `gener`; university, universe → `univers`; organ, organization →
  `organ`; news, new → `new`; was → `wa`; went, gone intocados.
- Lematização, spaCy 3.8.7 (`pt_core_news_sm` / `en_core_web_sm` 3.8.0) **[v]**: em "Eu fui
  ontem", **fui → ser** (é "ir"); vou, iria → ir; foi, era → ser; boa → bom; amava → amar,
  mas **Amei → Amei** e **amo → amo**; quebrado → quebrar; entregas → entrega. en: went,
  going → go; was, am → be; **better → well**; broken → break; phones → phone.

## Candidatos a punch

### P1 — Parecido na forma, oposto no sentido
- Pergunta: "Qual par de frases é mais parecido: 'é ruim' / 'não é ruim', ou 'ótimo' / 'excelente'?"
- Erro comum: achar que o computador "vê" o que a gente vê.
- Revelação: por letras, o par oposto é o mais próximo; o par sinônimo não tem uma letra em
  comum na mesma posição. Em números (a fruta de 150 g e a de 151 g), perto é parecido; em
  texto, não.
- Widget: pares de frases; o aluno vota; um medidor mostra quantas letras mudam.
- A verificar: distâncias de edição dos pares (conta trivial; fazer na fase 3).

### P2 — A lista de palavras fica muda
- Pergunta: "Escreva as palavras que denunciam uma avaliação positiva e uma negativa."
- Erro comum: "com umas 20 palavras eu pego quase tudo".
- Revelação: a lista acerta 46,9% (pt) / 34,1% (en) e fica muda em quase metade (pt) ou
  dois terços (en). Ecoa Pang 2002 e o bloco 1 de `ml-intro`.
- Widget: duas listas editáveis, pré-preenchidas com a lista a priori; botão testa nas 2000
  avaliações e mostra certas / erradas / mudas, com exemplos de mudas.
- A verificar: feito **[v]**.

### P3 — Cada palavra vira uma coluna, e a tabela é quase só zeros
- Pergunta: "Quantas colunas tem a tabela? Quantos zeros tem a linha da sua frase?"
- Erro comum: estimar dezenas de colunas.
- Revelação: 6193 colunas cruas (pt, corpus inteiro); a frase do aluno tem ~12 uns e ~6180
  zeros (99,8%). Nome: vocabulário, saco de palavras, esparso.
- Widget: o aluno escreve; aparece a linha da tabela (só as colunas com 1, mais um contador
  de zeros) ao lado de algumas avaliações.

### P4 — A ordem some
- Pergunta: "'chegou rápido mas veio quebrado' e 'veio quebrado mas chegou rápido' viram a
  mesma linha?"
- Revelação: sim, idênticas; a nota dada pelo classificador também (−1,73 nas duas) **[v]**.
  Idem "não é bom, é ótimo" / "não é ótimo, é bom".

### P5 — 18 colunas para "ótimo"
- Pergunta: "Em quantas colunas diferentes o 'ótimo' se espalhou?"
- Erro comum: 1 ou 2.
- Revelação: 18. Cada uma tem poucas avaliações para aprender. Minúsculas + separar
  pontuação: 6193 → 3696 colunas; acerto +1,5 pt (pt) / +4,9 pt (en), 20/20 divisões.
  Nome: tokenização, normalização.

### P6 — Stopwords jogam fora o "não"
- Pergunta: "39% do texto são 'o', 'de', 'e', 'que'… Jogar fora?"
- Erro comum: "claro, não dizem nada".
- Revelação: na lista padrão está `não`, a 4ª palavra mais comum e uma das mais
  informativas (65 positivas / 546 negativas). Sem ela, "não gostei" vira positiva (+0,82) e
  "não recomendo" também (+1,37) **[v]**. E só 122 colunas somem. Acerto −1,5 pt (pt, 20/20
  piores) / −2,2 pt (en, 19/20). Mesmo mantendo as negações, empata: não ajuda.

### P7 — A tesoura corta demais e de menos
- Pergunta: "barato e barata viram a mesma coluna? E bom e boa?"
- Revelação: barato/barata(inseto) → `barat`; bom/boa ficam separados; amei/amo/amor, três
  colunas. Stemming é regra de corte, não dicionário. Colunas −35% (pt); acerto +0,4 pt.
  Nome: stemming, radical.

### P8 — Lema precisa de contexto, e ainda erra
- Pergunta: "Qual é o 'verbo de dicionário' de 'fui'?"
- Revelação: "ir" ou "ser" — depende da frase; o spaCy escolheu "ser" em "Eu fui ontem".
  "Amei" ficou "Amei". Nome: lematização, lema.

### P9 — "atrasou" é palavra positiva
- Pergunta: "Esta palavra puxa para positiva ou negativa: atrasou? dentro? avaliar? produto?"
- Erro comum: julgar pelo sentido.
- Revelação: o classificador só sabe onde a palavra apareceu. "atrasou" só apareceu em "não
  atrasou" (2 / 0); "dentro" em "dentro do prazo" (33 / 2); "avaliar" em "não posso avaliar,
  não recebi" (2 / 72); "produto" não diz nada (447 / 448). en: `disappoint`, `town`,
  `money`, `the`.
- Consequência **[v]**: "a entrega atrasou" → positiva (+2,29).

### P10 — Aprender é contar
- Pergunta: "Como o computador chegou nesses pesos?"
- Revelação: contando em quantas positivas e negativas cada palavra aparece. A nota da frase
  é a soma dos pesos das palavras dela: a "fórmula com espaços em branco" de `ml-intro`, com
  um espaço por coluna. Nome: peso; Naive Bayes.

### P11 — Faça o classificador errar
- Pergunta: "Escreva uma frase que ele erre."
- Revelações **[v]** (pt, pipeline base, corpus inteiro): "não é ruim" → negativa (−4,86;
  `não` −2,03 e `ruim` −2,78 somam); "encontrei uma barata dentro da caixa" → positiva
  (+2,37, puxada por `dentro` +2,51); "que maravilha, esperei dois meses pela entrega" →
  negativa sem stemming (`maravilha` fora do vocabulário) mas **positiva com stemming**
  (`maravilh` +3,18); "top demais" → positiva (+3,06). en: "not bad" → negativa (−5,09);
  "not bad at all" → −5,82; com stopwords removidas, "i do not recommend it" → positiva.

### P12 — A receita completa piora
- Pergunta: "Liga tudo: minúsculas, acentos, stopwords, stemming. A nota sobe?"
- Revelação: cai (pt −0,7, pior em 13/20; en −2,2, pior em 19/20). O que ajuda de verdade:
  tokenizar (+1,5 / +4,9) e pares de palavras com stemming (+1,3 / +1,7, com 4× mais
  colunas).

### P13 — Pares de palavras consertam "não recomendo", a um preço
- Revelação **[v]**: com pares, "não recomendo" −4,39 (`não_recomendo` −3,78); "veio
  quebrado mas chegou rápido" deixa de ser igual à versão invertida (+0,14 vs −1,65); colunas
  3107 → 14069. Nome: n-grama/bigrama.

### P14 — Vizinha mais próxima por palavras em comum (reserva)
- Com todas as palavras, a vizinha de "i did not like this phone" é "I did not expect this
  to be so good!" (positiva, 4 palavras em comum: i, did, not, this) **[v]**. Liga ao k-NN de
  `ml-intro`. Em pt o efeito é fraco ("não gostei do produto" acha a própria frase). Fica de
  reserva.

## Dados e exemplos

- **Fio de dados:** as 2000 avaliações de loja online (pt: B2W; en: UCI Amazon + Yelp),
  dos blocos 2 a 9. Um corpus só, que o aluno vê virar tabela, ser limpo e treinar o
  classificador.
- **Domínios dos exemplos verbais, por bloco** (variar): 1 mensagens de celular e manchetes;
  2 críticas de restaurante; 3 letras de música / receitas; 4 buscas no Google; 5 SMS e
  legendas; 6 dicionário e palavras cruzadas; 7 comentários de loja; 8 atendimento ao
  cliente; 9 filmes.
- Os corpora pt e en são diferentes: números e exemplos saem de cada um, no `STR` de cada
  língua; a estrutura é a mesma.

## Ferramentas no navegador

- **Pyodide 0.27.5** (o do `core.js`) tem nltk 3.8.1 e scikit-learn 1.6.1 no lock. Os
  corpora do NLTK não vêm: `rslp.zip` (3,8 KB) e `stopwords.zip` (37,7 KB) estão em
  `https://cdn.jsdelivr.net/gh/nltk/nltk_data@gh-pages/packages/…`, com CORS aberto.
  **Testado em Chromium headless [v]:** `loadPackage(["nltk","scikit-learn"])`, `pyfetch`
  dos dois zips, `extractall` em `/home/pyodide/nltk_data/…`, `RSLPStemmer().stem("barata")
  == "barat"` e `"não" in stopwords.words("portuguese")`. `nltk.download()` não é usado
  (urllib não funciona no Pyodide). No Chromium headless desta máquina o QUIC falhou e foi
  preciso `--disable-quic`: registrar para a verificação da fase 5.
- **Sem rede:** stemmer RSLP portado para JS (137 linhas de Python + 246 regras em 7
  arquivos, que vão como dados JSON) e Porter original em JS; ambos conferidos palavra a
  palavra contra o nltk sobre o vocabulário inteiro de cada corpus. Tokenizador, saco de
  palavras, Naive Bayes e as 20 divisões: JS puro, com as divisões gravadas no JSON do
  corpus para bater com o scikit-learn.
- **Lematização** não tem implementação viável no navegador (spaCy não está no Pyodide;
  nltk não tem lematizador pt): exemplos pré-computados com spaCy, marcados como tal.
- **Local:** o `python` padrão da máquina está quebrado (trampoline do uv); tudo roda por
  `uv run --python 3.12`. O `check.py` vai precisar do mesmo.

## Licenças dos dados

- **B2W-Reviews01: CC BY-NC-SA 4.0.** Compatível com o hub (educacional, sem fins
  comerciais) se: (BY) crédito à B2W Digital + artigo + link da licença, na página e no
  arquivo; (NC) o site não monetiza; (SA) o arquivo de amostra sai sob CC BY-NC-SA 4.0, com
  o aviso dentro dele. Só `texto` e `rótulo` vão para a amostra (nada de id, idade, gênero,
  estado).
- **UCI Sentiment Labelled Sentences: CC BY 4.0.** Crédito a Kotzias et al. 2015.

## Riscos

1. **Uma divisão só engana** (ver tabela). O widget de "liga/desliga" precisa mostrar a
   média de 20 divisões e "melhorou em X de 20", ou o punch P12 vira sorte.
2. **Texto real de usuário:** o B2W tem palavrão, nomes de loja e possivelmente dados
   pessoais no texto. A amostra precisa de filtro (palavrões, sequências de dígitos
   longas, e-mails) e de uma leitura rápida antes de publicar.
3. **Paridade dos stemmers JS × nltk:** RSLP é curto; Porter no modo original tem porte
   conhecido. Se houver divergência em alguma palavra do vocabulário, a aula mostra o JS e o
   bloco Python mostra o nltk — precisa ser 100% igual, ou o aluno vê números diferentes.
4. **"Peso" como logaritmo.** O peso do Naive Bayes é `ln(P(palavra|positiva) /
   P(palavra|negativa))` com suavização +1. A página mostra contagens e barras; a fórmula
   fica num `details` para curiosos. Sem isso, o aluno de `ml-intro` não tem o log.
5. **Nota 3 descartada** e "nota ≠ sentimento": o B2W mostra 14 187 avaliações nota 3 que
   recomendam o produto. Não é punch desta aula; vira uma linha no bloco 2.
6. **Tamanho da página:** corpus + divisões + regras ≈ 200 KB por língua; aceitável, e
   carregado uma vez.
