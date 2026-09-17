from nltk.stem.porter import PorterStemmer
from nltk.stem import RSLPStemmer
po = PorterStemmer(mode=PorterStemmer.ORIGINAL_ALGORITHM); r = RSLPStemmer()
en = "liked like likes likely likable not general generous generate university universe organ organization news new was went go going gone better best good happy happiness arrived delivery broke broken".split()
print({w: po.stem(w) for w in en})
pt = "paisagem país pais fui vou ir iria foi era sou é seja melhor bom boa pior ruim amei amo amor amava disse dizer diz fiz fazer feito".split()
print({w: r.stem(w) for w in pt})
import spacy
for nome, ws in [("pt_core_news_sm", "Eu fui ontem, vou amanhã e iria de novo. Ela foi e era boa. Amei, amo e amava. O produto veio quebrado e as entregas atrasaram."), ("en_core_web_sm", "I went yesterday, I am going tomorrow and I was happy. The phones were better and she loved it. The deliveries arrived broken.")]:
    nlp = spacy.load(nome); print(nome, [(t.text, t.lemma_) for t in nlp(ws) if t.is_alpha])
