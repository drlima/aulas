import asyncio, sys, time
from playwright.async_api import async_playwright
lang=sys.argv[1]; URL="http://localhost:8000/aulas/nlp-intro/"+("" if lang=="pt" else "en/")
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=["--disable-quic"]); pg=await b.new_page(); erros=[]
        pg.on("pageerror",lambda e: erros.append(str(e))); pg.on("console",lambda m: erros.append(m.text) if m.type=="error" else None)
        await pg.goto(URL); t=time.time()
        await pg.click("#run1"); await pg.wait_for_function("!document.querySelector('#run1').disabled && document.querySelector('#pyOut1').textContent.length>0",timeout=300000)
        print("celula 1 (%.0fs):"%(time.time()-t)); print(await pg.inner_text("#pyOut1")); print("status:", await pg.inner_text("#pyStatus"))
        t=time.time(); await pg.click("#run2"); await pg.wait_for_function("!document.querySelector('#run2').disabled && document.querySelector('#pyOut2').textContent.trim().split(String.fromCharCode(10)).length>=3",timeout=300000)
        print("celula 2 (%.0fs):"%(time.time()-t)); print(await pg.inner_text("#pyOut2")); print("erros:", erros)
        await (await pg.query_selector("#s9")).screenshot(path=f"shots/{lang}-1280-s9-rodado.png")
        await b.close()
asyncio.run(main())
