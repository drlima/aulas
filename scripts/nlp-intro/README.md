# Scripts da aula `nlp-intro`

Geram os dados da aula e conferem, em Python, cada número que as páginas mostram. Ficam
fora de `site/`, então não são publicados. As regras da aula estão em
`site/aulas/nlp-intro/CLAUDE.md`.

## Ambiente

Tudo roda de dentro desta pasta, com `./env.sh script.py`. O `env.sh` usa `uv` com as
mesmas versões do Pyodide 0.27.5 da página: nltk 3.8.1, scikit-learn 1.6.1, numpy 2.0.2,
scipy 1.14.1 e pandas 2.2.3. Com outras versões, os sorteios e as acurácias podem mudar.
Os scripts de navegador (`harness.py`, `widgets.py`, `nav.py`, `pytest_page.py`,
`prod.py`, `prod2.py`, `pyo_run.py`) rodam com
`uv run --no-project --python 3.12 --with playwright python script.py`. O Chromium é
aberto com `--disable-quic`; é uma opção do ambiente de teste e não muda nada na página.

## Dados originais (fora do repositório)

A pasta `dados/` está no `.gitignore`. Para regenerar:

- **pt:** baixe https://github.com/americanas-tech/b2w-reviews01/archive/refs/heads/main.zip
  e descompacte em `dados/`, para ficar `dados/b2w-reviews01-main/B2W-Reviews01.csv`
  (49 MB, CC BY-NC-SA 4.0).
- **en:** baixe https://archive.ics.uci.edu/static/public/331/sentiment+labelled+sentences.zip
  e descompacte em `dados/`, para ficar
  `dados/sentiment labelled sentences/amazon_cells_labelled.txt` e `yelp_labelled.txt`
  (CC BY 4.0).

## Ordem

| Script | O que faz |
|---|---|
| `gerar_amostra.py` | Grava `avaliacoes-pt.json` e `avaliacoes-en.json` em `site/aulas/nlp-intro/assets/`. Critérios e semente estão no topo do arquivo. Com `--conferir`, só compara com os arquivos publicados. |
| `build_assets.py` | Grava `rslp.json` e `stopwords-*.json` e gera `esperado.json` (radicais, colunas e acerto em cada sorteio), que o `harness.py` usa. |
| `v12_final.py pt\|en` | Imprime os números dos Revelar: colunas por etapa, lista à mão, presença por classe, tabela das 20 divisões e frases. Saídas em `saida-v12-*.txt`. |
| `v21_revelar_en.py`, `v22_revelar_pt.py` | Uma linha por afirmação dos Revelar (en e pt), com o valor medido e se bate com o texto da página; termina em "TUDO BATE" ou na lista do que não bate. Saídas em `saida-v21-en.txt` e `saida-v22-pt.txt`. |
| `v14_bloco_python.py`, `v14_bloco_python_en.py` | As duas caixas do bloco 9, fora do navegador. |
| `harness.py pt\|en` | Com `python -m http.server --directory ../../site 8000` rodando, compara o JS da página com o `esperado.json`: radicais, colunas e acerto em cada sorteio. |
| `widgets.py pt\|en`, `nav.py`, `pytest_page.py pt\|en` | Página local: widgets e screenshots, navegação, bloco 9. |
| `gating.py` | Bloco em que cada termo técnico aparece pela primeira vez, nas duas línguas. |
| `prod.py`, `prod2.py` | Site publicado: carga, largura em 390 px, bloco 9 em sessão limpa e quiz. Saída em `saida-prod2.txt`. |
| `filtros.py`, `comum.py` | Filtro de conteúdo e funções comuns (tokenizador, stopwords, stemmers). |

## Exploração (histórico)

`v01` a `v11` e `v15` a `v20` são as rodadas da pesquisa e do roteiro. Vários usam a amostra
de exploração (1000 por classe, sem filtro) e não reproduzem os números finais. Ficam como
registro de onde saíram as decisões e os punches vetados. O mais importante deles é o
`v13_robustez.py`, o teste com 10 amostras que derrubou dois punches.
