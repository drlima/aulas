from comum import *
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
import sys
lang = sys.argv[1]; notas = eval(sys.argv[2]) if len(sys.argv)>2 else (1,5)
df = corpus(lang, notas=notas)
y = df.y.values
def accs(kw, seeds=range(20)):
    docs = [prepara(t, lang, **kw) for t in df.texto]; out=[]
    for s in seeds:
        tr, te = train_test_split(range(len(docs)), test_size=0.25, random_state=s, stratify=y)
        cv = CountVectorizer(analyzer=lambda d: d, binary=True)
        Xtr = cv.fit_transform([docs[i] for i in tr]); Xte = cv.transform([docs[i] for i in te])
        out.append(MultinomialNB().fit(Xtr,y[tr]).score(Xte,y[te]))
    return np.array(out)
A = {k: accs(kw) for k,kw in [("split",dict(split=True)),("tok",dict()),("stop",dict(stop=True)),("stopneg",dict(stop=True,stop_keepneg=True)),("stem",dict(stem=True))]}
print(lang, notas, "NB tok media", A["tok"].mean().round(3))
for a,b in [("tok","split"),("stop","tok"),("stopneg","stop"),("stem","tok")]:
    d = A[a]-A[b]; print(f"{a}-{b}: media {d.mean():+.3f}  melhor em {(d>0).sum()}/20, pior em {(d<0).sum()}/20")
# Zipf / esparsidade
toks = [prepara(t, lang) for t in df.texto]
c = Counter(w for d in toks for w in d); N = sum(c.values())
print("tokens", N, "tipos", len(c), "hapax", sum(1 for v in c.values() if v==1), f"({sum(1 for v in c.values() if v==1)/len(c):.0%} do vocab)")
top = c.most_common(20); print("top20", top, f"cobrem {sum(v for _,v in top)/N:.0%} dos tokens")
print(f"top10 cobrem {sum(v for _,v in c.most_common(10))/N:.0%}")
sw = SW[lang]; print(f"stopwords: {sum(v for w,v in c.items() if w in sw)/N:.0%} dos tokens, {sum(1 for w in c if w in sw)} tipos")
media_dist = np.mean([len(set(d)) for d in toks]); print(f"palavras distintas por review {media_dist:.1f} de {len(c)} colunas -> {1-media_dist/len(c):.2%} zeros")
# lista a priori (escrita antes de ver pesos)
L = {"pt": (["ótimo","ótima","bom","boa","excelente","recomendo","gostei","adorei","perfeito","lindo","maravilhoso","rápido","rápida"],
            ["péssimo","péssima","ruim","horrível","defeito","quebrado","quebrou","demorou","problema","errado","devolver","decepcionado"]),
     "en": (["good","great","excellent","love","recommend","perfect","nice","best","amazing","happy","awesome","delicious"],
            ["bad","terrible","worst","poor","hate","broken","awful","disappointed","waste","horrible","disgusting","slow"])}[lang]
p,n = set(L[0]), set(L[1]); cert=emp=0; errs=0
for d,yy in zip(toks,y):
    s = sum(w in p for w in d) - sum(w in n for w in d)
    if s==0: emp+=1
    elif (s>0)==(yy==1): cert+=1
    else: errs+=1
print(f"lista a mao: certas {cert/len(y):.1%}, empates (sem palavra da lista ou saldo 0) {emp/len(y):.1%}, erradas {errs/len(y):.1%}; chutando positivo nos empates: {(cert+sum(1 for d,yy in zip(toks,y) if (sum(w in p for w in d)-sum(w in n for w in d))==0 and yy==1))/len(y):.1%}")
