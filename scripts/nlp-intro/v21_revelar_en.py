# Mede, contra o JSON publicado da versao en, cada numero dos Revelar da en.
# Uso: ./env.sh v21_revelar_en.py
from comum import *
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import json

D = json.load(open("../../site/aulas/nlp-intro/assets/avaliacoes-en.json", encoding="utf-8"))
T, Y, DIV = D["texto"], np.array(D["rotulo"]), D["divisoes"]
N = len(T)
def out(bloco, afirm, pagina, medido):
    print(f"{bloco}\t{afirm}\t{pagina}\t{medido}")

def lev(a, b):
    d = list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        p, d[0] = d[0], i
        for j in range(1, len(b) + 1):
            t = d[j]; d[j] = min(d[j] + 1, d[j - 1] + 1, p + (a[i - 1] != b[j - 1])); p = t
    return d[len(b)]

# conferencia: o JSON publicado e o mesmo que sai do UCI cru
reg = corpus("en")
out("0", "JSON publicado = regenerado do UCI cru (textos, rotulos)", "-", reg.texto.tolist() == T and reg.y.tolist() == Y.tolist())
out("0", "reviews / pos / neg", "1,984 · 992 · 992", f"{N} · {(Y==1).sum()} · {(Y==0).sum()}")

# bloco 1
out("1", "letras: bad x not bad", "4", lev("bad", "not bad"))
out("1", "letras: great x excellent", "7", lev("great", "excellent"))
a, b = "fast delivery but it arrived broken", "it arrived broken but fast delivery"
out("1", "letras: frase x metades trocadas", "26", lev(a, b))

# bloco 2
L = (["good","great","excellent","love","recommend","perfect","nice","best","amazing","happy","awesome","delicious"],
     ["bad","terrible","worst","poor","hate","broken","awful","disappointed","waste","horrible","disgusting","slow"])
toks = [prepara(t, "en") for t in T]
r = Counter()
for d, yy in zip(toks, Y):
    s = sum(w in L[0] for w in d) - sum(w in L[1] for w in d)
    r["muda" if s == 0 else ("certa" if (s > 0) == (yy == 1) else "errada")] += 1
out("2", "lista: certas", "34%", f"{r['certa']/N:.1%} ({r['certa']})")
out("2", "lista: erradas", "under 4%", f"{r['errada']/N:.1%} ({r['errada']})")
out("2", "lista: sem resposta", "62%", f"{r['muda']/N:.1%} ({r['muda']})")

# bloco 3 (a pagina usa split por espaco)
raw = [t.split() for t in T]
cr = Counter(w for d in raw for w in set(d))
out("3", "colunas (split por espaco)", "4,977", len(cr))
md = np.mean([len(set(d)) for d in raw])
out("3", "palavras distintas por avaliacao", "10.1", f"{md:.2f}")
out("3", "% da linha que e zero", "99.80%", f"{1 - md/len(cr):.2%}")
out("3", "% das colunas em uma avaliacao so", "66%", f"{sum(1 for v in cr.values() if v==1)/len(cr):.1%}")

# bloco 4
cru = Counter(w for d in raw for w in d)
var = sorted(((w, k) for w, k in cru.items() if re.sub(r"[^\w]", "", w.lower()) == "great"), key=lambda x: -x[1])
out("4", "colunas de great", "11", len(var))
out("4", "great/Great/great./great,/great!/GREAT", "69/46/22/11/6/1", "/".join(str(dict(var).get(w, 0)) for w in ["great","Great","great.","great,","great!","GREAT"]))
cb = len(set(w for d in toks for w in d))
out("4", "colunas minusculas + so letras", "3,187", cb)
out("4", "queda", "-36%", f"{cb/len(cr)-1:.1%}")
out("4", "colunas sem acento", "3,185", len(set(w for t in T for w in prepara(t, "en", acento=True))))

# bloco 5
c = Counter(w for d in toks for w in d); tot = sum(c.values())
out("5", "palavras no corpus", "21,000", tot)
out("5", "% do texto que e stopword", "49%", f"{sum(v for w,v in c.items() if w in SW['en'])/tot:.1%}")
out("5", "colunas cortadas", "150", sum(1 for w in c if w in SW["en"]))
out("5", "posicao de not", "11th", [w for w, _ in c.most_common()].index("not") + 1)
out("5", "not na lista pronta", "yes", "not" in SW["en"])
S = [set(d) for d in toks]
out("5", "avaliacoes com not: neg / pos", "189 / 32", f"{sum(1 for s,y in zip(S,Y) if 'not' in s and y==0)} / {sum(1 for s,y in zip(S,Y) if 'not' in s and y==1)}")
for f, alvo in [("i did not like it", "like"), ("i do not recommend it", "recommend")]:
    out("5", f"'{f}' sem stopwords", alvo, " ".join(prepara(f, "en", stop=True)))

# bloco 6
st = STEM["en"]
for w1, w2, junta in [("liked","likely",1),("general","generous",1),("news","new",1),("good","better",0),("went","go",0),
                      ("loved","loving",None),("university","universe",None),("arrive","arrival",None)]:
    same = st(w1) == st(w2)
    out("6", f"{w1} x {w2}", {1: "same", 0: "apart", None: "(card, no claim)"}[junta], f"{st(w1)} / {st(w2)} -> {'same' if same else 'apart'}")
