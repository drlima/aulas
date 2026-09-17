import json, time
dados = json.load(open("../../site/aulas/nlp-intro/assets/avaliacoes-pt.json", encoding="utf-8"))   # na pagina: preludio escondido com pyfetch
textos, rotulos, divisoes = dados["texto"], dados["rotulo"], dados["divisoes"]
t0 = time.time()
# ---- celula 1 (como vai para a pagina) ----
import re
from nltk.stem import RSLPStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

radical = RSLPStemmer().stem
def preparar(texto):
    palavras = re.findall(r"[^\W\d_]+", texto.lower())   # bloco 4: minúsculas, só letras
    return [radical(p) for p in palavras]                 # bloco 6: o radical

vetorizador = CountVectorizer(analyzer=preparar, binary=True)   # bloco 3: uma coluna por palavra
X = vetorizador.fit_transform(textos)
modelo = MultinomialNB().fit(X, rotulos)                        # bloco 7: aprender é contar

frase = "a entrega atrasou"
pesos = modelo.feature_log_prob_[1] - modelo.feature_log_prob_[0]
colunas = vetorizador.vocabulary_
for palavra in preparar(frase):
    print(palavra, round(pesos[colunas[palavra]], 2) if palavra in colunas else "nunca vista")
print(X.shape, "->", ["negativa", "positiva"][modelo.predict(vetorizador.transform([frase]))[0]])
# ---- fim celula 1 ----
print("tempo celula 1", round(time.time()-t0,1), "s")
t0=time.time()
# ---- celula 2 ----
from nltk.corpus import stopwords
vazias = set(stopwords.words("portuguese"))

def nota_media(preparo):
    docs = [preparo(t) for t in textos]
    notas = []
    for divisao in divisoes:                                  # os mesmos 20 sorteios dos widgets
        treino = [i for i, d in enumerate(divisao) if d == "0"]
        teste = [i for i, d in enumerate(divisao) if d == "1"]
        vet = CountVectorizer(analyzer=lambda d: d, binary=True)
        m = MultinomialNB().fit(vet.fit_transform([docs[i] for i in treino]), [rotulos[i] for i in treino])
        notas.append(m.score(vet.transform([docs[i] for i in teste]), [rotulos[i] for i in teste]))
    return round(sum(notas) / len(notas), 3)

so_letras = lambda t: re.findall(r"[^\W\d_]+", t.lower())
print("só letras:        ", nota_media(so_letras))
print("sem stopwords:    ", nota_media(lambda t: [p for p in so_letras(t) if p not in vazias]))
print("com radical:      ", nota_media(preparar))
# ---- fim celula 2 ----
print("tempo celula 2", round(time.time()-t0,1), "s")
