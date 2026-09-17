import asyncio, time
from playwright.async_api import async_playwright
B="https://drlima.github.io/aulas"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=["--disable-quic"])
        for lang,path in [("pt","/aulas/nlp-intro/"),("en","/aulas/nlp-intro/en/")]:
            for W,H,mob in [(1280,900,False),(390,844,True)]:
                ctx=await b.new_context(viewport={"width":W,"height":H},is_mobile=mob,has_touch=mob); pg=await ctx.new_page(); erros=[]
                pg.on("console",lambda m: erros.append(m.text) if m.type=="error" else None); pg.on("pageerror",lambda e: erros.append(str(e)))
                for tent in range(10):
                    r=await pg.goto(B+path)
                    if r.status==200 and "nlp" in (await pg.content()) and await pg.query_selector("#frText"): break
                    await pg.wait_for_timeout(15000)
                await pg.wait_for_function("TXT.length>0",timeout=60000); await pg.wait_for_timeout(2500)
                wide=await pg.evaluate("[...document.querySelectorAll('body *')].filter(e=>e.getBoundingClientRect().right>innerWidth+1&&!e.closest('nav.map,.grid,table,pre,textarea,.console')).length")
                print(lang,W,"status",r.status,"| docs",await pg.evaluate("TXT.length"),"|",await pg.inner_text("#frAcc"),"| largos",wide,"| erros",erros)
                if W==1280:
                    t=time.time();await pg.click("#run1");await pg.wait_for_function("!document.querySelector('#run1').disabled&&document.querySelector('#pyOut1').textContent.length>0",timeout=300000)
                    print("   python:",(await pg.inner_text("#pyOut1")).strip().split("\n")[-1],"(%.0fs)"%(time.time()-t))
                    await pg.click("nav.map .lang a");await pg.wait_for_load_state();print("   alternador ->",pg.url)
                    await pg.click("nav.map a.home");await pg.wait_for_load_state();print("   home ->",pg.url,"| nlp-intro no hub?", "nlp-intro" in await pg.content())
                await ctx.close()
        await b.close()
asyncio.run(main())
