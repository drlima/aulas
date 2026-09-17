import re, unicodedata, random
import pandas as pd, numpy as np
import nltk
for p in ["rslp","stopwords"]: nltk.download(p, quiet=True)
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer, PorterStemmer

from filtros import FORA_PT, FORA_EN
def corpus(lang, n_por_classe=1000, notas=(1,5), seed=7, maxw=20, minw=3):
    if lang=="pt":
        df = pd.read_csv("dados/b2w-reviews01-main/B2W-Reviews01.csv", low_memory=False, usecols=["overall_rating","review_text"]).dropna()
        df["n"] = df.review_text.str.split().str.len()
        df = df[(df.n>=minw)&(df.n<=maxw)]
        df = df.drop_duplicates("review_text")
        df = df[~df.review_text.str.contains(FORA_PT, case=False, regex=True)]
        neg = df[df.overall_rating.isin([notas[0]] if isinstance(notas[0],int) else notas[0])]
        pos = df[df.overall_rating.isin([notas[1]] if isinstance(notas[1],int) else notas[1])]
        neg = neg.sample(n_por_classe, random_state=seed); pos = pos.sample(n_por_classe, random_state=seed)
        out = pd.concat([neg.assign(y=0), pos.assign(y=1)])[["review_text","y"]].rename(columns={"review_text":"texto"})
    else:
        fs = ["amazon_cells_labelled.txt","yelp_labelled.txt"]
        rows=[]
        for f in fs:
            for line in open(f"dados/sentiment labelled sentences/{f}", encoding="utf-8"):
                line=line.rstrip("\n")
                if "\t" in line:
                    t,y=line.rsplit("\t",1); rows.append((t.strip(),int(y)))
        out = pd.DataFrame(rows, columns=["texto","y"]).drop_duplicates("texto")
        out = out[~out.texto.str.contains(FORA_EN, case=False, regex=True)]
    return out.sample(frac=1, random_state=seed).reset_index(drop=True)

TOK = {"pt": re.compile(r"[^\W\d_]+"), "en": re.compile(r"[^\W\d_]+(?:'[^\W\d_]+)?")}
def tira_acento(s): return "".join(c for c in unicodedata.normalize("NFD", s) if not unicodedata.combining(c))

SW = {"pt": set(stopwords.words("portuguese")), "en": set(stopwords.words("english"))}
NEG = {"pt": {"não","nem","nunca","sem","jamais","nada","nao"}, "en": {"not","no","nor","never","don't","didn't","wasn't","isn't","doesn't","won't","can't","couldn't","aren't","weren't","nothing","t"}}
STEM = {"pt": RSLPStemmer().stem, "en": PorterStemmer(mode=PorterStemmer.ORIGINAL_ALGORITHM).stem}

def prepara(texto, lang, split=False, minusc=True, acento=False, stop=False, stop_keepneg=False, stem=False):
    if split: return texto.split()
    t = texto.lower() if minusc else texto
    toks = TOK[lang].findall(t)
    if stop: toks = [w for w in toks if w not in SW[lang] or (stop_keepneg and w in NEG[lang])]
    if stem: toks = [STEM[lang](w) for w in toks]
    if acento: toks = [tira_acento(w) for w in toks]
    return toks
