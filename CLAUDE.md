# CLAUDE.md — contexto do projeto aula-ml

Aula introdutória de Machine Learning, ao vivo (~1h30), para iniciantes absolutos.
Publicada em https://drlima.github.io/aula-ml/ (pt-BR) e https://drlima.github.io/aula-ml/en/ (en-US).

## O que este repositório é

- Uma página estática por idioma: `site/index.html` e `site/en/index.html`.
- `site/assets/style.css` e `site/assets/app.js` são compartilhados. **Nenhum texto de interface no JS**: tudo vem de `window.STR`, definido inline em cada HTML antes de `app.js`. Confira com `grep -nE "[áàâãéêíóôõúüç]" site/assets/app.js` (deve retornar vazio).
- Sem build, sem npm, sem framework, sem CDN além do Pyodide (jsdelivr) e das fontes do Google.
- Deploy: push na `main` publica `site/` via `.github/workflows/deploy.yml` (Pages em modo GitHub Actions).
- `GUIA_DO_PROFESSOR.md` é o roteiro com tempos; atualize-o quando a estrutura da página mudar.

## Estrutura pedagógica (não altere sem pedir)

Formato de cada bloco: **pergunta (`div.q`) → widget interativo (`div.widget`) → `details.reveal` (o punch)**. Painéis `details.code` ("O mesmo, em Python") são apêndice e nunca substituem o widget.

| id | Bloco | Ideia |
|---|---|---|
| s1 | Regras | regras à mão não escalam; ML inverte a lógica |
| s2 | Aprender | Mitchell: tarefa / experiência / desempenho |
| s3 | Gabarito | frutas peso×doçura; supervisionado vs não; dados viram números |
| s4 | Rótulo ou número | classificação vs regressão; quiz |
| s5 | Modelo = fórmula | `preço = a×área + b`; sliders e ajuste automático. **Centro da aula.** |
| s6 | Vizinhos | k-NN, só k-NN: playground de 60 frutas → código → Revelar → "Em câmera lenta" |
| s7 | Armadilha | treino vs teste; k como hiperparâmetro |
| s8 | Python | Pyodide + scikit-learn; fronteira de decisão e árvore (matplotlib); "árvore vista de cima" |
| s9 | Mapa | resumo, perguntas abertas, quiz de autoavaliação |
| s10 | Referências | links verificados |

Regras firmes, decididas com o autor:
- A palavra "modelo" só aparece a partir do bloco 5. Nada antes disso pode parecer um modelo (nem regras à mão com esse nome).
- O bloco 6 é apenas k-NN. Reta/limiar e árvore ali foram tentados e rejeitados. A árvore vive no bloco 8.
- Notebook/marimo foi tentado e descartado: o autor quer HTML visual e dinâmico.
- Exemplos variam por bloco; o fio de dados é frutas (3, 6, 7), apartamentos (4, 5), Iris (8).
- `random_state=7` no `train_test_split`: com 42 a acurácia de teste não cai e o punch do bloco 7 morre.

## Design

Paleta: paper `#F3F6FB`, ink `#17203A`, marker `#FFD84D`, coral `#FF6B57` (laranja), teal `#1BA39C` (maçã), grape `#7B61FF`. Fontes: Bricolage Grotesque (títulos), Source Serif 4 (texto), JetBrains Mono (código). Coluna de texto 780px; widgets que precisam de espaço usam `.widget.wide` (até 980px, margem negativa simétrica).

## Contrato HTML ↔ JS

Os ids das seções (`s1`–`s10`) e dos widgets (`#svgKnn`, `#slK`, `#stepBtn`, `#slHide`, `#py`, `#runBtn`, `#vizBtn`, `#slKviz`, `#slDepth`, `#cutsBtn`…) são lidos pelo `app.js`. Renomeou em um idioma, renomeie no outro. Os dois HTMLs têm as mesmas seções, na mesma ordem, com os mesmos ids.

## Como verificar antes de dar push

```bash
python3 -m http.server --directory site 8000   # pt: /  en: /en/
```

Com Playwright, em 1280px e 390px, nas duas línguas: zero erros de console; todos os links da nav visíveis em 1280px; nenhum elemento além da largura da viewport em 390px; os widgets respondem (regra, cartões, etiquetas, sliders a/b + "deixar o computador aprender", clique no playground, mapa de decisão, "Em câmera lenta", sliders do bloco 7, quizzes dos blocos 4 e 9). O bloco 8 exige rede (Pyodide); se o ambiente não tiver, diga isso em vez de assumir que funciona.

## Fluxo de trabalho com o autor

O autor avalia a página publicada e devolve prompts com correções numeradas. Faça commits por tema, um push ao final de cada tema, confirme o deploy verde (`gh run watch`) e entregue: o que mudou, screenshots dos blocos afetados nas duas línguas, e qualquer decisão tomada por conta própria. Pergunte antes de qualquer coisa fora do que foi pedido.
