// aula.js — Texto vira numero (nlp-intro). Tudo o que e so desta aula mora aqui.
// O motor esta em core.js, carregado antes: $, $$, el, T, fmt, esc, rnd, C,
// quizOptions, highlight, PyUI e getPy vem de la. Nenhum texto de interface mora
// aqui: tudo sai de window.STR, definido no HTML de cada idioma, inclusive os
// caminhos dos dados (as avaliacoes, as stopwords e as regras do RSLP).
//
// A mesma logica roda nas duas linguas; muda o stemmer (RSLP em pt, Porter no modo
// original em en) e o tokenizador (en aceita apostrofo no meio: didn't).
// Tudo aqui foi conferido contra o nltk 3.8.1 e o scikit-learn 1.6.1: os mesmos
// radicais, as mesmas colunas e o mesmo acerto medio nos 20 sorteios.

// ---------------------------------------------------------------- formatos
const MINUS="−";
const nf=(v,d)=>Math.abs(v).toLocaleString(S.locale,{minimumFractionDigits:d,maximumFractionDigits:d});
const signed=v=>(v<0?MINUS:"+")+nf(v,1);                     // peso: +1,2 / -3,7
const pct=(v,d=1)=>nf(v*100,d)+"%";                            // 0,917 -> 91,7%

// ---------------------------------------------------------------- texto
const LET="[\\p{L}\\p{Nl}\\p{No}]+";                            // o [^\W\d_]+ do Python
const RE_TOK=S.stemmer==="porter"?new RegExp(LET+"(?:'"+LET+")?","gu"):new RegExp(LET,"gu");
const tokens=t=>t.toLowerCase().match(RE_TOK)||[];
const rawSplit=t=>t.split(/\s+/).filter(Boolean);
const noAccent=w=>w.normalize("NFD").replace(/\p{Mn}/gu,"");
const uniq=a=>[...new Set(a)];

// RSLP (Orengo e Huyck, 2001): porte do nltk.stem.rslp. As regras vem de rslp.json,
// no mesmo formato que o nltk le: [sufixo, tamanho minimo do radical, troca, excecoes].
let RSLP=null;
function rslpRule(w,i){for(const [suf,min,rep,exc] of RSLP[i]){
    if(w.endsWith(suf)&&w.length>=suf.length+min&&!exc.includes(w))return w.slice(0,w.length-suf.length)+rep}
  return w}
function rslp(word){let w=word.toLowerCase();
  if(w.endsWith("s"))w=rslpRule(w,0);        // plural
  if(w.endsWith("a"))w=rslpRule(w,1);        // feminino
  w=rslpRule(w,3);                            // aumentativo e diminutivo
  w=rslpRule(w,2);                            // adverbio
  let prev=w;w=rslpRule(w,4);                 // substantivo
  if(w===prev){prev=w;w=rslpRule(w,5);        // verbo
    if(w===prev)w=rslpRule(w,6)}              // vogal final
  return w}

// Porter (1980), modo ORIGINAL_ALGORITHM do nltk.stem.porter, regra por regra.
const isCons=(w,i)=>{const c=w[i];if("aeiou".includes(c))return false;if(c==="y")return i===0?true:!isCons(w,i-1);return true};
const measure=s=>{let cv="";for(let i=0;i<s.length;i++)cv+=isCons(s,i)?"c":"v";return (cv.match(/vc/g)||[]).length};
const hasVowel=s=>{for(let i=0;i<s.length;i++)if(!isCons(s,i))return true;return false};
const endsDouble=w=>w.length>=2&&w[w.length-1]===w[w.length-2]&&isCons(w,w.length-1);
const endsCvc=w=>w.length>=3&&isCons(w,w.length-3)&&!isCons(w,w.length-2)&&isCons(w,w.length-1)&&!"wxy".includes(w[w.length-1]);
function rules(word,list){for(const [suf,rep,cond] of list){
    if(suf==="*d"&&endsDouble(word)){const st=word.slice(0,-2);return !cond||cond(st)?st+rep:word}
    if(word.endsWith(suf)){const st=suf===""?word:word.slice(0,-suf.length);return !cond||cond(st)?st+rep:word}}
  return word}
