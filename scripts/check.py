#!/usr/bin/env python3
"""Verificações estáticas do repositório. Rode antes de todo push.

    python3 scripts/check.py

Sai com código 1 e lista os problemas se qualquer verificação falhar:

  1. nenhum caractere acentuado em site/assets/*.js e site/aulas/*/assets/*.js
  2. site/data/aulas.json é JSON válido e segue o contrato (campos, valores
     aceitos, os dois idiomas, slugs únicos)
  3. toda aula do JSON existe em disco nos dois idiomas, e toda pasta de aula
     em disco está no JSON
  4. por aula (e no hub): as mesmas chaves de window.STR em pt e en, as mesmas
     sections na mesma ordem, e todo id que o aula.js usa existe nos dois HTMLs
  5. todo href/src relativo dos HTMLs de site/ aponta para um arquivo que existe
     (e os absolutos /aulas/..., que só a 404 usa, também)
"""
import datetime
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SITE = RAIZ / "site"
INDICE = SITE / "data" / "aulas.json"

ACENTOS = re.compile(r"[áàâãéêíóôõúüç]")
STATUS = {"publicada", "rascunho"}
CORES = {"marker", "coral", "teal", "grape"}
IDIOMAS = ("pt-BR", "en")
SLUG_OK = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
COMENTARIO_HTML = re.compile(r"<!--.*?-->", re.S)
HEX = re.compile(r"^(?:[0-9A-Fa-f]{3}|[0-9A-Fa-f]{4}|[0-9A-Fa-f]{6}|[0-9A-Fa-f]{8})$")

problemas = []


def erro(secao, msg):
    problemas.append((secao, msg))


def rel(p):
    return p.relative_to(RAIZ).as_posix()


def ler(p):
    return p.read_text(encoding="utf-8")


# ---------------------------------------------------------------- 1. acentos
def checa_acentos():
    arquivos = sorted(SITE.glob("assets/*.js")) + sorted(SITE.glob("aulas/*/assets/*.js"))
    for arq in arquivos:
        for n, linha in enumerate(ler(arq).splitlines(), 1):
            if ACENTOS.search(linha):
                erro("acentos em JS", f"{rel(arq)}:{n}: {linha.strip()[:100]}")
    return len(arquivos)


# ------------------------------------------------------------- 2. aulas.json
def texto_ok(v):
    return isinstance(v, str) and v.strip() != ""


def checa_indice():
    try:
        dados = json.loads(ler(INDICE))
    except FileNotFoundError:
        erro("aulas.json", f"{rel(INDICE)} não existe")
        return None
    except ValueError as e:
        erro("aulas.json", f"JSON inválido: {e}")
        return None
    aulas = dados.get("aulas") if isinstance(dados, dict) else None
    if not isinstance(aulas, list):
        erro("aulas.json", 'o topo precisa ser {"aulas": [ ... ]}')
        return None
    vistos = set()
    validas = []
    for i, a in enumerate(aulas):
        repetido = False
        nome = f"aula #{i + 1}" + (f' ("{a.get("slug")}")' if isinstance(a, dict) and a.get("slug") else "")
        if not isinstance(a, dict):
            erro("aulas.json", f"{nome}: precisa ser um objeto")
            continue
        slug = a.get("slug")
        if not (isinstance(slug, str) and SLUG_OK.match(slug)):
            erro("aulas.json", f"{nome}: slug ausente ou inválido (letras minúsculas, números e hífens)")
        elif slug in vistos:
            erro("aulas.json", f'{nome}: slug "{slug}" repetido')
            repetido = True
        else:
            vistos.add(slug)
        if not (isinstance(a.get("ordem"), int) and not isinstance(a.get("ordem"), bool)):
            erro("aulas.json", f"{nome}: ordem precisa ser um inteiro")
        if a.get("status") not in STATUS:
            erro("aulas.json", f'{nome}: status "{a.get("status")}" não é "publicada" nem "rascunho"')
        dur = a.get("duracao_min")
        if not (isinstance(dur, int) and not isinstance(dur, bool) and dur > 0):
            erro("aulas.json", f"{nome}: duracao_min precisa ser um inteiro positivo")
        if not texto_ok(a.get("nivel")):
            erro("aulas.json", f"{nome}: nivel ausente")
        tags = a.get("tags")
        if not (isinstance(tags, list) and all(texto_ok(t) for t in tags)):
            erro("aulas.json", f"{nome}: tags precisa ser uma lista de textos")
        try:
            datetime.date.fromisoformat(a.get("atualizada_em") or "")
        except (TypeError, ValueError):
            erro("aulas.json", f"{nome}: atualizada_em precisa ser uma data AAAA-MM-DD")
        capa = a.get("capa")
        if not isinstance(capa, dict):
            erro("aulas.json", f"{nome}: capa ausente")
        else:
            if not texto_ok(capa.get("emoji")):
                erro("aulas.json", f"{nome}: capa.emoji ausente")
            if capa.get("cor") not in CORES:
                erro("aulas.json", f'{nome}: capa.cor "{capa.get("cor")}" não é {", ".join(sorted(CORES))}')
        idiomas_ok = True
        for lang in IDIOMAS:
            L = a.get(lang)
            if not isinstance(L, dict):
                erro("aulas.json", f'{nome}: falta o idioma "{lang}"')
                idiomas_ok = False
                continue
            for campo in ("titulo", "resumo", "url"):
                if not texto_ok(L.get(campo)):
                    erro("aulas.json", f"{nome}: {lang}.{campo} ausente")
                    idiomas_ok = False
        if isinstance(slug, str) and SLUG_OK.match(slug) and idiomas_ok and not repetido:
            validas.append(a)
    return validas


