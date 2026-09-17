import asyncio, pathlib
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--disable-quic"]); pg = await b.new_page()
        pg.on("console", lambda m: print("console:", m.text) if m.type=="error" else None)
        await pg.goto(pathlib.Path("pyo.html").resolve().as_uri())
        await pg.wait_for_function("document.getElementById('o').textContent.match(/OK|ERRO/)", timeout=240000)
        print(await pg.inner_text("#o")); await b.close()
asyncio.run(main())