const m0=s=>measure(s)>0, m1=s=>measure(s)>1;
function porter(word){let w=word.toLowerCase();
  w=rules(w,[["sses","ss"],["ies","i"],["ss","ss"],["s",""]]);
  w=(w=>{if(w.endsWith("eed")){const st=w.slice(0,-3);return measure(st)>0?st+"ee":w}
    let st=null;for(const suf of ["ed","ing"])if(w.endsWith(suf)){const t=w.slice(0,-suf.length);if(hasVowel(t)){st=t;break}}
    if(st===null)return w;const last=st[st.length-1];
    return rules(st,[["at","ate"],["bl","ble"],["iz","ize"],["*d",last,()=>!"lsz".includes(last)],["","e",s=>measure(s)===1&&endsCvc(s)]])})(w);
  w=rules(w,[["y","i",hasVowel]]);
  w=rules(w,[["ational","ate",m0],["tional","tion",m0],["enci","ence",m0],["anci","ance",m0],["izer","ize",m0],["abli","able",m0],["alli","al",m0],["entli","ent",m0],["eli","e",m0],["ousli","ous",m0],["ization","ize",m0],["ation","ate",m0],["ator","ate",m0],["alism","al",m0],["iveness","ive",m0],["fulness","ful",m0],["ousness","ous",m0],["aliti","al",m0],["iviti","ive",m0],["biliti","ble",m0]]);
  w=rules(w,[["icate","ic",m0],["ative","",m0],["alize","al",m0],["iciti","ic",m0],["ical","ic",m0],["ful","",m0],["ness","",m0]]);
  w=rules(w,[["al","",m1],["ance","",m1],["ence","",m1],["er","",m1],["ic","",m1],["able","",m1],["ible","",m1],["ant","",m1],["ement","",m1],["ment","",m1],["ent","",m1],["ion","",s=>measure(s)>1&&"st".includes(s[s.length-1])],["ou","",m1],["ism","",m1],["ate","",m1],["iti","",m1],["ous","",m1],["ive","",m1],["ize","",m1]]);
  if(w.endsWith("e")){const st=w.slice(0,-1);if(measure(st)>1||(measure(st)===1&&!endsCvc(st)))w=st}
  const ww=w;w=rules(w,[["ll","l",()=>measure(ww.slice(0,-1))>1]]);
  return w}

const stemCache=new Map();
const stem=w=>{let r=stemCache.get(w);if(r===undefined){r=S.stemmer==="porter"?porter(w):rslp(w);stemCache.set(w,r)}return r};

// o preparo de uma frase, com as opcoes do bloco 8: stopwords, radical e pares
let STOP=new Set();
function prep(text,o={}){let d=tokens(text);
  if(o.stop)d=d.filter(w=>!STOP.has(w));
  if(o.stem)d=d.map(stem);
  if(o.pairs)d=d.concat(d.slice(1).map((w,i)=>d[i]+"_"+w));
  return d}

// ---------------------------------------------------------------- Naive Bayes
// Multinomial sobre presenca (0/1) com alpha=1, como MultinomialNB sobre
// CountVectorizer(binary=True). flp[c] = log((docs da classe c com a palavra + 1) /
// (total de presencas na classe c + V)). A decisao soma na ordem das colunas do
// scikit-learn (palavras em ordem alfabetica), para empates sairem iguais.
let TXT=[],Y=[],DIV=[];
function train(docs,idx){const cnt=[new Map(),new Map()],nd=[0,0],tot=[0,0];
  for(const i of idx){const y=Y[i];nd[y]++;for(const w of docs[i]){cnt[y].set(w,(cnt[y].get(w)||0)+1);tot[y]++}}
  const vocab=new Set([...cnt[0].keys(),...cnt[1].keys()]),V=vocab.size,N=nd[0]+nd[1];
  const flp=(c,w)=>Math.log(((cnt[c].get(w)||0)+1)/(tot[c]+V));
  return {vocab,V,count:(c,w)=>cnt[c].get(w)||0,
    weight:w=>vocab.has(w)?flp(1,w)-flp(0,w):null,
    score(doc){const ws=doc.filter(w=>vocab.has(w)).sort();let s0=0,s1=0;
      for(const w of ws){s0+=flp(0,w);s1+=flp(1,w)}
      s0+=Math.log(nd[0]/N);s1+=Math.log(nd[1]/N);return {pos:s1>s0,diff:s1-s0}}}}

