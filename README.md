# Aula 1 — Machine Learning do zero

Aula ao vivo, interativa, para iniciantes absolutos. Páginas HTML estáticas hospedadas no
GitHub Pages, em português e inglês. Sem build, sem npm, sem framework, sem servidor.

**Português:** https://drlima.github.io/aulas/aulas/ml-intro/
**English:** https://drlima.github.io/aulas/aulas/ml-intro/en/

## Estrutura

| Arquivo | O que é |
|---|---|
| `site/index.html` | A aula em pt-BR: texto, widgets (SVG/JS puro) e o bloco de Python que roda no navegador. |
| `site/en/index.html` | A mesma aula em en-US. Mesmos ids, mesma ordem de seções. |
| `site/assets/style.css` | Todo o CSS, compartilhado pelas duas páginas. |
| `site/assets/app.js` | Todo o JS, compartilhado. Não contém nenhum texto de interface. |
| `GUIA_DO_PROFESSOR.md` | Roteiro com tempos e os *punches* de cada bloco. |
| `.github/workflows/deploy.yml` | Publica a pasta `site/` a cada push na `main`. |

## Como os dois idiomas funcionam

O HTML carrega o texto; o JS carrega o comportamento. Cada página define `window.STR`
num `<script>` inline **antes** de carregar `app.js`:

```html
<script>window.STR = { locale: "pt-BR", apple: "maçã", ... };</script>
<script src="assets/app.js"></script>
```

`app.js` lê tudo de `STR` e nunca contém texto de interface. Se você adicionar uma
mensagem nova ao JS, ela **tem** que sair de `STR`, ou a versão em inglês vai mostrar
português. Para conferir:

```bash
grep -nE "[áàâãéêíóôõúüç]" site/assets/app.js   # não deve retornar nada
```

### Onde ficam as strings

| Tipo de texto | Onde editar |
|---|---|
| Títulos, perguntas, Revelar, tabelas, referências | direto no HTML de cada idioma |
| Respostas do testador de regras, mensagens de acerto/erro, quiz, rótulos dos eixos, legendas das barras, status do Pyodide, resultado da votação | no bloco `window.STR` de cada HTML |
| Código Python dos painéis e das figuras | direto no HTML (`<pre><code class="py">` e `#codeTree`), com os comentários no idioma da página |

O Python das figuras do bloco 8 mora no HTML de propósito: o `app.js` executa exatamente
o mesmo texto que o aluno lê, então os dois não podem divergir, e a tradução acontece
junto com o resto da página.

## Editar

Abra os arquivos em qualquer editor. Para ver localmente, sirva a pasta por HTTP (os
caminhos relativos e o alternador PT · EN precisam disso):

```bash
python3 -m http.server --directory site 8000
# pt: http://localhost:8000/   ·   en: http://localhost:8000/en/
```

Cada bloco da aula é uma `<section class="block">` com um id de `s1` a `s10`. **Os ids
são o contrato entre o HTML e o `app.js`**: se você renomear um, renomeie nos dois
idiomas.

## Publicar

`git push` na `main`. O GitHub Pages precisa estar em **Source: GitHub Actions**
(Settings → Pages).

## Na aula ao vivo

- Peça que abram o link antes de começar. A página carrega instantaneamente; o que pesa é
  o bloco 8, e só quando o aluno pede.
- O bloco 8 baixa em duas etapas: ~20 MB de Python + scikit-learn no botão "Rodar Python",
  e ~10 MB de matplotlib no botão "Carregar exemplos visuais". Os dois exigem internet.
- As interações são individuais. Para votação da turma, use o chat da plataforma de vídeo.
