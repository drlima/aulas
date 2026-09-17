# Grava rslp.json e stopwords-*.json em site/aulas/nlp-intro/assets/ e esperado.json (valores para conferir o JS com harness.py).
# As avaliacoes vem de gerar_amostra.py; este script so le o JSON publicado.
from comum import *
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from nltk.stem import RSLPStemmer
import json, itertools, pathlib
DEST = pathlib.Path("../../site/aulas/nlp-intro/assets")
esperado = {}
for lang in ["pt", "en"]:
    base = json.load(open(f"../../site/aulas/nlp-intro/assets/avaliacoes-{lang}.json", encoding="utf-8"))
    T, Y, DIV = base["texto"], np.array(base["rotulo"]), base["divisoes"]
    json.dump(sorted(SW[lang]), open(DEST / f"stopwords-{lang}.json", "w", encoding="utf-8"), ensure_ascii=False)
    E = {}
    toks = [prepara(t, lang) for t in T]
    vocab = sorted(set(w for d in toks for w in d))
    extra = ["gostei","gostaria","barato","barata","casa","casamento","livro","livre","bom","boa","amei","amo","demora","demorou","fui","ir","paisagem","pais","maravilha","maravilhoso","atrasou","atraso",
             "liked","likely","general","generous","university","universe","news","new","is","i","happy","happiness","good","better","went","go","disappoint","disappointed","caresses","ponies","agreed","hopping","relational","electrical","controll","rolls"]
    E["stems"] = {w: STEM[lang](w) for w in sorted(set(vocab + extra))}
    E["cols"] = {"cru": len(set(w for t in T for w in t.split())), "base": len(vocab),
                 "acento": len(set(w for t in T for w in prepara(t, lang, acento=True))),
                 "stop": len(set(w for t in T for w in prepara(t, lang, stop=True))),
                 "stem": len(set(w for t in T for w in prepara(t, lang, stem=True)))}
    acc = {}
    for stop, stem, pares in itertools.product([0, 1], repeat=3):
        docs = [prepara(t, lang, stop=bool(stop), stem=bool(stem)) for t in T]
        if pares: docs = [d + [a + "_" + b for a, b in zip(d, d[1:])] for d in docs]
        notas = []; cols = []
        for dv in DIV:
            te = [i for i, c in enumerate(dv) if c == "1"]; tr = [i for i, c in enumerate(dv) if c == "0"]
            cv = CountVectorizer(analyzer=lambda d: d, binary=True); Xtr = cv.fit_transform([docs[i] for i in tr])
            notas.append(MultinomialNB().fit(Xtr, Y[tr]).score(cv.transform([docs[i] for i in te]), Y[te])); cols.append(Xtr.shape[1])
        acc[f"{stop}{stem}{pares}"] = {"media": round(float(np.mean(notas)), 4), "notas": [round(float(n), 4) for n in notas]}
        cvall = CountVectorizer(analyzer=lambda d: d, binary=True); cvall.fit(docs)
        acc[f"{stop}{stem}{pares}"]["colunas_corpus"] = len(cvall.vocabulary_)
    E["acc"] = acc
    esperado[lang] = E
    print(lang, E["cols"], {k: (v["media"], v["colunas_corpus"]) for k, v in acc.items()})
r = RSLPStemmer()
json.dump(r._model, open(DEST / "rslp.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
json.dump(esperado, open("esperado.json", "w", encoding="utf-8"), ensure_ascii=False)
