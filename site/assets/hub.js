// hub.js — lista as aulas de data/aulas.json. Carregado depois de core.js, de
// onde vem $, esc e T. Nenhum texto de interface mora aqui: rotulos e mensagens
// saem de window.STR; o endereco do indice, o idioma e a base dos links saem de
// window.HUB, definido inline em cada pagina do hub.
(function(){
  const H=window.HUB, box=$("#aulas");
  const CORES=["marker","coral","teal","grape"];
  const msg=(txt,erro)=>{box.innerHTML=`<p class="hub-msg${erro?" erro":""}" role="status">${txt}</p>`};
  const card=a=>{const L=a[H.lang],capa=a.capa||{};
    const cor=CORES.includes(capa.cor)?capa.cor:"grape";
    const nivel=(S.hubNiveis&&S.hubNiveis[a.nivel])||a.nivel;
    const tags=(a.tags||[]).map(t=>`<span class="tag">${esc(t)}</span>`).join("");
    return `<a class="aula-card" href="${esc(H.base+L.url)}">`+
      `<div class="capa" style="background:var(--${cor})" aria-hidden="true">${esc(capa.emoji||"")}</div>`+
      `<div class="corpo"><h2>${esc(L.titulo)}</h2><p>${esc(L.resumo)}</p>`+
      `<p class="meta">${esc(T(S.hubMeta,{min:a.duracao_min,nivel}))}</p>`+
      (tags?`<div class="tags">${tags}</div>`:"")+`</div></a>`};
  fetch(H.json)
    .then(r=>{if(!r.ok)throw new Error(r.status+" "+H.json);return r.json()})
    .then(d=>{const lista=(d.aulas||[]).filter(a=>a.status!=="rascunho"&&a[H.lang])
        .sort((x,y)=>x.ordem-y.ordem);
      if(!lista.length){msg(S.hubEmpty);return}
      box.innerHTML=lista.map(card).join("")})
    .catch(e=>{console.warn(e);msg(S.hubLoadError,true)});
})();
