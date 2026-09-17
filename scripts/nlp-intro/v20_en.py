from comum import *
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
st=STEM["en"]
print({w:st(w) for w in "loved loving liked likely general generous news new university universe good better went go arrive arrival went going was am were better loved broken phones deliveries arrived happy is i".split()})
d=json.load(open("../../site/aulas/nlp-intro/assets/avaliacoes-en.json",encoding="utf-8")); T=d["texto"]; Y=np.array(d["rotulo"])
cv=CountVectorizer(analyzer=lambda t: prepara(t,"en"),binary=True); X=cv.fit_transform(T); m=MultinomialNB().fit(X,Y); w=m.feature_log_prob_[1]-m.feature_log_prob_[0]
for q in ["town","money","the","minutes","great","not","waste","of","late","delivery"]: print(q, round(float(w[cv.vocabulary_[q]]),2))
S=[set(prepara(t,"en")) for t in T]
for q in ["arrived","fast","broken","not","no","very"]:
    c=[t for t,s in zip(T,S) if q in s and len(t.split())>=5]; print(q, len(c), sorted(c,key=len)[:1])
from collections import Counter
c=Counter(x for t in T for x in prepara(t,"en")); print([ (k,i+1) for i,(k,_) in enumerate(c.most_common(30)) if k in ("not","no","very","but")])
