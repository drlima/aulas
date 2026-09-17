# Licenças dos dados e do código de terceiros da aula `nlp-intro`

A aula "Texto vira número" usa, nesta pasta, material de terceiros. Cada item segue a
própria licença, listada abaixo. O restante da aula (HTML, CSS, o `aula.js` fora dos
trechos indicados e os textos) não é regido por estas licenças.

## `avaliacoes-pt.json` — CC BY-NC-SA 4.0

- **Origem:** B2W-Reviews01, da B2W Digital. Real, L.; Oshiro, M.; Mafra, A. "B2W-Reviews01:
  an open product reviews corpus". STIL 2019.
  https://github.com/americanas-tech/b2w-reviews01
- **Licença:** Creative Commons Atribuição-NãoComercial-CompartilhaIgual 4.0 Internacional,
  https://creativecommons.org/licenses/by-nc-sa/4.0/
- **Alterações:** amostra de 4000 avaliações (2000 com nota 1 ou 2, rótulo 0; 2000 com
  nota 4 ou 5, rótulo 1; a nota 3 ficou de fora), de 3 a 20 palavras, sem texto
  duplicado, sem palavrão forte nem dados pessoais, sorteada com semente 7. Só o texto e
  o rótulo foram mantidos, e o arquivo traz 20 divisões treino/teste.
- **Esta amostra é distribuída sob a mesma licença, CC BY-NC-SA 4.0.** O script que a gera
  é `scripts/nlp-intro/gerar_amostra.py`, no repositório https://github.com/drlima/aulas.

## `avaliacoes-en.json` — CC BY 4.0

- **Origem:** Sentiment Labelled Sentences. Kotzias, D.; Denil, M.; de Freitas, N.; Smyth, P.
  "From Group to Individual Labels using Deep Features". KDD 2015. UCI Machine Learning
  Repository, https://archive.ics.uci.edu/dataset/331/sentiment+labelled+sentences
- **Licença:** Creative Commons Atribuição 4.0 Internacional,
  https://creativecommons.org/licenses/by/4.0/
- **Alterações:** só as partes Amazon e Yelp (sem IMDb), sem frases duplicadas e sem
  palavrão forte, embaralhadas com semente 7, mais 20 divisões treino/teste.

## `stopwords-pt.json` e `stopwords-en.json`

- **Origem:** corpus "stopwords" do NLTK Data (https://www.nltk.org/nltk_data/), que reúne
  as listas do projeto Snowball distribuídas com o PostgreSQL. A lista em inglês tem os
  acréscimos do próprio NLTK Data.
- **Licença:** o NLTK Data não declara licença para este corpus. As listas estão aqui sem
  alteração, só convertidas para JSON e em ordem alfabética.

## `rslp.json`

- **Origem:** regras do stemmer RSLP (Removedor de Sufixos da Língua Portuguesa), de Orengo,
  V. M.; Huyck, C. "A Stemming Algorithm for the Portuguese Language". SPIRE 2001. As
  regras vêm do pacote `stemmers/rslp` do NLTK Data, no formato que o NLTK lê.
- **Licença:** o NLTK Data não declara licença para este pacote. As regras estão aqui sem
  alteração, só convertidas para JSON.

## Trechos do `aula.js`: funções `rslp()` e `porter()` — Apache License 2.0

- **Origem:** porte para JavaScript de `nltk.stem.rslp` e `nltk.stem.porter` (modo
  `ORIGINAL_ALGORITHM`), do NLTK 3.8.1. Copyright (C) 2001-2023 NLTK Project.
  https://www.nltk.org/
- **Licença:** Apache License, Version 2.0, https://www.apache.org/licenses/LICENSE-2.0
- **Alterações:** tradução de Python para JavaScript, com a mesma lógica, conferida palavra
  a palavra contra o NLTK sobre o vocabulário das duas amostras.
- Os algoritmos são de Orengo e Huyck (2001), para o RSLP, e de Martin Porter (1980), "An
  algorithm for suffix stripping", para o Porter.
