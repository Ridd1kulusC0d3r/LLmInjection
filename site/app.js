const state={graph:null,landscape:null,diff:null,eco:[],translations:null,search:"",type:"",confidence:"",region:"",ecoClass:"",ecoSection:""};
const TYPE_ORDER=["actor","campaign","incident","vulnerability","technique","test-case","detection","control","framework","model","source"];
const CONF_ORDER=["confirmed","high","medium","low","unverified"];
const MATURITY_ORDER=["observed-in-the-wild","disclosed-vulnerability","research-demonstrated","no-linked-evidence"];
const DATASET_TYPE={actors:"actor",campaigns:"campaign",incidents:"incident",techniques:"technique","test-cases":"test-case",controls:"control",detections:"detection",vulnerabilities:"vulnerability",models:"model",frameworks:"framework"};
const EVID=["campaign","incident","vulnerability"];

function esc(v){return String(v??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));}
const $=s=>document.querySelector(s);
const typeLabel=x=>tOr("type."+x,x), confLabel=x=>tOr("conf."+x,x), matLabel=x=>tOr("mat."+x,String(x||"").replace(/-/g," "));
const grade=g=>t("common.grade.short",{g});

/* Confidence is encoded by shape so it survives greyscale and colour-blindness. */
function confShape(c,x=6,y=6,r=4.5){
  switch(c){
    case"confirmed":return`<rect class="mk" x="${x-r}" y="${y-r}" width="${2*r}" height="${2*r}"/>`;
    case"high":return`<circle class="mk" cx="${x}" cy="${y}" r="${r}"/>`;
    case"medium":return`<circle cx="${x}" cy="${y}" r="${r}" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M${x} ${y-r}A${r} ${r} 0 0 0 ${x} ${y+r}Z" fill="currentColor"/>`;
    case"low":return`<circle cx="${x}" cy="${y}" r="${r}" fill="none" stroke="currentColor" stroke-width="1.4"/>`;
    case"unverified":return`<circle cx="${x}" cy="${y}" r="${r}" fill="none" stroke="currentColor" stroke-width="1.4" stroke-dasharray="2.2 2"/>`;
    default:return`<path d="M${x} ${y-r}L${x+r} ${y}L${x} ${y+r}L${x-r} ${y}Z" fill="none" stroke="currentColor" stroke-width="1.2"/>`;
  }
}
const conf=c=>c?`<span class="conf"><svg viewBox="0 0 12 12" aria-hidden="true" fill="currentColor">${confShape(c)}</svg>${esc(confLabel(c))}</span>`:"";

