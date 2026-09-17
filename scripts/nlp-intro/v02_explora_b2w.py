import pandas as pd, re
df = pd.read_csv("dados/b2w-reviews01-main/B2W-Reviews01.csv", low_memory=False)
print(df.shape); print(df.overall_rating.value_counts().sort_index()); print(df.recommend_to_a_friend.value_counts())
df = df.dropna(subset=["review_text"])
df["n"] = df.review_text.str.split().str.len()
print(df.n.describe())
print(pd.crosstab(df.overall_rating, df.recommend_to_a_friend))
curtas = df[(df.n>=3)&(df.n<=20)]
print("curtas 3-20 palavras:", len(curtas), curtas.overall_rating.value_counts().sort_index().to_dict())
t = df.review_text.str.lower()
for a,b in [("ótimo","otimo"),("péssimo","pessimo"),("não","nao"),("excelente","excelente"),("rápida","rapida")]:
    print(a, t.str.contains(rf"\b{a}\b").sum(), b, t.str.contains(rf"\b{b}\b").sum())
print("MAIUSCULAS inteiras:", (df.review_text.str.upper()==df.review_text).sum())
print(curtas.sample(12, random_state=1)[["overall_rating","review_text"]].to_string())
