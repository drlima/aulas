import json
from collections import Counter
for lang in ["pt","en"]:
    d=json.load(open(f"../../site/aulas/nlp-intro/assets/avaliacoes-{lang}.json",encoding="utf-8")); T=d["texto"]
    docs=[t.split() for t in T]; c=Counter(w for x in docs for w in x); V=len(c)
    md=sum(len(set(x)) for x in docs)/len(docs); h=sum(1 for v in c.values() if v==1)
    print(lang, "cru colunas", V, f"distintas/aval {md:.1f} zeros {1-md/V:.2%}", f"uma vez so {h} ({h/V:.0%})", "linhas", len(T), "casas", len(T)*V)
