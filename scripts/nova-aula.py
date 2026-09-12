#!/usr/bin/env python3
"""Cria uma aula nova a partir de template/.

    python3 scripts/nova-aula.py <slug>

Pergunta título, resumo e duração no terminal, copia template/ para
site/aulas/<slug>/ trocando os marcadores __SLUG__, __TITULO__, __RESUMO__ e
__DURACAO__, e acrescenta a aula ao site/data/aulas.json como "rascunho", com
`ordem` igual à maior existente + 1.

Escreve só essas duas coisas. Recusa-se a rodar se o slug já existe, em disco
ou no aulas.json.
"""
import datetime
import html
import json
import re
import sys
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
TEMPLATE = RAIZ / "template"
AULAS = RAIZ / "site" / "aulas"
INDICE = RAIZ / "site" / "data" / "aulas.json"
SLUG_OK = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def falha(msg):
    print(f"nova-aula: {msg}", file=sys.stderr)
    sys.exit(1)


def sem_acento(texto):
    """Para .js e .css, onde a regra da casa proíbe acentos até em comentário."""
    base = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in base if not unicodedata.combining(c))


def formata_indice(dados):
    """Escreve o aulas.json no mesmo desenho do arquivo à mão: um campo por linha,
    listas e a capa numa linha só, os dois idiomas abertos."""
    d = lambda v: json.dumps(v, ensure_ascii=False)
    linhas = ["{", '  "aulas": [']
    aulas = dados["aulas"]
    for i, aula in enumerate(aulas):
        linhas.append("    {")
        campos = list(aula.items())
        for j, (k, v) in enumerate(campos):
            virgula = "," if j < len(campos) - 1 else ""
            if isinstance(v, dict) and k in ("pt-BR", "en"):
                linhas.append(f"      {d(k)}: {{")
                sub = list(v.items())
                for m, (kk, vv) in enumerate(sub):
                    linhas.append(f"        {d(kk)}: {d(vv)}" + ("," if m < len(sub) - 1 else ""))
                linhas.append("      }" + virgula)
            elif isinstance(v, dict):
                dentro = ", ".join(f"{d(kk)}: {d(vv)}" for kk, vv in v.items())
                linhas.append(f"      {d(k)}: {{ {dentro} }}" + virgula)
            else:
                linhas.append(f"      {d(k)}: {d(v)}" + virgula)
        linhas.append("    }" + ("," if i < len(aulas) - 1 else ""))
    linhas += ["  ]", "}"]
    return "\n".join(linhas) + "\n"


def pergunta(rotulo, valida=lambda s: bool(s), erro="não pode ficar vazio"):
    while True:
        try:
            valor = input(rotulo).strip()
        except EOFError:
            falha("entrada encerrada antes de responder tudo; nada foi escrito")
        if valida(valor):
            return valor
        print(f"  {erro}.")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stdin, "reconfigure"):
        sys.stdin.reconfigure(encoding="utf-8", errors="replace")
    if len(sys.argv) != 2:
        falha("uso: python3 scripts/nova-aula.py <slug>")
    slug = sys.argv[1]
    if not SLUG_OK.match(slug):
        falha(f'slug "{slug}" inválido: use só letras minúsculas sem acento, números e hífens (ex.: estatistica-basica)')
    destino = AULAS / slug
    if destino.exists():
        falha(f"{destino.relative_to(RAIZ).as_posix()} já existe; escolha outro slug")
    if not TEMPLATE.is_dir():
        falha("pasta template/ não encontrada")
    try:
        dados = json.loads(INDICE.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        falha(f"não consegui ler {INDICE.relative_to(RAIZ).as_posix()}: {e}")
    if any(a.get("slug") == slug for a in dados.get("aulas", [])):
        falha(f'o slug "{slug}" já está no aulas.json; escolha outro')

    print(f"Aula nova: {slug}")
    titulo = pergunta("Título (pt-BR): ")
    resumo = pergunta("Resumo, uma frase (pt-BR): ")
    duracao = pergunta("Duração em minutos: ", lambda s: s.isdigit() and int(s) > 0,
                       "responda com um número inteiro de minutos")

    trocas = {"__SLUG__": slug, "__TITULO__": titulo, "__RESUMO__": resumo, "__DURACAO__": duracao}

    def preenche(texto, sufixo):
        for marca, valor in trocas.items():
            if sufixo == ".html":
                valor = html.escape(valor, quote=True)
            elif sufixo in (".js", ".css"):
                valor = sem_acento(valor).replace("*/", "* /")
            texto = texto.replace(marca, valor)
        return texto

    # monta tudo em memória antes de escrever qualquer coisa
    arquivos = {}
    for origem in sorted(TEMPLATE.rglob("*")):
        if origem.is_file():
            conteudo = origem.read_text(encoding="utf-8")
            arquivos[destino / origem.relative_to(TEMPLATE)] = preenche(conteudo, origem.suffix.lower())

    ordem = max((a.get("ordem", 0) for a in dados.get("aulas", [])), default=0) + 1
    dados.setdefault("aulas", []).append({
        "slug": slug,
        "ordem": ordem,
        "status": "rascunho",
        "duracao_min": int(duracao),
        "nivel": "iniciante",
        "tags": [],
        "atualizada_em": datetime.date.today().isoformat(),
        "capa": {"emoji": "📘", "cor": "grape"},
        "pt-BR": {"titulo": titulo, "resumo": resumo, "url": f"aulas/{slug}/"},
        "en": {"titulo": titulo, "resumo": resumo, "url": f"aulas/{slug}/en/"},
    })
    indice_novo = formata_indice(dados)

    for caminho, conteudo in arquivos.items():
        caminho.parent.mkdir(parents=True, exist_ok=True)
        with open(caminho, "w", encoding="utf-8", newline="\n") as f:
            f.write(conteudo)
    with open(INDICE, "w", encoding="utf-8", newline="\n") as f:
        f.write(indice_novo)

    print(f"\nCriada {destino.relative_to(RAIZ).as_posix()}/ ({len(arquivos)} arquivos) e registrada no aulas.json")
    print(f'como "rascunho", ordem {ordem}. Ela não aparece no hub até virar "publicada".')
    print("\nPróximos passos:")
    print("  1. Escreva os blocos em index.html e en/index.html.")
    print("  2. Apague o bloco 4 (e o trecho dele no aula.js) se a aula não usa Python.")
    print("  3. Traduza a versão en: ela nasce com o título e o resumo em pt, no HTML e no aulas.json.")
    print("  4. Acerte nivel, tags e capa no aulas.json; preencha CLAUDE.md e GUIA_DO_PROFESSOR.md.")
    print("  5. Rode python3 scripts/check.py.")


if __name__ == "__main__":
    main()
