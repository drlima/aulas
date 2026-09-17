from comum import *
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from collections import defaultdict
W="não produto dentro atrasou atrasado avaliar hoje top entrega prazo ainda recebi posso esperei maravilha nada nunca".split()
FR=[("não gostei","NEG"),("não recomendo","NEG"),("não é ruim","POS"),("a entrega atrasou","NEG"),("encontrei uma barata dentro da caixa","NEG"),("que maravilha, esperei dois meses pela entrega","NEG"),("não posso avaliar","NEG"),("chegou antes do prazo","POS"),("ainda não chegou","NEG"),("nada bom","NEG"),("nunca mais compro","NEG"),("não tenho do que reclamar","POS"),("sem defeito nenhum","POS"),("demorou mas chegou","POS")]
for n in [1000,2000]:
    pres=defaultdict(list); ver=defaultdict(list)
    for sd in range(10):
        df=corpus("pt",n_por_classe=n,notas=([1,2],[4,5]),seed=sd); y=df.y.values
        for nome,kw in [("base",{}),("stop",dict(stop=True)),("stem",dict(stem=True))]:
            docs=[prepara(t,"pt",**kw) for t in df.texto]
            if nome=="base":
                S=[set(d) for d in docs]
                for w in W: pres[w].append((sum(1 for s,yy in zip(S,y) if w in s and yy==1), sum(1 for s,yy in zip(S,y) if w in s and yy==0)))
            cv=CountVectorizer(analyzer=lambda d:d,binary=True); X=cv.fit_transform(docs); m=MultinomialNB().fit(X,y)
            wv=m.feature_log_prob_[1]-m.feature_log_prob_[0]; voc=cv.vocabulary_
            for f,_ in FR:
                s=sum(wv[voc[t]] for t in set(prepara(f,"pt",**kw)) if t in voc); ver[(f,nome)].append("P" if s>0 else "N")
    print(f"=== n={n}/classe")
    for w in W: print(f"  {w:10s}", pres[w])
    for f,humano in FR: print(f"  {f!r:52s} humano {humano} | " + " | ".join(f"{nome}: {''.join(ver[(f,nome)])}" for nome in ["base","stop","stem"]))
