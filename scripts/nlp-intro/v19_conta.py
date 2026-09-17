import json
d=json.load(open("../../site/aulas/nlp-intro/assets/avaliacoes-pt.json",encoding="utf-8")); textos, rotulos = d["texto"], d["rotulo"]
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

palavras = lambda t: re.findall(r"[^\W\d_]+", t.lower())
vetorizador = CountVectorizer(analyzer=palavras, binary=True)   # 1 se a palavra está lá
X = vetorizador.fit_transform(textos)
modelo = MultinomialNB().fit(X, rotulos)       # conta as avaliações com cada palavra

pesos = modelo.feature_log_prob_[1] - modelo.feature_log_prob_[0]
print(round(pesos[vetorizador.vocabulary_["avaliar"]], 2))   # -3.7
d=json.load(open("../../site/aulas/nlp-intro/assets/avaliacoes-en.json",encoding="utf-8")); texts, labels = d["texto"], d["rotulo"]
words = lambda t: re.findall(r"[^\W\d_]+(?:'[^\W\d_]+)?", t.lower())
vectorizer = CountVectorizer(analyzer=words, binary=True)
X = vectorizer.fit_transform(texts)
model = MultinomialNB().fit(X, labels)
weights = model.feature_log_prob_[1] - model.feature_log_prob_[0]
print(round(weights[vectorizer.vocabulary_["money"]], 2))
