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

## Etapa 3 — Índice e hub

- **Resumo no aulas.json**: a primeira frase da lead de cada versão, sem editar.
  A frase seguinte da lead ("Sem matemática pesada...") ficou de fora para o
  resumo continuar sendo uma frase só.
- **O hub carrega core.js antes do hub.js.** O prompt fala só das folhas de
  estilo do hub. O hub.js precisa de `$`, `esc` e `T`, que já existem no core;
  copiar esses helpers para o hub.js contrariaria a regra de que o reutilizável
  mora na camada compartilhada. No hub, o core não faz nada sozinho além disso:
  o realce da nav não acha seções e o Pyodide só baixa quando alguém chama.
- **Textos do hub, escolhidos por mim**: título "Aulas" / "Lessons" e uma linha
  sobre o que é, no mesmo tom da lead da aula. Título da aba "Aulas interativas"
  / "Interactive lessons". Sem rodapé e sem eyebrow: o prompt pede barra, hero e
  grade, e o `.eyebrow` mora no aula.css, que o hub não carrega.
- **O card mostra** emoji e cor da capa, título, resumo, a linha
  "90 min · nível iniciante" (chave `hubMeta`, um molde só, porque a ordem das
  palavras muda entre pt e en) e as tags. `atualizada_em` não aparece: o prompt
  cita tags e nível como informação do card, e não a data. O card inteiro é o
  link.
- **Mensagens no lugar dos cards**: além da falha de carregamento
  (`hubLoadError`), acrescentei `hubEmpty` para quando não há nenhuma aula
  publicada. Sem ela, um aulas.json só com rascunhos deixaria a grade em branco.
- **Valores fora do contrato não quebram o hub**: `capa.cor` desconhecida cai em
  `grape`; uma aula sem o objeto do idioma da página não gera card. O check.py
  impede os dois casos antes do push.
- **`.wrap.wide` (980px) no hero e na grade do hub**, para os dois alinharem à
  esquerda. É a mesma largura que o `.widget.wide` já usa nas aulas.
- **`nav.map.solo` no base.css.** Em 390px, o degradê que a nav usa para sugerir
  rolagem desbotava o "EN", porque no hub e na 404 não há nada para rolar. A
  regra fica no base.css, e não no hub.css, porque a 404 só carrega o base.css.
  A nav da aula não tem a classe e não muda.
- **Link "Todas as aulas" sem CSS novo.** Ele usa o estilo dos outros links da
  nav. Em 1280px a nav continua com duas linhas e 89px, os 12 links visíveis;
  em 390px ele entra na faixa que já rola sozinha. Conferido por pixels: nas
  duas línguas e larguras, com os details fechados e abertos, toda diferença na
  aula está dentro da faixa da nav, e a altura da página não mudou.
- **404 bilíngue.** Ela é uma só para qualquer caminho, então não tem como saber
  o idioma de quem chegou. Título e frase em pt, uma linha em en, e o alternador
  PT · EN apontando para os dois hubs. Leva `noindex`.
- **Como a 404 foi testada localmente.** O `http.server` não serve `404.html`, e
  os caminhos absolutos `/aulas/...` só batem com o Pages. Usei um servidor de
  teste, fora do repositório, que serve `site/` sob `/aulas/` e devolve a 404
  para caminhos inexistentes. O único erro de console ali é o próprio status 404
  do documento, que o navegador sempre registra. Depois do deploy, conferi também
  no Pages.

## Etapa 4 — Template e scripts

- **Os caminhos do template já são os de dentro de `site/aulas/<slug>/`.** Em
  `template/` eles não resolvem, porque o template só existe para ser copiado. O
  check.py olha só `site/`, então não reclama.
- **O STR do template traz as chaves do core e as dos quizzes, e não as do hub.**
  O prompt pede "as do hub/quiz". Uma aula não lê nenhuma chave do hub (quem lê é
  o hub.js, nas páginas do hub), e colocá-las na aula faria o check.py exigir as
  mesmas chaves inúteis em toda aula nova. Li como as chaves de quiz.
- **O template en está em inglês, comentários incluídos**, exceto a linha
  "APAGUE ESTE BLOCO INTEIRO SE A AULA NÃO USA PYTHON", que o prompt pede com
  esse texto e aparece igual nos dois HTMLs.
- **O trecho do bloco 4 no aula.js do template é marcado, não protegido por `if`.**
  Um comentário manda apagá-lo junto com o bloco do HTML. Se o autor esquecer, a
  página dá erro no console e o check.py aponta cada id que ficou sem HTML, em vez
  de o código morto seguir escondido.
