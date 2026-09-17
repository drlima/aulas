import nltk
for p in ["rslp","stopwords"]: nltk.download(p, quiet=True)
from nltk.stem import RSLPStemmer, PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
import sklearn; print("nltk", nltk.__version__, "sklearn", sklearn.__version__)
pt = stopwords.words("portuguese"); en = stopwords.words("english")
print("pt stopwords", len(pt), [w for w in ["não","nem","nunca","mais","muito","pouco","bem","mal","sem","nada"] if w in pt])
print("en stopwords", len(en), [w for w in ["not","no","nor","never","very","too","don't","didn't","wasn't","isn't","but","against"] if w in en])
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS as SK
print("sklearn en", len(SK), [w for w in ["not","no","never","nothing","very","too","but","against","cry","fire","bill","amount"] if w in SK])
r = RSLPStemmer()
ws = "não Não NÃO nunca gostei gostaria gosto gosta gostoso bom boa bons ótimo ótima péssimo péssima ruim ruins barato barata baratinho casa casamento casal livro livre livraria fui vou ir iria foi era sou é seja entrega entregue entregador entregaram produto produção produtivo chegou chegada rápido rapidez rapidamente demorou demora demorado lindo linda lindeza amei amor amo amoroso odeio ódio recomendo recomendação quebrado quebrou quebra".split()
print({w: r.stem(w) for w in ws})
# colisões dentro da lista
from collections import defaultdict
g=defaultdict(list)
for w in ws: g[r.stem(w)].append(w)
print("grupos RSLP:", {k:v for k,v in g.items() if len(v)>1})
ps = PorterStemmer(); sb = SnowballStemmer("english")
we = "not Not never liked like likes likely likable good goods goodness great terrible bad badly cheap cheaply university universe universal general generous generate organ organization organic news new went go going gone was is be being arrive arrival arrived delivery deliver delivered broken broke break love lovely loved hate hated happy happiness happily recommend recommendation".split()
print({w:(ps.stem(w), sb.stem(w)) for w in we})
for name, st in [("porter",ps),("snowball",sb)]:
    g=defaultdict(list)
    for w in we: g[st.stem(w)].append(w)
    print(name, {k:v for k,v in g.items() if len(v)>1})
