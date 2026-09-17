from comum import *
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import sys
lang = sys.argv[1]; notas = ([1,2],[4,5])
df = corpus(lang, notas=notas)
FR = {"pt": ["gostei muito do produto","não gostei do produto","não gostei","o produto não é ruim","não é ruim","não recomendo","recomendo, não tive nenhum problema",
  "chegou rápido mas veio quebrado","veio quebrado mas chegou rápido","que maravilha, esperei dois meses pela entrega","ótimo produto","otimo produto","Ótimo!!!",
  "top demais","a entrega atrasou","encontrei uma barata dentro da caixa","o preço é barato","bom","nada bom","nem um pouco bom","poderia ser melhor","não é ótimo, é bom", "não é bom, é ótimo"],
  "en": ["i liked this phone","i did not like this phone","not bad at all","not bad","i do not recommend it","great phone, no problems",
  "fast delivery but it arrived broken","it arrived broken but fast delivery","oh great, it broke after two days","great product","Great!!!",
  "this is likely to break","the food was cold","nothing good","could be better","it is not great, it is good","it is not good, it is great","awesome sauce"]}[lang]
def treina(kw, ngram=False):
    docs = [prepara(t, lang, **kw) for t in df.texto]
    if ngram: docs = [d + [a+"_"+b for a,b in zip(d,d[1:])] for d in docs]
    cv = CountVectorizer(analyzer=lambda d: d, binary=True); X = cv.fit_transform(docs)
    nb = MultinomialNB().fit(X, df.y.values)
    w = nb.feature_log_prob_[1]-nb.feature_log_prob_[0]; voc = cv.vocabulary_
    return voc, w, nb.class_log_prior_[1]-nb.class_log_prior_[0]
for nome, kw, ng in [("tok",{},False),("stem",dict(stem=True),False),("stop",dict(stop=True),False),("tok+pares",{},True)]:
    voc, w, b = treina(kw, ng)
    print(f"== {nome} | vocab {len(voc)} | vies {b:+.2f}")
    if nome=="tok":
        ks = sorted(voc, key=lambda k: w[voc[k]])
        print(" mais negativas:", [(k, round(w[voc[k]],2)) for k in ks[:15]])
        print(" mais positivas:", [(k, round(w[voc[k]],2)) for k in ks[-15:]])
        for q in (["não","nao","barata","barato","ruim","bom","muito","produto","o","mas","nada","nem","melhor"] if lang=="pt" else ["not","no","bad","good","very","the","but","nothing","better","likely","like"]):
            print("  peso", q, round(w[voc[q]],2) if q in voc else "fora do vocab")
    if nome=="stem":
        for q in (["barat","não"] if lang=="pt" else ["like","not"]): print("  peso stem", q, round(w[voc[q]],2) if q in voc else "fora")
    for f in FR:
        toks = sorted(set(prepara(f, lang, **kw)))
        if ng:
            d = prepara(f, lang, **kw); toks = sorted(set(d + [a+"_"+b for a,b in zip(d,d[1:])]))
        parts = [(t, round(w[voc[t]],2)) if t in voc else (t,"?") for t in toks]
        s = b + sum(p for _,p in parts if p!="?")
        print(f"  {'POS' if s>0 else 'NEG'} {s:+.2f}  {f!r}  {parts}")
