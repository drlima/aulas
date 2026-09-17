# Site publicado: bloco 9 (as duas caixas, e a segunda antes da primeira) e o quiz, em sessao limpa.
# Uso: python prod2.py [url base]   (padrao: o site publicado; local: http://localhost:8000)
import asyncio, sys, time
from playwright.async_api import async_playwright
B = sys.argv[1] if len(sys.argv) > 1 else "https://drlima.github.io/aulas"
PATHS = [("pt", "/aulas/nlp-intro/"), ("en", "/aulas/nlp-intro/en/")]
DONE = lambda n: f"!document.querySelector('#run{n}').disabled && document.querySelector('#pyOut{n}').textContent.trim().length>0"

async def sessao(p, lang, path, ordem):
    b = await p.chromium.launch(args=["--disable-quic"])            # navegador novo: cache vazio
    ctx = await b.new_context(viewport={"width": 1280, "height": 900}); pg = await ctx.new_page()
    erros, bytes_ = [], {"n": 0, "req": 0}
    pg.on("pageerror", lambda e: erros.append(str(e)))
    async def fim(req):
        try: s = await req.sizes(); bytes_["n"] += s["responseBodySize"] + s["responseHeadersSize"]; bytes_["req"] += 1
        except Exception: pass
    pg.on("requestfinished", lambda r: asyncio.ensure_future(fim(r)))
    await pg.goto(B + path); await pg.wait_for_function("TXT.length>0", timeout=60000); await pg.wait_for_timeout(1000)
    antes = bytes_["n"]
    print(f"== {lang} · ordem {ordem}")
    for i, n in enumerate(ordem):
        t = time.time(); await pg.click(f"#run{n}")
        await pg.wait_for_function(f"document.querySelector('#pyOut{n}').textContent.trim().length>0 && !document.querySelector('#run{n}').disabled", timeout=300000)
        dt = time.time() - t
        await pg.wait_for_timeout(1500); dl = bytes_["n"] - antes; antes = bytes_["n"]
        print(f"  run{n} ({dt:.1f}s) · baixou {dl/1e6:.1f} MB")
        print("    status:", await pg.inner_text("#pyStatus"))
        print("    " + (await pg.inner_text(f"#pyOut{n}")).strip().replace("\n", "\n    "))
    if ordem[0] == 2:
        orig = await pg.input_value("#py1")
        await pg.fill("#py1", "print(1/0)"); await pg.click("#run1"); await pg.wait_for_function(DONE(1), timeout=300000)
        print("    caixa 1 com erro -> status:", await pg.inner_text("#pyStatus"))
        await pg.fill("#py1", orig); await pg.click("#run1"); await pg.wait_for_function(DONE(1), timeout=300000)
        print("    caixa 1 corrigida -> status:", await pg.inner_text("#pyStatus"))
    print("  erros de pagina:", erros)
    await pg.locator("#s9").screenshot(path=f"shots/{'prod' if 'github' in B else 'local'}-{lang}-s9-{''.join(map(str, ordem))}.png")
    await b.close()

async def quiz(p, lang, path, modo):
    b = await p.chromium.launch(args=["--disable-quic"]); pg = await b.new_page(viewport={"width": 390, "height": 844} if modo == "errado" else {"width": 1280, "height": 900})
    erros = []; pg.on("pageerror", lambda e: erros.append(str(e)))
    await pg.goto(B + path); await pg.wait_for_selector("#quiz10 .row")
    itens = await pg.evaluate("S.quiz10")
    rows = await pg.query_selector_all("#quiz10 .row")
    marcas = []
    for k, (row, (perg, opts, certa)) in enumerate(zip(rows, itens)):
        esc = certa if modo == "certo" or (modo == "misto" and k % 3) else (certa + 1) % len(opts)
        await (await row.query_selector_all("button"))[esc].click()
        cls = await row.get_attribute("class")
        hint = await (await row.query_selector_all("button"))[certa].get_attribute("style")
        marcas.append(("right" in cls) == (esc == certa) and (esc == certa or "--ok" in (hint or "")))
    print(f"  quiz {lang} {modo}: {await pg.inner_text('#quiz10Out')!r} · marcacoes corretas {sum(marcas)}/{len(marcas)} · erros {erros}")
    await pg.locator("#s10 .widget").screenshot(path=f"shots/{'prod' if 'github' in B else 'local'}-{lang}-quiz-{modo}.png")
    await b.close()

async def main():
    async with async_playwright() as p:
        for lang, path in PATHS:
            await sessao(p, lang, path, [1, 2])
            await sessao(p, lang, path, [2, 1, 2])
            for modo in ["certo", "errado", "misto"]: await quiz(p, lang, path, modo)
asyncio.run(main())
