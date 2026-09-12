# CLAUDE.md — aula `__SLUG__` (__TITULO__)

__RESUMO__

Aula ao vivo, com cerca de __DURACAO__ minutos. Publicada em
https://drlima.github.io/aulas/aulas/__SLUG__/ (pt-BR) e
https://drlima.github.io/aulas/aulas/__SLUG__/en/ (en-US).

As regras do repositório inteiro (camada compartilhada, API do core.js, i18n,
verificação, fluxo com o autor) estão no `CLAUDE.md` da raiz. Aqui fica só o que
vale para esta aula. `GUIA_DO_PROFESSOR.md`, nesta pasta, é o roteiro com tempos;
atualize-o quando a estrutura da página mudar.

## Estado

Rascunho criado a partir de `template/`. Enquanto o `status` no
`site/data/aulas.json` for `"rascunho"`, a aula não aparece no hub, mas a página
já é publicada no endereço acima.

## Estrutura pedagógica

Cada bloco segue o formato padrão do repositório: pergunta → widget → Revelar.
Substitua esta tabela pela da aula real.

| id | Bloco | Ideia |
|---|---|---|
| s1 | Desenho | exemplo de widget com SVG (`scale` + `axes`) |
| s2 | Duas opções | exemplo de `quizPair` |
| s3 | Várias opções | exemplo de `quizOptions` e de painel "O mesmo, em Python" |
| s4 | Python | exemplo de Pyodide e de figura com `drawFig`; apague se a aula não usa Python |
| s5 | Referências | links conferidos |

## Regras firmes, decididas com o autor

Nenhuma ainda. Registre aqui cada decisão que o autor tomar sobre esta aula e o
motivo, para que ela não seja desfeita numa correção futura.

## Contrato de ids desta aula

Os ids abaixo são lidos pelo `aula.js`. Pt e en têm exatamente os mesmos.

| Bloco | ids |
|---|---|
| seções | `s1` a `s5` |
| s1 | `slDemo`, `vDemo`, `svgDemo`, `demoOut` |
| s2 | `quiz`, `quizOut` |
| s3 | `quiz3`, `quiz3Out` |
| s4 | `py`, `runBtn`, `pyStatus`, `pyOut`, `vizBtn`, `vizNote`, `vizWrap`, `slFig`, `vFig`, `figDemo`, `imgDemo`, `codeDemo` |

## Widgets a conferir antes do push

Slider do bloco 1, os dois quizzes, "Rodar Python" e "Carregar a figura" do bloco
4 (exigem rede).
