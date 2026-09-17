from comum import *
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
import sys, json
lang=sys.argv[1]; SEED=7
df = corpus(lang, notas=([1,2],[4,5]), seed=SEED); y=df.y.values
tr, te = train_test_split(np.arange(len(df)), test_size=0.25, random_state=SEED, stratify=y)
print(lang, "docs", len(df), "treino", len(tr), "teste", len(te))
def nb(kw, pares=False, idx_tr=tr, idx_te=te):
    docs=[prepara(t, lang, **kw) for t in df.texto]
    if pares: docs=[d+[a+"_"+b for a,b in zip(d,d[1:])] for d in docs]
    cv=CountVectorizer(analyzer=lambda d:d, binary=True); Xtr=cv.fit_transform([docs[i] for i in idx_tr]); Xte=cv.transform([docs[i] for i in idx_te])
    return Xtr.shape[1], MultinomialNB().fit(Xtr,y[idx_tr]).score(Xte,y[idx_te])
CFG=[("cru (split)",dict(split=True),False),("minusc+tokens",{},False),("+sem acento",dict(acento=True),False),("minusc+stop",dict(stop=True),False),("minusc+stop mantendo neg",dict(stop=True,stop_keepneg=True),False),("minusc+stem",dict(stem=True),False),("minusc+pares",{},True),("minusc+stem+pares",dict(stem=True),True)]
for nome,kw,p in CFG:
    v,a=nb(kw,p); print(f"  {nome:28s} colunas(treino) {v:6d} acuracia teste {a:.3f}")
# vocabulario do corpus inteiro por etapa
for nome,kw in [("cru",dict(split=True)),("minusc",{}),("sem acento",dict(acento=True)),("stop",dict(stop=True)),("stem",dict(stem=True))]:
    print("  corpus inteiro colunas", nome, len(set(w for t in df.texto for w in prepara(t,lang,**kw))))
# variantes de otimo / great no cru
alvo = "otimo" if lang=="pt" else "great"
cru = Counter(w for t in df.texto for w in t.split())
var = {w:c for w,c in cru.items() if tira_acento(re.sub(r"[^\w]","",w.lower()))==alvo}
print("  variantes cru de", alvo, len(var), sorted(var.items(), key=lambda x:-x[1]))
# vizinha mais proxima (k-NN por palavras em comum) para frases
FR={"pt":["não gostei do produto","o produto chegou quebrado","gostei muito, chegou antes do prazo"],"en":["i did not like this phone","the phone arrived broken","i really liked it, it arrived early"]}[lang]
for f in FR:
    for nome,kw in [("minusc",{}),("stop",dict(stop=True))]:
        q=set(prepara(f,lang,**kw)); best=sorted(((len(q & set(prepara(t,lang,**kw))), -len(set(prepara(t,lang,**kw))), t, yy) for t,yy in zip(df.texto,y)), reverse=True)[:2]
        print(f"  vizinha [{nome}] {f!r} q={sorted(q)} -> ", [(b[0], b[2], 'pos' if b[3] else 'neg') for b in best])
json.dump({"texto":df.texto.tolist(),"y":y.tolist(),"teste":sorted(te.tolist())}, open(f"corpus-{lang}.json","w",encoding="utf-8"), ensure_ascii=False)
