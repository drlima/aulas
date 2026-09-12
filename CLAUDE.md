# CLAUDE.md — repositório `aulas`

Hub de aulas interativas em HTML estático, publicado em https://drlima.github.io/aulas/
(pt-BR) e https://drlima.github.io/aulas/en/ (en-US). Cada aula mora numa pasta
própria sob `site/aulas/<slug>/` e tem o seu próprio `CLAUDE.md` com as regras que
valem só para ela. **Este arquivo trata do que vale para o repositório inteiro.**

Sem build, sem npm, sem framework. A única CDN é a do Pyodide (jsdelivr), mais as
fontes do Google. Deploy: todo push na `main` publica `site/` via
`.github/workflows/deploy.yml` (Pages em modo GitHub Actions).

## Mapa de pastas

```text
site/                      tudo aqui é publicado
  index.html               hub em pt-BR: lista as aulas lendo data/aulas.json
  en/index.html            hub em en-US
  404.html                 servida pelo Pages para qualquer caminho inexistente
  data/aulas.json          o índice das aulas (contrato abaixo)
  assets/
    base.css               esqueleto de qualquer página
    aula.css               componentes didáticos reutilizáveis
    core.js                motor das aulas, agnóstico de conteúdo
    hub.css, hub.js        só o hub
  aulas/<slug>/
    index.html             a aula em pt-BR
    en/index.html          a mesma aula em en-US
    assets/aula.js         o comportamento só desta aula
    assets/extra.css       o estilo só desta aula
    CLAUDE.md              regras firmes desta aula
    GUIA_DO_PROFESSOR.md   roteiro ao vivo, com tempos
template/                  molde de aula nova; fica FORA de site/ para não ser publicado
scripts/
  nova-aula.py             cria uma aula a partir de template/
  check.py                 verificações estáticas; rode antes de todo push
NOTAS-DA-EXECUCAO.md       decisões tomadas sem o autor, com o motivo
```

Tudo dentro de `site/` fica público, inclusive os `.md` das aulas. Não coloque em
`site/` nada que não possa ser lido por qualquer pessoa.

## A camada compartilhada

Uma aula carrega, nesta ordem, `base.css`, `aula.css`, `extra.css` e depois
`core.js`, `aula.js`. O hub carrega `base.css`, `hub.css`, `core.js`, `hub.js`.

- **`base.css`**: tokens da paleta e das fontes (`:root`), reset, tipografia
  (h1–h3, p, code, a), `.wrap` (coluna de 780px), `nav.map` com o link `.home`, o
  alternador `.lang` e a variante `.solo` (nav só com o alternador, sem o degradê
  de rolagem), `.hero`, `footer`, `.tag`. Não sabe que existe aula.
- **`aula.css`**: `section.block`, `.eyebrow`, `.q`, `mark`, `.widget` (e
  `.widget.wide`, até 980px com margem negativa simétrica), controles (`range`,
  `checkbox`, `text`, `button` com `.ghost`, `.small`), `.val`, `.out`, `.legend`,
  `.dot`, `details.reveal`, `.cards`/`.card`, `.quiz`, `.seg`, `.two`, tabelas,
  `details.code`, `pre` com o realce, o editor e o console do Python
  (`textarea`, `.console`), `.fig`/`.figmsg`, `.refs`, `h3.refgroup`.
- **`core.js`**: tudo o que qualquer aula pode usar (API abaixo). Declara; o
  `aula.js` de cada aula consome.

**Regra: o que é reutilizável sobe para a camada compartilhada, em vez de ser
copiado para uma segunda aula.** Se a aula nova precisa de algo que já existe
dentro do `aula.js` ou do `extra.css` de outra aula, mova para `core.js` ou
`aula.css`, generalize (sem ids nem textos de uma aula específica) e faça as duas
aulas usarem a versão compartilhada. Ao mover CSS, preserve a ordem da cascata.

Paleta: paper `#F3F6FB`, ink `#17203A`, marker `#FFD84D`, coral `#FF6B57`, teal
`#1BA39C`, grape `#7B61FF`. Fontes: Bricolage Grotesque (títulos), Source Serif 4
(texto), JetBrains Mono (código).

## API pública do core.js

