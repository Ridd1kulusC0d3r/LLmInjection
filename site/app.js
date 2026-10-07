const state={graph:null,landscape:null,diff:null,eco:[],search:"",type:"",confidence:"",ecoClass:"",ecoSection:""};
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
  const [g,l,d,e]=await Promise.all([
    fetch("graph.json").then(r=>r.json()),
    fetch("landscape.json").then(r=>r.json()),
    fetch("intelligence-diff.json").then(r=>r.ok?r.json():null).catch(()=>null),
    fetch("ecosystem.json").then(r=>r.ok?r.json():[]).catch(()=>[])
  ]);
  Object.assign(state,{graph:g,landscape:l,diff:d,eco:e});
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
  const cls=[...new Set(state.eco.map(e=>e.evidence_class))].sort(),sec=[...new Set(state.eco.map(e=>e.section))].sort();
  cls.forEach(c=>$("#ecoClass").insertAdjacentHTML("beforeend",`<option value="${esc(c)}">${esc(c)}</option>`));
  sec.forEach(c=>$("#ecoSection").insertAdjacentHTML("beforeend",`<option value="${esc(c)}">${esc(c)}</option>`));
  $("#ecoClass").addEventListener("change",e=>{state.ecoClass=e.target.value;renderEcosystem()});
  $("#ecoSection").addEventListener("change",e=>{state.ecoSection=e.target.value;renderEcosystem()});
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
const EVID=["campaign","incident","vulnerability"];
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
  $("#coverageTable").innerHTML="<thead><tr><th>Technique</th><th>Evidence</th><th>Tests</th><th>Detections</th><th>Controls</th><th>Tools</th></tr></thead><tbody>"+rows.map(r=>{
    const gaps=[r.tests?"":"no test",r.detections?"":"no detection"].filter(Boolean),pri=r.evidence>0&&gaps.length;
    return`<tr data-id="${esc(r.n.id)}"><td><b>${esc(r.n.label)}</b>${gaps.length?`<span class="gap${pri?"":" mute"}">${pri?"priority gap · ":""}${gaps.join(" · ")}</span>`:""}<br><span class="id">${esc(r.n.id)}</span></td><td>${heat(r.evidence)}</td><td>${heat(r.tests)}</td><td>${heat(r.detections)}</td><td>${heat(r.controls)}</td><td>${heat(r.tools)}</td></tr>`;
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
const link=(id,text)=>`<a href="#" data-id="${esc(id)}">${esc(text)}</a>`;
const meter=(label,n,total,cls="")=>`<div class="meter ${cls}"><span>${esc(label)}</span><em>${n}/${total}</em><i><b style="width:${total?(100*n/total).toFixed(1):0}%"></b></i></div>`;
function renderDashboard(){
  const rows=techStats(),N=rows.length;
  const full=rows.filter(r=>r.tests&&r.detections&&r.controls).length;
  $("#dashCoverage").innerHTML=meter("Techniques with a safe test",rows.filter(r=>r.tests).length,N)+meter("with a detection",rows.filter(r=>r.detections).length,N)+meter("with a control",rows.filter(r=>r.controls).length,N)+meter("fully covered (all three)",full,N,"hero")+meter("with a related ecosystem tool",rows.filter(r=>r.tools).length,N);
  const gaps=rows.filter(r=>r.evidence&&(!r.tests||!r.detections)).sort((a,b)=>b.evidence-a.evidence);
  $("#dashGaps").innerHTML=gaps.length?`<div class="gaplist">`+gaps.slice(0,6).map(r=>`<div class="gap-item" data-id="${esc(r.n.id)}"><span class="id">${esc(r.n.id.slice(-4))}</span><span><b>${esc(r.n.label)}</b><span class="tags note">${r.evidence} linked record${r.evidence>1?"s":""} · ${[r.tests?"":"no test",r.detections?"":"no detection"].filter(Boolean).join(", ")}</span></span></div>`).join("")+`</div>`:'<p class="empty">No priority gaps.</p>';
  const rated=state.graph.nodes.filter(n=>n.data.confidence),tot=rated.length,by={};rated.forEach(n=>by[n.data.confidence]=(by[n.data.confidence]||0)+1);
  const ramp=["var(--seq-4)","var(--seq-3)","var(--seq-2)","var(--seq-1)","var(--seq-0)"];
  $("#dashConf").innerHTML=`<div class="stack" role="img" aria-label="Confidence distribution">${CONF_ORDER.map((c,i)=>by[c]?`<i title="${esc(c)}: ${by[c]}" style="width:${(100*by[c]/tot).toFixed(1)}%;background:${ramp[i]}"></i>`:"").join("")}</div><div class="leg">${CONF_ORDER.map(c=>`<span>${conf(c)}</span><b>${by[c]||0}</b>`).join("")}</div><p class="note" style="margin-top:12px">${tot} records carry a confidence rating. Sources and frameworks are graded separately.</p>`;
  const L=state.landscape,pick=["METRIC-WEF-AI-DRIVER","METRIC-GTIG-6H-HARVEST","METRIC-GTIG-DISTILL","METRIC-IBM-SUPPLYCHAIN"].map(id=>(L.key_metrics||[]).find(m=>m.id===id)).filter(Boolean);
  const heads=pick.length?pick:(L.key_metrics||[]).slice(0,4);
  $("#dashHeadlines").innerHTML=heads.map(m=>`<div class="head"><b>${fmt(m.value)}${/percent/.test(m.unit)?"%":""}</b><span>${esc(m.name)}</span><small>${esc(m.unit.replace(/^percent.*/,"percent"))} · ${esc(m.source.publisher)} · grade ${esc(m.source.grade)}</small></div>`).join("");
  const ecoById=new Map(state.eco.map(e=>[e.id,e])),label=id=>state.graph.nodes.find(n=>n.id===id)?.label||ecoById.get(id)?.name||id;
  const ds=Object.entries(state.diff?.datasets||{}),ecoAdded=(ds.find(([k])=>k==="ecosystem.json")?.[1].added||[]).length;
  const added=ds.filter(([k])=>!/relationships|sources|ecosystem/.test(k)).flatMap(([k,v])=>v.added.map(id=>[k.replace(".json","").replace(/s$/,""),id]));
  $("#dashChanges").innerHTML=state.diff?`<div class="chg">${added.slice(0,8).map(([k,id])=>`<span class="k">${esc(k)}</span><span>${link(id,label(id))}</span>`).join("")}${ecoAdded?`<span class="k">ecosystem</span><span>${ecoAdded} related projects added</span>`:""}</div><p class="chg-more">${added.length>8?`+ ${added.length-8} more records · `:""}${state.diff.summary.added} added, ${state.diff.summary.removed} removed, ${state.diff.summary.changed} changed since ${esc(String(state.diff.baseline||"").slice(0,10))}</p>`:'<p class="empty">No diff available.</p>';
  const tl=state.graph.nodes.filter(n=>["campaign","incident","vulnerability"].includes(n.type)).map(n=>({n,date:String(n.data.first_seen||n.data.date||n.data.published||"")})).filter(x=>x.date).sort((a,b)=>b.date.localeCompare(a.date)).slice(0,7);
  $("#dashTimeline").innerHTML=`<div class="mini">${tl.map(({n,date})=>`<span class="d">${esc(date.slice(0,10))}</span><span>${link(n.id,n.label)}<br><span class="note">${esc(n.type)} · ${esc(n.data.confidence||n.data.severity||"")}</span></span>`).join("")}</div>`;
  const src=state.graph.nodes.filter(n=>n.type==="source"),gs=["A","B","C","D","E"].map(g=>[g,src.filter(n=>n.data.grade===g).length]),mx=Math.max(1,...gs.map(x=>x[1]));
  $("#dashGrades").innerHTML=`<div class="bars sm">${gs.map(([g,n])=>`<div class="bar"><span>Grade ${g}</span><i style="width:${(100*n/mx).toFixed(1)}%"></i><b>${n}</b></div>`).join("")}</div>`;
  const cl={};state.eco.forEach(e=>cl[e.evidence_class]=(cl[e.evidence_class]||0)+1);const cm=Math.max(1,...Object.values(cl));
  $("#dashEco").innerHTML=state.eco.length?`<div class="bars sm">${Object.entries(cl).sort((a,b)=>b[1]-a[1]).map(([k,n])=>`<div class="bar"><span>${esc(k)}</span><i style="width:${(100*n/cm).toFixed(1)}%"></i><b>${n}</b></div>`).join("")}</div><p class="note" style="margin-top:8px">${state.eco.length} projects, ${state.eco.filter(e=>e.priority==="start-here").length} flagged start here. None can support attribution.</p>`:'<p class="empty">Ecosystem data not published.</p>';
}
function renderEcosystem(){
  const q=state.search.toLowerCase();
  const rows=state.eco.filter(e=>(!state.ecoClass||e.evidence_class===state.ecoClass)&&(!state.ecoSection||e.section===state.ecoSection)&&(!q||(e.name+" "+e.owner+" "+e.summary).toLowerCase().includes(q)));
  $("#ecoCount").textContent=`${rows.length} of ${state.eco.length} projects`;
  $("#ecoTable").innerHTML="<thead><tr><th>Project</th><th>Evidence class</th><th>Techniques</th><th>Scope</th></tr></thead><tbody>"+(rows.map(e=>`<tr><td><a class="out" href="${esc(e.url)}" rel="noopener"><b>${esc(e.owner)}/${esc(e.name)}</b></a>${e.priority==="start-here"?'<span class="eco-flag">start here</span>':""}${e.status==="archived-reported"?'<span class="eco-flag mute">archived (reported)</span>':""}<br><span class="id">${esc(e.id)} · grade ${esc(e.source_grade)}</span></td><td><span class="id">${esc(e.evidence_class)}</span></td><td>${(e.techniques||[]).map(t=>link(t,t.slice(-4))).join(" ")||'<span class="id">none</span>'}</td><td>${esc(e.summary)}</td></tr>`).join("")||'<tr><td colspan="4">No project matches.</td></tr>')+"</tbody>";
}
function closeDrawer(){$("#drawer").classList.remove("open");$("#drawer").setAttribute("aria-hidden","true")}
const SKIP=new Set(["id","type","name","summary","source_ids","sources","external_mappings","label"]);
function openNode(id){
  const n=state.graph.nodes.find(x=>x.id===id);if(!n)return;
  const nodes=new Map(state.graph.nodes.map(x=>[x.id,x])),groups={};
  state.graph.edges.filter(e=>e.source===id||e.target===id).forEach(e=>{
    const out=e.source===id,other=out?e.target:e.source,key=out?e.relationship:`${e.relationship} (incoming)`;
    (groups[key]=groups[key]||[]).push({other,label:nodes.get(other)?.label||other,confidence:e.confidence});
  });
  const rel=Object.entries(groups).map(([k,v])=>`<div class="grp"><h4>${esc(k)} · ${v.length}</h4><ul>${v.map(x=>`<li><a href="#" data-id="${esc(x.other)}">${esc(x.label)}</a> ${conf(x.confidence)}</li>`).join("")}</ul></div>`).join("");
  const facts=Object.entries(n.data).filter(([k,v])=>!SKIP.has(k)&&v!==null&&v!==""&&(typeof v!=="object"||(Array.isArray(v)&&v.every(x=>typeof x!=="object")))).map(([k,v])=>`<dt>${esc(k.replace(/_/g," "))}</dt><dd>${esc(Array.isArray(v)?v.join(", "):v)}</dd>`).join("");
  const srcIds=(n.data.source_ids||[]).map(s=>nodes.get(s)).filter(Boolean),srcObj=Array.isArray(n.data.sources)?n.data.sources.filter(s=>s&&s.url):[];
  const sources=[...srcIds.map(s=>`<li><a class="out" href="${esc(s.data.url)}" rel="noopener">${esc(s.label)}</a> <span class="id">grade ${esc(s.data.grade)} · ${esc(s.data.publisher||"")}</span></li>`),...srcObj.map(s=>`<li><a class="out" href="${esc(s.url)}" rel="noopener">${esc(s.title||s.url)}</a> <span class="id">grade ${esc(s.grade||"")} · ${esc(s.publisher||"")}</span></li>`)].join("");
  const mapped=(n.data.external_mappings||[]).map(m=>`<li><a class="out" href="${esc(m.url)}" rel="noopener">${esc(m.framework)} ${esc(m.id)}</a> <span class="id">${esc(m.relation)} · ${esc(m.name)}</span></li>`).join("");
  const tools=n.type==="technique"?state.eco.filter(e=>(e.techniques||[]).includes(id)):[];
  $("#drawerBody").innerHTML=`<div class="eyebrow">${esc(TYPE_LABEL[n.type]||n.type)}</div><h2>${esc(n.label)}</h2><p class="id">${esc(n.id)}</p>${conf(n.data.confidence)}${n.data.summary?`<p style="margin-top:12px">${esc(n.data.summary)}</p>`:""}${n.data.hypothesis?`<p style="margin-top:12px">${esc(n.data.hypothesis)}</p>`:""}${facts?`<dl class="facts">${facts}</dl>`:""}${rel?`<h3>Relationships</h3>${rel}`:""}${mapped?`<h3>Framework mappings</h3><ul>${mapped}</ul>`:""}${tools.length?`<h3>Related ecosystem projects</h3><ul>${tools.map(e=>`<li><a class="out" href="${esc(e.url)}" rel="noopener">${esc(e.owner)}/${esc(e.name)}</a> <span class="id">${esc(e.evidence_class)}</span></li>`).join("")}</ul>`:""}${sources?`<h3>Evidence</h3><ul>${sources}</ul>`:""}<details><summary>Raw record</summary><pre>${esc(JSON.stringify(n.data,null,2))}</pre></details>`;
  $("#drawer").classList.add("open");$("#drawer").setAttribute("aria-hidden","false");
}
function renderAll(){if(!state.graph)return;renderMetrics();renderDashboard();renderEcosystem();renderActors();renderDomains();renderLandscape();renderWhatsNew();renderGraph();renderCoverage();renderTimeline();renderSources()}
load().catch(e=>{document.body.insertAdjacentHTML("afterbegin",`<p style="padding:12px 28px;background:var(--signal);color:var(--signal-ink);margin:0">Explorer data failed to load: ${esc(e.message)}</p>`)});
