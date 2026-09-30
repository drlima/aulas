#!/usr/bin/env python3
"""Verificador de fidelidade da aula github-windows.

    python3 scripts/verifica-github-windows.py

O CONTEUDO.md é a fonte da verdade da página. Este script extrai dele cada título,
parágrafo, item de lista, célula de tabela e bloco de código (tirando só a marcação
Markdown) e confere, no texto renderizado do index.html (sem executar JS), que:

  1. cada peça existe literalmente, e na mesma ordem do CONTEUDO.md;
  2. cada bloco de código é idêntico, caractere a caractere, ao <pre> correspondente;
  3. a página não traz texto que não esteja no CONTEUDO.md, a não ser os rótulos de
     interface listados em ROTULOS;
  4. os cinco domínios citados viram links que abrem em nova aba, e só eles;
  5. nem a página, nem seus assets, nem a entrada do aulas.json usam palavras de
     avaliação (lista em PROIBIDAS).

Termina em "TUDO BATE" (código 0) ou lista o que falta (código 1).
"""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
AULA = RAIZ / "site" / "aulas" / "github-windows"
CONTEUDO = AULA / "CONTEUDO.md"
PAGINA = AULA / "index.html"
INDICE = RAIZ / "site" / "data" / "aulas.json"

# Rótulos de interface que o HTML estático pode trazer dentro da capa e do <main>.
ROTULOS = ["Guia de consulta"]

# Domínios citados no CONTEUDO.md: texto visível -> destino do link.
LINKS = {
    "github.com/signup": "https://github.com/signup",
    "code.visualstudio.com": "https://code.visualstudio.com",
    "git-scm.com/download/win": "https://git-scm.com/download/win",
    "desktop.github.com": "https://desktop.github.com",
    "https://github.com/drlima/postech-tech-challenge-fase2-template":
        "https://github.com/drlima/postech-tech-challenge-fase2-template",
}

PROIBIDAS = re.compile(r"rubrica|avalia|\bnotas?\b", re.I)


# ------------------------------------------------------------ CONTEUDO.md
def tira_marcacao(texto):
    """Tira ** e * fora dos trechos de código em linha; os crases saem, o código fica como está."""
    codigos = []

    def guarda(m):
        codigos.append(m.group(1))
        return f"\x01{len(codigos) - 1}\x01"

    texto = re.sub(r"`([^`]*)`", guarda, texto)       # o negrito pode envolver um código em linha
    texto = re.sub(r"\*\*(.+?)\*\*", r"\1", texto)
    texto = re.sub(r"\*(.+?)\*", r"\1", texto)
    return re.sub(r"\x01(\d+)\x01", lambda m: codigos[int(m.group(1))], texto)


def espaco(texto):
    return re.sub(r"\s+", " ", texto).strip()


def pecas_do_conteudo():
    """Lista ordenada de ('texto'|'codigo', conteúdo)."""
    pecas, par, bloco = [], [], None

    def fecha_par():
        if par:
            pecas.append(("texto", espaco(tira_marcacao(" ".join(par)))))
            par.clear()

    for linha in CONTEUDO.read_text(encoding="utf-8").split("\n"):
        if bloco is not None:
            if linha.startswith("```"):
                pecas.append(("codigo", "\n".join(bloco)))
                bloco = None
            else:
                bloco.append(linha)
            continue
        if linha.startswith("```"):
            fecha_par()
            bloco = []
        elif not linha.strip():
            fecha_par()
        elif re.match(r"#{1,6} ", linha):
            fecha_par()
            pecas.append(("texto", espaco(tira_marcacao(re.sub(r"^#+ ", "", linha)))))
        elif linha.lstrip().startswith("|"):
            fecha_par()
            celulas = [c.strip() for c in linha.strip().strip("|").split("|")]
            if all(re.fullmatch(r":?-+:?", c) for c in celulas):
                continue
            for c in celulas:
                if c:
                    pecas.append(("texto", espaco(tira_marcacao(c))))
        elif re.match(r"\s*(?:[-*]|\d+\.) +", linha):
            fecha_par()
            par.append(re.sub(r"^\s*(?:[-*]|\d+\.) +", "", linha))
        else:
            par.append(linha.strip())
    fecha_par()
    return pecas


# ------------------------------------------------------------ index.html
BLOCOS = {"p", "li", "ul", "ol", "h1", "h2", "h3", "div", "section", "header", "main", "table", "thead",
          "tbody", "tr", "th", "td", "details", "summary", "br", "nav", "footer", "body"}