| Nome | Assinatura | O que faz |
|---|---|---|
| `S` | `window.STR` | os textos da página; o core só lê |
| `T` | `T(tpl, vars) → string` | troca `{chave}` em `tpl` pelos valores de `vars` |
| `$` | `$(sel) → Element` | `document.querySelector` |
| `$$` | `$$(sel) → Element[]` | `querySelectorAll`, já como array |
| `el` | `el(tag, attrs={}, parent?) → SVGElement` | cria elemento SVG, aplica atributos, anexa a `parent` |
| `fmt` | `fmt(n) → string` | número formatado em `S.locale` |
| `esc` | `esc(texto) → string` | escapa `&`, `<`, `>` para inserir como HTML |
| `rnd` | `rnd() → number` | sorteio em [0, 1) com semente global `seed` (começa em 7) |
| `gauss` | `gauss() → number` | normal padrão, a partir de `rnd` |
| `C` | `{coral, teal, ink, grey, line}` | a paleta, em hex, para desenhar em SVG |
| `quizPair` | `quizPair(boxSel, outSel, itens, L)` | quiz de duas alternativas; item `[enunciado, valorCerto]`; `L = {opts:[[valor,rótulo],[valor,rótulo]], answer(valor)→texto, done(saída, certos, total)}` |
| `quizOptions` | `quizOptions(boxSel, outSel, itens, L)` | quiz de N alternativas; item `[enunciado, [opções], índiceCerto]`; `L = {done(saída, certos, total)}` |
| `scale` | `scale(B, W, H, pad) → {X(pt), Y(pt)}` | leva o domínio `B = {x0,x1,y0,y1}` para um SVG W×H com margem `pad`; `X`/`Y` recebem `{x,y}` |
| `axes` | `axes(svg, W, H, pad, rótuloX, rótuloY)` | desenha os dois eixos e os rótulos |
| `highlight` | `highlight(src) → html` | realce de sintaxe de Python; a aula aplica em `pre code.py` |
| `PyUI` | `{statusSel, onFigFail}` | a aula registra onde o andamento aparece e o que fazer quando uma figura falha |
| `getPy` | `getPy() → Promise<pyodide>` | baixa Pyodide + scikit-learn uma vez só; escreve o andamento em `PyUI.statusSel` |
| `getViz` | `getViz() → Promise<pyodide>` | `getPy` + matplotlib |
| `drawFig` | `drawFig(boxId, imgId, código, globais) → Promise<bool>` | roda `código` (que devolve um PNG em base64) e mostra em `#imgId` dentro de `#boxId` |
| `figFail` | `figFail(boxId, msg)` | troca a figura por uma mensagem de erro visível |

O core também liga, sozinho, o realce do link da `nav.map` conforme a rolagem.
Chaves de `STR` que o core lê: `locale`, `pyDownload`, `pySklearn`, `pyReady`,
`pyNetError`, `vizDownload`, `vizFail`, `vizFailStatus`.

## i18n

- **Nenhum texto de interface em JS.** Nem no core, nem no `hub.js`, nem no
  `aula.js`. Todo texto sai de `window.STR`, definido num `<script>` inline no
  HTML, antes dos scripts. Comentários em JS também vão sem acento, para que a
  verificação abaixo seja exata:
  `grep -rnE "[áàâãéêíóôõúüç]" site/assets/*.js site/aulas/*/assets/*.js` deve
  voltar vazio.
- pt e en têm as **mesmas chaves** de `STR`, os **mesmos ids** e as **mesmas
  seções, na mesma ordem**. Renomeou em um idioma, renomeie no outro.
- A versão pt fica em `.../`, a en em `.../en/`. Os caminhos relativos da en têm
  um `../` a mais.

## Contrato do site/data/aulas.json

```json
{ "aulas": [ {
  "slug": "ml-intro", "ordem": 1, "status": "publicada", "duracao_min": 90,
  "nivel": "iniciante", "tags": ["..."], "atualizada_em": "AAAA-MM-DD",
  "capa": { "emoji": "🤖", "cor": "grape" },
  "pt-BR": { "titulo": "...", "resumo": "...", "url": "aulas/<slug>/" },
  "en":    { "titulo": "...", "resumo": "...", "url": "aulas/<slug>/en/" }
} ] }
```

- `slug`: nome da pasta em `site/aulas/`; único.
- `ordem`: inteiro; o hub mostra em ordem crescente.
- `status`: `"publicada"` ou `"rascunho"`. Rascunho **não aparece** no hub.
- `duracao_min`: inteiro, em minutos.
- `nivel`: texto livre; o hub traduz por `STR.hubNiveis` e, se não achar, mostra
  como está. Hoje há rótulo para `iniciante`, `intermediario` e `avancado`.
