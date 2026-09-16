# Texto vira número — roteiro (~84 min)

**Objetivo:** ao final, o aluno escreve uma avaliação, vê o classificador decidir e explica a
decisão apontando como a frase virou uma linha de números (quais palavras sobraram depois do
preparo, o peso de cada uma, a soma) — e diz por que ele erra em "não é ruim".
**Público:** iniciante absoluto em NLP que fez `ml-intro`.
**Formato:** setup-punch; página interativa; pt-BR e en-US; ao vivo, online.
**Fio de dados:** um corpus de avaliações de loja online com rótulo positiva/negativa, dos
blocos 2 a 9 (pt: 4000 do B2W; en: 1984 do UCI Amazon + Yelp).
**Pré-requisitos:** `ml-intro` inteira. Entram sem reexplicação: modelo ("fórmula com espaços
em branco; aprender = preencher"), rótulo, treino/teste, acurácia, k-NN, parâmetro,
overfitting, hiperparâmetro, classificação.

Todo número abaixo foi produzido pelos scripts de `verif/` (verificação local, fora do repositório) (Pyodide 0.27.5: nltk 3.8.1,
scikit-learn 1.6.1). Saídas completas em `verif/saida-v12-pt.txt` e `verif/saida-v12-en.txt`.
Onde pt e en diferem, o valor en vem entre colchetes: **[en: …]**.

## Mapa de tempo

| Bloco | id | Tema | Tempo | Acumulado |
|---|---|---|---|---|
| 1. Parecido | s1 | por que texto é diferente | 6 | 6 |
| 2. A lista | s2 | ponte com ML: regra à mão fica muda; o classificador quer uma tabela | 7 | 13 |
| 3. A tabela | s3 | cada palavra, uma coluna: vocabulário, saco de palavras, esparsidade, ordem perdida | 11 | 24 |
| 4. Pedaços | s4 | 19 colunas para "ótimo": tokenização e normalização | 7 | 31 |
| 5. Palavras vazias | s5 | stopwords apagam o "não" | 7 | 38 |
| 6. Radical | s6 | stemming corta demais e de menos; lematização precisa de contexto | 10 | 48 |
| 7. Pesos | s7 | **centro:** aprender é contar; a nota é a soma dos pesos | 13 | 61 |
| 8. Sua frase | s8 | pouso: o classificador decide a frase do aluno, e erra onde os números perderam o sentido | 12 | 73 |
| 9. Python | s9 | o mesmo com nltk + scikit-learn (Pyodide) | 6 | 79 |
| 10. Mapa | s10 | resumo, três perguntas abertas, quiz | 4 | 83 |
| 11. Para continuar | s11 | referências | 1 | 84 |

Folga: 6 min. O centro (bloco 7) começa aos 48 min e é o mais longo. O preparo (4–6) vem
**depois** da tabela e cada técnica abre com o custo que ela ataca, como o autor pediu; o
efeito delas na acurácia só é medido no bloco 8, quando existe um classificador para medir.

## Vocabulário — a partir de que bloco cada termo entra

| Termo | Bloco | Antes disso, dizemos |
|---|---|---|
| NLP / PLN, análise de sentimentos | 1 (título) | — |
| modelo, rótulo, treino, teste, acurácia, classificação, k-NN | 1 (vêm de `ml-intro`) | — |
| classificador | 2 | — (derivado de "classificação", liberado em `ml-intro`) |
| vocabulário | 3 | "todas as palavras diferentes" |
| vetor | 3 (Revelar) | "a linha da frase" |
| saco de palavras (bag of words) | 3 (Revelar) | "uma coluna por palavra" |
| esparsa | 3 (Revelar) | "quase só zeros" |
| token, tokenização | 4 (Revelar) | "pedaço", "cortar em pedaços" |
| normalização | 4 (Revelar) | "arrumar", "deixar igual" |
| stopwords | 5 (Revelar) | "palavras que aparecem em todo lugar" |
| stemming, radical | 6 (Revelar) | "cortar a ponta da palavra" |
| lematização, lema | 6 (Revelar do segundo movimento) | "a forma de dicionário" |
| peso | 7 | "quanto a palavra puxa" |
| Naive Bayes | 7 (Revelar) | "o classificador" |
| n-grama, bigrama | 8 (Revelar) | "pares de palavras" |
| embedding, Transformer | 10 (só no mapa) | — |

`grep` a rodar no HTML pt antes do push (e equivalente no en), cada termo não pode aparecer
em seção anterior à do seu bloco: `token`, `vocabulário`, `vetor`, `esparsa`, `stopword`,
`stemming`, `radical`, `lemat`, `lema`, `peso`, `Naive Bayes`, `n-grama`, `bigrama`,
`embedding`, `Transformer`. Exceção: o `STR` do bloco 9 (código).

## Domínios dos exemplos verbais

| Bloco | Exemplos falados e do contexto | Itens dos widgets |
|---|---|---|
| 1 | mensagens de celular, corretor automático | pares de frases curtas |
| 2 | críticas de restaurante | o corpus |
| 3 | letra de música ("a mesma letra, fora de ordem") | o corpus + a frase do aluno |
| 4 | busca no Google ignorando maiúsculas | colunas do corpus |
| 5 | telegrama que cortava artigos para pagar menos | as palavras mais comuns do corpus |
| 6 | dicionário e palavras cruzadas | pares de palavras |
| 7 | nota de aplicativo na loja do celular | palavras do corpus |
| 8 | atendimento ao cliente | frases do aluno e frases-desafio |
| 9 | — | código |

## Blocos

### Bloco 1 — Parecido (6 min)
**Domínio:** mensagens de celular.
**Contexto.** Na aula anterior, uma fruta de 150 g e uma de 151 g eram vizinhas no gráfico:
números perto querem dizer coisas parecidas. O corretor do celular troca "ruim" por "rim"
porque as letras são quase iguais. Texto funciona assim também?
**Pergunta.** Em cada par, as duas frases são parecidas ou diferentes? Vote antes de abrir.
**Widget (W1-pares).** Quatro cartões, cada um com um par e dois botões ("parecidas" /
"diferentes"). Ao votar, o cartão mostra um medidor "letras que mudam: N de M" e o sentido
("mesmo sentido" / "sentido oposto").

| Par (pt) | letras que mudam | sentido |
|---|---|---|
| "é ruim" × "não é ruim" | 4 de 10 | oposto |
| "ótimo" × "excelente" | 9 de 9 | igual |
| "ótimo" × "otimo" | 1 de 5 | igual |
| "chegou rápido mas veio quebrado" × "veio quebrado mas chegou rápido" | 20 de 31 | igual |

[en: "bad" × "not bad" 4 de 7, oposto; "great" × "excellent" 7 de 9, igual; "great" ×
"Great!!!" 4 de 8, igual; "fast delivery but it arrived broken" × "it arrived broken
but fast delivery" 26 de 35, igual]

**Revelação.**
(a) Pelas letras, "é ruim" e "não é ruim" são quase gêmeas, e "ótimo" e "excelente" não têm
nada em comum. Faz sentido medir assim: é o que o corretor do celular faz.
(b) Mas o sentido anda para o outro lado. Quatro letras invertem a frase; nove letras
diferentes não mudam nada; trocar a ordem das metades mexe em 20 letras e deixa o sentido
igual. Nas frutas, perto nos números era perto no sentido. No texto, não.
(c) Por isso texto é um problema à parte dentro de ML, com nome próprio: processamento de
linguagem natural, NLP. E a pergunta desta aula: se nem a distância entre letras serve,
como transformar uma frase em números que um classificador consiga usar?
**Punch:** em texto, parecido na forma não é parecido no sentido.
**Ponte:** "Mas a gente classifica essas frases sem esforço. Por que não escrever as regras?"

### Bloco 2 — A lista (7 min)
**Domínio:** críticas de restaurante (fala); o corpus (widget).
**Contexto.** Temos 4000 avaliações de uma loja online, escritas por clientes. As de 1 ou 2
estrelas ganharam o rótulo "negativa"; as de 4 ou 5, "positiva"; as de 3 ficaram de fora.
[en: 1984 frases de avaliações de produtos e restaurantes, já rotuladas.] Você lê uma crítica
de restaurante e sabe em dois segundos se a pessoa gostou. Dá para escrever isso como regra?
**Pergunta.** Escreva as palavras que entregam uma avaliação positiva e as que entregam uma
negativa. Quantas das 4000 a sua lista vai acertar?
**Widget (W2-lista).** Duas caixas de palavras (positivas / negativas), já preenchidas com
uma lista de partida, editáveis. O aluno anota o palpite num slider (0–100%). Botão "Testar
nas 4000 avaliações": conta, para cada avaliação, palavras positivas menos negativas; saldo
> 0 é positiva, < 0 é negativa, 0 é "sem resposta". Mostra três barras (certas, erradas, sem
resposta) e três exemplos sorteados de "sem resposta".
Lista de partida pt: ótimo, ótima, bom, boa, excelente, recomendo, gostei, adorei, perfeito,
lindo, maravilhoso, rápido, rápida / péssimo, péssima, ruim, horrível, defeito, quebrado,
quebrou, demorou, problema, errado, devolver, decepcionado. [en: good, great, excellent,
love, recommend, perfect, nice, best, amazing, happy, awesome, delicious / bad, terrible,
worst, poor, hate, broken, awful, disappointed, waste, horrible, disgusting, slow]
**Revelação.**
(a) Parecia fácil: são poucas as palavras que alguém usa para elogiar ou reclamar.
(b) A lista de partida acerta 47,1%, erra 6,0% e fica **sem resposta em 46,9%** [en: 34,1%,
3,5%, 62,4%]. O problema não é errar: é ficar muda, porque as pessoas escrevem de mil
jeitos ("chegou antes do prazo", "não posso avaliar, não recebi"). Em 2002, pesquisadores
de Cornell e da IBM fizeram o mesmo com críticas de cinema: listas escritas por pessoas acertaram 58%
e 64%.
(c) É o bloco 1 da aula anterior de novo: regra à mão não escala. Lá, a saída foi dar os
exemplos com gabarito e deixar o computador preencher a fórmula. Só que o classificador
quer uma **tabela de números** — uma linha por exemplo, uma coluna por medida, como peso e
doçura das frutas. Qual é a coluna de uma frase?
**Punch:** a lista escrita à mão não erra muito — ela fica muda.
**Ponte:** "E se, em vez de escolher 25 palavras, a gente usasse todas?"

### Bloco 3 — A tabela (11 min)
**Domínio:** letra de música (fala); o corpus + a frase do aluno (widget).
**Contexto.** Ideia mais simples possível: cada palavra diferente que aparece nas 4000
avaliações vira uma coluna. A linha de uma avaliação tem 1 nas colunas das palavras que ela
usa e 0 em todas as outras. Por enquanto, "palavra" é o que fica entre dois espaços.
**Pergunta.** Chute: quantas colunas tem essa tabela? E, na linha da frase que você vai
escrever, quantas casas são zero?
**Widget (W3-tabela).** Campo de palpite (número de colunas). Caixa de texto para a frase do
aluno (valor inicial: "chegou rápido mas veio quebrado"). Abaixo, uma tabela recortada:
linhas = três avaliações do corpus + a frase do aluno; colunas = as palavras dessas quatro
linhas (as que valem 1 em alguma), seguidas de uma coluna "… mais N colunas, todas 0". Um
contador grande: "N colunas · sua frase: K uns e N−K zeros (Z%)". Botão "Embaralhar a
frase": reordena as palavras da caixa, e a linha não muda (a célula pisca verde "linha
idêntica").
**Revelação.**
(a) A intuição é que a tabela teria algumas centenas de colunas: não usamos tantas palavras.
(b) São **9801 colunas** [en: 4977]. Uma avaliação usa em média 12,6 palavras diferentes
[en: 10,1]: **99,87% da linha é zero** [en: 99,80%]. E 67% das colunas aparecem em uma
avaliação só [en: 66%]. E a ordem sumiu: "chegou rápido mas veio quebrado" e "veio quebrado
mas chegou rápido" são a mesma linha, como uma letra de música com os versos embaralhados
que ainda usa as mesmas palavras.
(c) A lista de todas as palavras diferentes chama-se **vocabulário**; a linha da frase é um
**vetor**; e essa forma de montar a tabela, jogando as palavras num saco e anotando só quais
estão lá, é o **saco de palavras** (bag of words). Uma tabela quase só de zeros é
**esparsa**. Três custos ficaram na mesa: colunas demais, a maioria com um exemplo só, e a
ordem perdida. Os próximos três blocos atacam o primeiro e o segundo; o terceiro volta no
bloco 8.
**Punch:** a frase vira uma linha com quase 10 mil casas, quase todas zero, e a ordem das
palavras não entra.
**Ponte:** "Olhe as colunas da tabela: 'Ótimo', 'ótimo', 'ótimo.' … são colunas diferentes."

### Bloco 4 — Pedaços (7 min)
**Domínio:** busca no Google (fala); colunas do corpus (widget).
**Contexto.** Quando você busca "Ótimo Restaurante" ou "ótimo restaurante", o Google traz a
mesma coisa. A nossa tabela não é tão esperta.
**Pergunta.** Em quantas colunas diferentes a palavra "ótimo" se espalhou?
**Widget (W4-pedacos).** Busca (valor inicial "ótimo" [en: "great"]) que lista todas as
colunas cruas que viram a mesma palavra quando se tiram maiúsculas, pontuação e acentos,
cada uma com quantas avaliações a usam. Três interruptores, cumulativos: "tudo minúsculo",
"só letras (tirar pontuação e números)", "tirar acentos". Contador: total de colunas da
tabela e quantas sobram para a palavra buscada.
**Revelação.**
(a) Chutes típicos: uma, duas.
(b) **19 colunas** [en: 11]: ótimo (122 avaliações), Ótimo (101), otimo (28), ótimo. (15),
Otimo (13), ótimo, (11), ÓTIMO (7)… Cada uma com poucos exemplos, e o classificador vai
aprender cada uma separadamente. Minúsculas e só letras levam a tabela de 9801 para **5357
colunas** (−45%) [en: 4977 → 3187]; tirar acento, para 5145 [en: 3185].
(c) Cortar o texto em pedaços é a **tokenização**; cada pedaço é um **token**. Deixar formas
diferentes iguais (minúsculas, sem pontuação, sem acento) é **normalização**. Não é ritual de
limpeza: é juntar numa coluna só os exemplos que estavam espalhados.
**Punch:** a mesma palavra espalhada em 19 colunas divide os exemplos em 19 pedaços.
**Ponte:** "Das 52 mil palavras do texto, 39% são 'o', 'de', 'e', 'que'…"

### Bloco 5 — Palavras vazias (7 min)
**Domínio:** telegrama (fala); palavras mais comuns do corpus (widget).
**Contexto.** No telegrama, cada palavra custava, e as pessoas cortavam artigos: "chego
terça trem cinco". Das 52 mil palavras das avaliações, 39% são palavras assim, que aparecem
em todo lugar [en: 49% de 21 mil].
**Pergunta.** Marque as palavras que você jogaria fora, porque não dizem nada sobre gostar ou
não gostar.
**Widget (W5-vazias).** As 30 palavras mais comuns do corpus em "fichas" clicáveis, com
contagem. O aluno marca as que descartaria. Botão "Usar a lista pronta" marca as que estão na
lista padrão do NLTK — incluindo `não`, `nem`, `sem`, `muito`, `mais` [en: `not`, `no`,
`very`, `but`, `didn't`]. Painel embaixo: quatro avaliações reais do corpus, antes e depois do
corte (escolhidas na fase 4 entre as que usam "não", "nem" e "muito"), com as palavras
cortadas riscadas; logo abaixo, "não gostei" → "gostei" e "não recomendo" → "recomendo"; e o
contador "texto: −39% · colunas: −131" [en: −49%, −150].
**Revelação.**
(a) Jogar fora o que aparece em todo lugar parece economia pura.
(b) A lista pronta corta 39% do texto, mas só **131 colunas** (de 5357): são poucas palavras,
repetidas muitas vezes. E nela está **"não"**, a quarta palavra mais comum do corpus e uma
das que mais dizem: aparece em 1118 das 2000 negativas e em 136 das 2000 positivas [en:
`not` em 189 negativas e 32 positivas]. "não gostei" vira "gostei"; "não recomendo" vira
"recomendo".
(c) Essas listas de palavras frequentes se chamam **stopwords**. Foram feitas para busca, onde
"o" e "de" atrapalham mesmo. Para sentimento, palavra comum não é palavra vazia. O quanto
isso custa em acertos, a gente mede no bloco 8.
**Punch:** a lista de stopwords apaga o "não".
**Ponte:** "Sobrou outro espalhamento: gostei, gosto, gostaria…"

### Bloco 6 — Radical (10 min)
**Domínio:** dicionário e palavras cruzadas.
**Contexto.** gostei, gosto, gosta, gostaria, gostoso: cinco colunas para a mesma ideia. Uma
saída é cortar a ponta de cada palavra e deixar só o começo.
**Pergunta.** Para cada par, as duas palavras vão cair na mesma coluna depois do corte?
**Widget (W6-radical).** Oito cartões de par; o aluno vota "mesma" / "diferentes" e o cartão
vira mostrando os radicais calculados ao vivo pelo stemmer em JS:

| Par (pt) | Resultado RSLP | O que mostra |
|---|---|---|
| gostei × gostaria | gost × gost | junta, como queríamos |
| barato × barata (o inseto) | barat × barat | junta demais |
| casa × casamento | cas × cas | junta demais |
| livro × livre | livr × livr | junta demais |
| bom × boa | bom × boa | não junta |
| amei × amo | ame × amo | não junta |
| demora × demorou | dem × demor | não junta |
| fui × ir | fui × ir | não junta |

[en, Porter original: liked × likely → like × like; general × generous → gener × gener;
university × universe → univers × univers; news × new → new × new; is × I → i × i; happy ×
happiness → happi × happi; good × better → good × better; went × go → went × go]

Abaixo, caixa livre: o aluno digita qualquer palavra e vê o radical. Contador: "colunas:
5357 → 3195 (−40%)" [en: 3187 → 2554 (−20%)].

**Revelação.**
(a) Parece que cortar a ponta junta as palavras da mesma família e só elas.
(b) O corte é uma lista de regras de terminação, não um dicionário: junta barato com barata,
casa com casamento, e separa bom de boa, amei de amo. Ainda assim tira 40% das colunas.
(c) Isso é **stemming**, e o pedaço que sobra é o **radical**. O stemmer desta aula é o RSLP,
criado para o português por Viviane Orengo e Christian Huyck (2001) [en: Porter, 1980].
**Punch:** a tesoura corta demais e de menos, e mesmo assim junta bastante.

**Segundo movimento — "E com dicionário?"** (dentro do mesmo bloco, depois do Revelar).
Pergunta: "Qual é a forma de dicionário de 'fui'?" Tabela estática com a saída de uma
ferramenta de dicionário (spaCy 3.8.7, `pt_core_news_sm`), rodada sobre a frase "Eu fui
ontem, vou amanhã e iria de novo. Ela foi e era boa. Amei, amo e amava. O produto veio
quebrado e as entregas atrasaram.": fui → **ser**; vou → ir; iria → ir; foi → ser; era →
ser; boa → bom; Amei → **Amei**; amo → **amo**; amava → amar; quebrado → quebrar; entregas →
entrega. [en, `en_core_web_sm` 3.8.0, "I went yesterday, I am going tomorrow and I was
happy. The phones were better and she loved it. The deliveries arrived broken.": went → go;
am, was, were → be; **better → well**; loved → love; broken → break; phones → phone.]
Revelar curto: "fui" é "ir" ou "ser" dependendo da frase, e a ferramenta escolheu "ser" onde
era "ir". Achar a forma de dicionário é **lematização**, e ela precisa do contexto — e ainda
erra ("Amei" ficou como estava). É mais cara e não roda nesta página; os resultados acima
foram pré-calculados.

**Ponte:** "Juntamos, cortamos, limpamos. Mas nenhuma coluna diz ainda se a palavra é boa ou
ruim. Quem decide isso?"

### Bloco 7 — Pesos (13 min) — centro da aula
**Domínio:** nota de aplicativo na loja do celular (fala); palavras do corpus (widget).
**Contexto.** Na aula anterior, o modelo era uma fórmula com espaços em branco
(`preço = a × área + b`) e aprender era preencher os espaços. Aqui a fórmula tem um espaço
por coluna: quanto cada palavra puxa a avaliação para positiva ou negativa. A nota de uma
frase é a soma do quanto puxam as palavras dela. Falta saber como preencher 5357 espaços.
**Pergunta.** Para que lado puxa cada palavra? entrega, dentro, avaliar, produto, ainda,
top. [en: town, money, the, minutes, great, not]
**Widget (W7a-puxa).** Seis cartões; em cada um, três botões (← negativa · neutra ·
positiva →). Ao votar, o cartão mostra duas barras — em quantas das 2000 positivas e das
2000 negativas a palavra aparece — o **peso** (número com sinal e barra colorida) e duas
avaliações de exemplo com a palavra destacada.

| Palavra (pt) | positivas | negativas | peso | por quê (exemplo do corpus) |
|---|---|---|---|---|
| entrega | 364 | 116 | positivo | "entrega rápida" |
| dentro | 59 | 15 | positivo | "chegou dentro do prazo" |
| avaliar | 2 | 131 | muito negativo (−3,7) | "não posso avaliar, ainda não recebi" |
| produto | 886 | 857 | quase zero (+0,1) | aparece em tudo |
| ainda | 24 | 223 | negativo (−2,1) | "ainda não chegou" |
| top | 16 | 0 | positivo (+2,9) | "produto top" |

[en: town 7 / 0 ("best tacos in town"); money 1 / 24 ("waste of money", −2,5); the 413 / 408
(≈ 0); minutes 2 / 20 ("waited 45 minutes"); great 150 / 5 (+3,3); not 32 / 189 (−1,7)]

**Widget (W7b-soma).** Uma frase (valor inicial "não posso avaliar") com uma barra por
palavra, para a esquerda ou a direita conforme o peso, e a soma no fim com a decisão.
"não posso avaliar": não −2,0 · posso −3,4 · avaliar −3,7 → −9,2 → negativa. Contador:
"acerto nas avaliações de teste: 91,7% (média de 20 sorteios)" [en: 81,3%].
Botão "Como o peso é calculado?" abre um `details` com a conta (ver Exemplos).

**Revelação.**
(a) A gente julga a palavra pelo que ela quer dizer: "avaliar" é neutra, "dentro" também.
(b) O classificador não sabe o que nenhuma palavra quer dizer. Ele só contou onde cada uma
apareceu: "avaliar" apareceu em 131 negativas, quase sempre de quem ainda não tinha recebido
o produto; "dentro" veio de "dentro do prazo"; "produto" está em tudo e pesa quase zero. O
peso é essa comparação: aparece muito mais nas positivas, puxa para positiva. A nota da
frase é a soma, e com isso ele acerta 91,7% das avaliações que não viu no treino.
(c) Cada número desses é um **peso**, e é o "a" da fórmula da aula anterior, um por coluna.
Aprender, aqui, é contar. Esse classificador chama-se **Naive Bayes**. "Naive", ingênuo,
porque soma as palavras como se cada uma não tivesse nada a ver com as vizinhas — o que já
diz onde ele vai errar.
**Punch:** o peso vem de onde a palavra apareceu, não do que ela significa.
**Ponte:** "Agora é a sua vez de escrever — e de tentar fazê-lo errar."

### Bloco 8 — Sua frase (12 min) — pouso
**Domínio:** atendimento ao cliente (fala); frases do aluno (widget).
**Contexto.** Todas as peças estão na mesa: cortar em pedaços, arrumar, talvez tirar
stopwords, talvez cortar no radical, virar uma linha, somar os pesos.
**Pergunta.** Escreva uma avaliação que o classificador erre. Antes de apertar, diga por que
você acha que ele vai errar.
**Widget (W8-frase).** A peça principal da aula.
- Caixa de texto (valor inicial "chegou rápido mas veio quebrado").
- A esteira, da esquerda para a direita (em 390 px, de cima para baixo): pedaços → depois do
  preparo (palavras cortadas riscadas, radicais mostrados) → a linha (fichas com 1; "N
  colunas com 0") → uma barra por palavra com o peso (palavra nunca vista: cinza, "peso 0,
  nunca apareceu") → soma → decisão (positiva / negativa).
- Interruptores: "tirar stopwords", "cortar no radical", "pares de palavras". Mudam a esteira
  na hora (o classificador é retreinado nas 4000 avaliações).
- Painel de acerto: "média de 20 sorteios: X% · antes: 91,7% · melhorou em N de 20".
- Fichas-desafio que preenchem a caixa: "não é ruim", "sem defeito nenhum", "não tenho do que
  reclamar", "a entrega atrasou", "que maravilha, esperei dois meses pela entrega", "não
  gostei", "não recomendo". [en: "not bad", "no problems", "no complaints at all", "the
  delivery was late", "oh great, it broke after two days", "i did not like it", "i do not
  recommend it"]

Resultados verificados (sem opções ligadas, a não ser onde indicado):

| Frase (pt) | Decisão | Por quê |
|---|---|---|
| não é ruim | negativa −5,3 | não −2,0 + ruim −3,5 |
| sem defeito nenhum | negativa −3,6 | defeito −2,7, nenhum −0,9 |
| não tenho do que reclamar | negativa −1,1 | não −2,0 pesa mais que reclamar +0,8 |
| a entrega atrasou | **positiva** +0,2 | entrega +1,2; "atrasou" só aparece em 2 avaliações (−1,0) |
| a entrega atrasou, **com radical** | negativa −1,2 | `atras` junta atraso e atrasado (−2,0) |
| que maravilha, esperei dois meses pela entrega | negativa −2,3 | maravilha +1,2 perde para esperei −1,9, meses −1,9 |
| a mesma, **com radical** | **positiva** +3,0 | `maravilh` junta maravilhoso, maravilhosa (+4,2) |
| não gostei | negativa −0,9 | não −2,0, gostei +1,1 |
| não gostei, **sem stopwords** | **positiva** +1,1 | sobrou "gostei" |
| não recomendo, **sem stopwords** | **positiva** +1,5 | sobrou "recomendo" |
| não recomendo, **com pares** | negativa −4,5 | "não_recomendo" vira coluna (−3,9) |
| chegou rápido mas veio quebrado / veio quebrado mas chegou rápido | ambas negativa −2,6 | mesma linha |

[en: not bad → negativa −5,1 (not −1,7, bad −3,4); no problems → negativa −0,8; no
complaints at all → negativa −1,1; the delivery was late → positiva +0,07; oh great, it
broke after two days → negativa −0,4, **com radical positiva +0,2**; i do not recommend it
→ negativa −2,3, **sem stopwords positiva +0,9**; i did not like it, **com pares** → −5,9]

Acerto, média de 20 sorteios (pt / en):

| Opção ligada | pt | en |
|---|---|---|
| nenhuma | 91,7% | 81,3% |
| tirar stopwords | 91,2% (pior em 16 de 20) | 79,3% (pior em 18 de 20) |
| cortar no radical | 91,9% (melhor em 13 de 20) | 81,9% (melhor em 13 de 20) |
| pares de palavras | 92,7% (melhor em 20 de 20), 23 734 colunas | 82,4% (melhor em 15 de 20), 12 249 colunas |
| radical + pares | 93,0% | 83,2% |
| stopwords + radical (a "receita" completa, com acentos) | 91,3% (pior em 12 de 20) | 79,4% (pior em 18 de 20) |

**Revelação.**
(a) A gente esperava que ele errasse ironia — e erra —, mas talvez não esperasse que errasse
"não é ruim" ou "sem defeito nenhum", que qualquer pessoa entende.
(b) Cada erro está escrito nos números. "não" pesa −2,0 e "ruim" pesa −3,5: somados, dão uma
frase muito negativa, porque a soma não sabe que um desfaz o outro. "a entrega atrasou" sai
positiva porque "entrega" veio de "entrega rápida" e "atrasou" quase nunca apareceu; o
radical junta atraso e atrasado e conserta. O mesmo radical junta "maravilha" com
"maravilhoso" e cai na ironia. Tirar stopwords apaga o "não" e inverte "não gostei". E a
média quase não se mexe — 91,7% para 91,2% — enquanto frases inteiras trocam de lado.
(c) Pares de palavras ("não_recomendo") devolvem um pouco de ordem: são os **n-gramas**
(**bigramas**, para pares). Acertam mais, em 20 de 20 sorteios, e custam quatro vezes mais
colunas. Nenhuma técnica de preparo é boa ou ruim em geral: cada uma joga fora alguma coisa,
e o que importa é se aquilo que ela jogou fora era o que decidia.
**Punch:** o classificador erra exatamente onde a frase, ao virar números, perdeu o que
importava: a ordem, a negação, o contexto.
**Ponte:** "Tudo isso cabe em 20 linhas de Python."

### Bloco 9 — Python (6 min)
**Pergunta.** "Encontre, no código, a linha de cada bloco da aula." Botão "Rodar Python"
(Pyodide + scikit-learn + nltk; os downloads começam cedo, ver guia). Duas células editáveis,
no mesmo desenho do bloco 8 de `ml-intro` (textarea + console). Painéis e saída em
§Exemplos de código.
**Revelação** (curta). O mesmo classificador, com as bibliotecas que se usam de verdade: o
`CountVectorizer` é a tabela do bloco 3, `binary=True` é "1 se a palavra está lá", o
`RSLPStemmer` é a tesoura do bloco 6, `MultinomialNB` é a contagem do bloco 7. As 20
divisões são as mesmas dos widgets, por isso os números batem.
**Punch:** nada do que você viu era de brinquedo.

### Bloco 10 — Mapa (4 min)
Tabela-resumo (pergunta → ideia → nome):

| Bloco | Pergunta | Ideia | Nome |
|---|---|---|---|
| 1 | frases parecidas? | forma ≠ sentido | NLP |
| 2 | dá para listar as palavras? | a lista fica muda | classificador de sentimento |
| 3 | como vira tabela? | uma coluna por palavra, quase tudo zero, sem ordem | vocabulário, saco de palavras, esparsa |
| 4 | por que tantas colunas? | "ótimo" espalhado em 19 | tokenização, normalização |
| 5 | jogar fora as comuns? | a lista apaga o "não" | stopwords |
| 6 | juntar a família? | a tesoura corta demais e de menos | stemming, lematização |
| 7 | de onde vêm os pesos? | aprender é contar | peso, Naive Bayes |
| 8 | por que ele erra? | a soma não sabe negar | n-gramas |

Três perguntas abertas (provocadas pelos blocos 1, 8 e 7):
1. "ótimo" e "excelente" são colunas sem nada em comum. E se palavras de sentido parecido
   ficassem perto, como as frutas? → **embeddings**.
2. "não é ruim" erra porque a soma ignora a ordem. E se o modelo lesse a frase olhando cada
   palavra junto das outras? → **Transformers**.
3. Os pesos vêm de 4000 avaliações de uma loja, em português. "avaliar" é negativa aqui; em
   críticas de cinema, em inglês, ou numa mistura das duas línguas, o que muda? → domínio e
   **multilíngue**.

Quiz (`quizOptions`, 8 itens):

| # | Pergunta | Alternativas | Correta | Explicação |
|---|---|---|---|---|
| 1 | "Ótimo!" e "ótimo" no saco de palavras cru são… | mesma coluna / colunas diferentes / a mesma linha | colunas diferentes | tokenização e normalização existem para juntar |
| 2 | Por que tirar stopwords atrapalha em sentimento? | apaga o "não" / aumenta a tabela / deixa o treino lento | apaga o "não" | a lista padrão tem "não", "nem", "sem" |
| 3 | Com stemming, "barato" e "barata" (o inseto)… | viram a mesma coluna / continuam separadas / são apagadas | mesma coluna | a tesoura segue regras, não sentido |
| 4 | De onde vem o peso de uma palavra? | de um dicionário de sentimentos / da contagem em positivas e negativas / do tamanho da palavra | contagem | aprender é contar |
| 5 | "chegou rápido mas veio quebrado" e a mesma frase invertida… | viram a mesma linha / linhas diferentes | a mesma linha | o saco de palavras não guarda ordem |
| 6 | Uma palavra que nunca apareceu no treino pesa… | muito positivo / zero / muito negativo | zero | não há o que contar |
| 7 | Pares de palavras acertam mais. O custo? | nenhum / a tabela fica umas 4× maior / o "não" some | 4× maior | cada par vira coluna |
| 8 | A lista de palavras escrita à mão errou pouco, mas… | ficou sem resposta em quase metade / acertou tudo / demorou | sem resposta | as pessoas escrevem de mil jeitos |

### Bloco 11 — Para continuar (1 min)
- SLP3, Apêndice B "Naive Bayes, Text Classification, and Sentiment" — o classificador desta
  aula, com as mesmas melhorias (presença, negação).
- SLP3, Cap. 2 "Words and Tokens" — tokenização a sério.
- scikit-learn, 8.2.3 "Text feature extraction" — a tabela, a esparsidade e o aviso sobre
  stopwords, na documentação oficial.
- NLTK Book, §3.6 "Normalizing Text" — stemmers e lematizadores lado a lado.
- Pang, Lee & Vaithyanathan (2002), "Thumbs up?" — o experimento da lista do bloco 2.
- CS224n, aula 2 "Word Vectors" — o próximo passo: palavras como pontos no espaço.
- Dados: B2W-Reviews01 (Real, Oshiro & Mafra, 2019; CC BY-NC-SA 4.0) [en: UCI Sentiment
  Labelled Sentences, Kotzias et al. 2015; CC BY 4.0]; RSLP (Orengo & Huyck, 2001).

## Widgets (spec)

Dados comuns: `assets/avaliacoes-pt.json` / `assets/avaliacoes-en.json`
(`{fonte, licenca, texto[], rotulo[], divisoes[20 strings "0/1"]}`, gerados por
`verif/v12_final.py`), `assets/rslp.json` (as 7 tabelas de regras do nltk_data),
`assets/stopwords-pt.json` / `stopwords-en.json` (listas do nltk_data). Carregados uma vez ao
abrir a página; JSON e não `.js` por causa da regra de acentos. O caminho de cada língua vem
de `STR` (`dadosUrl`, `stopUrl`). Porte do Porter original: em `aula.js` (sem acentos).
Enquanto os dados não chegam, cada widget mostra `STR.carregando`; se falharem, `STR.dadosErro`.

### W1-pares (s1)
- Entrada: dois botões por cartão. Estado: votos. Saída: medidor de letras (distância de
  edição calculada em JS) e o rótulo de sentido (do `STR`).
- Dados: 4 pares no `STR`. Não depende do corpus.
- Ids: `pairCards`, `pairOut`.
- 390 px: cartões em uma coluna.

### W2-lista (s2)
- Entrada: `textarea` positivas, `textarea` negativas (palavras separadas por vírgula ou
  espaço, comparadas depois de minúsculas + só letras), slider de palpite, botão.
- Saída: três barras (certas / erradas / sem resposta) com % e contagem; três exemplos de
  "sem resposta" sorteados com `rnd()`.
- Ids: `listPos`, `listNeg`, `listGuess`, `vListGuess`, `listBtn`, `svgList`, `listOut`.
- Vazio: listas vazias → 100% sem resposta, mensagem do `STR`.

### W3-tabela (s3)
- Entrada: palpite (`input type=number`), frase, botão "Embaralhar".
- Saída: tabela HTML recortada (4 linhas × até 14 colunas + "… mais N"), contador de colunas,
  uns e zeros. Tokenização crua (`split` por espaço).
- Ids: `tabGuess`, `tabText`, `tabShuffle`, `tabGrid`, `tabOut`.
- 390 px: a tabela fica num container com rolagem horizontal própria (permitido).

### W4-pedacos (s4)
- Entrada: busca, três checkbox cumulativos. Saída: lista de variantes com contagem; contador
  total de colunas.
- Ids: `tokSearch`, `tokLower`, `tokLetters`, `tokAccents`, `tokList`, `tokOut`.

### W5-vazias (s5)
- Entrada: 30 fichas clicáveis; botão "lista pronta". Saída: 4 frases com cortes riscados;
  contadores de texto e colunas.
- Ids: `stopChips`, `stopBtn`, `stopSamples`, `stopOut`.

### W6-radical (s6)
- Entrada: 8 cartões com votos; caixa livre. Saída: radicais ao vivo (RSLP/Porter em JS),
  contador de colunas. Segundo movimento: tabela HTML estática no próprio HTML.
- Ids: `stemCards`, `stemInput`, `stemOut`, `lemmaTable`.

### W7a-puxa e W7b-soma (s7)
- Entrada: votos em 6 cartões; frase livre na W7b.
- Estado: classificador treinado no corpus inteiro, pipeline base.
- Saída: barras de presença pos/neg, peso, dois exemplos; SVG de barras de peso + soma.
- Ids: `pullCards`, `sumText`, `svgSum`, `sumOut`, `accOut`.
- `details` com a conta do peso (fica no HTML, não no JS).

### W8-frase (s8)
- Entrada: frase, três checkbox, 7 fichas-desafio.
- Estado: 8 classificadores possíveis (um por combinação das 3 opções) (treino sob demanda, com cache
  por combinação); acerto médio das 20 divisões calculado sob demanda e guardado.
- Saída: esteira em HTML + SVG de barras; painel de acerto.
- Ids: `frText`, `frStop`, `frStem`, `frPairs`, `frChips`, `frBelt`, `svgFrase`, `frVerdict`,
  `frAcc`.
- Desempenho: 4000 avaliações × 20 divisões por combinação; medir na fase 4 (esperado < 300
  ms por combinação). Se passar de 1 s, pré-calcular as 16 médias em Python e gravar no JSON.
- 390 px: esteira vertical.

### Bloco 9 (s9)
- Ids: `py1`, `run1`, `py2`, `run2`, `pyStatus`, `pyOut1`, `pyOut2`.
- `PyUI.statusSel = "#pyStatus"`. Prelúdio escondido (em `aula.js`, sem texto): `getPy()`,
  `loadPackage("nltk")`, `pyfetch` dos zips `rslp` e `stopwords` do jsdelivr, extração em
  `/home/pyodide/nltk_data/`, `pyfetch` do JSON do corpus para `textos/rotulos/divisoes`
  [en: `texts/labels/splits`].
- Falha de rede: mensagem `STR.pyNetError` no console da célula; o resto da página segue.

### s10
- Ids: `quiz10`, `quiz10Out`.

## Exemplos de código (verificados)

### Bloco 7 — a conta do peso (dentro do `details`)
peso(palavra) = ln( (positivas com a palavra + 1) / (palavras nas positivas + V) ) −
ln( (negativas com a palavra + 1) / (palavras nas negativas + V) ), com V = colunas. É o que
`MultinomialNB(alpha=1)` guarda em `feature_log_prob_` sobre a tabela 0/1; a diferença das
duas linhas é o peso. A soma dos pesos das palavras da frase, mais `ln(P(positiva)/P(negativa))`
= 0 (classes do mesmo tamanho), decide o lado. Verificado em `verif/v12_final.py` (a
decisão pela soma coincide com `modelo.predict`).

### Bloco 9 — célula 1 (pt)
```python
import re
from nltk.stem import RSLPStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

radical = RSLPStemmer().stem
def preparar(texto):
    palavras = re.findall(r"[^\W\d_]+", texto.lower())   # bloco 4: minúsculas, só letras
    return [radical(p) for p in palavras]                 # bloco 6: o radical

vetorizador = CountVectorizer(analyzer=preparar, binary=True)   # bloco 3: uma coluna por palavra
X = vetorizador.fit_transform(textos)
modelo = MultinomialNB().fit(X, rotulos)                        # bloco 7: aprender é contar

frase = "a entrega atrasou"
pesos = modelo.feature_log_prob_[1] - modelo.feature_log_prob_[0]
colunas = vetorizador.vocabulary_
for palavra in preparar(frase):
    print(palavra, round(pesos[colunas[palavra]], 2) if palavra in colunas else "nunca vista")
print(X.shape, "->", ["negativa", "positiva"][modelo.predict(vetorizador.transform([frase]))[0]])
```
Saída verificada (local, nltk 3.8.1 / scikit-learn 1.6.1; 1,7 s):
```
a 0.03
entreg 0.69
atras -1.95
(4000, 3195) -> negativa
```

### Bloco 9 — célula 2 (pt)
```python
from nltk.corpus import stopwords
vazias = set(stopwords.words("portuguese"))

def nota_media(preparo):
    docs = [preparo(t) for t in textos]
    notas = []
    for divisao in divisoes:                                  # os mesmos 20 sorteios dos widgets
        treino = [i for i, d in enumerate(divisao) if d == "0"]
        teste = [i for i, d in enumerate(divisao) if d == "1"]
        vet = CountVectorizer(analyzer=lambda d: d, binary=True)
        m = MultinomialNB().fit(vet.fit_transform([docs[i] for i in treino]), [rotulos[i] for i in treino])
        notas.append(m.score(vet.transform([docs[i] for i in teste]), [rotulos[i] for i in teste]))
    return round(sum(notas) / len(notas), 3)

so_letras = lambda t: re.findall(r"[^\W\d_]+", t.lower())
print("só letras:        ", nota_media(so_letras))
print("sem stopwords:    ", nota_media(lambda t: [p for p in so_letras(t) if p not in vazias]))
print("com radical:      ", nota_media(preparar))
```
Saída verificada (1,4 s):
```
só letras:         0.917
sem stopwords:     0.912
com radical:       0.919
```

### Bloco 9 — en
Mesma lógica, nomes em inglês (`texts`, `labels`, `splits`, `prepare`, `vectorizer`, `model`,
`sentence`, `weights`, `columns`, `mean_score`, `letters`, `empty`),
`PorterStemmer(mode="ORIGINAL_ALGORITHM").stem`, regex `[^\W\d_]+(?:'[^\W\d_]+)?`, frase
"it did not disappoint". Saída verificada: `it -0.2 / did -0.47 / not -1.69 / disappoint
-1.66 / (1984, 2554) -> negative`; `letters only: 0.813 / no stopwords: 0.793 / with stem:
0.819`. Script: `verif/v14_bloco_python_en.py`.

Pyodide: pacotes e corpora do NLTK testados em Chromium headless (ver PESQUISA.md); as duas
células ainda não foram cronometradas dentro do Pyodide — fase 4.

## Decisões e vetos

1. **Classificador: Naive Bayes multinomial sobre presença (0/1), `alpha=1`.** É linear, com
   um peso por palavra e a soma decidindo — a ponte direta com `preço = a × área + b` — e o
   peso se explica por contagem, sem otimização. Regressão logística acerta parecido e
   também seria linear, mas os pesos não se explicam contando. Nas mesmas 20 divisões: Naive Bayes 91,7% [en: 81,3%], regressão logística 91,9% [en: 82,7%], k-NN (k = 5) 87,5% [en: 73,9%]. k-NN fica só no vocabulário
   (`verif/v17_conferencias.py`).
2. **Presença, não contagem.** Pang 2002 e SLP3 B.4; e "Excelente! Excelente! Excelente!"
   não vale três vezes.
3. **Rótulo pt: notas 1–2 negativa, 4–5 positiva, 3 fora.** Convenção da literatura (o artigo
   do B2W usa 1–2 / 3–4 / 5; a nossa é binária). Nota 1 contra 5 deixa a tarefa fácil demais
   (94%) e com menos erros para explicar.
4. **Tamanho: 2000 por classe em pt.** Com 1000, punches de frase dependiam da amostra: "nada
   bom" saía positiva em 8 de 10 amostras e a ironia com radical em 9 de 10; com 2000, 10 de
   10. Custo: 314 KB de texto (em pt), e efeitos médios menores no bloco 8 (stopwords −0,5
   pt em vez de −1,5).
5. **Punches descartados por não se sustentarem com outra amostra:** "atrasou só aparece em
   'não atrasou'" e "encontrei uma barata dentro da caixa sai positiva" (morreram ao aplicar
   o filtro de conteúdo e trocar a amostra; teste de 10 amostras em `verif/v13_robustez.py`).
   Não reintroduzir sem refazer esse teste.
6. **Acurácia sempre como média de 20 divisões fixas**, gravadas no JSON. Com uma divisão só
   (`random_state=7`), o radical parece ganhar +1,8 pt, o que é ruído.
7. **Filtro de conteúdo antes da amostragem:** fora palavrão forte, acusação a terceiros
   ("golpe", "ladrão", "revendedor" com nome) e dados pessoais (sequências de dígitos, e-mail,
   URL). Palavrão leve (en "crap", "damn") fica. Lista em `verif/filtros.py`.
8. **Stemmer en: Porter no modo original**, não o default do NLTK (NLTK_EXTENSIONS, 715
   linhas): o original tem porte curto e conhecido, e o bloco 9 usa o mesmo modo.
9. **Lematização só com exemplos pré-calculados** (spaCy fora do navegador). A página diz que
   foram pré-calculados.
10. **Dados em JSON, não em `.js`,** por causa do grep de acentos; o `check.py` não confere
    caminhos usados em `fetch` — ver Riscos.
11. **O "centro" é o bloco 7**, não o 3. O 3 é a fundação (texto vira tabela); o 7 é o que
    torna a decisão explicável, e é o que o objetivo da aula exige.
12. **Descartado:** vizinha mais próxima por palavras em comum (reserva P14 da pesquisa) —
    em pt o efeito é fraco e o bloco 5 já tem punch próprio.

## Riscos e planos B

- **Turma silenciosa nos setups** → votação binária no chat ("1 = mesma coluna, 2 =
  diferentes"); os blocos 1, 6 e 7 já são votos.
- **Sobrou tempo** → no bloco 8, pedir que cada um cole no chat a frase que enganou o
  classificador e explicar duas delas pela esteira; no bloco 9, trocar a frase da célula 1.
- **Faltou tempo** → o segundo movimento do bloco 6 (lematização) vira leitura; o bloco 9
  vira tarefa. **Inegociáveis: blocos 3, 7 e 8.**
- **Ambiente sem rede** → só o bloco 9 depende de rede (Pyodide + zips do NLTK no jsdelivr).
  Os dados da aula vêm do mesmo site da página e carregam na abertura.
- **Desempenho do W8** em celular fraco (retreino + 20 divisões) → se passar de 1 s,
  pré-calcular as médias das 8 combinações em Python e gravar no JSON.
- **Paridade stemmer JS × nltk** → teste palavra a palavra sobre o vocabulário inteiro dos
  dois corpora na fase 4; qualquer divergência bloqueia a publicação.
- **`check.py` não vê os JSON carregados por `fetch`** → a verificação da fase 5 confere no
  Playwright que os widgets carregaram (e anoto a lacuna em `NOTAS-DA-EXECUCAO.md`, sem mexer
  no `check.py`, que está fora do escopo pedido).
- **Licença SA do B2W** → o JSON pt leva `fonte` e `licenca` (CC BY-NC-SA 4.0) dentro dele, e
  o bloco 11 dá o crédito.

## Mudanças durante a construção (fase 4)

- **Menu do topo com rótulos neutros** ("6 A ponta", "7 Quanto puxa"; en "6 The ending",
  "7 How hard"): "Radical" e "Pesos" no menu entregavam os termos antes do bloco.
- **Bloco 2:** "como o peso e a doçura das frutas" virou "como nas frutas da aula
  anterior", para "peso" não aparecer antes do bloco 7 com outro sentido. O Revelar diz
  "47%, 6% e 47%" em vez de uma casa decimal: 1886/4000 = 47,15%, e o navegador e o
  Python arredondam essa metade para lados diferentes.
- **Bloco 5 en:** as avaliações de exemplo usam "not", "very" e "but" (a mais curta com
  "no" tinha palavrão leve).
- **Bloco 6 en:** pares loved/loving, liked/likely, general/generous, news/new,
  university/universe, good/better, went/go, arrive/arrival. A pergunta do segundo
  movimento é "better" (a ferramenta devolveu "well" onde era "good").
- **Bloco 7 en:** palavras town, money, the, minutes, great, not; frase inicial "waste of
  money".
- **Bloco 8, correção de número:** com o tokenizador final, "não_recomendo" pesa −4,5 e
  "não recomendo" com pares soma −5,0 (a tabela acima trazia −3,9 e −4,5, de uma rodada
  anterior à correção do tokenizador). A página não cita esses dois valores.
- **Conferência:** radicais JS × nltk idênticos em 5383 palavras (pt) e 3221 (en); colunas
  idênticas em todas as etapas; acerto idêntico em cada um dos 20 sorteios das 8
  combinações do bloco 8, nas duas línguas; bloco 9 rodado no Pyodide com a saída acima.