async function load(){
  const [g,l,d,e,tr]=await Promise.all([
    fetch("graph.json").then(r=>r.json()),
    fetch("landscape.json").then(r=>r.json()),
    fetch("intelligence-diff.json").then(r=>r.ok?r.json():null).catch(()=>null),
    fetch("ecosystem.json").then(r=>r.ok?r.json():[]).catch(()=>[]),
    fetch("translations.json").then(r=>r.ok?r.json():null).catch(()=>null)
  ]);
  Object.assign(state,{graph:g,landscape:l,diff:d,eco:e,translations:tr});
  await setLang(detectLang(),{persist:false});
  initControls();buildFilters();renderAll();applyHash();
}
function visibleNodes(){
  const q=norm(state.search);
  return state.graph.nodes.filter(n=>{
    const c=n.data.confidence||"";
    return(!state.type||n.type===state.type)&&(!state.confidence||c===state.confidence)&&(!state.region||(n.data.regions||[]).includes(state.region))&&(!q||norm(n.label+" "+JSON.stringify(n.data)).includes(q));
  });
}
/* filter selects hold stable English values and translated labels; rebuilt on language change */
function fillSelect(sel,allKey,values,labelFn,current){
  sel.innerHTML=`<option value="">${esc(t(allKey))}</option>`+values.map(v=>`<option value="${esc(v)}">${esc(labelFn(v))}</option>`).join("");
  sel.value=current||"";
}
const byLabel=fn=>(a,b)=>fn(a).localeCompare(fn(b),I18N.locale);
function buildFilters(){
  fillSelect($("#typeFilter"),"filter.type.all",[...new Set(state.graph.nodes.map(n=>n.type))].sort(byLabel(typeLabel)),typeLabel,state.type);
  fillSelect($("#regionFilter"),"filter.region.any",[...new Set(state.graph.nodes.flatMap(n=>n.data.regions||[]))].sort(),x=>x,state.region);
  fillSelect($("#confidenceFilter"),"filter.conf.any",CONF_ORDER,confLabel,state.confidence);
  fillSelect($("#ecoClass"),"filter.eco.class.all",[...new Set(state.eco.map(e=>e.evidence_class))].sort(byLabel(x=>tOr("ecoclass."+x,x))),x=>tOr("ecoclass."+x,x),state.ecoClass);
  fillSelect($("#ecoSection"),"filter.eco.section.all",[...new Set(state.eco.map(e=>e.section))].sort(byLabel(x=>tOr("ecosec."+x,x))),x=>tOr("ecosec."+x,x),state.ecoSection);
  const legend=CONF_ORDER.map(c=>`<span title="${esc(t("confnote."+c))}">${conf(c)}</span>`).join("")+`<span class="conf"><svg viewBox="0 0 12 12" aria-hidden="true" fill="currentColor">${confShape("")}</svg>${esc(t("conf.notrated"))}</span>`;
  $("#confLegend").innerHTML=$("#graphLegend").innerHTML=legend;
  $("#asof").textContent=t("mast.asof",{date:state.landscape.meta?.as_of||"n/a"});
  $("#dataNotice").hidden=I18N.lang==="en";
  const sel=$("#lang");sel.innerHTML=LANGS.map(l=>`<option value="${l.code}">${esc(l.name)}</option>`).join("");sel.value=I18N.lang;
}
function initControls(){
  $("#search").addEventListener("input",e=>{state.search=e.target.value;renderAll()});
  $("#typeFilter").addEventListener("change",e=>{state.type=e.target.value;renderAll()});
  $("#regionFilter").addEventListener("change",e=>{state.region=e.target.value;renderAll()});
  $("#confidenceFilter").addEventListener("change",e=>{state.confidence=e.target.value;renderAll()});
  $("#ecoClass").addEventListener("change",e=>{state.ecoClass=e.target.value;renderEcosystem();afterRender()});
  $("#ecoSection").addEventListener("change",e=>{state.ecoSection=e.target.value;renderEcosystem();afterRender()});
  $("#lang").addEventListener("change",e=>switchLang(e.target.value));
  document.querySelectorAll(".tab").forEach(b=>{b.onclick=()=>showTab(b.dataset.tab,true);b.onkeydown=tabKeys});
  document.querySelectorAll("[data-export]").forEach(b=>b.onclick=()=>exportCsv(b.dataset.export));
  window.addEventListener("hashchange",applyHash);
  $("#closeDrawer").onclick=closeDrawer;
  document.addEventListener("keydown",e=>{
    if(e.key==="Escape"&&$("#drawer").classList.contains("open"))closeDrawer();
    if(e.key==="Tab"&&$("#drawer").classList.contains("open")&&$("#drawer").contains(document.activeElement))trapFocus(e);
    if((e.key==="Enter"||e.key===" ")&&e.target.matches?.("[data-id]:not(a):not(button)")){e.preventDefault();openNode(e.target.dataset.id)}
  });
  document.addEventListener("click",e=>{const el=e.target.closest("[data-id]");if(el&&!el.closest("svg")){if(e.target.closest("a[href]"))e.preventDefault();openNode(el.dataset.id)}});
  $("#theme").onclick=()=>{
    const cur=document.documentElement.dataset.theme||(matchMedia("(prefers-color-scheme:dark)").matches?"dark":"light");
    const next=cur==="dark"?"light":"dark";document.documentElement.dataset.theme=next;
    try{localStorage.setItem("llmi-theme",next)}catch(_){}
  };
  try{const th=localStorage.getItem("llmi-theme");if(th)document.documentElement.dataset.theme=th}catch(_){}
}
async function switchLang(code){
  await setLang(code);
  patchHash({lang:code==="en"?null:code});
  buildFilters();renderAll();
}
const stat=(v,k)=>`<div class="stat"><b>${v}</b><span>${esc(k)}</span></div>`;

/* ---------- tabs, hash, keyboard */
function showTab(name,push){
  const tab=document.querySelector(`.tab[data-tab="${name}"]`);if(!tab)return;
  document.querySelectorAll(".tab").forEach(x=>{const on=x===tab;x.classList.toggle("active",on);x.setAttribute("aria-selected",on);x.tabIndex=on?0:-1});
  document.querySelectorAll(".view").forEach(x=>x.classList.toggle("active",x.id===name));
  if(push)patchHash({tab:name});
}
function tabKeys(e){
  const tabs=[...document.querySelectorAll(".tab")],i=tabs.indexOf(e.currentTarget);
  const to={ArrowRight:(i+1)%tabs.length,ArrowLeft:(i-1+tabs.length)%tabs.length,Home:0,End:tabs.length-1}[e.key];
  if(to===undefined)return;
  e.preventDefault();tabs[to].focus();showTab(tabs[to].dataset.tab,true);
}
function patchHash(patch){
  const p=new URLSearchParams(location.hash.slice(1));
  Object.entries(patch).forEach(([k,v])=>v==null?p.delete(k):p.set(k,v));
  const h=p.toString()?"#"+p.toString():location.pathname+location.search;
  try{history.replaceState(null,"",h)}catch(_){location.hash=h}
}
function applyHash(){
  const p=new URLSearchParams(location.hash.slice(1));
  const l=p.get("lang");if(l&&l!==I18N.lang&&LANGS.some(x=>x.code===l)){switchLang(l);return}
  if(p.get("tab"))showTab(p.get("tab"),false);
  if(p.get("node")){const tb=nodeTab(p.get("node"));if(tb&&!p.get("tab"))showTab(tb,false);openNode(p.get("node"),false)}
}
function nodeTab(id){const n=state.graph.nodes.find(x=>x.id===id);return{technique:"coverage",source:"sources",actor:"overview",campaign:"timeline",incident:"timeline",vulnerability:"timeline"}[n?.type]||null}
/* rows and cards that open a record must be reachable and operable from the keyboard */
function afterRender(){
  document.querySelectorAll("[data-id]:not(a):not(.node)").forEach(el=>{if(!el.hasAttribute("tabindex"))el.tabIndex=0;if(el.tagName!=="TR"&&!el.hasAttribute("role"))el.setAttribute("role","button")});
}