- `tags`: lista de textos, mostrados como estão nos dois idiomas.
- `capa.cor`: um token da paleta, `marker`, `coral`, `teal` ou `grape`.
- `url`: relativa à raiz de `site/`.
- `pt-BR` e `en`: os dois obrigatórios, cada um com `titulo`, `resumo` e `url`.

O hub (`site/index.html` e `site/en/index.html`) define, inline e antes dos
scripts, `window.HUB = { json, lang, base }` (o caminho do JSON, `"pt-BR"` ou
`"en"`, e o prefixo dos links dos cards) e as chaves de `STR` que o `hub.js` lê:
`hubMeta` (o molde `"{min} min · nível {nivel}"`), `hubNiveis`, `hubEmpty` e
`hubLoadError`. Se o JSON não carregar, o hub mostra `hubLoadError` no lugar
dos cards.

## Formato pedagógico padrão

Cada bloco é uma `section.block` com id e segue **pergunta (`div.q`) → widget
(`div.widget`) → `details.reveal`** (o punch). O aluno pensa, mexe, erra, e só
depois abre a resposta. Painéis `details.code` ("O mesmo, em Python") são
apêndice: vêm depois do widget e **nunca o substituem**.

## Criar uma aula nova

```bash
python3 scripts/nova-aula.py <slug>
```

O script pergunta título, resumo e duração, copia `template/` para
`site/aulas/<slug>/`, troca os marcadores e acrescenta a aula ao `aulas.json` como
`"rascunho"`, com a próxima `ordem`. Recusa slug que já existe. Depois:

1. Escreva os blocos nos dois HTMLs; os do template mostram cada padrão pronto.
2. Apague o bloco de Python se a aula não usa Python.
3. Traduza a versão en, que nasce com o título e o resumo em pt, e acerte os
   dois idiomas no `aulas.json`, junto com `nivel`, `tags` e `capa`.
4. Preencha o `CLAUDE.md` e o `GUIA_DO_PROFESSOR.md` da aula.
5. Rode `python3 scripts/check.py`. Quando a aula estiver pronta, troque o
   `status` para `"publicada"`.

## Verificar antes do push

```bash
python3 -m http.server --directory site 8000   # hub: /  en: /en/  aula: /aulas/<slug>/
python3 scripts/check.py                       # sai com código 1 e lista o que falhou
```

`check.py` confere: nenhum acento nos JS; `aulas.json` válido e completo; toda
aula do JSON existe em disco nos dois idiomas, e vice-versa; por página, as mesmas
chaves de `STR` em pt e en; os ids de `section` e os ids que o `aula.js` usa
existem nos dois HTMLs; todo `href`/`src` relativo aponta para um arquivo que
existe.

Depois, com Playwright, em 1280px e 390px, nas duas línguas:

- zero erro de console em todas as páginas;
- nada além da largura da viewport em 390px (containers com rolagem própria, como a
  `nav.map` e tabelas, podem ter conteúdo mais largo dentro);
- o hub mostra os cards publicados, o card abre a aula no idioma certo, o
  alternador PT · EN vai e volta, e o link "Todas as aulas" de cada aula volta ao
  hub no idioma certo;
- os widgets da aula respondem (a lista de cada aula está no `CLAUDE.md` dela);
- o 404: o `http.server` não serve `404.html`, e ela usa caminhos absolutos
  (`/aulas/...`); confira na página publicada, abrindo um caminho inexistente.

Blocos com Pyodide exigem rede. Se o ambiente não tiver, diga isso em vez de
assumir que funcionam.

## Fluxo de trabalho com o autor

O autor avalia a página publicada e devolve prompts com correções numeradas.
Faça commits por tema, um push ao final de cada tema, confirme o deploy verde
(`gh run watch`) e entregue: o que mudou, screenshots das partes afetadas nas duas
línguas, e toda decisão tomada por conta própria. Pergunte antes de qualquer coisa
fora do que foi pedido; se o prompt mandar seguir sem perguntar, escolha a opção
que muda menos coisa e registre em `NOTAS-DA-EXECUCAO.md`. Encontrou algo fora do
escopo que parece errado? Anote e reporte, não corrija.