- **nova-aula.py, escolhas que o prompt não fixou:**
  - o slug aceita só letras minúsculas, números e hífens, o que também impede um
    slug como `../fora` de escrever fora de `site/aulas/`;
  - título e resumo são perguntados uma vez, em pt, e a versão en nasce com o
    mesmo texto, no HTML e no aulas.json, para o autor traduzir; o próprio script
    lembra disso ao terminar;
  - a entrada nova nasce com `nivel` "iniciante", `tags` vazias, capa 📘 em
    `grape` e `atualizada_em` com a data do dia;
  - nos `.html` o texto entra escapado (`&`, `<`, aspas); nos `.js` e `.css` entra
    sem acento, porque até comentário acentuado reprova o check.py;
  - tudo é montado em memória e só é escrito depois de todas as respostas: entrada
    incompleta, slug inválido ou repetido não deixam nenhum arquivo para trás;
  - o aulas.json é regravado no mesmo desenho do arquivo escrito à mão (conferido:
    reformatar o índice atual reproduz o arquivo byte a byte), para o diff de uma
    aula nova mostrar só a entrada nova;
  - entrada e saída forçadas para UTF-8: no console do Windows os acentos
    digitados chegavam corrompidos.
- **check.py, verificações além da lista mínima:**
  - a igualdade de chaves de STR e de sections vale também para o par do hub, não
    só para as aulas, porque a regra de i18n do CLAUDE.md vale para toda página;
  - as sections são comparadas na mesma ordem, como a regra pede;
  - os ids passados a `drawFig`/`figFail` contam como ids usados pelo aula.js,
    porque o core faz o `querySelector` com eles;
  - os caminhos absolutos `/aulas/...` da 404 também são conferidos, porque o
    `http.server` não serve a 404 e um erro ali passaria despercebido;
  - o conjunto de acentos procurado é exatamente o do `grep` documentado, para os
    dois darem sempre o mesmo resultado.
- **Como os scripts foram testados.** Numa cópia do repositório fora do projeto:
  o nova-aula.py criou uma aula com título acentuado, `&` e aspas; o check.py
  passou; a aula abriu sem erro de console nas duas línguas e larguras, com o
  slider, os dois quizzes, o Python e a figura funcionando, e o hub continuou
  escondendo o rascunho. Depois, cada verificação do check.py foi provocada de
  propósito (acento em JS, status e cor inválidos, idioma faltando, slug
  repetido, JSON quebrado, pasta órfã, chave de STR só em pt, sections trocadas,
  id sumido, link quebrado) e todas saíram com código 1 e a mensagem certa.
  Nenhuma aula de teste foi commitada.
- **Fora do escopo, só registrado:** o rótulo "Pergunta" acima de cada `.q` vem de
  `content:"Pergunta"` no aula.css e aparece também nas páginas em inglês. Isso já
  acontecia na aula de ML, e o template en herda o mesmo problema.

## Aula nlp-intro — construção (fases 4 e 5)

Decisões fora do roteiro aprovado. As que mudam a página também estão no fim do
`site/aulas/nlp-intro/ROTEIRO.md`.

- **Scripts de verificação em `scripts/nlp-intro/`.** Estão lá os scripts que produziram
  cada número, mais um `gerar_amostra.py` que reproduz byte a byte os dois JSON publicados.
  Os dados originais (o CSV do B2W tem 49 MB) ficam em `scripts/nlp-intro/dados/`,
  ignorados por um `.gitignore` local da pasta; o da raiz não mudou. Ficaram de fora dos
  commits: uma cópia do código do nltk usada só como consulta para o porte, os
  `corpus-*.json` e o `esperado.json` (arquivos gerados) e os screenshots.
- **Versões do Python.** Os scripts rodaram com `uv run --python 3.12`, inclusive o
  `nova-aula.py` (respostas por stdin) e o `check.py`, com as versões fixadas em
  `scripts/nlp-intro/env.sh`.
- **Dados em JSON dentro de `assets/`** (`avaliacoes-pt.json`, `avaliacoes-en.json`,
  `rslp.json`, `stopwords-*.json`), carregados por `fetch`. O `check.py` só confere
  `href`/`src`, não esses caminhos; a conferência foi feita no Playwright. Não alterei o
  `check.py`.
- **Chave `rslpUrl` vazia na página en.** As duas páginas precisam das mesmas chaves de
  `STR`; o en usa o Porter e não carrega o arquivo.
- **nltk_data pelo jsdelivr.** O bloco 9 baixa `rslp.zip` e `stopwords.zip` de
  `cdn.jsdelivr.net/gh/nltk/nltk_data@gh-pages/`: mesma CDN do Pyodide, outro caminho.
- **Arquivo JS único.** Tokenizador, stemmers, Naive Bayes e widgets ficaram todos no
  `aula.js` (sem um segundo arquivo), para seguir a ordem de scripts do `CLAUDE.md` da raiz.
  Nada foi subido para o `core.js`: nenhuma outra aula usa texto.
- **Testes no Chromium com `--disable-quic`.** É uma opção do ambiente de teste e não muda
  nada na página.
- **Fora do escopo, só registrado:** a meta `description` dos dois HTMLs ficou com o
  resumo que o `nova-aula.py` gravou; o `aulas.json` ganhou um resumo reescrito. Os dois
  dizem a mesma coisa.