/* ---------- CSV: UTF-8 with a byte-order mark so Excel reads accents and non-Latin text */
function csvCell(v){const s=Array.isArray(v)?v.join("; "):String(v??"");return /[",\n]/.test(s)?`"${s.replace(/"/g,'""')}"`:s}
function csvText(headers,rows){return"﻿"+[headers,...rows].map(r=>r.map(csvCell).join(",")).join("\r\n")}
function exportCsv(kind){
  let headers,rows;
  const ids=new Set(visibleNodes().map(n=>n.id));
  if(kind==="coverage"){headers=["id","technique","maturity","evidence","tests","detections","controls","tools"];rows=techStats().filter(r=>ids.has(r.n.id)).map(r=>[r.n.id,r.n.label,r.n.data.maturity,r.evidence,r.tests,r.detections,r.controls,r.tools])}
  else if(kind==="ecosystem"){headers=["id","repository","evidence_class","section","priority","status","techniques","grade","summary"];rows=ecoRows().map(e=>[e.id,`${e.owner}/${e.name}`,e.evidence_class,e.section,e.priority,e.status,e.techniques,e.source_grade,e.summary])}
  else if(kind==="sources"){headers=["id","name","publisher","grade","published","url"];rows=visibleNodes().filter(n=>n.type==="source").map(n=>[n.id,n.label,n.data.publisher,n.data.grade,n.data.published,n.data.url])}
  else{headers=["id","type","name","date","confidence","regions"];rows=timelineItems().map(({n,date})=>[n.id,n.type,n.label,date,n.data.confidence,n.data.regions])}
  const a=document.createElement("a");a.href=URL.createObjectURL(new Blob([csvText(headers,rows)],{type:"text/csv;charset=utf-8"}));a.download=`llminjection-${kind}.csv`;document.body.appendChild(a);a.click();a.remove();
}

/* ---------- renderers */
function renderMetrics(){
  const c={};state.graph.nodes.forEach(n=>c[n.type]=(c[n.type]||0)+1);
  $("#metrics").innerHTML=[["actors",c.actor],["campaigns",c.campaign],["incidents",c.incident],["vulnerabilities",c.vulnerability],["techniques",c.technique],["sources",c.source]].map(([k,v])=>stat(nf(v||0),t("stat."+k))).join("");
}
function renderActors(){
  const ns=visibleNodes().filter(n=>n.type==="actor");
  $("#actors").innerHTML=ns.map(n=>`<div class="row" data-id="${esc(n.id)}"><div class="k">${esc(n.data.nexus||t("actors.unattributed"))}</div><div><h3>${esc(n.label)}</h3><p>${esc(n.data.summary||"")}</p></div>${conf(n.data.confidence)}</div>`).join("")||`<p class="empty">${esc(t("actors.none"))}</p>`;
}
function renderDomains(){
  $("#domains").innerHTML=(state.landscape.domains||[]).map(d=>`<div class="dom"><header><h3>${esc(d.name)}</h3><span class="trend ${esc(d.trend)}">${esc(tOr("trend."+d.trend,d.trend))}</span></header><p>${esc(d.summary)}</p><div class="tags">${(d.defensive_focus||[]).slice(0,4).map(x=>`<span>${esc(x)}</span>`).join("")}</div></div>`).join("");
}
const fmt=v=>v&&typeof v==="object"&&"from"in v?`${esc(v.from)} → ${esc(v.to)}`:typeof v==="number"?(v>=1e6?nf(v,{notation:"compact",maximumFractionDigits:1}):nf(v)):esc(v);
function renderLandscape(){
  const L=state.landscape;
  $("#metricTable").innerHTML=`<thead><tr><th>${esc(t("th.metric"))}</th><th class="num">${esc(t("th.value"))}</th><th>${esc(t("th.unit"))}</th><th>${esc(t("th.source"))}</th><th>${esc(t("th.conf"))}</th></tr></thead><tbody>`+
    (L.key_metrics||[]).map(m=>`<tr><td>${esc(m.name)}</td><td class="num"><b>${fmt(m.value)}</b></td><td>${esc(m.unit)}<br><span class="id">${esc(m.timeframe)}</span></td><td><a href="${esc(m.source.url)}" rel="noopener">${esc(m.source.publisher)}</a> <span class="id">${esc(grade(m.source.grade))}</span></td><td>${conf(m.confidence)}</td></tr>`).join("")+"</tbody>";
  const groups={};(L.sector_signals||[]).forEach(s=>(groups[s.metric]=groups[s.metric]||[]).push(s));
  $("#sectors").innerHTML=Object.entries(groups).map(([metric,rows])=>{
    const max=Math.max(...rows.map(r=>r.value));
    return`<h3 style="margin:0 0 8px">${esc(metric)}</h3><div class="bars">`+rows.map(r=>`<div class="bar"><span>${esc(r.sector)}</span><i style="width:${(100*r.value/max).toFixed(1)}%" title="${esc(r.source)}"></i><b>${fmt(r.value)}${r.unit==="percent"?"%":""}</b></div>`).join("")+`</div><p class="note" style="margin:-14px 0 24px">${esc(rows[0].source)}${rows[0].timeframe?", "+esc(rows[0].timeframe):""}</p>`;
  }).join("");
  $("#leads").innerHTML=(L.research_queue||[]).map(q=>`<div class="dom"><header><h3 style="font-weight:500">${esc(q.claim)}</h3></header><p>${esc(q.reason)}</p><div class="tags"><span>${esc(q.status)}</span></div></div>`).join("");
}
function renderGraph(){
  const nodes=visibleNodes().slice(0,400),ids=new Set(nodes.map(n=>n.id));
  const edges=state.graph.edges.filter(e=>ids.has(e.source)&&ids.has(e.target));
  $("#graphCount").textContent=t("graph.count",{n:nf(nodes.length),e:nf(edges.length)});
  const types=[...TYPE_ORDER.filter(x=>nodes.some(n=>n.type===x)),...[...new Set(nodes.map(n=>n.type))].filter(x=>!TYPE_ORDER.includes(x))];
  const W=1900,pad=44,rowH=22,top=64,groups=types.map(x=>nodes.filter(n=>n.type===x));
  const H=top+Math.max(1,...groups.map(g=>g.length))*rowH+30,pos={};
  const colX=i=>types.length===1?W/2:pad+i*(W-2*pad-150)/(types.length-1);
  types.forEach((x,i)=>groups[i].forEach((n,j)=>pos[n.id]={x:colX(i),y:top+j*rowH,col:i,row:j}));
  const svg=$("#graphSvg");svg.setAttribute("viewBox",`0 0 ${W} ${H}`);
  svg.innerHTML=types.map((x,i)=>`<text class="gcol" x="${colX(i)-6}" y="30">${esc(typeLabel(x))} · ${groups[i].length}</text><line x1="${colX(i)-6}" x2="${colX(i)+150}" y1="40" y2="40" stroke="currentColor" opacity=".35"/>`).join("")+
    edges.map(e=>{const a=pos[e.source],b=pos[e.target];return`<line class="edge" data-a="${esc(e.source)}" data-b="${esc(e.target)}" x1="${a.x}" y1="${a.y}" x2="${b.x}" y2="${b.y}"/>`}).join("")+
    nodes.map((n,k)=>{const p=pos[n.id],name=`${n.label} (${typeLabel(n.type)}, ${n.data.confidence?confLabel(n.data.confidence):t("conf.notrated")})`;return`<g class="node" data-nid="${esc(n.id)}" data-col="${p.col}" data-row="${p.row}" tabindex="${k===0?0:-1}" role="button" aria-label="${esc(name)}" transform="translate(${p.x} ${p.y})" style="color:var(--ink)"><title>${esc(name)}</title><g transform="translate(-6 -6)">${confShape(n.data.confidence)}</g><text x="12" y="4">${esc(n.label.length>23?n.label.slice(0,22)+"…":n.label)}</text></g>`}).join("");
  const trace=(id,on)=>{
    const near=new Set([id]);svg.querySelectorAll(".edge").forEach(l=>{const hit=l.dataset.a===id||l.dataset.b===id;l.classList.toggle("on",on&&hit);if(hit){near.add(l.dataset.a);near.add(l.dataset.b)}});
    svg.querySelectorAll(".node").forEach(g=>{g.classList.toggle("dim",on&&!near.has(g.dataset.nid));g.classList.toggle("on",on&&g.dataset.nid===id)});
  };
  svg.onmouseover=e=>{const g=e.target.closest(".node");if(g)trace(g.dataset.nid,true)};
  svg.onmouseout=e=>{const g=e.target.closest(".node");if(g)trace(g.dataset.nid,false)};
  svg.onfocusin=e=>{const g=e.target.closest(".node");if(g)trace(g.dataset.nid,true)};
  svg.onfocusout=e=>{const g=e.target.closest(".node");if(g)trace(g.dataset.nid,false)};
  svg.onclick=e=>{const g=e.target.closest(".node");if(g)openNode(g.dataset.nid)};
  /* roving tabindex: one tab stop for the graph, arrows move between nodes */
  svg.onkeydown=e=>{
    const g=e.target.closest(".node");if(!g)return;
    if(e.key==="Enter"||e.key===" "){e.preventDefault();openNode(g.dataset.nid);return}
    const col=+g.dataset.col,row=+g.dataset.row,all=[...svg.querySelectorAll(".node")];
    const inCol=c=>all.filter(n=>+n.dataset.col===c).sort((a,b)=>a.dataset.row-b.dataset.row);
    let next=null;
    if(e.key==="ArrowDown")next=inCol(col)[row+1];
    else if(e.key==="ArrowUp")next=inCol(col)[row-1];
    else if(e.key==="ArrowRight"||e.key==="ArrowLeft"){
      for(let c=col+(e.key==="ArrowRight"?1:-1);c>=0&&c<types.length&&!next;c+=(e.key==="ArrowRight"?1:-1)){const list=inCol(c);if(list.length)next=list[Math.min(row,list.length-1)]}
    }else return;
    e.preventDefault();
    if(next){all.forEach(n=>n.tabIndex=-1);next.tabIndex=0;next.focus()}
  };
}
function techStats(){
  const nodes=new Map(state.graph.nodes.map(n=>[n.id,n]));
  return state.graph.nodes.filter(n=>n.type==="technique").map(n=>{
    const es=state.graph.edges.filter(e=>e.source===n.id||e.target===n.id);
    const other=e=>e.source===n.id?e.target:e.source;
    const evidence=new Set(es.map(other).filter(o=>EVID.includes(nodes.get(o)?.type)));
    const c=rel=>es.filter(e=>e.relationship===rel).length;
    return{n,evidence:evidence.size,tests:c("validates"),detections:c("detects"),controls:c("mitigated-by"),tools:state.eco.filter(e=>(e.techniques||[]).includes(n.id)).length};
  });
}
const heat=n=>`<span class="heat h${Math.min(n,4)}">${n||"0"}</span>`;
function renderCoverage(){
  const q=new Set(visibleNodes().map(n=>n.id));
  const rows=techStats().filter(r=>q.has(r.n.id));
  $("#coverageTable").innerHTML=`<thead><tr><th>${esc(t("th.technique"))}</th><th>${esc(t("th.maturity"))}</th><th>${esc(t("th.evidence"))}</th><th>${esc(t("th.tests"))}</th><th>${esc(t("th.detections"))}</th><th>${esc(t("th.controls"))}</th><th>${esc(t("th.tools"))}</th></tr></thead><tbody>`+rows.map(r=>{
    const gaps=[r.tests?"":t("gaps.notest"),r.detections?"":t("gaps.nodet")].filter(Boolean),pri=r.evidence>0&&gaps.length;
    return`<tr data-id="${esc(r.n.id)}"><td><b>${esc(r.n.label)}</b>${gaps.length?`<span class="gap${pri?"":" mute"}">${pri?esc(t("gaps.priority"))+" · ":""}${esc(gaps.join(" · "))}</span>`:""}<br><span class="id">${esc(r.n.id)}</span></td><td><span class="mat ${esc(r.n.data.maturity)}">${esc(matLabel(r.n.data.maturity))}</span></td><td>${heat(r.evidence)}</td><td>${heat(r.tests)}</td><td>${heat(r.detections)}</td><td>${heat(r.controls)}</td><td>${heat(r.tools)}</td></tr>`;
  }).join("")+"</tbody>";
}
const nodeDate=n=>String(n.data.reported||n.data.first_seen||n.data.date||n.data.published||"");
function timelineItems(){return visibleNodes().filter(n=>["campaign","incident","vulnerability"].includes(n.type)).map(n=>({n,date:nodeDate(n)||t("common.undated")})).sort((a,b)=>b.date.localeCompare(a.date))}
function renderTimeline(){
  $("#timelineList").innerHTML=timelineItems().map(({n,date})=>`<div class="d">${esc(date)}</div><div class="e" data-id="${esc(n.id)}"><div class="kind">${esc(typeLabel(n.type))}${(n.data.regions||[]).length?" · "+esc(n.data.regions.join(", ")):""}</div><h3>${esc(n.label)}</h3><p>${esc(n.data.summary||"")}</p><div style="margin-top:6px">${conf(n.data.confidence)}</div></div>`).join("")||`<p class="empty">${esc(t("common.nothing"))}</p>`;
}
function renderSources(){
  $("#sourceList").innerHTML=visibleNodes().filter(n=>n.type==="source").map(n=>`<div class="it" data-id="${esc(n.id)}"><div class="grade" aria-label="${esc(grade(n.data.grade))}">${esc(n.data.grade)}</div><div><h3>${esc(n.label)}</h3><p>${esc(n.data.publisher||"")} · ${esc(n.data.role||"")}</p></div></div>`).join("")||`<p class="empty">${esc(t("common.nothing"))}</p>`;
}
function renderWhatsNew(){
  const box=$("#diffSummary"),table=$("#diffTable");
  if(!state.diff){box.innerHTML=stat("–",t("new.nodiff"));table.innerHTML="";return}
  const s=state.diff.summary||{};
  box.innerHTML=stat(nf(s.added||0),t("new.added"))+stat(nf(s.removed||0),t("new.removed"))+stat(nf(s.changed||0),t("new.changed"));
  const rows=Object.entries(state.diff.datasets||{}).filter(([,v])=>v.added.length||v.removed.length||v.changed.length);
  table.innerHTML=`<thead><tr><th>${esc(t("th.dataset"))}</th><th class="num">${esc(t("th.added"))}</th><th class="num">${esc(t("th.removed"))}</th><th class="num">${esc(t("th.changed"))}</th></tr></thead><tbody>`+
    (rows.length?rows.map(([k,v])=>`<tr><td>${esc(k)}</td><td class="num">${v.added.length}</td><td class="num">${v.removed.length}</td><td class="num">${v.changed.length}</td></tr>`).join(""):`<tr><td colspan="4">${esc(t("new.nochanges"))}</td></tr>`)+"</tbody>";
}
const link=(id,text)=>`<a href="#" data-id="${esc(id)}">${esc(text)}</a>`;
const meter=(label,n,total,cls="")=>`<div class="meter ${cls}"><span>${esc(label)}</span><em>${n}/${total}</em><i><b style="width:${total?(100*n/total).toFixed(1):0}%"></b></i></div>`;
function renderDashboard(){
  const rows=techStats(),N=rows.length;
  const full=rows.filter(r=>r.tests&&r.detections&&r.controls).length;
  $("#dashCoverage").innerHTML=meter(t("cov.test"),rows.filter(r=>r.tests).length,N)+meter(t("cov.det"),rows.filter(r=>r.detections).length,N)+meter(t("cov.ctl"),rows.filter(r=>r.controls).length,N)+meter(t("cov.full"),full,N,"hero")+meter(t("cov.tool"),rows.filter(r=>r.tools).length,N);
  const gaps=rows.filter(r=>r.evidence&&(!r.tests||!r.detections)).sort((a,b)=>b.evidence-a.evidence);
  const noCtl=rows.filter(r=>!r.controls).sort((a,b)=>b.evidence-a.evidence);
  const gapRow=(r,txt)=>`<div class="gap-item" data-id="${esc(r.n.id)}"><span class="id">${esc(r.n.id.slice(-4))}</span><span><b>${esc(r.n.label)}</b><span class="tags note">${esc(txt)}</span></span></div>`;
  const why=r=>[r.tests?"":t("gaps.notest"),r.detections?"":t("gaps.nodet")].filter(Boolean).join(", ");
  $("#dashGaps").innerHTML=gaps.length?`<div class="gaplist">`+gaps.slice(0,6).map(r=>gapRow(r,`${t("gaps.linked",{n:r.evidence})} · ${why(r)}`)).join("")+`</div>`:
    `<p class="empty" style="padding-top:0">${esc(t("gaps.none"))}</p>`+(noCtl.length?`<p class="note" style="margin-top:14px">${esc(t("gaps.next"))}</p><div class="gaplist">`+noCtl.slice(0,5).map(r=>gapRow(r,`${t("gaps.linked",{n:r.evidence})} · ${t("gaps.noctl")}`)).join("")+`</div>`:"");
  const rated=state.graph.nodes.filter(n=>n.data.confidence),tot=rated.length,by={};rated.forEach(n=>by[n.data.confidence]=(by[n.data.confidence]||0)+1);
  const ramp=["var(--seq-4)","var(--seq-3)","var(--seq-2)","var(--seq-1)","var(--seq-0)"];
  $("#dashConf").innerHTML=`<div class="stack" role="img" aria-label="${esc(t("dash.conf.aria"))}">${CONF_ORDER.map((c,i)=>by[c]?`<i title="${esc(confLabel(c))}: ${by[c]}" style="width:${(100*by[c]/tot).toFixed(1)}%;background:${ramp[i]}"></i>`:"").join("")}</div><div class="leg">${CONF_ORDER.map(c=>`<span>${conf(c)}</span><b>${by[c]||0}</b>`).join("")}</div><p class="note" style="margin-top:12px">${esc(t("dash.conf.note",{n:nf(tot)}))}</p>`;
  const L=state.landscape,pick=["METRIC-WEF-AI-DRIVER","METRIC-GTIG-6H-HARVEST","METRIC-GTIG-DISTILL","METRIC-IBM-SUPPLYCHAIN"].map(id=>(L.key_metrics||[]).find(m=>m.id===id)).filter(Boolean);
  const heads=pick.length?pick:(L.key_metrics||[]).slice(0,4);
  $("#dashHeadlines").innerHTML=heads.map(m=>`<div class="head"><b>${fmt(m.value)}${/percent/.test(m.unit)?"%":""}</b><span>${esc(m.name)}</span><small>${esc(m.unit.replace(/^percent.*/,"percent"))} · ${esc(m.source.publisher)} · ${esc(grade(m.source.grade))}</small></div>`).join("");
  const ecoById=new Map(state.eco.map(e=>[e.id,e])),label=id=>state.graph.nodes.find(n=>n.id===id)?.label||ecoById.get(id)?.name||id;
  const ds=Object.entries(state.diff?.datasets||{}),ecoAdded=(ds.find(([k])=>k==="ecosystem.json")?.[1].added||[]).length;
  const added=ds.filter(([k])=>!/relationships|sources|ecosystem/.test(k)).flatMap(([k,v])=>v.added.map(id=>[DATASET_TYPE[k.replace(".json","")]||k.replace(".json",""),id]));
  $("#dashChanges").innerHTML=state.diff?`<div class="chg">${added.slice(0,8).map(([k,id])=>`<span class="k">${esc(typeLabel(k))}</span><span>${link(id,label(id))}</span>`).join("")}${ecoAdded?`<span class="k">${esc(t("tab.ecosystem"))}</span><span>${esc(t("changes.eco",{n:nf(ecoAdded)}))}</span>`:""}</div><p class="chg-more">${added.length>8?esc(t("changes.more",{n:nf(added.length-8)}))+" · ":""}${esc(t("changes.summary",{added:nf(state.diff.summary.added),removed:nf(state.diff.summary.removed),changed:nf(state.diff.summary.changed),date:String(state.diff.baseline||"").slice(0,10)}))}</p>`:`<p class="empty">${esc(t("diff.none"))}</p>`;
  const tl=state.graph.nodes.filter(n=>["campaign","incident","vulnerability"].includes(n.type)).map(n=>({n,date:nodeDate(n)})).filter(x=>x.date).sort((a,b)=>b.date.localeCompare(a.date)).slice(0,7);
  $("#dashTimeline").innerHTML=`<div class="mini">${tl.map(({n,date})=>`<span class="d">${esc(date.slice(0,10))}</span><span>${link(n.id,n.label)}<br><span class="note">${esc(typeLabel(n.type))} · ${esc(n.data.confidence?confLabel(n.data.confidence):(n.data.severity||""))}</span></span>`).join("")}</div>`;
  const mt={};rows.forEach(r=>mt[r.n.data.maturity]=(mt[r.n.data.maturity]||0)+1);
  $("#dashMaturity").innerHTML=`<div class="bars sm">${MATURITY_ORDER.map(k=>`<div class="bar"><span>${esc(matLabel(k))}</span><i style="width:${(100*(mt[k]||0)/Math.max(1,...Object.values(mt))).toFixed(1)}%"></i><b>${mt[k]||0}</b></div>`).join("")}</div><p class="note" style="margin-top:8px">${esc(t("dash.maturity.note"))}</p>`;
  const src=state.graph.nodes.filter(n=>n.type==="source"),gs=["A","B","C","D","E"].map(g=>[g,src.filter(n=>n.data.grade===g).length]),mx=Math.max(1,...gs.map(x=>x[1]));
  $("#dashGrades").innerHTML=`<div class="bars sm">${gs.map(([g,n])=>`<div class="bar"><span>${esc(t("common.grade",{g}))}</span><i style="width:${(100*n/mx).toFixed(1)}%"></i><b>${n}</b></div>`).join("")}</div>`;
  const cl={};state.eco.forEach(e=>cl[e.evidence_class]=(cl[e.evidence_class]||0)+1);const cm=Math.max(1,...Object.values(cl));
  $("#dashEco").innerHTML=state.eco.length?`<div class="bars sm">${Object.entries(cl).sort((a,b)=>b[1]-a[1]).map(([k,n])=>`<div class="bar"><span>${esc(tOr("ecoclass."+k,k))}</span><i style="width:${(100*n/cm).toFixed(1)}%"></i><b>${n}</b></div>`).join("")}</div><p class="note" style="margin-top:8px">${esc(t("dash.eco.note",{n:nf(state.eco.length),s:nf(state.eco.filter(e=>e.priority==="start-here").length)}))}</p>`:`<p class="empty">${esc(t("dash.eco.none"))}</p>`;
}
function ecoRows(){
  const q=norm(state.search);
  return state.eco.filter(e=>(!state.ecoClass||e.evidence_class===state.ecoClass)&&(!state.ecoSection||e.section===state.ecoSection)&&(!q||norm(e.name+" "+e.owner+" "+e.summary).includes(q)));
}
function renderEcosystem(){
  const rows=ecoRows();
  $("#ecoCount").textContent=t("eco.count",{n:nf(rows.length),total:nf(state.eco.length)});
  $("#ecoTable").innerHTML=`<thead><tr><th>${esc(t("th.project"))}</th><th>${esc(t("th.class"))}</th><th>${esc(t("th.techniques"))}</th><th>${esc(t("th.scope"))}</th></tr></thead><tbody>`+(rows.map(e=>`<tr><td><a class="out" href="${esc(e.url)}" rel="noopener"><b>${esc(e.owner)}/${esc(e.name)}</b></a>${e.priority==="start-here"?`<span class="eco-flag">${esc(t("eco.starthere"))}</span>`:""}${e.status==="archived-reported"?`<span class="eco-flag mute">${esc(t("eco.archived"))}</span>`:""}<br><span class="id">${esc(e.id)} · ${esc(grade(e.source_grade))}</span></td><td><span class="id">${esc(tOr("ecoclass."+e.evidence_class,e.evidence_class))}</span></td><td>${(e.techniques||[]).map(x=>link(x,x.slice(-4))).join(" ")||`<span class="id">${esc(t("common.none"))}</span>`}</td><td>${esc(e.summary)}</td></tr>`).join("")||`<tr><td colspan="4">${esc(t("eco.nomatch"))}</td></tr>`)+"</tbody>";
}
function renderLanguages(){
  $("#langPicker").innerHTML=LANGS.map(l=>`<button type="button" class="lang-btn${l.code===I18N.lang?" on":""}" data-lang="${l.code}" lang="${l.htmlLang}" aria-pressed="${l.code===I18N.lang}">${esc(l.name)}</button>`).join("");
  $("#langPicker").querySelectorAll("button").forEach(b=>b.onclick=()=>{switchLang(b.dataset.lang);$("#lang").value=b.dataset.lang});
  const tr=state.translations,base=tr?.base||"";
  const cell=p=>p?`<a class="out" href="${esc(base+p)}" rel="noopener">${esc(p.split("/").pop())}</a>`:`<span class="id">${esc(t("lang.na"))}</span>`;
  const rows=LANGS.map(l=>{const m=(tr?.languages||[]).find(x=>x.code===l.code)||{};
    return`<tr><td lang="${l.htmlLang}"><b>${esc(l.name)}</b></td><td>${l.code==="en"?esc(t("lang.original")):esc(t("lang.yes"))}</td><td>${cell(m.readme)}</td><td>${cell(m.regional)}</td><td>${esc(m.review==="original"?t("lang.original"):t("lang.status.machine"))}</td></tr>`}).join("");
  $("#langTable").innerHTML=`<thead><tr><th>${esc(t("th.language"))}</th><th>${esc(t("th.interface"))}</th><th>${esc(t("th.readme"))}</th><th>${esc(t("th.regional"))}</th><th>${esc(t("th.review"))}</th></tr></thead><tbody>${rows}</tbody>`;
}
/* ---------- drawer */
let lastFocus=null;
function focusables(root){return[...root.querySelectorAll('a[href],button:not([disabled]),summary,[tabindex]:not([tabindex="-1"])')].filter(x=>x.offsetParent!==null)}
function trapFocus(e){
  const f=focusables($("#drawer"));if(!f.length)return;
  const first=f[0],last=f[f.length-1];
  if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus()}
  else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus()}
}
function closeDrawer(){
  const d=$("#drawer");if(!d.classList.contains("open"))return;
  d.classList.remove("open");d.setAttribute("aria-hidden","true");
  patchHash({node:null});
  if(lastFocus&&document.contains(lastFocus))lastFocus.focus();
}
const SKIP=new Set(["id","type","name","summary","source_ids","sources","external_mappings","label","hypothesis","verification"]);
function openNode(id,push=true){
  const n=state.graph.nodes.find(x=>x.id===id);if(!n)return;
  if(push)patchHash({node:id});
  if(!$("#drawer").classList.contains("open"))lastFocus=document.activeElement;
  const nodes=new Map(state.graph.nodes.map(x=>[x.id,x])),groups={};
  state.graph.edges.filter(e=>e.source===id||e.target===id).forEach(e=>{
    const out=e.source===id,other=out?e.target:e.source,rel=tOr("rel."+e.relationship,e.relationship),key=out?rel:t("rel.incoming",{rel});
    (groups[key]=groups[key]||[]).push({other,label:nodes.get(other)?.label||other,confidence:e.confidence});
  });
  const rel=Object.entries(groups).map(([k,v])=>`<div class="grp"><h4>${esc(k)} · ${v.length}</h4><ul>${v.map(x=>`<li><a href="#" data-id="${esc(x.other)}">${esc(x.label)}</a> ${conf(x.confidence)}</li>`).join("")}</ul></div>`).join("");
  const factVal=(k,v)=>k==="maturity"?matLabel(v):k==="confidence"?confLabel(v):Array.isArray(v)?v.join(", "):v;
  const facts=Object.entries(n.data).filter(([k,v])=>!SKIP.has(k)&&v!==null&&v!==""&&(typeof v!=="object"||(Array.isArray(v)&&v.every(x=>typeof x!=="object")))).map(([k,v])=>`<dt>${esc(tOr("fact."+k,k.replace(/_/g," ")))}</dt><dd>${esc(factVal(k,v))}</dd>`).join("");
  const srcIds=(n.data.source_ids||[]).map(s=>nodes.get(s)).filter(Boolean),srcObj=Array.isArray(n.data.sources)?n.data.sources.filter(s=>s&&s.url):[];
  const sources=[...srcIds.map(s=>`<li><a class="out" href="${esc(s.data.url)}" rel="noopener">${esc(s.label)}</a> <span class="id">${esc(grade(s.data.grade))} · ${esc(s.data.publisher||"")}</span></li>`),...srcObj.map(s=>`<li><a class="out" href="${esc(s.url)}" rel="noopener">${esc(s.title||s.url)}</a> <span class="id">${esc(grade(s.grade||""))} · ${esc(s.publisher||"")}</span></li>`)].join("");
  const mapped=(n.data.external_mappings||[]).map(m=>`<li><a class="out" href="${esc(m.url)}" rel="noopener">${esc(m.framework)} ${esc(m.id)}</a> <span class="id">${esc(m.relation)} · ${esc(m.name)}</span></li>`).join("");
  const tools=n.type==="technique"?state.eco.filter(e=>(e.techniques||[]).includes(id)):[];
  $("#drawerBody").innerHTML=`<div class="eyebrow">${esc(typeLabel(n.type))}</div><h2 id="drawerTitle">${esc(n.label)}</h2><p class="id">${esc(n.id)}</p>${conf(n.data.confidence)}${n.data.summary?`<p style="margin-top:12px">${esc(n.data.summary)}</p>`:""}${n.data.hypothesis?`<p style="margin-top:12px">${esc(n.data.hypothesis)}</p>`:""}${facts?`<dl class="facts">${facts}</dl>`:""}${rel?`<h3>${esc(t("drawer.relationships"))}</h3>${rel}`:""}${mapped?`<h3>${esc(t("drawer.mappings"))}</h3><ul>${mapped}</ul>`:""}${tools.length?`<h3>${esc(t("drawer.tools"))}</h3><ul>${tools.map(e=>`<li><a class="out" href="${esc(e.url)}" rel="noopener">${esc(e.owner)}/${esc(e.name)}</a> <span class="id">${esc(tOr("ecoclass."+e.evidence_class,e.evidence_class))}</span></li>`).join("")}</ul>`:""}${sources?`<h3>${esc(t("drawer.evidence"))}</h3><ul>${sources}</ul>`:""}<details><summary>${esc(t("drawer.raw"))}</summary><pre>${esc(JSON.stringify(n.data,null,2))}</pre></details>`;
  const d=$("#drawer");d.classList.add("open");d.setAttribute("aria-hidden","false");
  $("#closeDrawer").focus();
}
function renderAll(){
  if(!state.graph)return;
  renderMetrics();renderDashboard();renderEcosystem();renderActors();renderDomains();renderLandscape();renderWhatsNew();renderGraph();renderCoverage();renderTimeline();renderSources();renderLanguages();afterRender();
}
load().catch(e=>{document.body.insertAdjacentHTML("afterbegin",`<p role="alert" style="padding:12px 28px;background:var(--signal);color:var(--signal-ink);margin:0">${esc(t("err.load",{msg:e.message}))}</p>`)});
