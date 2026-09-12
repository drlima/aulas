# Aulas

Um hub de aulas ao vivo e interativas, para iniciantes. Cada aula é uma página HTML
estática, em português e inglês, com widgets para mexer, errar e só depois ver a
resposta. Sem build, sem npm, sem framework, sem servidor: tudo roda no navegador.

**Hub em português:** https://drlima.github.io/aulas/
**Hub in English:** https://drlima.github.io/aulas/en/

## Aulas disponíveis

| Aula | Português | English |
|---|---|---|
| Machine Learning do zero | [abrir](https://drlima.github.io/aulas/aulas/ml-intro/) | [open](https://drlima.github.io/aulas/aulas/ml-intro/en/) |

A lista que o hub mostra vem de `site/data/aulas.json`.

## Estrutura

| Caminho | O que é |
|---|---|
| `site/index.html`, `site/en/index.html` | O hub, que lê `site/data/aulas.json` e mostra um card por aula publicada. |
| `site/data/aulas.json` | O índice das aulas: título, resumo, duração, nível, status. |
| `site/assets/` | A camada compartilhada: `base.css`, `aula.css` e `core.js` servem todas as aulas; `hub.css` e `hub.js` servem o hub. |
| `site/aulas/<slug>/` | Uma aula: `index.html` (pt), `en/index.html`, `assets/aula.js`, `assets/extra.css`, `CLAUDE.md` e `GUIA_DO_PROFESSOR.md`. |
| `site/404.html` | A página de caminho inexistente, com link para o hub. |
| `template/` | O molde de aula nova. Fica fora de `site/` para não ser publicado. |
| `scripts/` | `nova-aula.py` cria uma aula; `check.py` verifica o repositório. |
| `.github/workflows/deploy.yml` | Publica `site/` a cada push na `main`. |

## Como os dois idiomas funcionam

O HTML carrega o texto; o JS carrega o comportamento. Cada página define
`window.STR` num `<script>` inline **antes** dos scripts, e nenhum JS contém texto
de interface. Assim a versão em inglês nunca mostra português por acidente. As
duas versões de cada página têm as mesmas chaves de `STR`, os mesmos ids e as
mesmas seções na mesma ordem.

## Criar uma aula

```bash
python3 scripts/nova-aula.py minha-aula
```

O script pergunta título, resumo e duração, cria `site/aulas/minha-aula/` a partir
do template e registra a aula como rascunho no `aulas.json`. Rascunhos não aparecem
no hub. Os passos seguintes estão no `CLAUDE.md` da raiz.

## Ver localmente e verificar

```bash
python3 -m http.server --directory site 8000
# hub: http://localhost:8000/   ·   en: http://localhost:8000/en/
python3 scripts/check.py
```

Sirva por HTTP, e não abrindo o arquivo direto: o hub busca o `aulas.json` e os
caminhos relativos precisam de um servidor.

## Na aula ao vivo

- Peça que abram o link antes de começar. As páginas carregam na hora; o que pesa são
  os blocos de Python, e só quando o aluno pede. Eles exigem internet.
- As interações são individuais. Para votação da turma, use o chat da plataforma de vídeo.
- O roteiro com tempos de cada aula está no `GUIA_DO_PROFESSOR.md` da pasta dela.

## Publicar

`git push` na `main`. O GitHub Pages precisa estar em **Source: GitHub Actions**
(Settings → Pages).