class Pagina(HTMLParser):
    """Texto renderizado da capa e do <main>: sem script/style/nav/footer, <pre> em marcadores."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.partes, self.pres, self.links = [], [], []
        self.dentro = 0        # dentro de header.hero ou main
        self.pilha = []        # tags abertas (nome, conta?)
        self.pre = None
        self.ignora = 0        # script, style, nav, footer
        self.a = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        conta = False
        if tag in ("script", "style", "nav", "footer"):
            self.ignora += 1
            conta = True
        elif tag == "main" or (tag == "header" and "hero" in (a.get("class") or "").split()):
            self.dentro += 1
            conta = True
        if tag not in ("br", "meta", "link", "img", "input", "hr"):
            self.pilha.append((tag, conta))
        if self.dentro and not self.ignora:
            if tag == "pre":
                self.pre = []
            elif tag == "a":
                self.a = {"href": a.get("href"), "target": a.get("target"), "rel": a.get("rel"), "texto": ""}
            if tag in BLOCOS and self.pre is None:
                self.partes.append(" ")

    def handle_endtag(self, tag):
        while self.pilha:
            nome, conta = self.pilha.pop()
            if conta:
                if nome in ("script", "style", "nav", "footer"):
                    self.ignora -= 1
                else:
                    self.dentro -= 1
            if nome == tag:
                break
        if self.dentro and not self.ignora:
            if tag == "pre" and self.pre is not None:
                self.pres.append("".join(self.pre))
                self.partes.append(f" \x00{len(self.pres) - 1}\x00 ")
                self.pre = None
            elif tag == "a" and self.a is not None:
                self.links.append(self.a)
                self.a = None
            if tag in BLOCOS and self.pre is None:
                self.partes.append(" ")

    def handle_data(self, data):
        if not self.dentro or self.ignora:
            return
        if self.pre is not None:
            self.pre.append(data)
        else:
            self.partes.append(data)
            if self.a is not None:
                self.a["texto"] += data


def main():
    problemas = []
    pecas = pecas_do_conteudo()
    pagina = Pagina()
    pagina.feed(PAGINA.read_text(encoding="utf-8"))
    texto = espaco("".join(pagina.partes))
    # cobertura[i] = True se o caractere i do texto foi explicado por uma peça
    cobertura = [False] * len(texto)
    pos, n_texto, n_codigo = 0, 0, 0
    proximo_pre = 0

    for tipo, conteudo in pecas:
        if tipo == "codigo":
            n_codigo += 1
            marca = f"\x00{proximo_pre}\x00"
            i = texto.find(marca, pos)
            if proximo_pre >= len(pagina.pres) or i < 0:
                problemas.append(f"bloco de código {n_codigo} não aparece na página, ou fora de ordem:\n      "
                                 + conteudo.replace("\n", "\n      "))
                continue
            real = pagina.pres[proximo_pre]
            if real != conteudo:
                problemas.append(f"bloco de código {n_codigo} difere do CONTEUDO.md:\n"
                                 f"    esperado: {conteudo!r}\n    na página: {real!r}")
            for k in range(i, i + len(marca)):
                cobertura[k] = True
            pos = i + len(marca)
            proximo_pre += 1
        else:
            n_texto += 1
            i = texto.find(conteudo, pos)
            if i < 0:
                ja = texto.find(conteudo)
                por_que = "existe, mas fora de ordem" if ja >= 0 else "não existe"
                problemas.append(f"texto {por_que} na página: {conteudo!r}")
                continue
            for k in range(i, i + len(conteudo)):
                cobertura[k] = True
            pos = i + len(conteudo)

    if proximo_pre != len(pagina.pres):
        problemas.append(f"a página tem {len(pagina.pres)} blocos <pre>; o CONTEUDO.md, {proximo_pre} casados")

    # texto na página que o CONTEUDO.md não explica (só os rótulos de ROTULOS são aceitos)
    sobra = "".join(c if not cobertura[i] else " " for i, c in enumerate(texto))
    for r in ROTULOS:
        sobra = sobra.replace(r, " ")
    sobra = espaco(sobra)
    if sobra:
        problemas.append(f"texto na página que não está no CONTEUDO.md: {sobra!r}")

    # links: os cinco domínios, abrindo em nova aba, e nenhum outro dentro do conteúdo
    achados = {l["texto"]: l for l in pagina.links}
    for txt, href in LINKS.items():
        l = achados.get(txt)
        if not l:
            problemas.append(f"domínio sem link: {txt}")
            continue
        if l["href"] != href:
            problemas.append(f"link de {txt} aponta para {l['href']}, esperado {href}")
        if l["target"] != "_blank" or "noopener" not in (l["rel"] or ""):
            problemas.append(f"link de {txt} não abre em nova aba com rel=noopener")
    for l in pagina.links:
        if l["texto"] not in LINKS:
            problemas.append(f"link fora da lista: {l['texto']!r} -> {l['href']}")

    # palavras de avaliação
    alvos = [PAGINA, AULA / "assets" / "aula.js", AULA / "assets" / "extra.css", CONTEUDO]
    for arq in alvos:
        for n, linha in enumerate(arq.read_text(encoding="utf-8").splitlines(), 1):
            m = PROIBIDAS.search(linha)
            if m:
                problemas.append(f"palavra proibida {m.group()!r} em {arq.relative_to(RAIZ).as_posix()}:{n}")
    for a in json.loads(INDICE.read_text(encoding="utf-8"))["aulas"]:
        if a["slug"] == "github-windows":
            m = PROIBIDAS.search(json.dumps(a, ensure_ascii=False))
            if m:
                problemas.append(f"palavra proibida {m.group()!r} na entrada do aulas.json")

    if problemas:
        print(f"verifica-github-windows: {len(problemas)} problema(s)\n")
        for p in problemas:
            print(f"  - {p}")
        sys.exit(1)
    print(f"{n_texto} textos (títulos, parágrafos, itens, células) e {n_codigo} blocos de código conferidos, "
          f"na ordem do CONTEUDO.md; {len(LINKS)} links em nova aba; nenhuma palavra proibida.")
    print("TUDO BATE")


if __name__ == "__main__":
    main()
