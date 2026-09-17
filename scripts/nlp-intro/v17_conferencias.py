from comum import *
r=STEM["pt"]; print({w:r(w) for w in ["maravilha","maravilhoso","maravilhosa","maravilhosos","atrasou","atraso","atrasado","atrasada","atrasar"]})
df=corpus("pt",n_por_classe=2000,notas=([1,2],[4,5]),seed=7); y=df.y.values
S=[set(prepara(t,"pt")) for t in df.texto]
for w in ["maravilhoso","maravilhosa","atraso","atrasado","atrasada"]:
    print(w, sum(1 for s,yy in zip(S,y) if w in s and yy==1), sum(1 for s,yy in zip(S,y) if w in s and yy==0))
from v15_distancias import lev
print("great x Great!!!", lev("great","Great!!!"), "de", 8)
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
import json
for lang in ["pt","en"]:
    d=json.load(open(f"../../site/aulas/nlp-intro/assets/avaliacoes-{lang}.json",encoding="utf-8")); T=d["texto"]; Y=np.array(d["rotulo"])
    docs=[prepara(t,lang) for t in T]; a={"nb":[],"lr":[],"knn5":[]}
    for dv in d["divisoes"]:
        te=[i for i,c in enumerate(dv) if c=="1"]; tr=[i for i,c in enumerate(dv) if c=="0"]
        cv=CountVectorizer(analyzer=lambda x:x,binary=True); Xtr=cv.fit_transform([docs[i] for i in tr]); Xte=cv.transform([docs[i] for i in te])
        a["nb"].append(MultinomialNB().fit(Xtr,Y[tr]).score(Xte,Y[te])); a["lr"].append(LogisticRegression(max_iter=2000).fit(Xtr,Y[tr]).score(Xte,Y[te])); a["knn5"].append(KNeighborsClassifier(5,metric="cosine").fit(Xtr,Y[tr]).score(Xte,Y[te]))
    print(lang, {k:round(float(np.mean(v)),3) for k,v in a.items()})
