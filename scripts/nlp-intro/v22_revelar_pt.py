# Mede, contra o JSON publicado da versao pt, cada numero dos Revelar da pt.
# Cada linha: bloco | afirmacao | valor na pagina | valor medido | bate?
# Uso: ./env.sh v22_revelar_pt.py
from comum import *
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import json, pathlib

PAG = pathlib.Path("../../site/aulas/nlp-intro/index.html").read_text(encoding="utf-8")
D = json.load(open("../../site/aulas/nlp-intro/assets/avaliacoes-pt.json", encoding="utf-8"))
T, Y, DIV = D["texto"], np.array(D["rotulo"]), D["divisoes"]
N = len(T)
ruins = []
def out(bloco, afirm, pagina, medido, ok, trecho=None):
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
pct = lambda x, casas=0: f"{100*x:.{casas}f}%".replace(".", ",")

out("0", "avaliacoes / pos / neg", "4000 · 2000 · 2000", f"{N} · {(Y==1).sum()} · {(Y==0).sum()}", (N, (Y==1).sum()) == (4000, 2000), "Temos 4000 avaliações")

# bloco 1
a, b = "chegou rápido mas veio quebrado", "veio quebrado mas chegou rápido"
m = (lev("é ruim", "não é ruim"), lev("ótimo", "excelente"), lev(a, b))
out("1", "letras: é ruim/não é ruim · ótimo/excelente · metades", "4 · 9 · 20", " · ".join(map(str, m)), m == (4, 9, 20), "trocar a ordem das metades mexe em vinte letras")

# bloco 2
L = (["ótimo","ótima","bom","boa","excelente","recomendo","gostei","adorei","perfeito","lindo","maravilhoso","rápido","rápida"],
     ["péssimo","péssima","ruim","horrível","defeito","quebrado","quebrou","demorou","problema","errado","devolver","decepcionado"])
toks = [prepara(t, "pt") for t in T]
r = Counter()
for d, yy in zip(toks, Y):
    s = sum(w in L[0] for w in d) - sum(w in L[1] for w in d)
    r["muda" if s == 0 else ("certa" if (s > 0) == (yy == 1) else "errada")] += 1
res = " / ".join(pct(r[k]/N, 2) for k in ["certa", "errada", "muda"])
out("2", "lista: certas / erradas / sem resposta", "47% / 6% / 47%", res, [pct(r[k]/N) for k in ["certa", "errada", "muda"]] == ["47%", "6%", "47%"], "acerta 47% das avaliações, erra 6%")

# bloco 3
raw = [t.split() for t in T]
cr = Counter(w for d in raw for w in set(d))
md = np.mean([len(set(d)) for d in raw]); um = sum(1 for v in cr.values() if v == 1) / len(cr)
out("3", "colunas (split por espaco)", "9801", len(cr), len(cr) == 9801, "9801 colunas")
out("3", "palavras distintas por avaliacao · % de zeros", "12,6 · 99,87%", f"{md:.2f} · {pct(1-md/len(cr), 3)}", f"{md:.1f}" == "12.6" and pct(1-md/len(cr), 2) == "99,87%", "99,87% da linha é zero")
out("3", "% das colunas em uma avaliacao so", "67%", pct(um, 1), pct(um) == "67%", "E 67% das colunas")

# bloco 4
cru = Counter(w for d in raw for w in d)
var = {w: k for w, k in cru.items() if tira_acento(re.sub(r"[^\w]", "", w.lower())) == "otimo"}
cont = "/".join(str(var.get(w, 0)) for w in ["ótimo", "Ótimo", "otimo", "ótimo.", "Otimo", "ótimo,", "ÓTIMO"])
cb = len(set(w for d in toks for w in d)); ca = len(set(w for t in T for w in prepara(t, "pt", acento=True)))
out("4", "colunas de ótimo", "19", len(var), len(var) == 19, "São <strong>19 colunas</strong>")
out("4", "ótimo/Ótimo/otimo/ótimo./Otimo/ótimo,/ÓTIMO", "122/101/28/15/13/11/7", cont, cont == "122/101/28/15/13/11/7", "ótimo (122 vezes), Ótimo (101)")
out("4", "minusculas + so letras · queda", "5357 · −45%", f"{cb} · {pct(cb/len(cr)-1, 1)}", cb == 5357 and pct(cb/len(cr)-1) == "-45%", "de 9801 para 5357 colunas (−45%)")
out("4", "sem acento", "5145", ca, ca == 5145, "para 5145")