const docsCache=new Map();                 // docs preparados, por combinacao de opcoes
const key=o=>`${+!!o.stop}${+!!o.stem}${+!!o.pairs}`;
function docsFor(o){const k=key(o);if(!docsCache.has(k))docsCache.set(k,TXT.map(t=>uniq(prep(t,o))));return docsCache.get(k)}
const modelCache=new Map();                // classificador treinado nas avaliacoes todas
function modelFor(o){const k=key(o);if(!modelCache.has(k))modelCache.set(k,train(docsFor(o),TXT.map((_,i)=>i)));return modelCache.get(k)}
const accCache=new Map();                  // acerto em cada um dos 20 sorteios
function accFor(o){const k=key(o);if(accCache.has(k))return accCache.get(k);
  const docs=docsFor(o),res=DIV.map(dv=>{const tr=[],te=[];for(let i=0;i<dv.length;i++)(dv[i]==="1"?te:tr).push(i);
    const m=train(docs,tr);let ok=0;for(const i of te)if(m.score(docs[i]).pos===(Y[i]===1))ok++;return ok/te.length});
  accCache.set(k,res);return res}
const mean=a=>a.reduce((s,x)=>s+x,0)/a.length;
const later=f=>new Promise(r=>setTimeout(()=>r(f()),30));   // deixa a tela pintar "calculando"

// exemplos curtos do corpus que usam uma palavra (os mais curtos, a partir de n palavras)
function shortest(pred,k,minWords=4){return TXT.map((t,i)=>[t,i]).filter(([t,i])=>rawSplit(t).length>=minWords&&pred(t,i))
  .sort((a,b)=>a[0].length-b[0].length||a[1]-b[1]).slice(0,k)}

// barras de peso em SVG: uma linha por palavra, a soma embaixo. A largura do
// desenho acompanha a da tela, para o texto ficar sempre no tamanho natural.
const redraws=[];addEventListener("resize",()=>{clearTimeout(redraws.t);redraws.t=setTimeout(()=>redraws.forEach(f=>f()),150)});
function drawWeights(svg,items,sum,label){svg.innerHTML="";const W=Math.max(330,Math.min(640,svg.clientWidth||640)),row=30,top=10,mid=W/2,sc=(mid-12)/5.6;
  const H=top+row*(items.length+1)+16;svg.setAttribute("viewBox",`0 0 ${W} ${H}`);
  el("line",{x1:mid,y1:4,x2:mid,y2:H-4,stroke:C.line,"stroke-width":2},svg);
  const bar=(y,v,txt,fill,bold)=>{const len=Math.min(Math.abs(v),5.6)*sc;
    if(v!==null)el("rect",{x:v<0?mid-len:mid,y:y+5,width:Math.max(len,2),height:row-10,rx:4,fill},svg);
    const t=el("text",{x:v===null||v>=0?mid-8:mid+8,y:y+row/2+5,"font-size":bold?16:15,"text-anchor":v===null||v>=0?"end":"start",fill:C.ink},svg);t.textContent=txt};
  items.forEach((it,i)=>bar(top+i*row,it.w,it.w===null?`${it.t} · ${S.sumUnknown}`:`${it.t}  ${signed(it.w)}`,it.w===null?C.grey:it.w<0?C.coral:C.teal));
  bar(top+items.length*row+8,sum,`${label}  ${signed(sum)}`,sum>0?C.teal:C.coral,true)}

