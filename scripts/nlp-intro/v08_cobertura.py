from comum import *
import sys
FR = {"pt": ["o fone parou de funcionar em uma semana","amei a cor e o tamanho","chegou antes do prazo e bem embalado","não recomendo essa loja para ninguém",
 "a bateria dura pouco","produto de ótima qualidade pelo preço","veio faltando peça e ninguém responde","meu filho adorou o presente",
 "o tecido é fino e rasgou na primeira lavagem","atendimento horrível, quero meu dinheiro de volta","funciona muito bem, estou satisfeita","a tela trincou sozinha",
 "valeu cada centavo","esperava mais pelo valor","a panela gruda tudo"],
 "en": ["the headphones stopped working after a week","i love the color and the size","arrived early and well packed","i would not recommend this store to anyone",
 "the battery dies quickly","great quality for the price","a piece was missing and nobody answers","my son loved the gift",
 "the fabric is thin and ripped after one wash","horrible service, i want my money back","works very well, i am satisfied","the screen cracked by itself",
 "worth every penny","expected more for the price","the pan sticks to everything"]}
lang=sys.argv[1]
for n, extra in ([(1000,None),(2000,None),(4000,None)] if lang=="pt" else [(0,"ay"),(0,"ayi")]):
    if lang=="pt": df = corpus("pt", n_por_classe=n, notas=([1,2],[4,5]))
    else:
        import pandas as pd
        fs={"a":"amazon_cells_labelled.txt","y":"yelp_labelled.txt","i":"imdb_labelled.txt"}; rows=[]
        for k in extra:
            for line in open(f"dados/sentiment labelled sentences/{fs[k]}", encoding="utf-8"):
                if "\t" in line: t,y=line.rstrip("\n").rsplit("\t",1); rows.append((t.strip(),int(y)))
        df = pd.DataFrame(rows, columns=["texto","y"]).drop_duplicates("texto")
    voc = set(w for t in df.texto for w in prepara(t, lang)); vs = set(prepara(" ".join(voc), lang, stem=True))
    tot=fora=fs_=0; inteiras=0
    for f in FR[lang]:
        d = prepara(f, lang); tot+=len(d); fo=[w for w in d if w not in voc]; fora+=len(fo)
        fs_ += sum(1 for w in prepara(f, lang, stem=True) if w not in vs)
    kb = df.texto.str.len().sum()/1024
    print(f"{lang} {n or extra} docs {len(df)} ({kb:.0f} KB) vocab {len(voc)}: fora do vocab {fora}/{tot} = {fora/tot:.0%}; com stem {fs_/tot:.0%}")
