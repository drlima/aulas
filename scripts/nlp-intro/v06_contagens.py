from comum import *
import sys
lang=sys.argv[1]; df = corpus(lang, notas=([1,2],[4,5]))
docs=[set(prepara(t,lang)) for t in df.texto]; y=df.y.values
P=(y==1).sum(); N=(y==0).sum(); print(lang, "pos",P,"neg",N)
ws = sys.argv[2].split(",")
for w in ws:
    p=sum(1 for d,yy in zip(docs,y) if w in d and yy==1); n=sum(1 for d,yy in zip(docs,y) if w in d and yy==0)
    ex=[t for t,d in zip(df.texto,docs) if w in d][:4]
    print(f"{w}: pos {p} neg {n} | ex: {ex}")
