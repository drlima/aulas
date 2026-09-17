import asyncio, sys
from playwright.async_api import async_playwright
lang=sys.argv[1]; URL="http://localhost:8000/aulas/nlp-intro/"+("" if lang=="pt" else "en/")
FR={"pt":[("não é ruim",{}),("sem defeito nenhum",{}),("não tenho do que reclamar",{}),("a entrega atrasou",{}),("a entrega atrasou",{"frStem":1}),
          ("que maravilha, esperei dois meses pela entrega",{}),("que maravilha, esperei dois meses pela entrega",{"frStem":1}),("não gostei",{}),("não gostei",{"frStop":1}),
          ("não recomendo",{"frStop":1}),("não recomendo",{"frPairs":1}),("chegou rápido mas veio quebrado",{}),("veio quebrado mas chegou rápido",{})],
    "en":[("not bad",{}),("no problems",{}),("no complaints at all",{}),("the delivery was late",{}),("oh great, it broke after two days",{}),("oh great, it broke after two days",{"frStem":1}),
          ("i do not recommend it",{}),("i do not recommend it",{"frStop":1}),("i did not like it",{"frPairs":1}),("it did not disappoint",{})]}[lang]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=["--disable-quic"])
        for W,H,mob in [(1280,900,False),(390,844,True)]:
            ctx=await b.new_context(viewport={"width":W,"height":H},is_mobile=mob,has_touch=mob,device_scale_factor=1)
            pg=await ctx.new_page(); erros=[]
            pg.on("console",lambda m: erros.append(m.text) if m.type=="error" else None); pg.on("pageerror",lambda e: erros.append(str(e)))
            await pg.goto(URL); await pg.wait_for_function("TXT.length>0",timeout=60000); await pg.wait_for_timeout(1500)
            if W==1280:
                for f,o in FR:
                    for cb in ["frStop","frStem","frPairs"]:
                        await pg.set_checked("#"+cb, bool(o.get(cb)))
                    await pg.fill("#frText",f); await pg.wait_for_timeout(400)
                    print(f"  {f!r} {o} -> {await pg.inner_text('#frVerdict')} | {await pg.inner_text('#frAcc')}")
                await pg.set_checked("#frStop",False);await pg.set_checked("#frStem",False);await pg.set_checked("#frPairs",False)
                await pg.fill("#frText","chegou rápido mas veio quebrado" if lang=="pt" else "fast delivery but it arrived broken")
                await pg.click("#listBtn"); print("lista:", await pg.inner_text("#listOut"))
                print("tabela:", await pg.inner_text("#tabOut"))
                print("pedacos:", await pg.inner_text("#tokOut"))
                await pg.click("#stopBtn"); print("vazias:", await pg.inner_text("#stopOut"))
                print("radical:", await pg.inner_text("#stemOut"))
                print("soma:", await pg.inner_text("#sumOut"), "|", await pg.inner_text("#accOut"))
                for c in await pg.query_selector_all("#pairCards .pair"): await (await c.query_selector("button")).click()
                for c in await pg.query_selector_all("#stemCards .pair"): await (await c.query_selector("button")).click()
                for c in await pg.query_selector_all("#pullCards .pullcard"): await (await c.query_selector("button")).click()
                print("pull:", [t.replace("\n"," / ")[:90] for t in await pg.eval_on_selector_all("#pullCards .res .wt","els=>els.map(e=>e.textContent)")])
                print("stem cards:", await pg.eval_on_selector_all("#stemCards .meter","els=>els.map(e=>e.textContent)"))
            await pg.evaluate("document.querySelectorAll('details').forEach(d=>d.open=true)")
            wide=await pg.evaluate("[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return r.right>innerWidth+1 && !e.closest('nav.map,.grid,table,pre,textarea,.console')}).map(e=>e.tagName+'#'+e.id+'.'+e.className).slice(0,15)")
            print(W, "largos:", wide, "erros:", erros)
            for s in [f"s{i}" for i in range(1,12)]:
                el=await pg.query_selector("#"+s); await el.screenshot(path=f"shots/{lang}-{W}-{s}.png")
            await ctx.close()
        await b.close()
asyncio.run(main())