// ---------------------------------------------------------------- 1: pares
(function(){const box=$("#pairCards");let votes=0;
  const lev=(a,b)=>{const d=[...Array(b.length+1).keys()];for(let i=1;i<=a.length;i++){let p=d[0];d[0]=i;
    for(let j=1;j<=b.length;j++){const t=d[j];d[j]=Math.min(d[j]+1,d[j-1]+1,p+(a[i-1]!==b[j-1]));p=t}}return d[b.length]};
  S.pairs.forEach(([a,b,same])=>{const c=document.createElement("div");c.className="pair";
    c.innerHTML=`<div class="words"><span>${esc(a)}</span><em>&times;</em><span>${esc(b)}</span></div><div class="seg"><button class="ghost small">${S.pairSame}</button><button class="ghost small">${S.pairDiff}</button></div><div class="meter" hidden></div>`;
    c.querySelectorAll("button").forEach(bt=>bt.onclick=()=>{if(c.dataset.done)return;c.dataset.done=1;bt.setAttribute("aria-pressed","true");votes++;
      const n=lev(a,b),m=Math.max(a.length,b.length),mt=c.querySelector(".meter");mt.hidden=false;
      mt.innerHTML=`<div class="track"><i style="width:${100*n/m}%"></i></div><b>${T(S.pairMeter,{n,m})}</b> · <b class="${same?"same":"opp"}">${same?S.pairMeanSame:S.pairMeanOpp}</b>`;
      $("#pairOut").textContent=votes===S.pairs.length?S.pairOutDone:T(S.pairOutMore,{n:S.pairs.length-votes})});
    box.appendChild(c)})})();

// ---------------------------------------------------------------- 10: quiz e realce de codigo
quizOptions("#quiz10","#quiz10Out",S.quiz10,{
  done:(o,right,total)=>{const p=right/total;o.className="out "+(p===1?"ok":p<0.5?"bad":"");
    o.textContent=T(S.quiz10Score,{right,total})+(p===1?S.quiz10Perfect:p<0.5?S.quiz10Weak:S.quiz10Good)}});
$$("pre code.py").forEach(c=>{c.innerHTML=highlight(c.textContent)});

// ---------------------------------------------------------------- 9: Python
// O core baixa o Pyodide e o scikit-learn; aqui entram o nltk, as regras do RSLP e
// as stopwords (do nltk_data, pelo jsdelivr) e as mesmas avaliacoes dos widgets.
PyUI.statusSel="#pyStatus";
const NLTK_DATA="https://cdn.jsdelivr.net/gh/nltk/nltk_data@gh-pages/packages/";
let pyNlp=null;
function getPyNlp(){if(pyNlp)return pyNlp;pyNlp=(async()=>{const py=await getPy();
    $("#pyStatus").textContent=S.pyNltk;await py.loadPackage(["nltk"]);
    py.globals.set("_base",NLTK_DATA);py.globals.set("_dados",new URL(S.dadosUrl,location.href).href);
    await py.runPythonAsync(`
from pyodide.http import pyfetch
import io, os, zipfile
for _sub, _nome in [("stemmers", "rslp"), ("corpora", "stopwords")]:
    _r = await pyfetch(_base + _sub + "/" + _nome + ".zip")
    _pasta = "/home/pyodide/nltk_data/" + _sub
    os.makedirs(_pasta, exist_ok=True)
    zipfile.ZipFile(io.BytesIO(await _r.bytes())).extractall(_pasta)
`);
    $("#pyStatus").textContent=S.pyData;
    const [vt,vr,vd]=S.pyVars;
    await py.runPythonAsync(`_d = await (await pyfetch(_dados)).json()\n${vt}, ${vr}, ${vd} = _d["texto"], _d["rotulo"], _d["divisoes"]`);
    $("#pyStatus").textContent=S.pyReady;return py})();
  pyNlp.catch(()=>{pyNlp=null});return pyNlp}
let ran1=false;   // a caixa 2 usa o que a caixa 1 define
[["#run1","#py1","#pyOut1"],["#run2","#py2","#pyOut2"]].forEach(([b,src,dst])=>{
  $(b).onclick=async()=>{const btn=$(b),out=$(dst);
    if(b==="#run2"&&!ran1){out.textContent=S.pyNeedFirst;return}
    btn.disabled=true;out.textContent="";
    try{const py=await getPyNlp();py.setStdout({batched:s=>out.textContent+=s+"\n"});py.setStderr({batched:s=>out.textContent+=s+"\n"});
      await py.runPythonAsync($(src).value);$("#pyStatus").textContent=S.pyReady;if(b==="#run1")ran1=true}
    catch(e){out.textContent+=String(e.message||e).split("\n").slice(-3).join("\n");$("#pyStatus").textContent=pyNlp?S.pyCodeError:S.pyNetError}
    btn.disabled=false}});

