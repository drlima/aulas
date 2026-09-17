# Mede, contra o JSON publicado da versao en, cada numero dos Revelar da en.
# Cada linha: bloco | afirmacao | valor na pagina | valor medido | bate?
# Uso: ./env.sh v21_revelar_en.py
from comum import *
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import json, pathlib

PAG = pathlib.Path("../../site/aulas/nlp-intro/en/index.html").read_text(encoding="utf-8")
D = json.load(open("../../site/aulas/nlp-intro/assets/avaliacoes-en.json", encoding="utf-8"))
T, Y, DIV = D["texto"], np.array(D["rotulo"]), D["divisoes"]
N = len(T)
ruins = []
def out(bloco, afirm, pagina, medido, ok, trecho=None):
    # trecho: texto que tem de estar na pagina publicada, para a linha valer
    if trecho is not None and trecho not in PAG:
        ok = False; medido = f"{medido} [trecho ausente da pagina: {trecho!r}]"
    if not ok: ruins.append(afirm)
    print(f"{bloco}\t{afirm}\t{pagina}\t{medido}\t{'sim' if ok else 'NAO'}")

def lev(a, b):
    d = list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        p, d[0] = d[0], i
        for j in range(1, len(b) + 1):
            t = d[j]; d[j] = min(d[j] + 1, d[j - 1] + 1, p + (a[i - 1] != b[j - 1])); p = t
    return d[len(b)]
pct = lambda x, casas=0: f"{100*x:.{casas}f}%"

# conferencia: o JSON publicado e o mesmo que sai do UCI cru
reg = corpus("en")
out("0", "JSON publicado = regenerado do UCI cru", "-", "igual", reg.texto.tolist() == T and reg.y.tolist() == Y.tolist())
out("0", "avaliacoes / pos / neg", "1,984 · 992 · 992", f"{N} · {(Y==1).sum()} · {(Y==0).sum()}", (N, (Y==1).sum(), (Y==0).sum()) == (1984, 992, 992), "1,984")

# bloco 1 (o medidor e calculado ao vivo; o Revelar cita os tres)
a, b = "fast delivery but it arrived broken", "it arrived broken but fast delivery"
m = (lev("bad", "not bad"), lev("great", "excellent"), lev(a, b))
out("1", "letras: bad/not bad · great/excellent · metades", "4 · 7 · 26", " · ".join(map(str, m)), m == (4, 7, 26), "Four letters flip")

# bloco 2
L = (["good","great","excellent","love","recommend","perfect","nice","best","amazing","happy","awesome","delicious"],
     ["bad","terrible","worst","poor","hate","broken","awful","disappointed","waste","horrible","disgusting","slow"])
toks = [prepara(t, "en") for t in T]
r = Counter()
for d, yy in zip(toks, Y):
    s = sum(w in L[0] for w in d) - sum(w in L[1] for w in d)
    r["muda" if s == 0 else ("certa" if (s > 0) == (yy == 1) else "errada")] += 1
out("2", "lista: certas", "34%", pct(r["certa"]/N, 1), pct(r["certa"]/N) == "34%", "gets 34% of the reviews right")
out("2", "lista: erradas", "under 4%", pct(r["errada"]/N, 1), r["errada"]/N < 0.04, "gets under 4% wrong")
out("2", "lista: sem resposta", "62%", pct(r["muda"]/N, 1), pct(r["muda"]/N) == "62%", "has no answer for 62%")

# bloco 3 (a pagina separa por espaco)
raw = [t.split() for t in T]
cr = Counter(w for d in raw for w in set(d))
md = np.mean([len(set(d)) for d in raw])
um = sum(1 for v in cr.values() if v == 1) / len(cr)
out("3", "colunas (split por espaco)", "4,977", len(cr), len(cr) == 4977, "4,977 columns")
out("3", "palavras distintas por avaliacao", "10.1", f"{md:.2f}", f"{md:.1f}" == "10.1", "10.1 different words")
out("3", "% da linha que e zero", "99.80%", pct(1 - md/len(cr), 2), pct(1 - md/len(cr), 2) == "99.80%", "99.80% of the row is zero")
out("3", "% das colunas em uma avaliacao so", "67%", pct(um, 1), pct(um) == "67%", "67% of the columns")

# bloco 4
cru = Counter(w for d in raw for w in d)
var = dict(sorted(((w, k) for w, k in cru.items() if re.sub(r"[^\w]", "", w.lower()) == "great"), key=lambda x: -x[1]))
cont = "/".join(str(var.get(w, 0)) for w in ["great","Great","great.","great,","great!","GREAT"])
out("4", "colunas de great", "11", len(var), len(var) == 11, "11 columns")
out("4", "great/Great/great./great,/great!/GREAT", "69/46/22/11/6/1", cont, cont == "69/46/22/11/6/1", "great (69 times), Great (46)")
cb = len(set(w for d in toks for w in d))
ca = len(set(w for t in T for w in prepara(t, "en", acento=True)))
out("4", "colunas minusculas + so letras · queda", "3,187 · -36%", f"{cb} · {pct(cb/len(cr)-1, 1)}", cb == 3187 and pct(cb/len(cr)-1) == "-36%", "from 4,977 to 3,187 columns (−36%)")
out("4", "colunas sem acento", "3,185", ca, ca == 3185, "3,185")

