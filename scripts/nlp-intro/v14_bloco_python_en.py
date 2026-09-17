import json, time
data = json.load(open("../../site/aulas/nlp-intro/assets/avaliacoes-en.json", encoding="utf-8"))
texts, labels, splits = data["texto"], data["rotulo"], data["divisoes"]
t0=time.time()
import re
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

stem = PorterStemmer(mode="ORIGINAL_ALGORITHM").stem
def prepare(text):
    words = re.findall(r"[^\W\d_]+(?:'[^\W\d_]+)?", text.lower())   # block 4: lowercase, letters only
    return [stem(w) for w in words]                                 # block 6: the stem

vectorizer = CountVectorizer(analyzer=prepare, binary=True)   # block 3: one column per word
X = vectorizer.fit_transform(texts)
model = MultinomialNB().fit(X, labels)                        # block 7: learning is counting

sentence = "it did not disappoint"
weights = model.feature_log_prob_[1] - model.feature_log_prob_[0]
columns = vectorizer.vocabulary_
for word in prepare(sentence):
    print(word, round(weights[columns[word]], 2) if word in columns else "never seen")
print(X.shape, "->", ["negative", "positive"][model.predict(vectorizer.transform([sentence]))[0]])
print("t1", round(time.time()-t0,1))
from nltk.corpus import stopwords
empty = set(stopwords.words("english"))
def mean_score(prep):
    docs = [prep(t) for t in texts]; scores = []
    for split in splits:
        train = [i for i, s in enumerate(split) if s == "0"]; test = [i for i, s in enumerate(split) if s == "1"]
        vec = CountVectorizer(analyzer=lambda d: d, binary=True)
        m = MultinomialNB().fit(vec.fit_transform([docs[i] for i in train]), [labels[i] for i in train])
        scores.append(m.score(vec.transform([docs[i] for i in test]), [labels[i] for i in test]))
    return round(sum(scores) / len(scores), 3)
letters = lambda t: re.findall(r"[^\W\d_]+(?:'[^\W\d_]+)?", t.lower())
print("letters only:  ", mean_score(letters))
print("no stopwords:  ", mean_score(lambda t: [w for w in letters(t) if w not in empty]))
print("with stem:     ", mean_score(prepare))
