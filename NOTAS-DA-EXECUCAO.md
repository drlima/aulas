# Notas da execução

Decisões que o prompt de reestruturação (etapas 1 a 4) não cobria, tomadas sem
perguntar. Em cada uma, a alternativa escolhida foi a que muda menos coisa.

## Etapa 1 — textarea e .console sobem para aula.css

- **Posição dentro do aula.css.** As duas regras entraram logo depois de
  `th{...}` e antes do `@media(max-width:700px)` dos sliders e tabelas. É a
  mesma posição relativa que tinham no style.css original, então a ordem da
  cascata entre elas e as vizinhas não muda. Nenhuma outra regra mira
  `textarea` ou `.console`, e o conjunto de regras das três folhas somadas
  continua idêntico (131 regras, comparadas como multiconjunto de mídia,
  seletor e declarações). Capturas de página inteira antes e depois, com os
  details fechados e abertos, nas duas línguas e nas duas larguras: bit a bit
  iguais.
- **Comentário do topo do extra.css.** Ele citava "o editor e o console do
  bloco 8", que deixaram de morar ali. Tirei só essa menção; o resto do
  comentário ficou como estava.

## Etapa 2 — Documentação

- **A documentação descreve o que as etapas 3 e 4 ainda vão criar.** O prompt
  pede o CLAUDE.md antes do hub, do template e dos scripts. Para ele não nascer
  desatualizado, fixei antes os nomes que essas etapas usam (as chaves
  `hubMeta`, `hubNiveis`, `hubLoadError`, `hubEmpty` do `STR` do hub; o link
  `a.home` na nav; os parâmetros dos scripts) e escrevi o CLAUDE.md já com eles.
  No fim da etapa 4 conferi o texto contra o que foi construído.
- **O CLAUDE.md da aula fica dentro de `site/`, portanto é publicado.** Ele fica
  acessível em `/aulas/aulas/ml-intro/CLAUDE.md`, como o `GUIA_DO_PROFESSOR.md`
  já estava desde o tema 2. O prompt pede esse caminho, então mantive. O
  CLAUDE.md da raiz registra o aviso de que tudo em `site/` é público.
- **Mudança de conteúdo nas regras da aula: nenhuma.** As regras firmes foram
  transcritas do CLAUDE.md antigo. Acrescentei só dois fatos já verdadeiros no
  código e que decorrem delas: a saída esperada do "Rodar Python" (1.0 e 0.933),
  que é o que prova o `random_state=7`, e o aviso de que a ordem de
  `makeFruits()` e de `apts` define os pontos, porque o sorteio tem semente.
- **Contrato de ids da aula**: a tabela foi conferida por script contra os dois
  HTMLs e contra o `aula.js`. Todo id da tabela existe nos dois idiomas, e todo
  id que o `aula.js` lê está na tabela.
- **`nivel` no aulas.json é texto livre.** O prompt lista valores aceitos para
  `status` e `capa.cor`, mas não para `nivel`. Não inventei uma lista fechada: o
  hub traduz por `STR.hubNiveis` quando conhece o valor e mostra o texto como
  está quando não conhece.
- **`tags` aparecem como estão nos dois idiomas.** O JSON tem uma lista só de
  tags, em pt. Traduzir exigiria mudar o formato que o prompt fixou.
- **README**: a seção "Na aula ao vivo" falava da aula de ML em particular (os
  ~20 MB do bloco 8). Mantive a seção, reescrita para valer para qualquer aula, e
  apontei para o `GUIA_DO_PROFESSOR.md` de cada uma, onde os números da aula de
  ML já estão. Nenhuma dica se perdeu.