// ---------------------------------------------------------------- dados
const getJSON=u=>fetch(u).then(r=>{if(!r.ok)throw new Error(u);return r.json()});
Promise.all([getJSON(S.dadosUrl),getJSON(S.stopUrl),S.stemmer==="rslp"?getJSON(S.rslpUrl):null])
  .then(([d,sw,rs])=>{TXT=d.texto;Y=d.rotulo;DIV=d.divisoes;STOP=new Set(sw);RSLP=rs;start()})
  .catch(e=>{console.warn(e);["#listOut","#tabOut","#tokOut","#stopOut","#stemOut","#sumOut","#frAcc"].forEach(s=>{$(s).textContent=S.dataError;$(s).className="out bad"})});

function start(){
  const BASE=TXT.map(t=>tokens(t));                              // minusculas, so letras
  const nPos=Y.filter(y=>y===1).length,nNeg=Y.length-nPos;
  const vocabBase=new Set(BASE.flat());

  // ------------------------------------------------------------ 2: a lista
  (function(){const g=$("#listGuess");const showG=()=>$("#vListGuess").textContent=T(S.listGuessFmt,{v:g.value});g.oninput=showG;showG();
    const bars=$("#listBars");
    $("#listBtn").onclick=()=>{const P=new Set(tokens($("#listPos").value)),Ng=new Set(tokens($("#listNeg").value));
      let ok=0,bad=0;const mute=[];
      BASE.forEach((d,i)=>{const s=d.reduce((a,w)=>a+(P.has(w)?1:0)-(Ng.has(w)?1:0),0);
        if(s===0)mute.push(i);else if((s>0)===(Y[i]===1))ok++;else bad++});
      const N=TXT.length,rows=[[S.listRight,ok,"ok"],[S.listWrong,bad,"bad"],[S.listMute,mute.length,"mute"]];
      bars.innerHTML=rows.map(([l,v,c])=>`<div class="bar ${c}"><span>${l}</span><div class="track"><i style="width:${100*v/N}%"></i></div><b>${pct(v/N)}</b></div>`).join("");
      $("#listOut").textContent=(P.size+Ng.size===0?S.listEmpty+" ":"")+T(S.listOut,{certas:pct(ok/N),erradas:pct(bad/N),mudas:pct(mute.length/N),palpite:g.value+"%"});
      const pick=[];const pool=mute.slice();while(pick.length<3&&pool.length)pick.push(pool.splice(Math.floor(rnd()*pool.length),1)[0]);
      $("#listMute").innerHTML=pick.length?`<p>${S.listMuteTitle}</p>`+pick.map(i=>`<blockquote>${esc(TXT[i])} <small>(${Y[i]?S.labelPos:S.labelNeg})</small></blockquote>`).join(""):""}})();

  // ------------------------------------------------------------ 3: a tabela
  (function(){const RAW=TXT.map(rawSplit),vocabRaw=new Set(RAW.flat()),V=vocabRaw.size;
    const rows=S.tabPick.map(w=>shortest((t,i)=>BASE[i].includes(w),1,5)[0][1]);
    let shuffled=false;
    function draw(){const text=$("#tabText").value,you=uniq(rawSplit(text));
      if(!you.length){$("#tabGrid").innerHTML="";$("#tabOut").textContent=S.tabEmpty;return}
      const lines=[...rows.map((r,k)=>[T(S.tabReview,{n:k+1}),uniq(RAW[r])]),[S.tabYou,you]];
      const cols=uniq(you.concat(...rows.map(r=>RAW[r]))).filter(w=>vocabRaw.has(w)).slice(0,12);
      const rest=V-cols.length;
      $("#tabGrid").innerHTML=`<table><tr><th></th>${cols.map(c=>`<th>${esc(c)}</th>`).join("")}<th class="more">${T(S.tabMore,{n:fmt(rest)})}</th></tr>`+
        lines.map(([name,ws],k)=>`<tr class="${k===lines.length-1?"you":""}"><th>${esc(name)}</th>${cols.map(c=>ws.includes(c)?`<td class="one">1</td>`:`<td>0</td>`).join("")}<td class="more">0 … 0</td></tr>`).join("")+`</table>`;
      const uns=you.filter(w=>vocabRaw.has(w)).length,novas=you.length-uns,zeros=V-uns,guess=parseInt($("#tabGuess").value.replace(/\D/g,""),10);
      $("#tabOut").textContent=(shuffled?S.tabSame+" ":"")+T(S.tabOut,{cols:fmt(V),uns,zeros:fmt(zeros),pct:pct(zeros/V,2)})+
        (isNaN(guess)?"":T(S.tabGuessOut,{g:fmt(guess)}))+(novas?T(S.tabNew,{n:novas}):"")}
    $("#tabText").oninput=()=>{shuffled=false;draw()};$("#tabGuess").oninput=draw;
    $("#tabShuffle").onclick=()=>{const w=rawSplit($("#tabText").value);for(let i=w.length-1;i>0;i--){const j=Math.floor(rnd()*(i+1));[w[i],w[j]]=[w[j],w[i]]}
      $("#tabText").value=w.join(" ");shuffled=true;draw();$("#tabGrid").classList.remove("flash");void $("#tabGrid").offsetWidth;$("#tabGrid").classList.add("flash")};
    draw()})();

  // ------------------------------------------------------------ 4: pedacos
  (function(){const norm=w=>noAccent(w.toLowerCase().replace(/[^\p{L}\p{N}_]/gu,""));
    const cache=new Map();
    function columns(lower,letters,acc){const k=`${+lower}${+letters}${+acc}`;if(cache.has(k))return cache.get(k);
      const c=new Map();for(const t of TXT){const s=lower?t.toLowerCase():t;
        for(let w of (letters?(s.match(RE_TOK)||[]):rawSplit(s))){if(acc)w=noAccent(w);c.set(w,(c.get(w)||0)+1)}}
      cache.set(k,c);return c}
    function draw(){const c=columns($("#tokLower").checked,$("#tokLetters").checked,$("#tokAccents").checked),q=$("#tokSearch").value.trim(),nq=norm(q);
      const hits=nq?[...c.entries()].filter(([w])=>norm(w)===nq).sort((a,b)=>b[1]-a[1]):[];
      $("#tokList").innerHTML=hits.length?hits.map(([w,n])=>`<span class="chip">${esc(T(S.tokItem,{w,n:fmt(n)}))}</span>`).join(""):`<span class="chip off">${S.tokNone}</span>`;
      $("#tokOut").textContent=T(S.tokOut,{cols:fmt(c.size),q,k:hits.length})}
    ["#tokLower","#tokLetters","#tokAccents"].forEach(s=>$(s).onchange=draw);$("#tokSearch").oninput=draw;draw()})();

  // ------------------------------------------------------------ 5: palavras vazias
  (function(){const occ=new Map();let total=0;BASE.forEach(d=>d.forEach(w=>{occ.set(w,(occ.get(w)||0)+1);total++}));
    const top=[...occ.entries()].sort((a,b)=>b[1]-a[1]||(a[0]<b[0]?-1:1)).slice(0,30);
    const mine=new Set();let ready=false;
    const cut=()=>{const s=new Set(mine);if(ready)STOP.forEach(w=>s.add(w));return s};
    const samples=S.stopSampleWords.map(w=>shortest((t,i)=>BASE[i].includes(w),1,4)[0][0]);
    function draw(){const s=cut();
      $$("#stopChips .chip").forEach(ch=>ch.classList.toggle("on",s.has(ch.dataset.w)));
      $("#stopBtn").setAttribute("aria-pressed",ready);
      const strike=t=>t.replace(RE_TOK,m=>s.has(m.toLowerCase())?`<s>${esc(m)}</s>`:esc(m));
      $("#stopSamples").innerHTML=samples.concat(S.stopExtra).map(t=>{const kept=tokens(t).filter(w=>!s.has(w)).join(" ");
        return `<blockquote>${strike(t)} <small>→ ${esc(kept)||"∅"}</small></blockquote>`}).join("");
      let gone=0;occ.forEach((n,w)=>{if(s.has(w))gone+=n});const cols=[...vocabBase].filter(w=>s.has(w)).length;
      $("#stopOut").textContent=s.size?T(S.stopOut,{pct:pct(gone/total,0),cols:fmt(cols),total:fmt(vocabBase.size)}):S.stopNone}
    $("#stopChips").innerHTML=top.map(([w,n])=>`<button class="chip" data-w="${esc(w)}">${esc(w)} <small>${fmt(n)}</small></button>`).join("");
    $$("#stopChips .chip").forEach(ch=>ch.onclick=()=>{const w=ch.dataset.w;mine.has(w)?mine.delete(w):mine.add(w);draw()});
    $("#stopBtn").onclick=()=>{ready=!ready;draw()};draw()})();

  // ------------------------------------------------------------ 6: cortar a ponta
  (function(){const box=$("#stemCards");
    const before=vocabBase.size,after=new Set([...vocabBase].map(stem)).size,change=signed((after-before)/before*100).replace(/^\+/,"")+"%";
    S.stemPairs.forEach(([a,b])=>{const c=document.createElement("div");c.className="pair";const same=stem(a)===stem(b);
      c.innerHTML=`<div class="words"><span>${esc(a)}</span><em>&times;</em><span>${esc(b)}</span></div><div class="seg"><button class="ghost small" data-v="1">${S.stemSame}</button><button class="ghost small" data-v="0">${S.stemDiff}</button></div><div class="meter" hidden></div>`;
      c.querySelectorAll("button").forEach(bt=>bt.onclick=()=>{if(c.dataset.done)return;c.dataset.done=1;bt.setAttribute("aria-pressed","true");
        c.classList.add((bt.dataset.v==="1")===same?"right":"wrong");
        const mt=c.querySelector(".meter");mt.hidden=false;
        mt.innerHTML=`<code>${esc(a)} → ${esc(stem(a))}</code> <code>${esc(b)} → ${esc(stem(b))}</code> · <b class="${same?"same":"opp"}">${same?S.stemSame:S.stemDiff}</b>`});
      box.appendChild(c)});
    const draw=()=>{const ws=tokens($("#stemInput").value),v={antes:fmt(before),depois:fmt(after),pct:change};
      $("#stemOut").textContent=ws.length?T(S.stemOut,{...v,w:ws.join(" "),r:ws.map(stem).join(" ")}):T(S.stemEmpty,v)};
    $("#stemInput").oninput=draw;draw()})();

  // ------------------------------------------------------------ 7: pesos
  const M0=modelFor({});
  (function(){const box=$("#pullCards");
    S.pullWords.forEach(w=>{const p=M0.count(1,w),n=M0.count(0,w),wt=M0.weight(w)??0,side=wt>0.5?1:wt<-0.5?-1:0;
      const c=document.createElement("div");c.className="card pullcard";
      c.innerHTML=`<div class="word">${esc(w)}</div><div class="seg"><button class="ghost small" data-v="-1">${S.pullNeg}</button><button class="ghost small" data-v="0">${S.pullNeu}</button><button class="ghost small" data-v="1">${S.pullPos}</button></div><div class="res" hidden></div>`;
      c.querySelectorAll("button").forEach(bt=>bt.onclick=()=>{if(c.dataset.done)return;c.dataset.done=1;bt.setAttribute("aria-pressed","true");
        c.classList.add(+bt.dataset.v===side?"right":"wrong");
        const ex=shortest((t,i)=>BASE[i].includes(w)&&Y[i]===(p>=n?1:0),2,3).map(([t])=>`<blockquote>${esc(t).replace(new RegExp(`(^|[^\\p{L}])(${w})(?![\\p{L}])`,"giu"),"$1<mark>$2</mark>")}</blockquote>`).join("");
        const r=c.querySelector(".res");r.hidden=false;
        r.innerHTML=`<div class="duo"><div class="bar ok"><span>${S.labelPos}</span><div class="track"><i style="width:${100*p/nPos}%"></i></div><b>${fmt(p)}</b></div><div class="bar bad"><span>${S.labelNeg}</span><div class="track"><i style="width:${100*n/nNeg}%"></i></div><b>${fmt(n)}</b></div></div>`+
          `<p class="wt ${wt>0?"same":"opp"}">${T(S.pullWeight,{w:signed(wt)})} · ${T(S.pullCounts,{p:fmt(p),n:fmt(n)})}</p>${ex}`});
      box.appendChild(c)});
    const draw=()=>{const d=uniq(prep($("#sumText").value)),svg=$("#svgSum");
      if(!d.length){svg.innerHTML="";$("#sumOut").textContent=S.sumEmpty;return}
      const items=d.map(t=>({t,w:M0.weight(t)})),r=M0.score(d),label=r.pos?S.labelPos:S.labelNeg;
      drawWeights(svg,items,r.diff,label);const o=$("#sumOut");o.textContent=T(S.sumOut,{s:signed(r.diff),label});o.className="out "+(r.pos?"ok":"bad")};
    $("#sumText").oninput=draw;redraws.push(draw);draw();
    later(()=>{$("#accOut").textContent=T(S.accOut,{acc:pct(mean(accFor({})))})})})();

  // ------------------------------------------------------------ 8: sua frase
  (function(){const opts=()=>({stop:$("#frStop").checked,stem:$("#frStem").checked,pairs:$("#frPairs").checked});
    $("#frChips").innerHTML=S.frChips.map(t=>`<button class="chip">${esc(t)}</button>`).join("");
    $$("#frChips .chip").forEach(ch=>ch.onclick=()=>{$("#frText").value=ch.textContent;draw()});
    function draw(){const o=opts(),text=$("#frText").value,raw=tokens(text),belt=$("#frBelt");
      if(!raw.length){belt.innerHTML="";$("#svgFrase").innerHTML="";$("#frVerdict").textContent=S.frEmpty;return}
      const M=modelFor(o);
      const prepChips=raw.map(w=>o.stop&&STOP.has(w)?`<span class="chip off"><s>${esc(w)}</s></span>`:
        `<span class="chip">${esc(o.stem&&stem(w)!==w?w+" → "+stem(w):w)}</span>`).join("");
      const d=uniq(prep(text,o)),ones=d.filter(w=>M.vocab.has(w)).length;
      const pairChips=o.pairs?d.filter(w=>w.includes("_")).map(w=>`<span class="chip pairchip">${esc(w)}</span>`).join(""):"";
      belt.innerHTML=`<div class="step"><span>${S.beltTokens}</span><div>${raw.map(w=>`<span class="chip">${esc(w)}</span>`).join("")}</div></div>`+
        `<div class="step"><span>${S.beltPrep}</span><div>${prepChips}${pairChips}</div></div>`+
        `<div class="step"><span>${S.beltRow}</span><div><span class="rowinfo">${T(S.beltRowOut,{uns:fmt(ones),zeros:fmt(M.V-ones)})}</span></div></div>`;
      const r=M.score(d),label=r.pos?S.labelPos:S.labelNeg;
      drawWeights($("#svgFrase"),d.map(t=>({t,w:M.weight(t)})),r.diff,label);
      const v=$("#frVerdict");v.textContent=T(S.frVerdict,{label,s:signed(r.diff)});v.className="verdict "+(r.pos?"pos":"neg");
      showAcc(o)}
    let ticket=0;
    function showAcc(o){const my=++ticket,out=$("#frAcc");out.textContent=S.frCalc;
      later(()=>{if(my!==ticket)return;const a=accFor(o),b=accFor({}),k=key(o);
        const better=a.filter((x,i)=>x>b[i]).length,worse=a.filter((x,i)=>x<b[i]).length;
        const cmp=k==="000"?S.frBase:better>=worse?(better?T(S.frBetter,{n:better}):S.frEqual):T(S.frWorse,{n:worse});
        out.textContent=T(S.frAcc,{acc:pct(mean(a)),base:pct(mean(b)),cmp})})}
    $("#frText").oninput=draw;redraws.push(draw);["#frStop","#frStem","#frPairs"].forEach(s=>$(s).onchange=draw);draw()})();
}
