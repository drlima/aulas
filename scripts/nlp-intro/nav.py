import asyncio
from playwright.async_api import async_playwright
B="http://localhost:8000"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={"width":1280,"height":900})
        await pg.goto(B+"/aulas/nlp-intro/"); await pg.click("nav.map .lang a"); await pg.wait_for_load_state(); print("PT->EN:", pg.url, await pg.title())
        await pg.click("nav.map .lang a"); await pg.wait_for_load_state(); print("EN->PT:", pg.url, await pg.title())
        await pg.click("nav.map a.home"); await pg.wait_for_load_state(); print("home pt:", pg.url)
        await pg.goto(B+"/aulas/nlp-intro/en/"); await pg.click("nav.map a.home"); await pg.wait_for_load_state(); print("home en:", pg.url)
        vis=await pg.goto(B+"/aulas/nlp-intro/") or True
        print("nav visivel 1280:", await pg.eval_on_selector_all("nav.map a, nav.map .lang","els=>els.every(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.bottom<=innerHeight&&r.right<=innerWidth})"))
        for u in ["/","/en/"]:
            await pg.goto(B+u); await pg.wait_for_timeout(1200); html=await pg.content()
            print(u, "nlp-intro no hub?", "nlp-intro" in html, "| ml-intro no hub?", "ml-intro" in html)
        await b.close()
asyncio.run(main())
