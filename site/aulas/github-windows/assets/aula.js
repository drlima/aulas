// aula.js - GitHub no Windows (Tech Challenge Fase 2): guia de consulta.
// Copiar comandos, seletor 5A/5B/5C, progresso (secoes e checklist) e indice.
// Nenhum texto de interface mora aqui: tudo sai de window.STR (S). Do core vem:
// $, $$, T, safeStore, copyButtons, tabSet.
// Sem JS a pagina continua completa: 5A, 5B e 5C aparecem em sequencia.
(function(){
  const KEY="aulas:github-windows:progresso", TABKEY="aulas:github-windows:aba";

  // 1: copiar comandos (um botao em cada bloco de codigo)
  copyButtons("main pre",{label:S.copyLabel,done:S.copyDone,fail:S.copyFail,note:S.copyNote,aria:S.copyAria});

  // 2: seletor 5A / 5B / 5C (5A e o padrao; #5b e #5c abrem a aba certa)
  tabSet({root:"#tabs5",list:S.tabsLabel,def:"5a",key:TABKEY,
    tabs:[{id:"5a",label:S.tab5a},{id:"5b",label:S.tab5b},{id:"5c",label:S.tab5c}]});

  // 3: progresso. st.sec tem um 0/1 por secao de 1 a 10; st.chk, um por item do
  // checklist (secao 10). Tudo passa por safeStore: se o armazenamento falhar, a
  // pagina funciona do mesmo jeito e so avisa que nao vai lembrar.
  const secs=$$("main section.block").filter(s=>/^s\d+$/.test(s.id));
  const itens=$$("#checklist li");
  const st={sec:secs.map(()=>0),chk:itens.map(()=>0)};
  try{const j=JSON.parse(safeStore.get(KEY)||"null");
    if(j&&Array.isArray(j.sec)&&Array.isArray(j.chk)){
      secs.forEach((_,i)=>{st.sec[i]=j.sec[i]?1:0});
      itens.forEach((_,i)=>{st.chk[i]=j.chk[i]?1:0})}}catch(e){}

  const tocLinks=$$("#toc a"), prog=$("#tocProg");
  const aviso=document.createElement("span");
  aviso.className="store-warn";aviso.setAttribute("role","status");
  let salvo=true;
  const pinta=()=>{
    secs.forEach((s,i)=>{
      marcas[i].setAttribute("aria-pressed",st.sec[i]?"true":"false");
      s.classList.toggle("feita",!!st.sec[i]);
      // a secao 5 tem tres ancoras no indice (5A, 5B, 5C): as tres acendem juntas
      tocLinks.filter(l=>{const h=l.getAttribute("href");return h==="#"+s.id||(s.id==="s5"&&/^#5[abc]$/.test(h))})
        .forEach(l=>l.parentNode.classList.toggle("feita",!!st.sec[i]))});
    caixas.forEach((cx,i)=>{cx.checked=!!st.chk[i];itens[i].classList.toggle("feita",!!st.chk[i])});
    const n=st.sec.reduce((a,b)=>a+b,0);
    prog.textContent=T(S.progTpl,{n,total:secs.length})+(salvo?"":" "+S.storeOff);
    aviso.textContent=salvo?"":S.storeOff};
  const save=()=>{salvo=safeStore.set(KEY,JSON.stringify(st));pinta()};

  const marcas=secs.map((s,i)=>{
    const b=document.createElement("button"),box=document.createElement("div");
    b.type="button";b.className="ghost small mark";b.textContent=S.doneMark;b.setAttribute("aria-pressed","false");
    b.addEventListener("click",()=>{st.sec[i]=st.sec[i]?0:1;save()});
    box.className="secdone";box.appendChild(b);s.querySelector(".wrap").appendChild(box);return b});

  const caixas=itens.map((li,i)=>{
    const lb=document.createElement("label"),cx=document.createElement("input");
    cx.type="checkbox";lb.appendChild(cx);lb.append(...li.childNodes);li.appendChild(lb);
    cx.addEventListener("change",()=>{st.chk[i]=cx.checked?1:0;save()});return cx});

  if(itens.length){
    const tudo=document.createElement("button"),linha=document.createElement("div");
    tudo.type="button";tudo.className="ghost small";tudo.textContent=S.checkAll;
    tudo.addEventListener("click",()=>{st.chk.fill(1);save()});
    linha.className="checktools";linha.appendChild(tudo);linha.appendChild(aviso);$("#checklist").after(linha)}

  const limpar=document.createElement("button");
  limpar.type="button";limpar.className="ghost small";limpar.textContent=S.clearProg;
  limpar.addEventListener("click",()=>{st.sec.fill(0);st.chk.fill(0);save()});
  $("#tocTools").appendChild(limpar);
  pinta();

  // 4: indice. Aberto e fixo na lateral no desktop, recolhido no mobile
  const det=$("#toc details"), larga=matchMedia("(min-width:1240px)");
  const ajusta=()=>{det.open=larga.matches};
  ajusta();larga.addEventListener("change",ajusta);
  tocLinks.forEach(l=>l.addEventListener("click",()=>{if(!larga.matches)det.open=false}));
  // realce do item conforme a rolagem; na secao 5 vale a aba aberta
  let vista="s1";
  const atual=()=>{
    const aba=document.querySelector('.tab[aria-selected="true"]');
    const alvo=vista==="s5"&&aba?"#"+aba.id.slice(4):"#"+vista;
    tocLinks.forEach(l=>{if(l.getAttribute("href")===alvo)l.setAttribute("aria-current","true");else l.removeAttribute("aria-current")})};
  $$("main section.block").forEach(s=>new IntersectionObserver(es=>{
    es.forEach(e=>{if(e.isIntersecting){vista=s.id;atual()}})},{rootMargin:"-30% 0px -60% 0px"}).observe(s));
  $$(".tab").forEach(b=>b.addEventListener("click",atual));
  addEventListener("hashchange",atual);
})();
