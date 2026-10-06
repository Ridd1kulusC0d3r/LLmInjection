const state={graph:null,landscape:null,diff:null,search:"",type:"",confidence:""};
const TYPE_ORDER=["actor","campaign","incident","vulnerability","technique","test-case","detection","control","framework","model","source"];
const CONF_ORDER=["confirmed","high","medium","low","unverified"];
const CONF_NOTE={confirmed:"direct authoritative evidence",high:"strong or multiple sources",medium:"plausible, gaps remain",low:"limited support",unverified:"research lead only"};

function esc(v){return String(v??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));}
const $=s=>document.querySelector(s);

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
const conf=c=>c?`<span class="conf"><svg viewBox="0 0 12 12" aria-hidden="true" fill="currentColor">${confShape(c)}</svg>${esc(c)}</span>`:"";

async function load(){
  const [g,l,d]=await Promise.all([
    fetch("graph.json").then(r=>r.json()),
    fetch("landscape.json").then(r=>r.json()),
    fetch("intelligence-diff.json").then(r=>r.ok?r.json():null).catch(()=>null)
  ]);
  Object.assign(state,{graph:g,landscape:l,diff:d});
  initControls();renderAll();
}
function visibleNodes(){
  const q=state.search.toLowerCase();
  return state.graph.nodes.filter(n=>{
    const c=n.data.confidence||"";
    return(!state.type||n.type===state.type)&&(!state.confidence||c===state.confidence)&&(!q||(n.label+" "+JSON.stringify(n.data)).toLowerCase().includes(q));
  });
}
function initControls(){
  const s=$("#typeFilter");
  [...new Set(state.graph.nodes.map(n=>n.type))].sort().forEach(t=>s.insertAdjacentHTML("beforeend",`<option value="${esc(t)}">${esc(t)}</option>`));
  $("#search").addEventListener("input",e=>{state.search=e.target.value;renderAll()});
  s.addEventListener("change",e=>{state.type=e.target.value;renderAll()});
  $("#confidenceFilter").addEventListener("change",e=>{state.confidence=e.target.value;renderAll()});
  document.querySelectorAll(".tab").forEach(b=>b.onclick=()=>{
    document.querySelectorAll(".tab,.view").forEach(x=>x.classList.remove("active"));
    b.classList.add("active");$("#"+b.dataset.tab).classList.add("active");
  });
  $("#closeDrawer").onclick=closeDrawer;
  document.addEventListener("keydown",e=>{if(e.key==="Escape")closeDrawer()});
  document.addEventListener("click",e=>{const t=e.target.closest("[data-id]");if(t){if(e.target.closest("a[href]"))e.preventDefault();openNode(t.dataset.id)}});
  $("#theme").onclick=()=>{
    const cur=document.documentElement.dataset.theme||(matchMedia("(prefers-color-scheme:dark)").matches?"dark":"light");
    const next=cur==="dark"?"light":"dark";document.documentElement.dataset.theme=next;
    try{localStorage.setItem("llmi-theme",next)}catch(_){}
  };
  try{const t=localStorage.getItem("llmi-theme");if(t)document.documentElement.dataset.theme=t}catch(_){}
  $("#asof").textContent="As of "+(state.landscape.meta?.as_of||"n/a");
  $("#confLegend").innerHTML=$("#graphLegend").innerHTML=CONF_ORDER.map(c=>`<span title="${esc(CONF_NOTE[c])}">${conf(c)}</span>`).join("")+`<span class="conf"><svg viewBox="0 0 12 12" aria-hidden="true" fill="currentColor">${confShape("")}</svg>not rated</span>`;
}
const stat=(v,k)=>`<div class="stat"><b>${v}</b><span>${esc(k)}</span></div>`;
function renderMetrics(){
  const c={};state.graph.nodes.forEach(n=>c[n.type]=(c[n.type]||0)+1);
  $("#metrics").innerHTML=[["Actors",c.actor],["Campaigns",c.campaign],["Incidents",c.incident],["Vulnerabilities",c.vulnerability],["Techniques",c.technique],["Sources",c.source]].map(([k,v])=>stat(v||0,k)).join("");
}
function renderActors(){
  const ns=visibleNodes().filter(n=>n.type==="actor");
  $("#actors").innerHTML=ns.map(n=>`<div class="row" data-id="${esc(n.id)}"><div class="k">${esc(n.data.nexus||"Unattributed")}</div><div><h3>${esc(n.label)}</h3><p>${esc(n.data.summary||"")}</p></div>${conf(n.data.confidence)}</div>`).join("")||'<p class="empty">No matching actors.</p>';
}
function renderDomains(){
  const arrow={rising:"↑ rising",stable:"→ stable",falling:"↓ falling"};
  $("#domains").innerHTML=(state.landscape.domains||[]).map(d=>`<div class="dom"><header><h3>${esc(d.name)}</h3><span class="trend ${esc(d.trend)}">${esc(arrow[d.trend]||d.trend)}</span></header><p>${esc(d.summary)}</p><div class="tags">${(d.defensive_focus||[]).slice(0,4).map(x=>`<span>${esc(x)}</span>`).join("")}</div></div>`).join("");
}
const fmt=v=>v&&typeof v==="object"&&"from"in v?`${esc(v.from)} → ${esc(v.to)}`:typeof v==="number"?(v>=1e6?new Intl.NumberFormat("en",{notation:"compact",maximumFractionDigits:1}).format(v):v.toLocaleString("en")):esc(v);
function renderLandscape(){
  const L=state.landscape;
  $("#metricTable").innerHTML="<thead><tr><th>Metric</th><th class='num'>Value</th><th>Unit and window</th><th>Source</th><th>Confidence</th></tr></thead><tbody>"+
    (L.key_metrics||[]).map(m=>`<tr><td>${esc(m.name)}</td><td class="num"><b>${fmt(m.value)}</b></td><td>${esc(m.unit)}<br><span class="id">${esc(m.timeframe)}</span></td><td><a href="${esc(m.source.url)}" rel="noopener">${esc(m.source.publisher)}</a> <span class="id">grade ${esc(m.source.grade)}</span></td><td>${conf(m.confidence)}</td></tr>`).join("")+"</tbody>";
  const groups={};(L.sector_signals||[]).forEach(s=>(groups[s.metric]=groups[s.metric]||[]).push(s));
  $("#sectors").innerHTML=Object.entries(groups).map(([metric,rows])=>{
    const max=Math.max(...rows.map(r=>r.value));
    return`<h3 style="margin:0 0 8px">${esc(metric)}</h3><div class="bars">`+rows.map(r=>`<div class="bar"><span>${esc(r.sector)}</span><i style="width:${(100*r.value/max).toFixed(1)}%" title="${esc(r.source)}"></i><b>${fmt(r.value)}${r.unit==="percent"?"%":""}</b></div>`).join("")+`</div><p class="note" style="margin:-14px 0 24px">${esc(rows[0].source)}${rows[0].timeframe?", "+esc(rows[0].timeframe):""}</p>`;
  }).join("");
  $("#leads").innerHTML=(L.research_queue||[]).map(q=>`<div class="dom"><header><h3 style="font-weight:500">${esc(q.claim)}</h3></header><p>${esc(q.reason)}</p><div class="tags"><span>${esc(q.status)}</span></div></div>`).join("");
}
const TYPE_LABEL={"test-case":"test case"};
function renderGraph(){
  const nodes=visibleNodes().slice(0,400),ids=new Set(nodes.map(n=>n.id));
  const edges=state.graph.edges.filter(e=>ids.has(e.source)&&ids.has(e.target));
  $("#graphCount").textContent=`${nodes.length} nodes · ${edges.length} edges`;
  const types=[...TYPE_ORDER.filter(t=>nodes.some(n=>n.type===t)),...[...new Set(nodes.map(n=>n.type))].filter(t=>!TYPE_ORDER.includes(t))];
  const W=1900,pad=44,rowH=22,top=64,groups=types.map(t=>nodes.filter(n=>n.type===t));
  const H=top+Math.max(1,...groups.map(g=>g.length))*rowH+30,pos={};
  const colX=i=>types.length===1?W/2:pad+i*(W-2*pad-150)/(types.length-1);
  types.forEach((t,i)=>groups[i].forEach((n,j)=>pos[n.id]={x:colX(i),y:top+j*rowH}));
  const svg=$("#graphSvg");svg.setAttribute("viewBox",`0 0 ${W} ${H}`);
  svg.innerHTML=types.map((t,i)=>`<text class="gcol" x="${colX(i)-6}" y="30">${esc((TYPE_LABEL[t]||t))} · ${groups[i].length}</text><line x1="${colX(i)-6}" x2="${colX(i)+150}" y1="40" y2="40" stroke="currentColor" opacity=".35"/>`).join("")+
    edges.map(e=>{const a=pos[e.source],b=pos[e.target];return`<line class="edge" data-a="${esc(e.source)}" data-b="${esc(e.target)}" x1="${a.x}" y1="${a.y}" x2="${b.x}" y2="${b.y}"/>`}).join("")+
    nodes.map(n=>{const p=pos[n.id];return`<g class="node" data-id="${esc(n.id)}" transform="translate(${p.x} ${p.y})" style="color:var(--ink)"><title>${esc(n.label)} (${esc(n.data.confidence||"not rated")})</title><g transform="translate(-6 -6)">${confShape(n.data.confidence)}</g><text x="12" y="4">${esc(n.label.length>23?n.label.slice(0,22)+"…":n.label)}</text></g>`}).join("");
  const trace=(id,on)=>{
    const near=new Set([id]);svg.querySelectorAll(".edge").forEach(l=>{const hit=l.dataset.a===id||l.dataset.b===id;l.classList.toggle("on",on&&hit);if(hit){near.add(l.dataset.a);near.add(l.dataset.b)}});
    svg.querySelectorAll(".node").forEach(g=>{g.classList.toggle("dim",on&&!near.has(g.dataset.id));g.classList.toggle("on",on&&g.dataset.id===id)});
  };
  svg.onmouseover=e=>{const g=e.target.closest(".node");if(g)trace(g.dataset.id,true)};
  svg.onmouseout=e=>{const g=e.target.closest(".node");if(g)trace(g.dataset.id,false)};
}
function counts(id){
  const es=state.graph.edges.filter(e=>e.source===id||e.target===id);
  const n=rel=>es.filter(e=>e.relationship===rel).length;
  return{tests:n("validates"),detections:n("detects"),controls:n("mitigated-by")};
}
const heat=n=>`<span class="heat h${Math.min(n,4)}">${n||"0"}</span>`;
function renderCoverage(){
  const ts=visibleNodes().filter(n=>n.type==="technique");
  $("#coverageTable").innerHTML="<thead><tr><th>Technique</th><th>Tests</th><th>Detections</th><th>Controls</th></tr></thead><tbody>"+ts.map(n=>{
    const c=counts(n.id),gaps=[c.tests?"":"no test",c.detections?"":"no detection"].filter(Boolean);
    return`<tr data-id="${esc(n.id)}"><td><b>${esc(n.label)}</b>${gaps.map(g=>`<span class="gap">${g}</span>`).join("")}<br><span class="id">${esc(n.id)}</span></td><td>${heat(c.tests)}</td><td>${heat(c.detections)}</td><td>${heat(c.controls)}</td></tr>`;
  }).join("")+"</tbody>";
}
function renderTimeline(){
  const items=visibleNodes().filter(n=>["campaign","incident","vulnerability"].includes(n.type)).map(n=>({n,date:String(n.data.first_seen||n.data.date||n.data.published||n.data.last_seen||"undated")})).sort((a,b)=>b.date.localeCompare(a.date));
  $("#timelineList").innerHTML=items.map(({n,date})=>`<div class="d">${esc(date)}</div><div class="e" data-id="${esc(n.id)}"><div class="kind">${esc(n.type)}</div><h3>${esc(n.label)}</h3><p>${esc(n.data.summary||"")}</p><div style="margin-top:6px">${conf(n.data.confidence)}</div></div>`).join("")||'<p class="empty">Nothing matches.</p>';
}
function renderSources(){
  $("#sourceList").innerHTML=visibleNodes().filter(n=>n.type==="source").map(n=>`<div class="it" data-id="${esc(n.id)}"><div class="grade">${esc(n.data.grade)}</div><div><h3>${esc(n.label)}</h3><p>${esc(n.data.publisher||"")} · ${esc(n.data.role||"")}</p></div></div>`).join("")||'<p class="empty">Nothing matches.</p>';
}
function renderWhatsNew(){
  const box=$("#diffSummary"),table=$("#diffTable");
  if(!state.diff){box.innerHTML=stat("–","no diff available");table.innerHTML="";return}
  const s=state.diff.summary||{};
  box.innerHTML=stat(s.added||0,"added")+stat(s.removed||0,"removed")+stat(s.changed||0,"changed");
  const rows=Object.entries(state.diff.datasets||{}).filter(([,v])=>v.added.length||v.removed.length||v.changed.length);
  table.innerHTML="<thead><tr><th>Dataset</th><th class='num'>Added</th><th class='num'>Removed</th><th class='num'>Changed</th></tr></thead><tbody>"+
    (rows.length?rows.map(([k,v])=>`<tr><td>${esc(k)}</td><td class="num">${v.added.length}</td><td class="num">${v.removed.length}</td><td class="num">${v.changed.length}</td></tr>`).join(""):'<tr><td colspan="4">No changes since the latest snapshot.</td></tr>')+"</tbody>";
}
function closeDrawer(){$("#drawer").classList.remove("open");$("#drawer").setAttribute("aria-hidden","true")}
function openNode(id){
  const n=state.graph.nodes.find(x=>x.id===id);if(!n)return;
  const links=state.graph.edges.filter(e=>e.source===id||e.target===id).map(e=>{
    const other=e.source===id?e.target:e.source,on=state.graph.nodes.find(x=>x.id===other);
    return`<li><span class="id">${esc(e.relationship)}</span> <a href="#" data-id="${esc(other)}">${esc(on?.label||other)}</a> ${conf(e.confidence)}</li>`}).join("");
  $("#drawerBody").innerHTML=`<div class="eyebrow">${esc(TYPE_LABEL[n.type]||n.type)}</div><h2>${esc(n.label)}</h2><p class="id">${esc(n.id)}</p>${conf(n.data.confidence)}<h3>Relationships</h3><ul>${links||"<li>None recorded</li>"}</ul><h3>Record</h3><pre>${esc(JSON.stringify(n.data,null,2))}</pre>`;
  $("#drawer").classList.add("open");$("#drawer").setAttribute("aria-hidden","false");
}
function renderAll(){if(!state.graph)return;renderMetrics();renderActors();renderDomains();renderLandscape();renderWhatsNew();renderGraph();renderCoverage();renderTimeline();renderSources()}
load().catch(e=>{document.body.insertAdjacentHTML("afterbegin",`<p style="padding:12px 28px;background:var(--signal);color:var(--signal-ink);margin:0">Explorer data failed to load: ${esc(e.message)}</p>`)});
