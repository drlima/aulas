def lev(a,b):
    d=list(range(len(b)+1))
    for i,ca in enumerate(a,1):
        p,d[0]=d[0],i
        for j,cb in enumerate(b,1):
            p,d[j]=d[j],min(d[j]+1,d[j-1]+1,p+(ca!=cb))
    return d[-1]
if __name__=="__main__":
  for a,b in [("é ruim","não é ruim"),("ótimo","excelente"),("ótimo","otimo"),("gostei","não gostei"),("adorei","detestei"),("chegou rápido mas veio quebrado","veio quebrado mas chegou rápido"),
            ("bad","not bad"),("great","excellent"),("liked it","did not like it"),("loved","hated"),("fast delivery but it arrived broken","it arrived broken but fast delivery")]:
    print(f"{a!r} x {b!r}: {lev(a,b)} letras mudam (de {max(len(a),len(b))})")
