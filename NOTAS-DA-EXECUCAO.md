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