# ------------------------------------------------ 3. JSON <-> pastas em disco
def slugs_do_indice():
    dados = json.loads(ler(INDICE))
    return {a.get("slug") for a in dados.get("aulas", []) if isinstance(a, dict)}


def pagina_de(url):
    alvo = (SITE / url).resolve()
    return alvo / "index.html" if url.endswith("/") or alvo.is_dir() else alvo


def checa_disco(aulas, slugs_no_json):
    no_json = slugs_no_json
    for a in aulas:
        pasta = (SITE / "aulas" / a["slug"]).resolve()
        for lang in IDIOMAS:
            url = a[lang]["url"]
            pag = pagina_de(url)
            if pasta not in pag.parents:
                erro("JSON e disco", f'{a["slug"]}: {lang}.url "{url}" não aponta para dentro de site/aulas/{a["slug"]}/')
            elif not pag.is_file():
                erro("JSON e disco", f'{a["slug"]}: {lang}.url "{url}" não existe em disco ({rel(pag)})')
    if (SITE / "aulas").is_dir():
        for pasta in sorted(p for p in (SITE / "aulas").iterdir() if p.is_dir()):
            if pasta.name not in no_json:
                erro("JSON e disco", f"{rel(pasta)}/ existe em disco mas não está no aulas.json")


# ------------------------------------------- 4. pt x en: STR, sections e ids
def chaves_str(html_texto):
    """Chaves de primeiro nível do objeto literal window.STR = { ... }."""
    m = re.search(r"window\.STR\s*=\s*\{", html_texto)
    if not m:
        return None
    s, i, prof, chaves = html_texto, m.end(), 1, []
    espera_chave = True
    while i < len(s) and prof > 0:
        c = s[i]
        if s.startswith("//", i):
            i = s.find("\n", i)
            i = len(s) if i < 0 else i
            continue
        if s.startswith("/*", i):
            j = s.find("*/", i + 2)
            i = len(s) if j < 0 else j + 2
            continue
        if c in "\"'`":
            j, buf = i + 1, []
            while j < len(s) and s[j] != c:
                if s[j] == "\\":
                    j += 1
                buf.append(s[j] if j < len(s) else "")
                j += 1
            if prof == 1 and espera_chave and re.match(r"\s*:", s[j + 1:]):
                chaves.append("".join(buf))
                espera_chave = False
            i = j + 1
            continue
        if c in "{[(":
            prof += 1
        elif c in "}])":
            prof -= 1
        elif c == "," and prof == 1:
            espera_chave = True
        elif prof == 1 and espera_chave and (c.isalpha() or c in "_$"):
            m2 = re.match(r"[A-Za-z_$][\w$]*", s[i:])
            if re.match(r"\s*:", s[i + m2.end():]):
                chaves.append(m2.group())
                espera_chave = False
            i += m2.end()
            continue
        i += 1
    return chaves


def ids_html(html_texto):
    return set(re.findall(r'\bid="([^"]+)"', COMENTARIO_HTML.sub("", html_texto)))


def sections(html_texto):
    return re.findall(r'<section\b[^>]*\bid="([^"]+)"', COMENTARIO_HTML.sub("", html_texto))


