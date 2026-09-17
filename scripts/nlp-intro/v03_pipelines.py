from comum import *
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
PIPES = [
 ("0 split cru", dict(split=True)),
 ("1 tokeniza+minusc", dict()),
 ("2 +sem acento", dict(acento=True)),
 ("3 +stopwords", dict(acento=True, stop=True)),
 ("3b +stopwords mantendo negacao", dict(acento=True, stop=True, stop_keepneg=True)),
 ("4 tokeniza+stem", dict(stem=True)),
 ("5 +acento+stem", dict(acento=True, stem=True)),
 ("6 tudo (acento+stop+stem)", dict(acento=True, stop=True, stem=True)),
]
import sys
lang = sys.argv[1]
df = corpus(lang)
print(lang, len(df), df.y.value_counts().to_dict())
seeds = range(20)
for nome, kw in PIPES:
    docs = [prepara(t, lang, **kw) for t in df.texto]
    res = {"nb":[], "lr":[], "knn":[]}; vs=[]
    for s in seeds:
        tr, te = train_test_split(range(len(docs)), test_size=0.25, random_state=s, stratify=df.y)
        cv = CountVectorizer(analyzer=lambda d: d, binary=True)
        Xtr = cv.fit_transform([docs[i] for i in tr]); Xte = cv.transform([docs[i] for i in te])
        ytr = df.y.values[tr]; yte = df.y.values[te]; vs.append(Xtr.shape[1])
        res["nb"].append(MultinomialNB().fit(Xtr,ytr).score(Xte,yte))
        res["lr"].append(LogisticRegression(max_iter=2000).fit(Xtr,ytr).score(Xte,yte))
        res["knn"].append(KNeighborsClassifier(5, metric="cosine").fit(Xtr,ytr).score(Xte,yte))
    print(f"{nome:34s} vocab {np.mean(vs):6.0f} | " + " ".join(f"{k} {np.mean(v):.3f}±{np.std(v):.3f}" for k,v in res.items()))