# bloco 5
c = Counter(w for d in toks for w in d); tot = sum(c.values())
sw = sum(v for w, v in c.items() if w in SW["pt"]) / tot; ncut = sum(1 for w in c if w in SW["pt"])
pos_nao = [w for w, _ in c.most_common()].index("não") + 1
S = [set(d) for d in toks]
pn = lambda q: (sum(1 for s, y in zip(S, Y) if q in s and y == 1), sum(1 for s, y in zip(S, Y) if q in s and y == 0))
out("5", "palavras no texto · % stopwords", "52 mil · 39%", f"{tot} · {pct(sw, 1)}", round(tot, -3) == 52000 and pct(sw) == "39%", "Das 52 mil palavras destas avaliações, 39%")
out("5", "colunas cortadas", "131", ncut, ncut == 131, "só <strong>131 colunas</strong> das 5357")
out("5", "não na lista · posicao", "sim · 4ª", f"{'não' in SW['pt']} · {pos_nao}", "não" in SW["pt"] and pos_nao == 4, "a quarta palavra mais comum")
out("5", "avaliacoes com não: neg / pos", "1118 / 136", f"{pn('não')[1]} / {pn('não')[0]}", pn("não") == (136, 1118), "aparece em 1118 das 2000 negativas e em 136 das 2000 positivas")
for f, alvo in [("não gostei", "gostei"), ("não recomendo", "recomendo")]:
    got = " ".join(prepara(f, "pt", stop=True))
    out("5", f"'{f}' sem stopwords", alvo, got, got == alvo, f'"{f}" vira "{alvo}"')

# bloco 6
st = STEM["pt"]
for w1, w2, junta in [("barato","barata",1),("casa","casamento",1),("bom","boa",0),("amei","amo",0)]:
    out("6", f"{w1} x {w2}", "junta" if junta else "separa", f"{st(w1)} / {st(w2)}", (st(w1) == st(w2)) == bool(junta), f"{w1} {'com' if junta else 'de'} {w2}")
cs = len(set(w for t in T for w in prepara(t, "pt", stem=True)))
out("6", "colunas com radical · queda", "5357 -> 3195 · 40%", f"{cb} -> {cs} · {pct(1-cs/cb, 1)}", cs == 3195 and pct(1-cs/cb) == "40%", "tira 40% das colunas: de 5357 para 3195")
for w, rad in [("fui","fui"),("vou","vou"),("iria","iri"),("foi","foi"),("era","era"),("boa","boa"),("Amei","ame"),("amo","amo"),("amava","am"),("quebrado","quebr"),("entregas","entreg")]:
    out("6", f"tabela: radical de {w}", rad, st(w.lower()), st(w.lower()) == rad, f"<tr><td>{w}</td>")

# bloco 7
cv = CountVectorizer(analyzer=lambda t: prepara(t, "pt"), binary=True); X = cv.fit_transform(T)
mod = MultinomialNB().fit(X, Y); w = mod.feature_log_prob_[1] - mod.feature_log_prob_[0]; V = cv.vocabulary_
out("7", "espacos (colunas)", "5357", len(V), len(V) == 5357, "preencher 5357 espaços")
out("7", "peso de avaliar", "-3.7", f"{w[V['avaliar']]:+.2f}", round(float(w[V["avaliar"]]), 1) == -3.7, "# -3.7")
out("7", "avaliar em negativas", "131", f"{pn('avaliar')[1]} (e {pn('avaliar')[0]} positivas)", pn("avaliar")[1] == 131, '"avaliar" apareceu em 131 negativas')
SEM_RECEBER = re.compile(r"n[ãa]o (me )?(recebi|chegou|cheg|foi entregue|entreg|veio|recebemos|recebeu|receberei|o receberei)|ainda n[ãa]o|\bn recebi|nem (ao menos )?(recebi|chegou|vi)|aguard|sem receber|receber o produto|quando (o produto )?cheg|quando eu receber|produto chegar|sido entregue|at[ée] agora nada|n[ãa]o chega", re.I)
neg_av = [t for t, s, y in zip(T, S, Y) if "avaliar" in s and y == 0]
k = sum(1 for t in neg_av if SEM_RECEBER.search(t))
out("7", "avaliar: quase sempre sem ter recebido", "quase sempre", f"{k} de {len(neg_av)} ({pct(k/len(neg_av))}, contagem conservadora por regex)", k / len(neg_av) >= 0.75, "quase sempre de quem ainda não tinha recebido o produto")
pos_de = [t for t, s, y in zip(T, S, Y) if "dentro" in s and y == 1]
k1 = sum(1 for t in pos_de if "dentro do prazo" in t.lower()); k2 = sum(1 for t in pos_de if "chegou dentro do prazo" in t.lower())
out("7", "dentro: veio de 'chegou dentro do prazo'", "origem", f"dentro {pn('dentro')[0]} pos / {pn('dentro')[1]} neg; 'dentro do prazo' em {k1} das {len(pos_de)} positivas; 'chegou dentro do prazo' literal em {k2}", k2 / len(pos_de) >= 0.5, '"dentro" veio de "chegou dentro do prazo"')
out("7", "produto: em tudo, peso quase zero", "quase zero", f"{pn('produto')} peso {w[V['produto']]:+.2f}", abs(w[V["produto"]]) < 0.2, '"produto" está em tudo e pesa quase zero')