def ids_js(js):
    ids = set()
    for m in re.finditer(r"""["'`]#([A-Za-z][\w-]*)""", js):
        if not HEX.match(m.group(1)):
            ids.add(m.group(1))
    for m in re.finditer(r"""\b(?:drawFig|figFail)\(\s*["']([\w-]+)["'](?:\s*,\s*["']([\w-]+)["'])?""", js):
        ids.update(g for g in m.groups() if g)
    return ids


def checa_par(nome, pt, en, js=None):
    for p in (pt, en):
        if not p.is_file():
            erro("pt e en", f"{nome}: {rel(p)} não existe")
            return
    hpt, hen = ler(pt), ler(en)
    kpt, ken = chaves_str(hpt), chaves_str(hen)
    if kpt is None or ken is None:
        faltando = [rel(p) for p, k in ((pt, kpt), (en, ken)) if k is None]
        erro("pt e en", f"{nome}: sem window.STR em {', '.join(faltando)}")
    else:
        for k in sorted(set(kpt) - set(ken)):
            erro("pt e en", f'{nome}: chave de STR "{k}" existe em pt e falta em en')
        for k in sorted(set(ken) - set(kpt)):
            erro("pt e en", f'{nome}: chave de STR "{k}" existe em en e falta em pt')
    spt, sen = sections(hpt), sections(hen)
    if spt != sen:
        erro("pt e en", f"{nome}: sections diferentes ou fora de ordem (pt {spt} / en {sen})")
    if js is not None:
        if not js.is_file():
            erro("pt e en", f"{nome}: {rel(js)} não existe")
            return
        usados = ids_js(ler(js))
        for lang, h in (("pt", hpt), ("en", hen)):
            for i in sorted(usados - ids_html(h)):
                erro("pt e en", f'{nome}: o aula.js usa #{i}, que não existe no HTML {lang}')


def checa_pares(aulas):
    checa_par("hub", SITE / "index.html", SITE / "en" / "index.html")
    for a in aulas:
        pasta = SITE / "aulas" / a["slug"]
        checa_par(a["slug"], pasta / "index.html", pasta / "en" / "index.html", pasta / "assets" / "aula.js")


# ------------------------------------------------------------ 5. href e src
def checa_links():
    total, vistos = 0, set()
    for pag in sorted(SITE.rglob("*.html")):
        texto = COMENTARIO_HTML.sub("", ler(pag))
        for m in re.finditer(r"""\b(?:href|src)\s*=\s*["']([^"']*)["']""", texto):
            url = m.group(1).strip()
            if not url or url.startswith("#") or re.match(r"^(?:[a-z][a-z0-9+.-]*:|//)", url, re.I):
                continue
            caminho = url.split("#")[0].split("?")[0]
            if not caminho or (pag, caminho) in vistos:
                continue
            vistos.add((pag, caminho))
            if caminho.startswith("/"):
                if not caminho.startswith("/aulas/") and caminho != "/aulas":
                    erro("links", f'{rel(pag)}: "{url}" é absoluto fora de /aulas/')
                    continue
                alvo = (SITE / caminho[len("/aulas"):].lstrip("/")).resolve()
            else:
                alvo = (pag.parent / caminho).resolve()
            total += 1
            if SITE.resolve() not in alvo.parents and alvo != SITE.resolve():
                erro("links", f'{rel(pag)}: "{url}" sai de site/')
                continue
            if caminho.endswith("/") or alvo.is_dir():
                alvo = alvo / "index.html"
            if not alvo.is_file():
                erro("links", f'{rel(pag)}: "{url}" aponta para {alvo.relative_to(RAIZ).as_posix()}, que não existe')
    return total


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    n_js = checa_acentos()
    aulas = checa_indice()
    if aulas is None:                       # indice ilegivel: nao da para comparar com o disco
        aulas = []
    else:
        checa_disco(aulas, slugs_do_indice())
    checa_pares(aulas)
    n_links = checa_links()
    if problemas:
        print(f"check.py: {len(problemas)} problema(s)\n")
        secao_atual = None
        for secao, msg in problemas:
            if secao != secao_atual:
                print(f"[{secao}]")
                secao_atual = secao
            print(f"  - {msg}")
        sys.exit(1)
    print(f"check.py: tudo certo — {n_js} arquivos JS sem acento, {len(aulas)} aula(s) no índice "
          f"conferidas em disco e nos dois idiomas, {n_links} links relativos resolvidos.")


if __name__ == "__main__":
    main()
