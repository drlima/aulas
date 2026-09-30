#!/usr/bin/env python3
"""Testes de navegador da aula github-windows (Playwright), em 1280 px e 390 px.

    pip install playwright && playwright install chromium
    python3 -m http.server --directory site 8000 &
    python3 scripts/github-windows/testa_pagina.py --out /caminho/para/screenshots
    python3 scripts/github-windows/testa_pagina.py --url https://drlima.github.io/aulas/aulas/github-windows/ --out ...

O hub só tem tema claro, então não há variante escura para testar. Sai com código 1 se
qualquer verificação falhar; os screenshots ficam em --out (fora do repositório).
"""
import argparse
import importlib.util
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

RAIZ = Path(__file__).resolve().parent.parent.parent
spec = importlib.util.spec_from_file_location("verifica", RAIZ / "scripts" / "verifica-github-windows.py")
verifica = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifica)
BLOCOS = [c for t, c in verifica.pecas_do_conteudo() if t == "codigo"]
PLACEHOLDERS = {"Seu Nome", "email-da-conta-github", "USUARIO", "REPO", "URL-COPIADA", "nome-do-repo", "URL-DO-REPO"}

ap = argparse.ArgumentParser()
ap.add_argument("--url", default="http://localhost:8000/aulas/github-windows/")
ap.add_argument("--out", required=True)
args = ap.parse_args()
OUT = Path(args.out)
OUT.mkdir(parents=True, exist_ok=True)
URL = args.url

falhas, total = [], 0


def ok(cond, msg):
    global total
    total += 1
    print(("  ok    " if cond else "  FALHA ") + msg)
    if not cond:
        falhas.append(msg)


