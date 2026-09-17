from comum import *
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
import sys
lang=sys.argv[1]; df = corpus(lang, notas=([1,2],[4,5]), seed=7); y=df.y.values
CFG=[("base: minusc+tokens",{},False),("cru (split)",dict(split=True),False),("+sem acento",dict(acento=True),False),("+stopwords",dict(stop=True),False),("+stopwords mantendo neg",dict(stop=True,stop_keepneg=True),False),("+stem",dict(stem=True),False),("+pares",{},True),("+stem+pares",dict(stem=True),True),("+stop+stem (receita)",dict(stop=True,stem=True,acento=True),False)]
R={}
for nome,kw,p in CFG:
    docs=[prepara(t,lang,**kw) for t in df.texto]
    if p: docs=[d+[a+"_"+b for a,b in zip(d,d[1:])] for d in docs]
    acc=[];voc=[]
    for s in range(20):
        tr,te=train_test_split(np.arange(len(df)),test_size=0.25,random_state=s,stratify=y)
        cv=CountVectorizer(analyzer=lambda d:d,binary=True); Xtr=cv.fit_transform([docs[i] for i in tr]); Xte=cv.transform([docs[i] for i in te])
        acc.append(MultinomialNB().fit(Xtr,y[tr]).score(Xte,y[te])); voc.append(Xtr.shape[1])
    R[nome]=np.array(acc)
    d=R[nome]-R["base: minusc+tokens"]
    print(f"{lang} {nome:26s} colunas {np.mean(voc):6.0f} acc {np.mean(acc):.3f} (min {min(acc):.3f} max {max(acc):.3f}) vs base {d.mean():+.3f} melhor {(d>0).sum()}/20 pior {(d<0).sum()}/20")
