from comum import *
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
d=json.load(open("../../site/aulas/nlp-intro/assets/avaliacoes-pt.json",encoding="utf-8")); T=d["texto"]; Y=np.array(d["rotulo"])
f=lambda t:(lambda x:x+[a+"_"+b for a,b in zip(x,x[1:])])(prepara(t,"pt"))
cv=CountVectorizer(analyzer=f,binary=True); X=cv.fit_transform(T); m=MultinomialNB().fit(X,Y); w=m.feature_log_prob_[1]-m.feature_log_prob_[0]
for s in ["não recomendo","não gostei"]:
    parts={t:round(float(w[cv.vocabulary_[t]]),2) for t in set(f(s)) if t in cv.vocabulary_}; print(s, parts, round(sum(parts.values()),2), len(cv.vocabulary_))
print("lista 1886/4000 =", 1886/4000)
