// core.js — o motor, agnostico de conteudo. Serve qualquer aula do site.
// Nenhum texto de interface mora aqui, nem nenhum id de uma aula especifica:
// cada pagina define window.STR antes de carregar este arquivo, e o aula.js
// de cada aula passa os seletores que quiser usar.

const S = window.STR;
const T = (tpl, v) => tpl.replace(/\{(\w+)\}/g, (_, k) => v[k]);

const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const NS="http://www.w3.org/2000/svg";
const el=(t,a={},parent)=>{const e=document.createElementNS(NS,t);for(const k in a)e.setAttribute(k,a[k]);if(parent)parent.appendChild(e);return e};
const fmt=n=>n.toLocaleString(S.locale);
const esc=t=>t.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");

// gerador pseudoaleatorio com semente: a mesma aula desenha os mesmos pontos
// em toda visita, e o professor pode apontar para um ponto especifico ao vivo
let seed=7;const rnd=()=>{seed=(seed*16807)%2147483647;return (seed-1)/2147483646};
const gauss=()=>{let u=0,v=0;while(!u)u=rnd();while(!v)v=rnd();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v)};

const C={coral:"#FF6B57",teal:"#1BA39C",ink:"#17203A",grey:"#B9C0D8",line:"#C9D1E4"};

// nav highlight
const links=$$("nav.map a[href^='#']");
$$("section.block").forEach(s=>new IntersectionObserver(es=>{es.forEach(e=>{if(e.isIntersecting)links.forEach(l=>l.classList.toggle("on",l.getAttribute("href")==="#"+s.id))})},{rootMargin:"-30% 0px -60% 0px"}).observe(s));

// motor de quiz, nos dois formatos. Recebe o seletor do container, o seletor
// da saida, os itens (vindos de STR) e L, que traz o que e daquela aula:
// os rotulos dos botoes, o texto da resposta certa e o fecho da pontuacao.

// formato A: duas alternativas fixas. Item = [enunciado, valor certo].
// L = {opts:[[valor,rotulo],[valor,rotulo]], answer(valor), done(saida,certos,total)}
function quizPair(boxSel,outSel,items,L){const box=$(boxSel);let done=0,right=0;
  items.forEach(([t,a])=>{const row=document.createElement("div");row.className="row";
    row.innerHTML=`<span>${t}</span><button class="ghost small">${L.opts[0][1]}</button><button class="ghost small">${L.opts[1][1]}</button>`;
    const [b1,b2]=row.querySelectorAll("button");const pick=g=>{if(row.dataset.done)return;row.dataset.done=1;done++;const ok=g===a;if(ok)right++;row.classList.add(ok?"right":"wrong");b1.disabled=b2.disabled=true;
      if(!ok)row.querySelector("span").textContent+=L.answer(a);
      if(done===items.length)L.done($(outSel),right,items.length)};
    b1.onclick=()=>pick(L.opts[0][0]);b2.onclick=()=>pick(L.opts[1][0]);box.appendChild(row)})}

// formato B: N alternativas por pergunta. Item = [enunciado, opcoes, indice certo].
// L = {done(saida,certos,total)}
function quizOptions(boxSel,outSel,items,L){const box=$(boxSel);let done=0,right=0;
  items.forEach(([pergunta,opcoes,certa])=>{
    const row=document.createElement("div");row.className="row multi";
    row.innerHTML=`<span>${pergunta}</span><div class="opts">${opcoes.map(o=>`<button class="ghost small">${o}</button>`).join("")}</div>`;
    const bts=[...row.querySelectorAll("button")];
    bts.forEach((b,i)=>b.onclick=()=>{if(row.dataset.done)return;row.dataset.done=1;done++;
      const ok=i===certa;if(ok)right++;
      row.classList.add(ok?"right":"wrong");bts.forEach(x=>x.disabled=true);
      if(!ok)bts[certa].disabled=false,bts[certa].style.borderColor="var(--ok)",bts[certa].style.color="var(--ok)";
      if(done===items.length)L.done($(outSel),right,items.length)});
    box.appendChild(row)})}