# bloco 5
c = Counter(w for d in toks for w in d); tot = sum(c.values())
sw = sum(v for w, v in c.items() if w in SW["en"]) / tot
ncut = sum(1 for w in c if w in SW["en"])
pos_not = [w for w, _ in c.most_common()].index("not") + 1
S = [set(d) for d in toks]
pn = lambda q: (sum(1 for s, y in zip(S, Y) if q in s and y == 1), sum(1 for s, y in zip(S, Y) if q in s and y == 0))
out("5", "palavras no texto", "21,000", tot, round(tot, -3) == 21000, "Of the 21,000 words")
out("5", "% do texto que e stopword", "49%", pct(sw, 1), pct(sw) == "49%", "cuts 49% of the text")
out("5", "colunas cortadas", "150", ncut, ncut == 150, "only <strong>150 columns</strong>")
out("5", "not esta na lista · posicao", "sim · 11th", f"{'not' in SW['en']} · {pos_not}", "not" in SW["en"] and pos_not == 11, "the eleventh most common word")
out("5", "avaliacoes com not: neg / pos", "189 / 32", f"{pn('not')[1]} / {pn('not')[0]}", pn("not") == (32, 189), "189 of the 992 negative reviews and in 32 of the 992 positive")
for f, alvo in [("i did not like it", "like"), ("i do not recommend it", "recommend")]:
    got = " ".join(prepara(f, "en", stop=True))
    out("5", f"'{f}' sem stopwords", alvo, got, got == alvo, f'"{f}" becomes "{alvo}"')

# bloco 6
st = STEM["en"]
for w1, w2, junta in [("liked","likely",1),("general","generous",1),("news","new",1),("good","better",0),("went","go",0)]:
    same = st(w1) == st(w2)
    out("6", f"{w1} x {w2}", "junta" if junta else "separa", f"{st(w1)} / {st(w2)}", same == bool(junta), f"{w1} {'with' if junta else 'apart from'} {w2}")
cs = len(set(w for t in T for w in prepara(t, "en", stem=True)))
out("6", "colunas com radical · queda", "3,187 -> 2,554 · 20%", f"{cb} -> {cs} · {pct(1-cs/cb, 1)}", cs == 2554 and pct(1-cs/cb) == "20%", "removes 20% of the columns: from 3,187 to 2,554")
for w, rad in [("went","went"),("going","go"),("am","am"),("was","wa"),("were","were"),("better","better"),("loved","love"),("broken","broken"),("phones","phone"),("deliveries","deliveri"),("arrived","arriv")]:
    out("6", f"tabela: radical de {w}", rad, st(w), st(w) == rad, f"<tr><td>{w}</td>")

# bloco 7
cv = CountVectorizer(analyzer=lambda t: prepara(t, "en"), binary=True); X = cv.fit_transform(T)
mod = MultinomialNB().fit(X, Y); w = mod.feature_log_prob_[1] - mod.feature_log_prob_[0]; V = cv.vocabulary_
out("7", "lacunas (colunas)", "3,187", len(V), len(V) == 3187, "fill in 3,187 blanks")
out("7", "peso de money", "-2.47", round(float(w[V["money"]]), 2), round(float(w[V["money"]]), 2) == -2.47, "# -2.47")
out("7", "money: neg / pos", "24 / 1", f"{pn('money')[1]} / {pn('money')[0]}", pn("money") == (1, 24), '"money" appeared in 24 negative reviews and 1 positive one')
com_money = [t for t, s in zip(T, S) if "money" in s]
for frase in ["don't waste your money", "I want my money back"]:
    achou = [t for t in com_money if frase.lower() in t.lower()]
    out("7", f"exemplo de money: '{frase}'", "existe", f"{len(achou)}x", len(achou) > 0, frase)
out("7", "town: avaliacoes, todas positivas", "7, all positive", f"{sum(pn('town'))} ({pn('town')[0]} pos, {pn('town')[1]} neg)", pn("town") == (7, 0), '"town" appeared in 7 reviews, all positive')
out("7", "exemplo de town: 'best tacos in town'", "existe", f"{sum(1 for t in T if 'best tacos in town' in t.lower())}x", any("best tacos in town" in t.lower() for t in T), "best tacos in town")
out("7", "peso de the", "almost nothing", f"{w[V['the']]:+.2f}", abs(w[V["the"]]) < 0.2, "weighs almost nothing")

