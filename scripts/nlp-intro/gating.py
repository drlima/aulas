# Primeiro bloco em que cada termo aparece no texto da pagina (sem o STR e sem codigo).
import re, sys
TERMOS = {"pt": [("classificador",2),("vocabulário",3),("vetor",3),("saco de palavras",3),("esparsa",3),("token",4),("normaliza",4),("stopword",5),("stemming",6),("radical",6),("lematiza",6),(r"\blema\b",6),(r"\bpesos?\b",7),("naive bayes",7),("n-grama",8),("bigrama",8),("embedding",10),("transformer",10)],
          "en": [("classifier",2),("vocabulary",3),("vector",3),("bag of words",3),("sparse",3),("token",4),("normaliz",4),("stopword",5),("stemming",6),(r"\bstem\b",6),("lemmatiz",6),(r"\blemma\b",6),(r"\bweights?\b",7),("naive bayes",7),("n-gram",8),("bigram",8),("embedding",10),("transformer",10)]}
for lang, arq in [("pt","../../site/aulas/nlp-intro/index.html"),("en","../../site/aulas/nlp-intro/en/index.html")]:
    h = open(arq, encoding="utf-8").read()
    h = re.sub(r"<script>.*?</script>", "", h, flags=re.S)
    h = re.sub(r"<(pre|textarea)\b.*?</\1>", "", h, flags=re.S)
    partes = {int(m.group(1)): m.group(2) for m in re.finditer(r'<section class="block" id="s(\d+)">(.*?)</section>', h, flags=re.S)}
    hero = h.split('<section class="block"')[0].split("<body>")[1]
    for termo, bloco in TERMOS[lang]:
        onde = [0] if re.search(termo, re.sub("<[^>]+>", " ", hero), re.I) else []
        onde += [n for n, t in sorted(partes.items()) if re.search(termo, re.sub("<[^>]+>", " ", t), re.I)]
        primeiro = onde[0] if onde else None
        print(f"{lang} {termo:18s} permitido a partir de {bloco:2d} | primeiro em {primeiro} {'OK' if primeiro is None or primeiro >= bloco else 'ANTES'}")
