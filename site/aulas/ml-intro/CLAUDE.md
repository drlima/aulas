# CLAUDE.md — aula `ml-intro` (Machine Learning do zero)

Aula introdutória de Machine Learning, ao vivo (~1h30), para iniciantes absolutos.
Publicada em https://drlima.github.io/aulas/aulas/ml-intro/ (pt-BR) e
https://drlima.github.io/aulas/aulas/ml-intro/en/ (en-US).

As regras do repositório inteiro (camada compartilhada, API do core.js, i18n,
verificação, fluxo com o autor) estão no `CLAUDE.md` da raiz. Aqui fica só o que
vale para esta aula. `GUIA_DO_PROFESSOR.md`, nesta pasta, é o roteiro com tempos;
atualize-o quando a estrutura da página mudar.

## Estrutura pedagógica (não altere sem pedir)

Cada bloco segue o formato padrão do repositório: pergunta → widget → Revelar.

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

## Regras firmes, decididas com o autor

- **A palavra "modelo" só aparece a partir do bloco 5.** Nada antes disso pode
  parecer um modelo, nem regras à mão com esse nome. A conta que acende as
  caixas do bloco 4 fica, de propósito, sem nome.
- **O bloco 6 é apenas k-NN.** Reta/limiar e árvore foram tentadas ali e
  rejeitadas. A árvore vive no bloco 8.
- **Notebook/marimo foi tentado e descartado**: o autor quer HTML visual e
  dinâmico.
- **O fio de dados varia por bloco**: frutas nos blocos 3, 6 e 7; apartamentos
  nos blocos 4 e 5; Iris no bloco 8.
- **`random_state=7` no `train_test_split`.** Com 42 a acurácia de teste não cai,
  e o punch do bloco 7 morre. A saída esperada do "Rodar Python" é nota 1.0 nas
  flores vistas e 0.933 nas escondidas.
- **As frutas e os apartamentos saem do sorteio com semente do core** (`seed = 7`).
  A ordem das chamadas no `aula.js` define os pontos: trocar a ordem de
  `makeFruits()` e da montagem de `apts` muda o desenho de toda a aula.

## Contrato de ids desta aula

Os ids abaixo são lidos pelo `aula.js`. Pt e en têm exatamente os mesmos.
Renomeou em um idioma, renomeie no outro e no `aula.js`.

| Bloco | ids |
|---|---|
| seções | `s1` a `s10` |
| s1 | `rule`, `ruleBtn`, `ruleOut` |
| s2 | `learnCards`, `learnBtn`, `learnOut` |
| s3 | `lblToggle`, `svgLabels`, `lblLegend` |
| s4 | `ftArea`, `vArea`, `ftRooms`, `vRooms`, `ftYear`, `vYear`, `ftHood`, `priceKnob`, `priceTxt`, `binA`, `binB`, `quiz`, `quizOut` |
| s5 | `slA`, `vA`, `slB`, `vB`, `fitBtn`, `svgReg`, `errV` |
| s6 | `slK`, `vK`, `mapToggle`, `shuffleBtn`, `svgKnn`, `knnOut`, `stepBtn`, `stepK`, `svgSteps`, `stepOut` |
| s7 | `slHide`, `vHide`, `slK2`, `vK2`, `svgSplit`, `svgScore` |
| s8 | `py`, `runBtn`, `pyStatus`, `pyOut`, `vizBtn`, `vizNote`, `vizWrap`, `slKviz`, `vKviz`, `figKnn`, `imgKnn`, `codeKnn`, `slDepth`, `vDepth`, `figTree`, `imgTree`, `codeTree`, `cutsBtn`, `svgCuts`, `cutsOut` |
| s9 | `quiz9`, `quiz9Out` |

O `extra.css` desta aula também usa `#svgLabels`, `#svgReg`, `#svgKnn`,
`#svgSteps` e `#figTree` nos ajustes de telinha.

## Widgets a conferir antes do push

Testador de regras, cartões, etiquetas do bloco 3, sliders a/b + "deixar o
computador aprender", clique no playground k-NN, mapa de decisão, "Em câmera
lenta", sliders do bloco 7, quizzes dos blocos 4 e 9, "Rodar Python" e "Carregar
exemplos visuais" do bloco 8 (exigem rede), e "Ver os cortes" do 8b.