def acc(stop=False, stem=False, pares=False):
    docs = [prepara(t, "en", stop=stop, stem=stem) for t in T]
    if pares: docs = [d + [x + "_" + z for x, z in zip(d, d[1:])] for d in docs]
    r = []
    for dv in DIV:
        te = [i for i, ch in enumerate(dv) if ch == "1"]; tr = [i for i, ch in enumerate(dv) if ch == "0"]
        v = CountVectorizer(analyzer=lambda d: d, binary=True)
        r.append(MultinomialNB().fit(v.fit_transform([docs[i] for i in tr]), Y[tr]).score(v.transform([docs[i] for i in te]), Y[te]))
    return np.array(r), len(CountVectorizer(analyzer=lambda d: d, binary=True).fit(docs).vocabulary_)
A0, c0 = acc(); As, _ = acc(stop=True); Ar, _ = acc(stem=True); Ap, cp = acc(pares=True)
out("7", "acuracia sem opcoes", "81.3%", pct(A0.mean(), 2), pct(A0.mean(), 1) == "81.3%", "81.3% of the reviews")

# bloco 8
out("8", "acuracia sem stopwords · pior em", "79.3% · 18 of 20", f"{pct(As.mean(), 2)} · {(As<A0).sum()}", pct(As.mean(), 1) == "79.3%" and (As < A0).sum() == 18, "79.3% without the empty words, worse in 18 of 20")
out("8", "acuracia com pares · melhor em", "82.4% · 15 of 20", f"{pct(Ap.mean(), 2)} · {(Ap>A0).sum()}", pct(Ap.mean(), 1) == "82.4%" and (Ap > A0).sum() == 15, "82.4%, better in 15 of 20")
out("8", "tabela com pares", "almost five times", f"{c0} -> {cp} ({cp/c0:.2f}x)", 4.5 <= cp / c0 < 5, "almost five times bigger")
out("8", "peso de not / bad", "-1.7 / -3.4", f"{w[V['not']]:+.2f} / {w[V['bad']]:+.2f}", (round(float(w[V["not"]]), 1), round(float(w[V["bad"]]), 1)) == (-1.7, -3.4), '"not" weighs −1.7 and "bad" weighs −3.4')

def nota(f, **kw):
    cv = CountVectorizer(analyzer=lambda t: prepara(t, "en", **kw), binary=True); X = cv.fit_transform(T)
    m = MultinomialNB().fit(X, Y); ww = m.feature_log_prob_[1] - m.feature_log_prob_[0]; VV = cv.vocabulary_
    return m.class_log_prior_[1] - m.class_log_prior_[0] + sum(ww[VV[t]] for t in set(prepara(f, "en", **kw)) if t in VV)
s = nota("not bad"); out("8", "'not bad' sem opcoes", "negativa", f"{s:+.2f}", s < 0, "not bad")
s = nota("no problems"); out("8", "'no problems' sem opcoes", "negativa (erro)", f"{s:+.2f}", s < 0, "no problems")
s = nota("the delivery was late"); out("8", "'the delivery was late'", "positiva por um fio", f"{s:+.2f}", 0 < s < 0.5, "comes out positive by a hair")
out("8", "late: pos / neg · peso", "1 / 1 · nothing", f"{pn('late')[0]} / {pn('late')[1]} · {w[V['late']]:+.2f}", pn("late") == (1, 1) and abs(w[V["late"]]) < 0.2, "one positive and one negative review")
s0, s1 = nota("oh great, it broke after two days"), nota("oh great, it broke after two days", stem=True)
out("8", "'oh great, it broke…' sem / com radical", "neg -> pos", f"{s0:+.2f} -> {s1:+.2f}", s0 < 0 < s1, "Cutting the endings flips")
s0, s1 = nota("i do not recommend it"), nota("i do not recommend it", stop=True)
out("8", "'i do not recommend it' sem / com corte de stopwords", "neg -> pos", f"{s0:+.2f} -> {s1:+.2f}", s0 < 0 < s1, 'turns "i do not recommend it" positive')
s1 = nota("i did not like it", stop=True)
out("8", "nuance: 'i did not like it' sem stopwords", "(nao afirmado)", f"{s1:+.2f}, continua negativa", s1 < 0)

# bloco 9
m9 = f"{A0.mean():.3f} / {As.mean():.3f} / {Ar.mean():.3f}"
out("9", "Python: letters / no stopwords / stem", "0.813 / 0.793 / 0.819", m9, m9 == "0.813 / 0.793 / 0.819", "0.813, 0.793 and 0.819")

print(f"\n{'TUDO BATE' if not ruins else 'NAO BATE: ' + '; '.join(ruins)}")
