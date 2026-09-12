// aula.js — __TITULO__. Tudo o que e so desta aula mora aqui. O motor esta em
// core.js, carregado antes: $, el, T, fmt, rnd, gauss, C, scale, axes, quizPair,
// quizOptions, highlight, PyUI e drawFig vem de la. Nenhum texto de interface
// mora aqui: tudo sai de window.STR, definido no HTML de cada idioma.

// bloco 1: um SVG desenhado com scale() e axes() do core.
// Os pontos saem do sorteio com semente do core, entao cada visita ve os mesmos.
const DOM={x0:0,x1:10,y0:0,y1:10};            // o dominio dos dados desta aula
const PTS=Array.from({length:40},()=>{const x=rnd()*10;return {x,y:Math.max(0,Math.min(10,0.7*x+gauss()*1.5))}});
const dec=n=>S.decimalComma?n.replace(".",","):n;
function drawDemo(){const svg=$("#svgDemo"),W=640,H=360,pad=44,a=+$("#slDemo").value;
  const M=scale(DOM,W,H,pad);svg.innerHTML="";
  axes(svg,W,H,pad,S.axX,S.axY);
  const xf=Math.min(DOM.x1,DOM.y1/Math.max(a,1e-9));      // a reta y = a*x, cortada no dominio
  el("line",{x1:M.X({x:0,y:0}),y1:M.Y({x:0,y:0}),x2:M.X({x:xf,y:a*xf}),y2:M.Y({x:xf,y:a*xf}),
    stroke:"#7B61FF","stroke-width":4,"stroke-linecap":"round"},svg);
  let acima=0;
  PTS.forEach(p=>{const up=p.y>a*p.x;if(up)acima++;
    el("circle",{cx:M.X(p),cy:M.Y(p),r:7,fill:up?C.teal:C.coral,stroke:"#fff","stroke-width":1.5},svg)});
  $("#vDemo").textContent=dec(a.toFixed(1));
  $("#demoOut").textContent=T(S.demoOut,{acima:fmt(acima),abaixo:fmt(PTS.length-acima)})}
$("#slDemo").oninput=drawDemo;drawDemo();

// bloco 2: quiz de duas alternativas. Os itens e os rotulos vem de STR.
quizPair("#quiz","#quizOut",S.quiz,{
  opts:[["A",S.quizA],["B",S.quizB]],
  answer:v=>T(S.quizAnswer,{a:v==="A"?S.quizA:S.quizB}),
  done:(o,right,total)=>{o.className="out "+(right===total?"ok":"");
    o.textContent=T(S.quizScore,{right,total})+(right===total?S.quizPerfect:S.quizHint)}});

// bloco 3: quiz de N alternativas, e o realce dos paineis de codigo da pagina
quizOptions("#quiz3","#quiz3Out",S.quiz3,{
  done:(o,right,total)=>{const pct=right/total;
    o.className="out "+(pct===1?"ok":pct<0.5?"bad":"");
    o.textContent=T(S.quiz3Score,{right,total})+(pct===1?S.quiz3Perfect:pct<0.5?S.quiz3Weak:S.quiz3Good)}});
$$("pre code.py").forEach(c=>{c.innerHTML=highlight(c.textContent)});

// bloco 4: Python no navegador.
// APAGUE ESTE TRECHO JUNTO COM O BLOCO 4 DO HTML SE A AULA NAO USA PYTHON.
PyUI.statusSel="#pyStatus";                     // onde o core escreve o andamento
PyUI.onFigFail=()=>{$("#vizBtn").disabled=false};
$("#runBtn").onclick=async()=>{const btn=$("#runBtn"),out=$("#pyOut");btn.disabled=true;out.textContent="";
  try{const py=await getPy();py.setStdout({batched:s=>out.textContent+=s+"\n"});py.setStderr({batched:s=>out.textContent+=s+"\n"});await py.runPythonAsync($("#py").value)}
  catch(e){out.textContent+=String(e).split("\n").slice(-3).join("\n");$("#pyStatus").textContent=S.pyCodeError}
  btn.disabled=false};
// o codigo da figura e o texto do painel #codeDemo; o n do slider vira variavel do Python
const drawDemoFig=()=>drawFig("figDemo","imgDemo",$("#codeDemo").textContent,{n:+$("#slFig").value});
$("#vizBtn").onclick=async()=>{$("#vizBtn").disabled=true;$("#vizWrap").hidden=false;$("#vizNote").textContent=S.vizLoading;
  if(await drawDemoFig())$("#vizNote").textContent=S.vizDone};
let figTimer=null;
$("#slFig").oninput=e=>{$("#vFig").textContent=e.target.value;clearTimeout(figTimer);figTimer=setTimeout(drawDemoFig,260)};
