# Gera as amostras da aula nlp-intro a partir dos dados originais:
#   site/aulas/nlp-intro/assets/avaliacoes-pt.json   (B2W-Reviews01, CC BY-NC-SA 4.0)
#   site/aulas/nlp-intro/assets/avaliacoes-en.json   (UCI Sentiment Labelled Sentences, CC BY 4.0)
# Os arquivos originais ficam fora do repositorio, em dados/ (ver README.md).
#
# Uso, de dentro de scripts/nlp-intro:
#   ./env.sh gerar_amostra.py            grava os dois JSON
#   ./env.sh gerar_amostra.py --conferir so compara com os JSON publicados, sem gravar
#
# Mudar qualquer constante abaixo muda todos os numeros dos Revelar das duas paginas.
import json, pathlib, sys
import numpy as np, pandas as pd
from sklearn.model_selection import train_test_split
from filtros import FORA_PT, FORA_EN

AQUI = pathlib.Path(__file__).resolve().parent
DESTINO = AQUI.parent.parent / "site" / "aulas" / "nlp-intro" / "assets"
CSV_B2W = AQUI / "dados" / "b2w-reviews01-main" / "B2W-Reviews01.csv"
PASTA_UCI = AQUI / "dados" / "sentiment labelled sentences"

# ---- criterios pt (B2W) ----
NOTAS_NEGATIVA = [1, 2]        # rotulo 0
NOTAS_POSITIVA = [4, 5]        # rotulo 1; a nota 3 fica de fora
MIN_PALAVRAS, MAX_PALAVRAS = 3, 20   # palavras separadas por espaco, limites inclusos
POR_CLASSE = 2000
SEMENTE = 7                    # sorteio de cada classe e embaralhamento final

# ---- criterios en (UCI) ----
ARQUIVOS_UCI = ["amazon_cells_labelled.txt", "yelp_labelled.txt"]   # o imdb fica de fora

# ---- divisoes treino/teste gravadas no JSON ----
N_DIVISOES = 20                # random_state 0 a 19
FRACAO_TESTE = 0.25            # estratificadas pelo rotulo

FONTE = {"pt": "B2W-Reviews01 (B2W Digital; Real, Oshiro & Mafra, STIL 2019), https://github.com/americanas-tech/b2w-reviews01. Amostra: avaliacoes de 3 a 20 palavras, notas 1-2 (rotulo 0) e 4-5 (rotulo 1), 2000 de cada, sorteio random_state=7, sem palavrao forte nem dados pessoais. Campos mantidos: so o texto e o rotulo.",
         "en": "Sentiment Labelled Sentences (Kotzias et al., KDD 2015), UCI Machine Learning Repository, https://archive.ics.uci.edu/dataset/331/sentiment+labelled+sentences. Amazon + Yelp, sem duplicatas, sem palavrao forte."}
LICENCA = {"pt": "CC BY-NC-SA 4.0 (https://creativecommons.org/licenses/by-nc-sa/4.0/). Esta amostra e distribuida sob a mesma licenca.",
           "en": "CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/)."}


def amostra_pt():
    df = pd.read_csv(CSV_B2W, low_memory=False, usecols=["overall_rating", "review_text"]).dropna()
    n = df.review_text.str.split().str.len()
    df = df[(n >= MIN_PALAVRAS) & (n <= MAX_PALAVRAS)]
    df = df.drop_duplicates("review_text")                                   # fica a primeira ocorrencia
    df = df[~df.review_text.str.contains(FORA_PT, case=False, regex=True)]   # filtro de conteudo antes do sorteio
    neg = df[df.overall_rating.isin(NOTAS_NEGATIVA)].sample(POR_CLASSE, random_state=SEMENTE)
    pos = df[df.overall_rating.isin(NOTAS_POSITIVA)].sample(POR_CLASSE, random_state=SEMENTE)
    out = pd.concat([neg.assign(y=0), pos.assign(y=1)])[["review_text", "y"]].rename(columns={"review_text": "texto"})
    return out.sample(frac=1, random_state=SEMENTE).reset_index(drop=True)


def amostra_en():
    linhas = []
    for arq in ARQUIVOS_UCI:
        for linha in open(PASTA_UCI / arq, encoding="utf-8"):
            linha = linha.rstrip("\n")
            if "\t" in linha:
                texto, y = linha.rsplit("\t", 1)
                linhas.append((texto.strip(), int(y)))
    out = pd.DataFrame(linhas, columns=["texto", "y"]).drop_duplicates("texto")
    out = out[~out.texto.str.contains(FORA_EN, case=False, regex=True)]
    return out.sample(frac=1, random_state=SEMENTE).reset_index(drop=True)


def divisoes(y):
    N = len(y); res = []
    for s in range(N_DIVISOES):
        _, te = train_test_split(np.arange(N), test_size=FRACAO_TESTE, random_state=s, stratify=y)
        m = np.zeros(N, int); m[te] = 1
        res.append("".join(map(str, m)))                                     # "1" = teste
    return res


conferir = "--conferir" in sys.argv
for lang, gerar in [("pt", amostra_pt), ("en", amostra_en)]:
    df = gerar(); y = df.y.values
    dados = {"fonte": FONTE[lang], "licenca": LICENCA[lang], "texto": df.texto.tolist(), "rotulo": y.tolist(), "divisoes": divisoes(y)}
    txt = json.dumps(dados, ensure_ascii=False, separators=(",", ":"))
    arq = DESTINO / f"avaliacoes-{lang}.json"
    if conferir:
        igual = arq.read_text(encoding="utf-8") == txt
        print(f"{lang}: {len(y)} avaliacoes ({(y == 1).sum()} positivas, {(y == 0).sum()} negativas) · identico ao publicado: {igual}")
    else:
        arq.write_text(txt, encoding="utf-8")
        print(f"{lang}: {len(y)} avaliacoes gravadas em {arq}")
