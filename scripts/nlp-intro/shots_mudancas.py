# Screenshots das partes alteradas, no site publicado, com os Revelar abertos.
import asyncio
from playwright.async_api import async_playwright
B = "https://drlima.github.io/aulas"
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--disable-quic"])
        for lang, path, secs in [("en", "/aulas/nlp-intro/en/", ["s3", "s7"]), ("pt", "/aulas/nlp-intro/", ["s3", "s7"])]:
            pg = await b.new_page(viewport={"width": 1280, "height": 900})
            await pg.goto(B + path); await pg.wait_for_function("TXT.length>0", timeout=60000)
            for s in secs:
                await pg.evaluate(f"document.querySelectorAll('#{s} details.reveal').forEach(d=>d.open=true)")
                await pg.locator(f"#{s} details.reveal").last.screenshot(path=f"shots/mud-{lang}-{s}-revelar.png")
            await pg.click("#run2"); await pg.wait_for_timeout(300)
            await pg.locator("#s9 .widget").nth(1).screenshot(path=f"shots/mud-{lang}-s9-caixa2-antes.png")
            await pg.locator("#pyStatus").screenshot(path=f"shots/mud-{lang}-s9-status.png")
            await pg.close()
        await b.close()
asyncio.run(main())
