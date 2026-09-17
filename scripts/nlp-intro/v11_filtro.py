from comum import *
import re
df = corpus("pt", notas=([1,2],[4,5]))
PAL = r"\b(porra|merda|caralho|puta|puto|bosta|fdp|pqp|cu|foda|foder|fodido|lixo do caralho|vagabund\w*|safad\w*|ladr[aã]o|ladr\w+|filh\w* da puta|desgra[çc]\w*|cacete|vtnc|otári\w*|idiota\w*|imbecil\w*|burr[oa]s?|palha[çc]ada|golpe\w*|estelionat\w*|bandid\w*)\b"
PII = r"(\d[\d\s\.\-]{7,}\d|@\w|https?://|www\.|\bcpf\b|\bprotocolo\b|\bpedido\s*(n|nº|numero|número)?\s*\d)"
for nome, rx in [("palavrao/acusacao", PAL), ("pii", PII)]:
    m = df[df.texto.str.contains(rx, case=False, regex=True)]
    print(nome, len(m)); print(m.texto.head(25).to_string())
en = corpus("en")
m = en[en.texto.str.contains(r"\b(fuck\w*|shit\w*|damn|crap|ass|bitch\w*|jerks?|idiots?|scam\w*)\b|@|https?://|\d{7,}", case=False, regex=True)]
print("en", len(m)); print(m.texto.to_string())
