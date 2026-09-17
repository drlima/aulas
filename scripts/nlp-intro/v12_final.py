# Todos os numeros da pagina, na configuracao final. Uso: ./env.sh v12_final.py pt|en
from comum import *
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
import sys, json
lang=sys.argv[1]; df = corpus(lang, n_por_classe=2000, notas=([1,2],[4,5]), seed=7); y=df.y.values; N=len(df)
print(f"### {lang}: {N} avaliacoes, pos {(y==1).sum()} neg {(y==0).sum()}, {df.texto.str.len().sum()/1024:.0f} KB")
# 1. vocabulario por etapa (corpus inteiro)
for nome,kw in [("cru",dict(split=True)),("minusc",{}),("acento",dict(acento=True)),("stop",dict(stop=True)),("stem",dict(stem=True))]:
    print(f"colunas corpus inteiro [{nome}]", len(set(w for t in df.texto for w in prepara(t,lang,**kw))))
toks=[prepara(t,lang) for t in df.texto]; c=Counter(w for d in toks for w in d); T=sum(c.values())
h=sum(1 for v in c.values() if v==1)
print(f"palavras {T}, colunas {len(c)}, uma vez so {h} ({h/len(c):.0%}), top10 {[w for w,_ in c.most_common(10)]} cobrem {sum(v for _,v in c.most_common(10))/T:.0%}")
print(f"stopwords: {sum(v for w,v in c.items() if w in SW[lang])/T:.0%} do texto, {sum(1 for w in c if w in SW[lang])} colunas")
md=np.mean([len(set(d)) for d in toks]); print(f"distintas por avaliacao {md:.1f} -> zeros {1-md/len(c):.2%}")
cru=Counter(w for t in df.texto for w in t.split()); alvo={"pt":"otimo","en":"great"}[lang]
var=sorted(((w,k) for w,k in cru.items() if tira_acento(re.sub(r"[^\w]","",w.lower()))==alvo), key=lambda x:-x[1]); print("variantes cruas", alvo, len(var), var)
# 2. lista a mao
L={"pt":(["ótimo","ótima","bom","boa","excelente","recomendo","gostei","adorei","perfeito","lindo","maravilhoso","rápido","rápida"],["péssimo","péssima","ruim","horrível","defeito","quebrado","quebrou","demorou","problema","errado","devolver","decepcionado"]),
   "en":(["good","great","excellent","love","recommend","perfect","nice","best","amazing","happy","awesome","delicious"],["bad","terrible","worst","poor","hate","broken","awful","disappointed","waste","horrible","disgusting","slow"])}[lang]
p,n=set(L[0]),set(L[1]); r=Counter()
for d,yy in zip(toks,y):
    s=sum(w in p for w in d)-sum(w in n for w in d); r["muda" if s==0 else ("certa" if (s>0)==(yy==1) else "errada")]+=1
print("lista a mao:", {k:f"{v/N:.1%} ({v})" for k,v in r.items()})
# 3. presenca por classe
W={"pt":"não,produto,dentro,atrasou,atrasado,atraso,avaliar,posso,dinheiro,hoje,ainda,top,entrega,prazo,ótimo,otimo,ruim,bom,nem,sem,defeito,quebrado,gostei,recomendo,maravilha,barato,barata".split(","),"en":"not,the,product,town,spot,money,minutes,disappoint,great,bad,good,like,liked,recommend,late,phone".split(",")}[lang]
S=[set(d) for d in toks]
print("presenca pos/neg:", {w:(sum(1 for s,yy in zip(S,y) if w in s and yy==1), sum(1 for s,yy in zip(S,y) if w in s and yy==0)) for w in W})
# 4. tabela de 20 divisoes
DIV=[]
for s in range(20):
    tr,te=train_test_split(np.arange(N),test_size=0.25,random_state=s,stratify=y); m=np.zeros(N,int); m[te]=1; DIV.append("".join(map(str,m)))
CFG=[("base",{},False),("cru",dict(split=True),False),("acento",dict(acento=True),False),("stop",dict(stop=True),False),("stopneg",dict(stop=True,stop_keepneg=True),False),("stem",dict(stem=True),False),("pares",{},True),("stem+pares",dict(stem=True),True),("acento+stop+stem",dict(acento=True,stop=True,stem=True),False)]
R={}
for nome,kw,pp in CFG:
    docs=[prepara(t,lang,**kw) for t in df.texto]
    if pp: docs=[d+[a+"_"+b for a,b in zip(d,d[1:])] for d in docs]
    acc=[];voc=[]
    for dv in DIV:
        te=[i for i,ch in enumerate(dv) if ch=="1"]; tr=[i for i,ch in enumerate(dv) if ch=="0"]
        cv=CountVectorizer(analyzer=lambda d:d,binary=True); Xtr=cv.fit_transform([docs[i] for i in tr])
        acc.append(MultinomialNB().fit(Xtr,y[tr]).score(cv.transform([docs[i] for i in te]),y[te])); voc.append(Xtr.shape[1])
    R[nome]=np.array(acc); d=R[nome]-R["base"]
    print(f"20 divisoes [{nome:16s}] colunas treino {np.mean(voc):6.0f} acuracia {np.mean(acc):.3f} vs base {100*d.mean():+.1f} pt, melhor {(d>0).sum()} pior {(d<0).sum()} empate {(d==0).sum()}")
# 5. frases (treino no corpus inteiro)
FR={"pt":["não gostei","não recomendo","não é ruim","sem defeito nenhum","não tenho do que reclamar","a entrega atrasou","ainda não chegou","que maravilha, esperei dois meses pela entrega","top demais","chegou rápido mas veio quebrado","veio quebrado mas chegou rápido","não é bom, é ótimo","não é ótimo, é bom","nada bom","gostei muito do produto","não posso avaliar"],
    "en":["i did not like it","i do not recommend it","not bad","not bad at all","it did not disappoint","the delivery was late","oh great, it broke after two days","fast delivery but it arrived broken","it arrived broken but fast delivery","it is not good, it is great","it is not great, it is good","nothing good","i really liked this phone","best in town","waste of money","no complaints at all","nothing to complain about","no problems","still waiting for it","i can not rate it yet"]}[lang]
for nome,kw,pp in [("base",{},False),("stop",dict(stop=True),False),("stem",dict(stem=True),False),("pares",{},True)]:
    docs=[prepara(t,lang,**kw) for t in df.texto]
    f2=lambda d: d+[a+"_"+b for a,b in zip(d,d[1:])] if pp else d
    cv=CountVectorizer(analyzer=lambda d:d,binary=True); X=cv.fit_transform([f2(d) for d in docs]); m=MultinomialNB().fit(X,y)
    w=m.feature_log_prob_[1]-m.feature_log_prob_[0]; voc=cv.vocabulary_; b=m.class_log_prior_[1]-m.class_log_prior_[0]
    print(f"frases [{nome}] colunas {len(voc)} vies {b:+.3f}")
    for f in FR:
        ts=sorted(set(f2(prepara(f,lang,**kw)))); parts=[(t,round(float(w[voc[t]]),2)) if t in voc else (t,None) for t in ts]
        s=b+sum(v for _,v in parts if v is not None)
        print(f"   {'POS' if s>0 else 'NEG'} {s:+.2f} {f!r} {parts}")