// construtor de escala: leva o dominio dos dados {x0,x1,y0,y1} para as
// coordenadas de um SVG de W por H com margem pad. X e Y recebem um ponto.
// O dominio em si e de cada aula; so a conversao mora aqui.
const scale=(B,W,H,pad)=>({X:f=>pad+(f.x-B.x0)/(B.x1-B.x0)*(W-2*pad),
                           Y:f=>H-pad-(f.y-B.y0)/(B.y1-B.y0)*(H-2*pad)});

function axes(svg,W,H,pad,xl,yl){el("line",{x1:pad,y1:H-pad,x2:W-pad,y2:H-pad,stroke:C.line,"stroke-width":2},svg);el("line",{x1:pad,y1:pad,x2:pad,y2:H-pad,stroke:C.line,"stroke-width":2},svg);
  el("text",{x:W/2,y:H-8,"font-size":13,"text-anchor":"middle",fill:"#4A5472"},svg).textContent=xl;
  el("text",{x:14,y:H/2,"font-size":13,"text-anchor":"middle",fill:"#4A5472",transform:`rotate(-90 14 ${H/2})`},svg).textContent=yl}

// realce de sintaxe minimo para os paineis de codigo (sem dependencia externa)
const PY_RE=/(#[^\n]*)|("(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')|\b(\d+\.?\d*)\b|\b(from|import|as|def|return|print|if|else|elif|for|in|while|with|class|None|True|False|and|or|not|lambda)\b/g;
function highlight(src){let out="",last=0,m;PY_RE.lastIndex=0;
  while((m=PY_RE.exec(src))!==null){out+=esc(src.slice(last,m.index));
    const cls=m[1]?"c":m[2]?"s":m[3]?"n":"k";out+=`<span class="${cls}">${esc(m[0])}</span>`;last=PY_RE.lastIndex}
  return out+esc(src.slice(last))}

// Python no navegador via Pyodide, e matplotlib por cima. A aula registra em
// PyUI onde o andamento aparece e o que fazer quando uma figura falha; o core
// nao conhece nenhum id.
const PYODIDE="https://cdn.jsdelivr.net/pyodide/v0.27.5/full/";
const PyUI={statusSel:null,onFigFail:null};
const pySay=t=>{if(!PyUI.statusSel)return;const e=$(PyUI.statusSel);if(e)e.textContent=t};
let pyReady=null;
async function getPy(){if(pyReady)return pyReady;pyReady=(async()=>{pySay(S.pyDownload);
  await new Promise((res,rej)=>{const s=document.createElement("script");s.src=PYODIDE+"pyodide.js";s.onload=res;s.onerror=()=>rej(new Error(S.pyNetError));document.head.appendChild(s)});
  const py=await loadPyodide({indexURL:PYODIDE});pySay(S.pySklearn);await py.loadPackage(["scikit-learn"]);pySay(S.pyReady);return py})();
  pyReady.catch(()=>{pyReady=null});return pyReady}

let vizReady=null;
function getViz(){if(vizReady)return vizReady;
  vizReady=(async()=>{const py=await getPy();pySay(S.vizDownload);
    await py.loadPackage(["matplotlib"]);pySay(S.pyReady);return py})();
  vizReady.catch(()=>{vizReady=null});return vizReady}
const figFail=(boxId,msg)=>{$("#"+boxId).classList.remove("busy");$("#"+boxId).innerHTML=`<div class="figmsg">${msg}</div>`};
async function drawFig(boxId,imgId,code,globals){const box=$("#"+boxId);box.classList.add("busy");
  try{const py=await getViz();for(const g in globals)py.globals.set(g,globals[g]);
    const b64=await py.runPythonAsync(code);
    let img=$("#"+imgId);if(!img){box.innerHTML=`<img id="${imgId}">`;img=$("#"+imgId)}
    img.src="data:image/png;base64,"+b64;box.classList.remove("busy");return true}
  catch(e){console.warn(e);
    figFail(boxId,S.vizFail);
    pySay(S.vizFailStatus);if(PyUI.onFigFail)PyUI.onFigFail();return false}}