def novo(browser, vp, **kw):
    w, h, mob = vp
    ctx = browser.new_context(viewport={"width": w, "height": h}, is_mobile=mob, has_touch=mob, **kw)
    pg = ctx.new_page()
    pg.errs = []
    pg.on("console", lambda m: pg.errs.append(m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: pg.errs.append(str(e)))
    return ctx, pg


def abre(pg, sufixo=""):
    pg.goto(URL + sufixo)
    pg.wait_for_load_state("networkidle")


def espera_parar(pg):
    """Espera o scroll suave terminar (scrollY igual em duas leituras seguidas)."""
    ant = None
    for _ in range(40):
        atual = pg.evaluate("scrollY")
        if atual == ant:
            return
        ant = atual
        pg.wait_for_timeout(150)


def aba_ativa(pg):
    return pg.evaluate("(document.querySelector('.tab[aria-selected=\"true\"]')||{}).id")


def visiveis(pg):
    return [pg.locator(f'[id="{i}"]').is_visible() for i in ("5a", "5b", "5c")]


def testa_viewport(browser, nome, vp):
    print(f"\n=== {nome} ({vp[0]} px) ===")
    mob = vp[2]

    # --- carga, console, rolagem horizontal, screenshots
    ctx, pg = novo(browser, vp)
    ctx.grant_permissions(["clipboard-read", "clipboard-write"])
    abre(pg)
    ok(pg.errs == [], f"zero erro de console na carga {pg.errs}")
    extra = pg.evaluate("document.documentElement.scrollWidth - innerWidth")
    ok(extra <= 0 and pg.evaluate("document.body.scrollWidth - innerWidth") <= 0, f"sem rolagem horizontal no body (sobra {extra}px)")
    largos = pg.evaluate("""[...document.querySelectorAll('body *')].filter(e=>e.getBoundingClientRect().right>innerWidth+1
        && !e.closest('pre,table,.tablist')).map(e=>e.tagName+'.'+e.className).slice(0,5)""")
    ok(largos == [], f"nenhum elemento além da viewport {largos}")
    pg.screenshot(path=str(OUT / f"{nome}-pagina-inteira.png"), full_page=True)
    for sid in [f"s{i}" for i in range(1, 11)] + ["erros"]:
        if sid == "s5":
            for aba in ("5a", "5b", "5c"):
                pg.click(f"#tab-{aba}")
                pg.locator("#s5").screenshot(path=str(OUT / f"{nome}-s5-{aba}.png"))
            pg.click("#tab-5a")
        else:
            pg.locator(f"#{sid}").screenshot(path=str(OUT / f"{nome}-{sid}.png"))

    # --- abas: padrão, clique, teclado
    pg.evaluate("localStorage.clear()")
    abre(pg)
    ok(aba_ativa(pg) == "tab-5a" and visiveis(pg) == [True, False, False], "5A é a aba padrão; 5B e 5C escondidas")
    ok(pg.locator("[role=tablist]").count() == 1 and pg.locator("[role=tab]").count() == 3
       and pg.locator("[role=tabpanel]").count() == 3, "role=tablist, 3 role=tab, 3 role=tabpanel")
    ok(pg.get_attribute("#tab-5a", "aria-selected") == "true" and pg.get_attribute("#tab-5b", "aria-selected") == "false",
       "aria-selected reflete a aba")
    ok(pg.get_attribute("#tab-5b", "tabindex") == "-1" and pg.get_attribute("#tab-5a", "tabindex") == "0", "tabindex móvel (roving)")
    pg.click("#tab-5b")
    ok(aba_ativa(pg) == "tab-5b" and visiveis(pg) == [False, True, False], "clique em 5B abre 5B")
    pg.keyboard.press("ArrowRight")
    ok(aba_ativa(pg) == "tab-5c" and visiveis(pg) == [False, False, True], "seta direita vai para 5C")
    pg.keyboard.press("ArrowRight")
    ok(aba_ativa(pg) == "tab-5a", "seta direita em 5C volta para 5A (circular)")
    pg.keyboard.press("ArrowLeft")
    ok(aba_ativa(pg) == "tab-5c", "seta esquerda em 5A vai para 5C")
    pg.keyboard.press("Home")
    ok(aba_ativa(pg) == "tab-5a", "Home vai para a primeira aba")
    pg.keyboard.press("End")
    ok(pg.evaluate("document.activeElement.id") == "tab-5c" and aba_ativa(pg) == "tab-5c", "End vai para a última aba e mantém o foco nela")
    pg.reload(); pg.wait_for_load_state("networkidle")
    ok(aba_ativa(pg) == "tab-5c", "a escolha (5C) sobrevive ao recarregamento (localStorage)")
    ctx.close()

    # --- âncora direta
    for frag, esperado in (("#5b", "tab-5b"), ("#5c", "tab-5c"), ("#5a", "tab-5a")):
        ctx, pg = novo(browser, vp)
        abre(pg, frag)
        ok(aba_ativa(pg) == esperado and pg.locator(f'[id="{frag[1:]}"]').is_visible(), f"âncora {frag} abre a aba certa")
        ok(pg.evaluate(f"document.getElementById('{frag[1:]}').getBoundingClientRect().top") < vp[1],
           f"âncora {frag} leva o painel para dentro da tela")
        ctx.close()
    ctx, pg = novo(browser, vp)
    abre(pg)
    pg.evaluate("location.hash='#5b'")
    pg.wait_for_timeout(300)
    ok(aba_ativa(pg) == "tab-5b", "mudar o #hash depois de carregar também abre a aba")
    ctx.close()

    # --- copiar comandos
    ctx, pg = novo(browser, vp)
    ctx.grant_permissions(["clipboard-read", "clipboard-write"])
    abre(pg)
    botoes = pg.locator("button.copy")
    ok(botoes.count() == len(BLOCOS) == 6, f"um botão Copiar por bloco de código ({botoes.count()} de {len(BLOCOS)})")
    phs = set(pg.eval_on_selector_all(".ph", "els=>els.map(e=>e.textContent)"))
    ok(phs == PLACEHOLDERS, f"placeholders destacados (blocos e código em linha): {sorted(phs)}")
    em_blocos = set(pg.eval_on_selector_all("pre .ph", "els=>els.map(e=>e.textContent)"))
    ok(em_blocos <= PLACEHOLDERS and len(em_blocos) >= 6, f"placeholders dentro dos blocos de comando: {sorted(em_blocos)}")
    tab_de = {}
    for i in range(botoes.count()):
        painel = pg.evaluate(f"(document.querySelectorAll('button.copy')[{i}].closest('.tabpanel')||{{}}).id || ''")
        if painel:
            pg.click(f"#tab-{painel}")
        b = botoes.nth(i)
        b.scroll_into_view_if_needed()
        b.click()
        pg.wait_for_timeout(150)
        clip = pg.evaluate("navigator.clipboard.readText()")
        ok(clip == BLOCOS[i], f"bloco {i + 1}: a área de transferência tem o texto exato do CONTEUDO.md")
        ok(b.inner_text() == "Copiado" and "done" in (b.get_attribute("class") or ""), f"bloco {i + 1}: feedback 'Copiado'")
    pg.click("#tab-5a")
    pg.locator("#s3 pre").scroll_into_view_if_needed()
    pg.locator("#s3 button.copy").click()
    pg.locator("#s3").screenshot(path=str(OUT / f"{nome}-copiado.png"))
    pg.wait_for_timeout(2500)
    ok(pg.locator("#s3 button.copy").inner_text() == "Copiar", "o botão volta a 'Copiar' depois do aviso")
    ok(pg.errs == [], f"zero erro de console nas interações {pg.errs}")
    ctx.close()

    # --- cópia: Clipboard API recusada -> execCommand; tudo recusado -> seleciona o bloco
    ctx, pg = novo(browser, vp)
    ctx.grant_permissions(["clipboard-read", "clipboard-write"])
    pg.add_init_script("navigator.clipboard.writeText = () => Promise.reject(new Error('negado'))")
    abre(pg)
    pg.locator("#s3 button.copy").click()
    pg.wait_for_timeout(200)
    ok(pg.evaluate("navigator.clipboard.readText()") == BLOCOS[0], "fallback execCommand copia o texto exato quando a Clipboard API falha")
    ctx.close()
    ctx, pg = novo(browser, vp)
    pg.add_init_script("navigator.clipboard.writeText = () => Promise.reject(new Error('negado'));"
                       "document.execCommand = () => false")
    abre(pg)
    pg.locator("#s3 button.copy").click()
    pg.wait_for_timeout(200)
    ok(pg.locator("#s3 button.copy").inner_text() == "Use Ctrl+C", "sem nenhuma forma de copiar, o botão pede Ctrl+C")
    ok(pg.evaluate("getSelection().toString()") == BLOCOS[0], "e deixa o bloco inteiro selecionado")
    ctx.close()

    # --- checklist e progresso
    ctx, pg = novo(browser, vp)
    abre(pg)
    caixas = pg.locator("#checklist input[type=checkbox]")
    ok(caixas.count() == 4, "os 4 itens da seção 10 viram caixas de seleção")
    caixas.nth(0).check(); caixas.nth(2).check()
    pg.click("#s3 button.mark")
    ok(pg.locator("#tocProg").text_content().startswith("1 de 10"), f"marcador de progresso: {pg.locator('#tocProg').text_content()!r}")
    pg.reload(); pg.wait_for_load_state("networkidle")
    estado = [caixas.nth(i).is_checked() for i in range(4)]
    ok(estado == [True, False, True, False], f"checklist persiste após recarregar {estado}")
    ok(pg.get_attribute("#s3 button.mark", "aria-pressed") == "true", "marca da seção 3 persiste após recarregar")
    ok(pg.locator("#toc li.feita").count() == 1, "índice mostra a seção 3 como feita")
    pg.locator("#checklist").scroll_into_view_if_needed()
    pg.locator("#s10").screenshot(path=str(OUT / f"{nome}-s10-progresso.png"))
    pg.get_by_role("button", name="Marcar tudo como feito").click()
    ok(all(caixas.nth(i).is_checked() for i in range(4)), "'Marcar tudo como feito' marca os 4 itens")
    if mob:
        pg.click("#toc summary")
    pg.get_by_role("button", name="Limpar progresso").click()
    ok(not any(caixas.nth(i).is_checked() for i in range(4)) and pg.get_attribute("#s3 button.mark", "aria-pressed") == "false",
       "'Limpar progresso' zera caixas e marcas")
    pg.reload(); pg.wait_for_load_state("networkidle")
    ok(not any(caixas.nth(i).is_checked() for i in range(4)) and pg.locator("#toc li.feita").count() == 0,
       "e continua zerado após recarregar")
    ok(pg.errs == [], f"zero erro de console {pg.errs}")
    ctx.close()

    # --- armazenamento quebrado: a página funciona normalmente
    ctx, pg = novo(browser, vp)
    pg.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new Error('bloqueado')}})")
    abre(pg)
    ok(pg.errs == [], f"armazenamento bloqueado: zero erro de console {pg.errs}")
    pg.click("#tab-5b")
    ok(aba_ativa(pg) == "tab-5b", "armazenamento bloqueado: as abas funcionam")
    pg.locator("#checklist input").nth(1).check()
    ok(pg.locator("#checklist input").nth(1).is_checked(), "armazenamento bloqueado: a caixa marca na sessão")
    ok("bloqueou" in pg.locator(".store-warn").inner_text(), "armazenamento bloqueado: o aviso aparece junto do checklist")
    pg.locator("#s3 button.copy").click()
    ctx.close()

    # --- índice
    ctx, pg = novo(browser, vp)
    abre(pg)
    links = pg.locator("#toc a")
    ok(links.count() == 13, f"índice com 13 âncoras (1–4, 5A–5C, 6–10, Erros comuns): {links.count()}")
    destinos = pg.eval_on_selector_all("#toc a", "as=>as.map(a=>a.getAttribute('href'))")
    ok(all(pg.evaluate(f"!!document.getElementById('{h[1:]}')") for h in destinos), "todas as âncoras do índice existem na página")
    aberto = pg.evaluate("document.querySelector('#toc details').open")
    if not mob:
        ok(aberto and pg.locator("#toc").is_visible(), "desktop: índice aberto na lateral")
        y0 = pg.evaluate("document.querySelector('#toc').getBoundingClientRect().top")
        pg.evaluate("scrollTo(0, 3000)"); pg.wait_for_timeout(400)
        y1 = pg.evaluate("document.querySelector('#toc').getBoundingClientRect().top")
        ok(abs(y0 - y1) < 1 and pg.locator("#toc").is_visible(), f"desktop: índice fica fixo ao rolar ({y0}px -> {y1}px)")
        sobre = pg.evaluate("""(()=>{const t=document.querySelector('#toc').getBoundingClientRect(),
            c=document.querySelector('#s2 .wrap').getBoundingClientRect();return t.right<=c.left+22})()""")
        ok(sobre, "desktop: o índice não cobre a coluna de texto")
        ok(pg.locator("#toc a[aria-current]").count() == 1, "desktop: o item da seção visível fica realçado")
        pg.screenshot(path=str(OUT / f"{nome}-indice.png"))
    else:
        ok(not aberto, "mobile: índice recolhido")
        pg.click("#toc summary")
        ok(pg.evaluate("document.querySelector('#toc details').open") and pg.locator("#toc a").first.is_visible(), "mobile: abre ao tocar")
        pg.screenshot(path=str(OUT / f"{nome}-indice-aberto.png"))
        pg.evaluate("scrollTo(0, 2500)"); pg.wait_for_timeout(300)
        topo = pg.evaluate("document.querySelector('#toc').getBoundingClientRect().top")
        ok(0 <= topo <= 60 and pg.locator("#toc summary").is_visible(), f"mobile: o índice acompanha a rolagem (top {topo}px)")
    for href in ("#s7", "#erros", "#5c"):
        if mob and not pg.evaluate("document.querySelector('#toc details').open"):
            pg.click("#toc summary")
        pg.click(f'#toc a[href="{href}"]')
        espera_parar(pg)
        alvo = f'[id="{href[1:]}"] h2'
        topo = pg.evaluate(f"document.querySelector('{alvo}').getBoundingClientRect().top")
        barras = 53 + (50 if mob else 0)
        no_fim = pg.evaluate("scrollY + innerHeight >= document.documentElement.scrollHeight - 2")
        ok(barras - 4 <= topo and (topo < vp[1] * 0.4 or no_fim), f"âncora {href}: o título para abaixo das barras fixas (top {topo:.0f}px)")
        if mob:
            ok(not pg.evaluate("document.querySelector('#toc details').open"), f"mobile: o índice recolhe depois de {href}")
    ctx.close()

    # --- impressão: as três opções completas
    ctx, pg = novo(browser, vp)
    abre(pg)
    pg.emulate_media(media="print")
    ok(visiveis(pg) == [True, True, True] and not pg.locator(".tablist").is_visible(),
       "impressão: 5A, 5B e 5C completas em sequência, sem o seletor")
    ctx.close()


