const state={graph:null,landscape:null,search:"",type:"",confidence:""};
const colors={actor:"#ff7c8c",campaign:"#f3c969",incident:"#e98bff",technique:"#6ea8ff",model:"#43d7ff",framework:"#9f8cff","test-case":"#55d98d",control:"#6ed5b0",detection:"#ffae6e",source:"#71839e"};

async function load(){
  const [g,l]=await Promise.all([fetch("graph.json").then(r=>r.json()),fetch("landscape.json").then(r=>r.json())]);
  state.graph=g;state.landscape=l;
  initFilters();renderAll();
}
function esc(v){return String(v??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));}
function visibleNodes(){
  const q=state.search.toLowerCase();
  return state.graph.nodes.filter(n=>{
    const c=n.data.confidence||"";
    return(!state.type||n.type===state.type)&&(!state.confidence||c===state.confidence)&&(!q||(n.label+" "+JSON.stringify(n.data)).toLowerCase().includes(q));
  });
}
function initFilters(){
  const types=[...new Set(state.graph.nodes.map(n=>n.type))].sort();
  const s=document.querySelector("#typeFilter");types.forEach(t=>s.insertAdjacentHTML("beforeend",`<option value="${esc(t)}">${esc(t)}</option>`));
  document.querySelector("#search").addEventListener("input",e=>{state.search=e.target.value;renderAll()});
  s.addEventListener("change",e=>{state.type=e.target.value;renderAll()});
  document.querySelector("#confidenceFilter").addEventListener("change",e=>{state.confidence=e.target.value;renderAll()});
  document.querySelectorAll(".tab").forEach(b=>b.onclick=()=>{
    document.querySelectorAll(".tab").forEach(x=>x.classList.remove("active"));b.classList.add("active");
    document.querySelectorAll(".view").forEach(x=>x.classList.remove("active"));document.querySelector("#"+b.dataset.tab).classList.add("active");
  });
  document.querySelector("#closeDrawer").onclick=()=>document.querySelector("#drawer").classList.remove("open");
}
function renderMetrics(){
  const counts={};state.graph.nodes.forEach(n=>counts[n.type]=(counts[n.type]||0)+1);
  const items=[["Actors",counts.actor],["Campaigns",counts.campaign],["Techniques",counts.technique],["Tests",counts["test-case"]],["Detections",counts.detection],["Controls",counts.control]];
  document.querySelector("#metrics").innerHTML=items.map(([k,v])=>`<div class="metric"><strong>${v||0}</strong><span>${k}</span></div>`).join("");
}
function renderActors(){
  const ns=visibleNodes().filter(n=>n.type==="actor").slice(0,12);
  document.querySelector("#actors").innerHTML=ns.map(n=>`<div class="actor-row" onclick="openNode('${n.id}')"><b>${esc(n.label)}</b><span>${esc(n.data.nexus||"")}</span><span>${esc(n.data.summary||"")}</span><i class="pill">${esc(n.data.confidence||"")}</i></div>`).join("")||'<p class="muted">No matching actors.</p>';
}
function renderLandscape(){
  const domains=state.landscape.domains||[];
  document.querySelector("#landscape").innerHTML=domains.slice(0,9).map(d=>`<div class="card"><h3>${esc(d.name)}</h3><div class="meta">${esc(d.trend)} · ${esc(d.confidence)}</div><p>${esc(d.summary)}</p></div>`).join("");
}
function renderGraph(){
  const svg=document.querySelector("#graphSvg");svg.innerHTML="";
  let nodes=visibleNodes().slice(0,100);const ids=new Set(nodes.map(n=>n.id));
  const edges=state.graph.edges.filter(e=>ids.has(e.source)&&ids.has(e.target)).slice(0,240);
  document.querySelector("#graphCount").textContent=`${nodes.length} nodes · ${edges.length} edges`;
  const types=[...new Set(nodes.map(n=>n.type))];
  const width=1400,height=760,pad=70;
  const pos={};
  types.forEach((t,ti)=>{
    const group=nodes.filter(n=>n.type===t);const x=pad+(types.length===1?width/2:ti*(width-2*pad)/(types.length-1));
    group.forEach((n,i)=>{const y=80+(i+1)*(height-150)/(group.length+1);pos[n.id]={x,y};});
  });
  const NS="http://www.w3.org/2000/svg";
  edges.forEach(e=>{const a=pos[e.source],b=pos[e.target];if(!a||!b)return;const line=document.createElementNS(NS,"line");line.setAttribute("x1",a.x);line.setAttribute("y1",a.y);line.setAttribute("x2",b.x);line.setAttribute("y2",b.y);line.setAttribute("class","edge");svg.appendChild(line);});
  nodes.forEach(n=>{const p=pos[n.id],g=document.createElementNS(NS,"g");g.setAttribute("class","node");g.onclick=()=>openNode(n.id);
    const c=document.createElementNS(NS,"circle");c.setAttribute("cx",p.x);c.setAttribute("cy",p.y);c.setAttribute("r",7);c.setAttribute("fill",colors[n.type]||"#8ba3c4");g.appendChild(c);
    const t=document.createElementNS(NS,"text");t.setAttribute("x",p.x+11);t.setAttribute("y",p.y+4);t.textContent=n.label.length>26?n.label.slice(0,24)+"…":n.label;g.appendChild(t);svg.appendChild(g);});
}
function edgeCounts(id){
  const es=state.graph.edges.filter(e=>e.source===id||e.target===id);
  const targets=rel=>es.filter(e=>e.relationship===rel).map(e=>e.source===id?e.target:e.source);
  return {tests:targets("validates"),detections:targets("detects"),controls:targets("mitigated-by")};
}
function renderCoverage(){
  const techniques=visibleNodes().filter(n=>n.type==="technique");
  document.querySelector("#coverageTable").innerHTML="<thead><tr><th>Technique</th><th>Tests</th><th>Detections</th><th>Controls</th></tr></thead><tbody>"+techniques.map(n=>{const c=edgeCounts(n.id);return`<tr onclick="openNode('${n.id}')"><td><b>${esc(n.label)}</b><br><span class="muted">${esc(n.id)}</span></td><td>${c.tests.length}</td><td>${c.detections.length}</td><td>${c.controls.length}</td></tr>`}).join("")+"</tbody>";
}
function renderTimeline(){
  const items=visibleNodes().filter(n=>["campaign","incident"].includes(n.type)).map(n=>({n,date:n.data.first_seen||n.data.date||n.data.last_seen||"unknown"})).sort((a,b)=>String(b.date).localeCompare(String(a.date)));
  document.querySelector("#timelineList").innerHTML=items.map(({n,date})=>`<div class="timeline-item" onclick="openNode('${n.id}')"><div class="date">${esc(date)}</div><h3>${esc(n.label)}</h3><div class="meta">${esc(n.type)} · ${esc(n.data.confidence||n.data.status||"")}</div><p>${esc(n.data.summary||"")}</p></div>`).join("");
}
function renderSources(){
  const ns=visibleNodes().filter(n=>n.type==="source");
  document.querySelector("#sourceList").innerHTML=ns.map(n=>`<div class="card" onclick="openNode('${n.id}')"><h3>${esc(n.label)}</h3><div class="meta">Grade ${esc(n.data.grade)} · ${esc(n.data.role)}</div><p>${esc(n.data.publisher||"")}</p></div>`).join("");
}
function openNode(id){
  const n=state.graph.nodes.find(x=>x.id===id);if(!n)return;
  const edges=state.graph.edges.filter(e=>e.source===id||e.target===id);
  const links=edges.map(e=>{const other=e.source===id?e.target:e.source;const on=state.graph.nodes.find(x=>x.id===other);return `<li><b>${esc(e.relationship)}</b> → <a href="#" onclick="openNode('${other}');return false">${esc(on?.label||other)}</a> <span class="pill">${esc(e.confidence)}</span></li>`}).join("");
  document.querySelector("#drawerBody").innerHTML=`<div class="eyebrow">${esc(n.type)}</div><h2>${esc(n.label)}</h2><p class="muted">${esc(n.id)}</p><h3>Relationships</h3><ul>${links||"<li>None</li>"}</ul><h3>Record</h3><pre>${esc(JSON.stringify(n.data,null,2))}</pre>`;
  document.querySelector("#drawer").classList.add("open");
}
function renderAll(){if(!state.graph)return;renderMetrics();renderActors();renderLandscape();renderGraph();renderCoverage();renderTimeline();renderSources();}
window.openNode=openNode;load().catch(e=>{document.body.insertAdjacentHTML("afterbegin",`<div style="padding:12px;background:#6d1b2d;color:white">Explorer data failed to load: ${esc(e.message)}</div>`)});