def acc(stop=False, stem=False, pares=False):
    docs = [prepara(t, "pt", stop=stop, stem=stem) for t in T]
    if pares: docs = [d + [x + "_" + z for x, z in zip(d, d[1:])] for d in docs]
    r = []
    for dv in DIV:
        te = [i for i, ch in enumerate(dv) if ch == "1"]; tr = [i for i, ch in enumerate(dv) if ch == "0"]
        v = CountVectorizer(analyzer=lambda d: d, binary=True)
        r.append(MultinomialNB().fit(v.fit_transform([docs[i] for i in tr]), Y[tr]).score(v.transform([docs[i] for i in te]), Y[te]))
    return np.array(r), len(CountVectorizer(analyzer=lambda d: d, binary=True).fit(docs).vocabulary_)
A0, c0 = acc(); As, _ = acc(stop=True); Ar, _ = acc(stem=True); Ap, cp = acc(pares=True)
out("7", "acuracia sem opcoes", "91,7%", pct(A0.mean(), 2), pct(A0.mean(), 1) == "91,7%", "acerta 91,7% das avaliações")

# bloco 8
out("8", "sem stopwords · pior em", "91,2% · 16 de 20", f"{pct(As.mean(), 2)} · {(As<A0).sum()}", pct(As.mean(), 1) == "91,2%" and (As < A0).sum() == 16, "91,2% sem as palavras vazias, pior em 16 de 20")
out("8", "pares · melhor em", "92,7% · 20 de 20", f"{pct(Ap.mean(), 2)} · {(Ap>A0).sum()}", pct(Ap.mean(), 1) == "92,7%" and (Ap > A0).sum() == 20, "92,7%, melhor em 20 de 20")
out("8", "tabela com pares", "cinco vezes maior", f"{c0} -> {cp} ({cp/c0:.2f}x)", 4.5 <= cp / c0 < 5.5, "cinco vezes maior")
out("8", "peso de não / ruim", "−2,0 / −3,5", f"{w[V['não']]:+.2f} / {w[V['ruim']]:+.2f}", (round(float(w[V["não"]]), 1), round(float(w[V["ruim"]]), 1)) == (-2.0, -3.5), '"não" pesa −2,0 e "ruim" pesa −3,5')

def nota(f, **kw):
    cv = CountVectorizer(analyzer=lambda t: prepara(t, "pt", **kw), binary=True); X = cv.fit_transform(T)
    m = MultinomialNB().fit(X, Y); ww = m.feature_log_prob_[1] - m.feature_log_prob_[0]; VV = cv.vocabulary_
    return m.class_log_prior_[1] - m.class_log_prior_[0] + sum(ww[VV[t]] for t in set(prepara(f, "pt", **kw)) if t in VV)
for f in ["não é ruim", "sem defeito nenhum"]:
    s = nota(f); out("8", f"'{f}' sem opcoes", "negativa (erro)", f"{s:+.2f}", s < 0, f'"{f}"')
s0, s1 = nota("a entrega atrasou"), nota("a entrega atrasou", stem=True)
out("8", "'a entrega atrasou' sem / com radical", "pos -> neg", f"{s0:+.2f} -> {s1:+.2f}", s0 > 0 > s1, '"a entrega atrasou" sai positiva')
out("8", "atrasou quase nunca apareceu", "quase nunca", f"{sum(pn('atrasou'))} avaliacoes", sum(pn("atrasou")) <= 3, '"atrasou" quase nunca apareceu')
pos_en = [t for t, s, y in zip(T, S, Y) if "entrega" in s and y == 1]
k = sum(1 for t in pos_en if re.search(r"entrega r[aá]pida", t.lower()))
out("8", "entrega: veio de 'entrega rápida'", "origem", f"entrega {pn('entrega')[0]} pos / {pn('entrega')[1]} neg; 'entrega rápida' em {k} das {len(pos_en)} positivas", k / len(pos_en) >= 0.5, '"entrega" veio de "entrega rápida"')
f = "que maravilha, esperei dois meses pela entrega"; s0, s1 = nota(f), nota(f, stem=True)
out("8", "ironia sem / com radical", "neg -> pos", f"{s0:+.2f} -> {s1:+.2f}", s0 < 0 < s1, "cai na ironia")
out("8", "maravilha e maravilhoso: mesmo radical", "junta", f"{st('maravilha')} / {st('maravilhoso')}", st("maravilha") == st("maravilhoso"), 'junta "maravilha" com "maravilhoso"')
out("8", "atraso e atrasado: mesmo radical de atrasou", "junta", f"{st('atrasou')} / {st('atraso')} / {st('atrasado')}", st("atrasou") == st("atraso") == st("atrasado"), "junta atraso e atrasado")
s0, s1 = nota("não gostei"), nota("não gostei", stop=True)
out("8", "'não gostei' sem / com corte de stopwords", "neg -> pos", f"{s0:+.2f} -> {s1:+.2f}", s0 < 0 < s1, 'inverte "não gostei"')

# bloco 9
m9 = f"{A0.mean():.3f} / {As.mean():.3f} / {Ar.mean():.3f}"
out("9", "Python: só letras / sem stopwords / radical", "0,917 / 0,912 / 0,919", m9, m9 == "0.917 / 0.912 / 0.919", "0,917, 0,912 e 0,919")

print(f"\n{'TUDO BATE' if not ruins else 'NAO BATE: ' + '; '.join(ruins)}")