for w in ["love","loved","loves","loving"]:
    out("6", f"'{w}' tem coluna", "(four columns)", w in c)
cs = len(set(w for t in T for w in prepara(t, "en", stem=True)))
out("6", "colunas com radical", "3,187 -> 2,554", f"{cb} -> {cs}")
out("6", "queda com radical", "20%", f"{1-cs/cb:.1%}")
for w, rad in [("went","went"),("going","go"),("am","am"),("was","wa"),("were","were"),("better","better"),("loved","love"),("broken","broken"),("phones","phone"),("deliveries","deliveri"),("arrived","arriv")]:
    out("6", f"tabela: radical de {w}", rad, st(w))

# bloco 7 e 8: pesos no corpus inteiro, sem opcoes
def modelo(**kw):
    cv = CountVectorizer(analyzer=lambda t: prepara(t, "en", **kw), binary=True); X = cv.fit_transform(T)
    m = MultinomialNB().fit(X, Y)
    return cv, m, m.feature_log_prob_[1] - m.feature_log_prob_[0], m.class_log_prior_[1] - m.class_log_prior_[0]
cv, m, w, b = modelo()
V = cv.vocabulary_
out("7", "lacunas (colunas)", "3,187", len(V))
out("7", "peso de money", "-2.47", round(float(w[V["money"]]), 2))
pn = lambda q: (sum(1 for s,y in zip(S,Y) if q in s and y==1), sum(1 for s,y in zip(S,Y) if q in s and y==0))
out("7", "money em neg (pos)", "24 negative", f"{pn('money')[1]} ({pn('money')[0]} pos)")
out("7", "money dentro de 'waste of money'", "almost always", f"{sum(1 for t in T if 'waste of money' in t.lower())} de {sum(1 for s in S if 'money' in s)}")
out("7", "town: pos/neg e peso", "positive, from 'best tacos in town'", f"{pn('town')} peso {w[V['town']]:+.2f}; frases: {[t for t,s in zip(T,S) if 'town' in s]}")
out("7", "peso de the", "almost nothing", f"{w[V['the']]:+.2f} (em {sum(1 for s in S if 'the' in s)} avaliacoes)")
for q in ["minutes", "great", "not"]:
    out("7", f"card {q}: pos/neg, peso", "(computed live)", f"{pn(q)} {w[V[q]]:+.2f}")

def acc(stop=False, stem=False, pares=False):
    docs = [prepara(t, "en", stop=stop, stem=stem) for t in T]
    if pares: docs = [d + [x + "_" + z for x, z in zip(d, d[1:])] for d in docs]
    r = []
    for dv in DIV:
        te = [i for i, ch in enumerate(dv) if ch == "1"]; tr = [i for i, ch in enumerate(dv) if ch == "0"]
        v = CountVectorizer(analyzer=lambda d: d, binary=True)
        r.append(MultinomialNB().fit(v.fit_transform([docs[i] for i in tr]), Y[tr]).score(v.transform([docs[i] for i in te]), Y[te]))
    full = CountVectorizer(analyzer=lambda d: d, binary=True).fit(docs)
    return np.array(r), len(full.vocabulary_)
A0, c0 = acc(); As, _ = acc(stop=True); Ar, _ = acc(stem=True); Ap, cp = acc(pares=True)
out("7", "acuracia sem opcoes", "81.3%", f"{A0.mean():.1%}")
out("8", "acuracia sem stopwords", "79.3%", f"{As.mean():.1%}")
out("8", "sem stopwords pior em", "18 of 20", f"pior {(As<A0).sum()} melhor {(As>A0).sum()} empate {(As==A0).sum()}")
out("8", "acuracia com pares", "82.4%", f"{Ap.mean():.1%}")
out("8", "pares melhor em", "15 of 20", f"melhor {(Ap>A0).sum()} pior {(Ap<A0).sum()} empate {(Ap==A0).sum()}")
out("8", "tabela com pares", "almost five times bigger", f"{c0} -> {cp} ({cp/c0:.2f}x)")
out("9", "Python: letters/no stop/stem", "0.813 / 0.793 / 0.819", f"{A0.mean():.3f} / {As.mean():.3f} / {Ar.mean():.3f}")
out("8", "peso de not / bad", "-1.7 / -3.4", f"{w[V['not']]:+.1f} / {w[V['bad']]:+.1f}")

def frase(f, **kw):
    cv, m, w, b = modelo(**kw); V = cv.vocabulary_
    ts = sorted(set(prepara(f, "en", **{k: v for k, v in kw.items()})))
    s = b + sum(w[V[t]] for t in ts if t in V)
    return f"{'POS' if s > 0 else 'NEG'} {s:+.2f}"
for f in ["not bad", "no problems", "no complaints at all", "the delivery was late", "oh great, it broke after two days", "i did not like it", "i do not recommend it"]:
    out("8", f"frase '{f}' sem opcoes / stop / radical", "-", f"{frase(f)} / {frase(f, stop=True)} / {frase(f, stem=True)}")
out("8", "late: pos/neg, peso", "1 / 1, weighs nothing", f"{pn('late')} {w[V['late']]:+.2f}")