with sync_playwright() as p:
    browser = p.chromium.launch()
    testa_viewport(browser, "desktop-1280", (1280, 900, False))
    testa_viewport(browser, "mobile-390", (390, 844, True))

    print("\n=== sem JavaScript ===")
    for nome, vp in (("desktop-1280", (1280, 900, False)), ("mobile-390", (390, 844, True))):
        ctx, pg = novo(browser, vp, java_script_enabled=False)
        abre(pg)
        ok(visiveis(pg) == [True, True, True], f"{nome}: sem JS, 5A, 5B e 5C aparecem completas")
        ys = pg.evaluate("['5a','5b','5c'].map(i=>document.getElementById(i).getBoundingClientRect().top)")
        ok(ys == sorted(ys), f"{nome}: sem JS, em sequência")
        ok(pg.locator("button.copy").count() == 0 and pg.locator(".tablist").count() == 0, f"{nome}: sem JS, nenhum controle quebrado")
        ok(pg.evaluate("document.documentElement.scrollWidth - innerWidth") <= 0, f"{nome}: sem JS, sem rolagem horizontal")
        pg.screenshot(path=str(OUT / f"{nome}-sem-js.png"), full_page=True)
        ctx.close()
    browser.close()

print(f"\n{total - len(falhas)} de {total} verificações passaram.")
if falhas:
    print("FALHARAM:")
    for f in falhas:
        print("  -", f)
    sys.exit(1)
print("TUDO VERDE")
