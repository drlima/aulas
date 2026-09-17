# Em que contexto "entrega" (pt) e "delivery" (en) aparecem nas avaliacoes positivas.
# Uso: ./env.sh v23_contexto_entrega.py
from comum import *
from collections import Counter
import json

ALVO = {"pt": "entrega", "en": "delivery"}
# pistas de rapidez ou de prazo, procuradas na janela de 3 palavras em volta do alvo
PISTA = {"pt": re.compile(r"^(r[aá]pid\w*|ligeir\w*|express\w*|adiantad\w*|antecipad\w*|prazo|pontual\w*|antes|super|s[uú]per|imediat\w*|[aá]gil|agil\w*|cedo|certinh\w*|correta?)$"),
         "en": re.compile(r"^(fast|quick\w*|prompt\w*|speedy|rapid|early|time|timely|on|ahead|super)$")}

for lang in ["pt", "en"]:
    D = json.load(open(f"../../site/aulas/nlp-intro/assets/avaliacoes-{lang}.json", encoding="utf-8"))
    alvo = ALVO[lang]
    docs = [(prepara(t, lang), y, t) for t, y in zip(D["texto"], D["rotulo"])]
    pos = [(d, t) for d, y, t in docs if alvo in d and y == 1]
    neg = sum(1 for d, y, _ in docs if alvo in d and y == 0)
    print(f"\n=== {lang}: \"{alvo}\" em {len(pos)} positivas e {neg} negativas")
    antes, depois, com_pista = Counter(), Counter(), 0
    for d, _ in pos:
        pista = False
        for i, w in enumerate(d):
            if w != alvo: continue
            antes[d[i-1] if i else "(inicio da frase)"] += 1
            depois[d[i+1] if i + 1 < len(d) else "(fim da frase)"] += 1
            janela = d[max(0, i-3):i] + d[i+1:i+4]
            if any(PISTA[lang].match(x) for x in janela): pista = True
        com_pista += pista
    for nome, c in [("antes", antes), ("depois", depois)]:
        tot = sum(c.values())
        print(f"  10 palavras mais frequentes {nome} de \"{alvo}\" ({tot} ocorrencias):")
        for w, n in c.most_common(10):
            print(f"    {n:4d} ({n/tot:5.1%})  {w if nome == 'depois' else w} {alvo}" if nome == "antes" else f"    {n:4d} ({n/tot:5.1%})  {alvo} {w}")
        print(f"    top 10 cobrem {sum(n for _, n in c.most_common(10))/tot:.0%} das ocorrencias")
    print(f"  positivas com pista de rapidez ou prazo a ate 3 palavras do alvo: {com_pista} de {len(pos)} ({com_pista/len(pos):.0%})")
    # os bigramas inteiros mais frequentes, para ler os contextos de verdade
    bg = Counter()
    for d, _ in pos:
        for i, w in enumerate(d):
            if w != alvo: continue
            if i: bg[f"{d[i-1]} {alvo}"] += 1
            if i + 1 < len(d): bg[f"{alvo} {d[i+1]}"] += 1
    print("  10 bigramas mais frequentes:", ", ".join(f"{k} ({n})" for k, n in bg.most_common(10)))
    cob = set()
    tops = [k for k, _ in bg.most_common(10)]
    for j, (d, _) in enumerate(pos):
        pares = set()
        for i, w in enumerate(d):
            if w != alvo: continue
            if i: pares.add(f"{d[i-1]} {alvo}")
            if i + 1 < len(d): pares.add(f"{alvo} {d[i+1]}")
        if pares & set(tops): cob.add(j)
    print(f"  avaliacoes positivas cobertas por esses 10 bigramas: {len(cob)} de {len(pos)} ({len(cob)/len(pos):.0%})")
