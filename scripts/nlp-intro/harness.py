# Confere o JS da pagina contra o Python (esperado.json). Uso: python harness.py pt|en
import asyncio, json, sys
from playwright.async_api import async_playwright
lang = sys.argv[1]
E = json.load(open("esperado.json", encoding="utf-8"))[lang]
URL = "http://localhost:8000/aulas/nlp-intro/" + ("" if lang == "pt" else "en/")
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--disable-quic"]); pg = await b.new_page()
        erros = []
        pg.on("console", lambda m: erros.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: erros.append(str(e)))
        await pg.goto(URL); await pg.wait_for_function("TXT.length>0", timeout=60000)
        stems = await pg.evaluate("ws=>Object.fromEntries(ws.map(w=>[w,stem(w)]))", list(E["stems"].keys()))
        diff = [(w, E["stems"][w], stems[w]) for w in E["stems"] if E["stems"][w] != stems[w]]
        print("radicais:", len(E["stems"]), "diferentes:", len(diff), diff[:15])
        cols = await pg.evaluate("""()=>({cru:new Set(TXT.flatMap(rawSplit)).size, base:new Set(TXT.flatMap(tokens)).size,
            acento:new Set(TXT.flatMap(t=>tokens(t).map(noAccent))).size, stop:new Set(TXT.flatMap(t=>prep(t,{stop:true}))).size,
            stem:new Set(TXT.flatMap(t=>prep(t,{stem:true}))).size})""")
        print("colunas JS", cols, "Python", E["cols"], "OK" if cols == E["cols"] else "DIFERENTE")
        for k, v in E["acc"].items():
            r = await pg.evaluate("k=>{const o={stop:k[0]==='1',stem:k[1]==='1',pairs:k[2]==='1'};const a=accFor(o);return {media:mean(a),notas:a,cols:new Set(docsFor(o).flat()).size}}", k)
            dn = [i for i, (x, y) in enumerate(zip(r["notas"], v["notas"])) if abs(x - y) > 1e-9 and round(x, 4) != y]
            print(f"acerto {k}: JS {r['media']:.4f} Py {v['media']:.4f} | colunas JS {r['cols']} Py {v['colunas_corpus']} | sorteios diferentes {dn}")
        print("erros de console:", erros)
        await b.close()
asyncio.run(main())
