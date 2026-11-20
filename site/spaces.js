/* Explorer spaces built on the same graph: reports, trends, TTPs, threat hunting, detection and threat modelling.
   Everything here is computed from graph.json, coverage.json and reports.json at load; nothing is typed by hand. */
const SP={reports:null,report:null};
const REPO_BLOB="https://github.com/Ridd1kulusC0d3r/LLmInjection/blob/main/";
const nodeById=id=>state.graph.nodes.find(n=>n.id===id);
const edgesOf=(id,rel)=>state.graph.edges.filter(e=>(e.source===id||e.target===id)&&(!rel||e.relationship===rel));
const other=(e,id)=>e.source===id?e.target:e.source;
const monthOf=n=>{const d=nodeDate(n);return/^\d{4}-\d{2}/.test(d)?d.slice(0,7):""};
const chipLink=id=>{const n=nodeById(id);return n?`<a href="#" class="tchip" data-id="${esc(id)}">${esc(id.startsWith("LLMI-")?id.slice(5):n.label)}</a>`:""};
const ext=(n,fw)=>(n.data.external_mappings||[]).filter(m=>m.framework.startsWith(fw)&&m.relation==="exact").map(m=>m.id);

/* ---------- minimal Markdown for the repository's own reports (trusted, reviewed content) */
const KEEP_TAGS=/&lt;(\/?)(span|code|b|strong|em|i|br|p|div)((?: class=&quot;[\w -]+&quot;)?)(?: markdown=&quot;\w+&quot;)?\s*\/?&gt;/g;
function mdInline(s,base){
  return esc(s).replace(KEEP_TAGS,(_,c,tag,cls)=>`<${c}${tag}${cls.replace(/&quot;/g,'"')}>`)
    .replace(/`([^`]+)`/g,"<code>$1</code>")
    .replace(/!\[([^\]]*)\]\(([^)\s]+)\)/g,(_,a,u)=>`<img alt="${a}" src="${esc(safeUrl(u,base))}">`)
    .replace(/\[([^\]]+)\]\(([^)\s]+)\)/g,(_,a,u)=>`<a class="out" href="${esc(safeUrl(u,base,true))}" rel="noopener">${a}</a>`)
    .replace(/&lt;(https?:\/\/[^\s&]+)&gt;/g,'<a class="out" href="$1" rel="noopener">$1</a>')
    .replace(/\*\*([^*]+)\*\*/g,"<strong>$1</strong>").replace(/(^|[\s(])\*([^*\s][^*]*)\*/g,"$1<em>$2</em>");
}
function safeUrl(u,base,isLink){
  u=u.replace(/&amp;/g,"&");
  if(/^https?:\/\//.test(u)||u.startsWith("#"))return u;
  if(/^[a-z]+:/i.test(u))return "#";
  const abs=new URL(u,new URL(base,"https://x/"+"")).pathname.slice(1);
  /* a link to another Markdown report opens in the Reports space; anything else goes to GitHub */
  if(isLink)return /^reports\/.+\.md$/.test(abs)?`#tab=reports&report=${encodeURIComponent(abs)}`:REPO_BLOB+abs;
  return abs;
}
function md(text,base){
  text=text.replace(/^---\n[\s\S]*?\n---\n/,"");
  const lines=text.split("\n"),out=[];let i=0;
  const para=[];const flush=()=>{if(para.length){out.push(`<p>${mdInline(para.join(" "),base)}</p>`);para.length=0}};
  while(i<lines.length){
    const l=lines[i];
    if(/^```/.test(l)){flush();const buf=[];i++;while(i<lines.length&&!/^```/.test(lines[i]))buf.push(esc(lines[i++]));out.push(`<pre><code>${buf.join("\n")}</code></pre>`);i++;continue}
    if(!l.trim()){flush();i++;continue}
    let m;
    if((m=l.match(/^(#{1,4})\s+(.*)$/))){flush();const h=Math.min(6,m[1].length+1);out.push(`<h${h}>${mdInline(m[2],base)}</h${h}>`);i++;continue}
    if(/^\|/.test(l)&&/^\|?\s*:?-{2,}/.test(lines[i+1]||"")){flush();
      const cells=r=>r.trim().replace(/^\||\|$/g,"").split("|").map(c=>c.trim());
      const head=cells(l);i+=2;const body=[];while(i<lines.length&&/^\|/.test(lines[i]))body.push(cells(lines[i++]));
      out.push(`<div class="table-wrap" tabindex="0"><table class="tbl"><thead><tr>${head.map(c=>`<th>${mdInline(c,base)}</th>`).join("")}</tr></thead><tbody>${body.map(r=>`<tr>${r.map(c=>`<td>${mdInline(c,base)}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`);continue}
    if(/^\s*([-*]|\d+\.)\s+/.test(l)){flush();const ol=/^\s*\d+\./.test(l),items=[];
      while(i<lines.length&&/^\s*([-*]|\d+\.)\s+/.test(lines[i])){let it=lines[i++].replace(/^\s*([-*]|\d+\.)\s+/,"");while(i<lines.length&&/^\s{2,}\S/.test(lines[i])&&!/^\s*([-*]|\d+\.)\s+/.test(lines[i]))it+=" "+lines[i++].trim();items.push(`<li>${mdInline(it,base)}</li>`)}
      out.push(ol?`<ol>${items.join("")}</ol>`:`<ul>${items.join("")}</ul>`);continue}
    if(/^>\s?/.test(l)){flush();const buf=[];while(i<lines.length&&/^>\s?/.test(lines[i]))buf.push(lines[i++].replace(/^>\s?/,""));out.push(`<blockquote>${mdInline(buf.join(" "),base)}</blockquote>`);continue}
    if(/^---+$/.test(l)){flush();out.push("<hr>");i++;continue}
    if(/^<\/?(div|p)\b/.test(l)){flush();out.push(mdInline(l,base));i++;continue}
    para.push(l);i++;
  }
  flush();return out.join("\n");
}

/* ---------- reports */
async function loadReports(){
  try{SP.reports=await fetch("reports.json").then(r=>r.ok?r.json():null)}catch(_){SP.reports=null}
  try{SP.vault=await fetch("payload-vault.json").then(r=>r.ok?r.json():null)}catch(_){SP.vault=null}
}
const KIND_ORDER=["platform","landscape","trends","intel","dossier","intake","report","template"];
function renderReports(){
  const box=$("#reportList"),view=$("#reportView");if(!box)return;
  const rows=SP.reports?.reports||[];
  if(!rows.length){box.innerHTML=`<p class="empty">${esc(t("rep.none"))}</p>`;view.hidden=true;return}
  const groups=KIND_ORDER.map(k=>[k,rows.filter(r=>r.kind===k)]).filter(([,v])=>v.length);
  box.innerHTML=groups.map(([k,v])=>`<h3 class="sect">${esc(t("rep.kind."+k))}</h3><div class="rcards">${v.map(r=>`<button type="button" class="rcard${SP.report===r.path?" on":""}" data-report="${esc(r.path)}"><span class="eyebrow">${esc(t("rep.kind."+r.kind))}</span><b>${esc(r.kind==="platform"?t("rep.platform"):r.title)}</b><span class="id">${esc(r.date||r.path)}</span></button>`).join("")}</div>`).join("");
  box.querySelectorAll("[data-report]").forEach(b=>b.onclick=()=>openReport(b.dataset.report,true));
  if(SP.report)openReport(SP.report,false);else view.hidden=true;
}
async function openReport(path,push){
  const r=(SP.reports?.reports||[]).find(x=>x.path===path),view=$("#reportView");if(!r)return;
  SP.report=path;if(push)patchHash({tab:"reports",report:path});
  document.querySelectorAll(".rcard").forEach(b=>b.classList.toggle("on",b.dataset.report===path));
  view.hidden=false;view.innerHTML=`<p class="note">${esc(t("rep.loading"))}</p>`;
  try{
    const text=await fetch(path).then(x=>{if(!x.ok)throw new Error(x.status);return x.text()});
    view.innerHTML=`<div class="rbar"><span class="id">${esc(path)}</span><span><a class="out" href="${esc(r.github)}" rel="noopener">${esc(t("rep.github"))}</a> · <button type="button" class="export" data-close-report>${esc(t("rep.close"))}</button></span></div><article class="md-doc">${md(text,path)}</article>`;
    view.querySelector("[data-close-report]").onclick=()=>{SP.report=null;patchHash({report:null});view.hidden=true;document.querySelectorAll(".rcard").forEach(b=>b.classList.remove("on"))};
    if(push)view.scrollIntoView({behavior:"smooth",block:"start"});
  }catch(e){view.innerHTML=`<p class="empty">${esc(t("rep.fail",{msg:e.message}))}</p>`}
}

/* ---------- trends: what the evidence base shows month by month (reporting volume, not ground truth) */
function evidenceMonths(){
  const ev=state.graph.nodes.filter(n=>EVID.includes(n.type)).map(n=>({n,m:monthOf(n)})).filter(x=>x.m);
  const last=ev.map(x=>x.m).sort().pop();if(!last)return{ev,months:[],last};
  const [y,mo]=last.split("-").map(Number),months=[];
  for(let k=11;k>=0;k--){const d=new Date(Date.UTC(y,mo-1-k,1));months.push(d.toISOString().slice(0,7))}
  return{ev,months,last};
}
function windowCounts(items,keyFn,months){
  const recent=new Set(months.slice(-3)),prior=new Set(months.slice(-6,-3)),c={};
  items.forEach(x=>keyFn(x).forEach(k=>{c[k]=c[k]||{r:0,p:0};if(recent.has(x.m))c[k].r++;else if(prior.has(x.m))c[k].p++}));
  return Object.entries(c).filter(([,v])=>v.r||v.p).sort((a,b)=>(b[1].r-b[1].p)-(a[1].r-a[1].p)||b[1].r-a[1].r);
}
function renderTrends(){
  const box=$("#trendsBody");if(!box)return;
  const{ev,months}=evidenceMonths();
  if(!months.length){box.innerHTML=`<p class="empty">${esc(t("common.nothing"))}</p>`;return}
  const per=months.map(m=>({m,c:EVID.map(ty=>ev.filter(x=>x.m===m&&x.n.type===ty).length)})),mx=Math.max(1,...per.map(p=>p.c.reduce((a,b)=>a+b,0)));
  const cols=["var(--seq-4)","var(--seq-2)","var(--seq-1)"];
  const chart=`<div class="mchart" role="img" aria-label="${esc(t("tr.chart.aria"))}">${per.map(p=>`<div class="mcol"><div class="mstack">${p.c.map((v,i)=>v?`<i style="height:${(100*v/mx).toFixed(1)}%;background:${cols[i]}" title="${esc(typeLabel(EVID[i]))}: ${v}"></i>`:"").join("")}</div><b>${p.c.reduce((a,b)=>a+b,0)||""}</b><span>${esc(p.m.slice(2))}</span></div>`).join("")}</div><div class="leg">${EVID.map((ty,i)=>`<span><i class="sw" style="background:${cols[i]}"></i>${esc(typeLabel(ty))}</span>`).join("")}</div>`;
  const techOf=x=>edgesOf(x.n.id).filter(e=>["uses","demonstrates"].includes(e.relationship)).map(e=>other(e,x.n.id)).filter(id=>id.startsWith("LLMI-T"));
  const actorsOf=x=>edgesOf(x.n.id,"conducts").map(e=>nodeById(other(e,x.n.id))).filter(Boolean);
  const roleOf=x=>[...new Set(actorsOf(x).flatMap(a=>a.data.ai_role||[]))];
  const nexusOf=x=>[...new Set(actorsOf(x).map(a=>String(a.data.nexus||"").split(" (")[0].trim()).filter(Boolean))];
  const row=(k,v,label)=>{const d=v.r-v.p;return`<tr><td>${label}</td><td class="num">${v.p}</td><td class="num"><b>${v.r}</b></td><td class="num"><span class="trend${d>0?" rising":""}">${d>0?"+":""}${d}</span></td></tr>`};
  const table=(title,sub,rows,label)=>`<div class="dp"><h3>${esc(title)}</h3><p class="note">${esc(sub)}</p><div class="table-wrap" tabindex="0"><table class="tbl"><thead><tr><th></th><th class="num">${esc(t("tr.prior"))}</th><th class="num">${esc(t("tr.recent"))}</th><th class="num">Δ</th></tr></thead><tbody>${rows.slice(0,10).map(([k,v])=>row(k,v,label(k))).join("")||`<tr><td colspan="4">${esc(t("common.nothing"))}</td></tr>`}</tbody></table></div></div>`;
  const win=t("tr.window",{a:months[6],b:months[8],c:months[9],d:months[11]});
  const weekly=(SP.reports?.reports||[]).filter(r=>r.kind==="trends");
  box.innerHTML=`<div class="dp"><h3>${esc(t("tr.volume"))}</h3>${chart}<p class="note" style="margin-top:10px">${esc(t("tr.bias"))}</p></div>
    <p class="note" style="margin:18px 0 10px">${esc(win)}</p>
    <div class="dash two">${table(t("tr.tech"),t("tr.tech.sub"),windowCounts(ev,techOf,months),k=>`${chipLink(k)} ${esc(nodeById(k)?.label||k)}`)}${table(t("tr.role"),t("tr.role.sub"),windowCounts(ev,roleOf,months),k=>esc(tOr("role."+k,k.replace(/-/g," "))))}</div>
    <div class="dash two">${table(t("tr.nexus"),t("tr.nexus.sub"),windowCounts(ev,nexusOf,months),k=>esc(k))}<div class="dp"><h3>${esc(t("tr.weekly"))}</h3>${weekly.length?`<ul class="plain">${weekly.map(r=>`<li><a href="#tab=reports&report=${encodeURIComponent(r.path)}">${esc(r.title)}</a> <span class="id">${esc(r.date)}</span></li>`).join("")}</ul>`:`<p class="note">${esc(t("tr.weekly.none"))}</p>`}<p class="note" style="margin-top:10px"><a href="#tab=reports&report=${encodeURIComponent("reports/templates/tendencias-semana.md")}">${esc(t("tr.weekly.template"))}</a></p></div></div>`;
}

/* ---------- TTPs: the technique catalogue with its external IDs and who is seen using it */
function renderTTPs(){
  const box=$("#ttpBody");if(!box)return;
  const cov=new Map((state.cov?.techniques||[]).map(r=>[r.id,r]));
  const techs=state.graph.nodes.filter(n=>n.type==="technique");
  const cats=[...new Set(techs.map(n=>n.data.category))];
  box.innerHTML=`<p class="links" style="margin:0 0 18px"><a class="out" href="navigator/atlas-coverage.layer.json" download>${esc(t("ttp.layer.atlas"))}</a><a class="out" href="navigator/attack-coverage.layer.json" download>${esc(t("ttp.layer.attack"))}</a><a class="out" href="https://mitre-atlas.github.io/atlas-navigator/" rel="noopener">${esc(t("ttp.navigator"))}</a></p>`+
  cats.map(c=>`<h3 class="sect">${esc(tOr("cat."+c,c.replace(/-/g," ")))}</h3><div class="table-wrap" tabindex="0"><table class="tbl"><thead><tr><th>${esc(t("th.technique"))}</th><th>${esc(t("ttp.maturity"))}</th><th class="num">${esc(t("ttp.actors"))}</th><th class="num">${esc(t("ttp.evidence"))}</th><th>OWASP</th><th>MITRE ATLAS</th><th>${esc(t("ttp.playbook"))}</th></tr></thead><tbody>${techs.filter(n=>n.data.category===c).map(n=>{const r=cov.get(n.id)||{};return`<tr data-id="${esc(n.id)}"><td><span class="id">${esc(n.id)}</span><br><b>${esc(n.label)}</b></td><td>${esc(matLabel(n.data.maturity))}</td><td class="num">${(r.actors||[]).length}</td><td class="num">${(r.evidence||[]).length}${(r.evidence||[]).length?` <button type="button" class="rmore" data-explode="${esc(n.id)}">↗</button>`:""}</td><td class="id">${esc(ext(n,"OWASP").join(", ")||"–")}</td><td class="id">${esc(ext(n,"MITRE ATLAS").join(", ")||"–")}</td><td><a class="out" href="${REPO_BLOB}docs/playbooks/${esc(n.id)}.md" rel="noopener">${esc(t("ttp.open"))}</a></td></tr>`}).join("")}</tbody></table></div>`).join("");
}

/* ---------- threat hunting: detection hypotheses ranked by the evidence behind their techniques */
function huntRows(){
  const cov=new Map((state.cov?.techniques||[]).map(r=>[r.id,r])),w={"observed-in-the-wild":3,"disclosed-vulnerability":2,"research-demonstrated":1};
  return state.graph.nodes.filter(n=>n.type==="detection").map(n=>{
    const techs=edgesOf(n.id,"detects").map(e=>other(e,n.id)).filter(id=>id.startsWith("LLMI-T"));
    const evidence=new Set(techs.flatMap(id=>cov.get(id)?.evidence||[])),best=Math.max(0,...techs.map(id=>w[nodeById(id)?.data.maturity]||0));
    return{n,techs,evidence:evidence.size,best,score:best*100+evidence.size};
  }).sort((a,b)=>b.score-a.score);
}
function renderHunting(){
  const box=$("#huntBody");if(!box)return;
  const rows=huntRows(),sel=$("#huntTelemetry"),cur=sel?.value||"";
  const tele=[...new Set(rows.flatMap(r=>r.n.data.telemetry||[]))].sort();
  if(sel&&sel.options.length!==tele.length+1){sel.innerHTML=`<option value="">${esc(t("hunt.tele.all"))}</option>`+tele.map(x=>`<option>${esc(x)}</option>`).join("");sel.value=cur;sel.onchange=renderHunting}
  const shown=rows.filter(r=>!cur||(r.n.data.telemetry||[]).includes(cur));
  box.innerHTML=`<p class="note" style="margin:0 0 14px">${esc(t("hunt.count",{n:nf(shown.length)}))}</p><div class="hunts">${shown.map((r,i)=>`<div class="hunt" data-id="${esc(r.n.id)}"><div class="hunt-h"><span class="rank">${i+1}</span><span class="id">${esc(r.n.id)} · ${esc(r.n.data.severity||"")}</span><span class="trend${r.best===3?" rising":""}">${esc(r.best===3?t("hunt.wild"):r.best===2?t("hunt.vuln"):t("hunt.research"))}</span></div><h3>${esc(r.n.data.hypothesis||r.n.label)}</h3><p class="note">${esc(r.n.label)}</p><div class="tele">${(r.n.data.telemetry||[]).map(x=>`<span>${esc(x)}</span>`).join("")}</div><div class="hunt-f">${r.techs.map(chipLink).join(" ")}<span class="id">${esc(t("hunt.evidence",{n:r.evidence}))}</span>${(SP.reports?.rule_files?.[r.n.id]||[]).map(p=>`<a class="out tchip" href="${REPO_BLOB}${esc(p)}" rel="noopener">${esc(p.split("/")[1])}</a>`).join("")}</div>${extRules(r.n.id)}</div>`).join("")}</div>`;
}

/* ---------- detection engineering: every detection, its rule files and its tests */
function renderDetection(){
  const box=$("#detBody");if(!box)return;
  const rules=SP.reports?.rule_files||{},rows=state.graph.nodes.filter(n=>n.type==="detection");
  const withRule=rows.filter(n=>rules[n.id]).length;
  box.innerHTML=`<div class="strip" style="grid-template-columns:repeat(3,1fr)">${stat(nf(rows.length),t("det.total"))}${stat(nf(withRule),t("det.rules"))}${stat(nf(rows.filter(n=>(n.data.test_ids||[]).length).length),t("det.tested"))}</div>
    <div class="table-wrap" tabindex="0"><table class="tbl"><thead><tr><th>${esc(t("det.rule"))}</th><th>${esc(t("det.cat"))}</th><th>${esc(t("det.state"))}</th><th>${esc(t("det.files"))}</th><th>${esc(t("det.techs"))}</th><th>${esc(t("det.tests"))}</th></tr></thead><tbody>${rows.sort((a,b)=>(rules[b.id]?1:0)-(rules[a.id]?1:0)||a.id.localeCompare(b.id)).map(n=>`<tr data-id="${esc(n.id)}"><td><span class="id">${esc(n.id)}</span><br><b>${esc(n.label)}</b></td><td>${esc(n.data.category||"")} · ${esc(n.data.severity||"")}</td><td><span class="trend${rules[n.id]?" rising":""}">${esc(rules[n.id]?t("det.state.rule"):t("det.state.spec"))}</span></td><td>${(rules[n.id]||[]).map(p=>`<a class="out" href="${REPO_BLOB}${esc(p)}" rel="noopener">${esc(p.split("/")[1])}</a>`).join(" ")||"–"}${extRules(n.id)}</td><td>${edgesOf(n.id,"detects").map(e=>chipLink(other(e,n.id))).join(" ")}</td><td class="id">${esc((n.data.test_ids||[]).join(", ")||"–")}</td></tr>`).join("")}</tbody></table></div>`;
}

/* rules published by others for one of our detections (linked, not copied) */
function extRules(id){const x=SP.reports?.external_rules?.[id];if(!x||!x.urls.length)return"";
  return`<div class="rlinks"><a class="rlink" href="${esc(x.urls[0].replace(/\/blob\/main\/.*$/,""))}" target="_blank" rel="noopener"><b>B</b>${esc(t("det.external",{p:x.publisher,n:x.urls.length}))}<span aria-hidden="true">↗</span></a></div>`}
/* ---------- threat modelling: attack surface → techniques → controls → frameworks */
function renderThreatModel(){
  const box=$("#tmBody");if(!box)return;
  const techs=state.graph.nodes.filter(n=>n.type==="technique"),cats=[...new Set(techs.map(n=>n.data.category))];
  const ctl=id=>edgesOf(id,"mitigated-by").map(e=>other(e,id)).filter(x=>x.startsWith("CTRL-"));
  const fw=state.graph.nodes.filter(n=>n.type==="framework");
  box.innerHTML=`<div class="tm">${cats.map(c=>{const ts=techs.filter(n=>n.data.category===c);return`<div class="dp"><h3>${esc(tOr("cat."+c,c.replace(/-/g," ")))}</h3><ul class="plain">${ts.map(n=>{const cs=ctl(n.id);return`<li><a href="#" data-id="${esc(n.id)}">${esc(n.label)}</a> <span class="id">${esc(matLabel(n.data.maturity))}</span><div class="tm-ctl">${cs.length?cs.map(id=>`<a href="#" class="tchip ctl" data-id="${esc(id)}">${esc(nodeById(id)?.label||id)}</a>`).join(""):`<span class="gap">${esc(t("tm.noctl"))}</span>`}</div></li>`}).join("")}</ul></div>`}).join("")}</div>
    <h3 class="sect">${esc(t("tm.frameworks"))}</h3><div class="table-wrap" tabindex="0"><table class="tbl"><thead><tr><th>${esc(t("tm.fw"))}</th><th>${esc(t("tm.scope"))}</th><th>${esc(t("tm.use"))}</th></tr></thead><tbody>${fw.map(n=>`<tr><td>${n.data.url?`<a class="out" href="${esc(n.data.url)}" rel="noopener"><b>${esc(n.label)}</b></a>`:`<b>${esc(n.label)}</b>`}</td><td>${esc(n.data.scope||"")}</td><td>${esc(n.data.use||"")}</td></tr>`).join("")}</tbody></table></div>`;
}
function renderSpaces(){renderMatrix();renderReports();renderTrends();renderTTPs();renderHunting();renderDetection();renderThreatModel();renderLatam()}

/* ---------- Brazil and Latin America: records tagged with a LATAM region, or whose report text names the region */
const LATAM=new Set(["BR","MX","AR","CL","CO","PE","EC","BO","CR","UY","PY","VE","GT","HN","SV","NI","PA","DO","CU","LATAM"]);
const LATAM_TEXT=/Brazil|Brasil|Latin America|LATAM|\bPix\b|Mexic|Argentin|Colombia|Chile|Peru/i;
function latamRecords(){
  const ev=state.graph.nodes.filter(n=>["actor","campaign","incident"].includes(n.type));
  const hit=new Map();
  ev.forEach(n=>{const r=(n.data.regions||[]).filter(x=>LATAM.has(x));if(r.length||LATAM_TEXT.test(n.label+" "+(n.data.summary||"")))hit.set(n.id,{n,regions:r,byText:!r.length})});
  /* campaigns of a LATAM actor count too */
  [...hit.values()].filter(x=>x.n.type==="actor").forEach(a=>edgesOf(a.n.id,"conducts").forEach(e=>{const c=nodeById(other(e,a.n.id));if(c&&!hit.has(c.id))hit.set(c.id,{n:c,regions:a.regions,byText:false,via:a.n.id})}));
  return[...hit.values()];
}
function renderLatam(){
  const box=$("#latamBody");if(!box)return;
  const rows=latamRecords(),by=ty=>rows.filter(r=>r.n.type===ty);
  const ctry={};rows.forEach(r=>(r.regions.length?r.regions:["–"]).forEach(c=>ctry[c]=(ctry[c]||0)+1));const cm=Math.max(1,...Object.values(ctry));
  const tech={};rows.filter(r=>r.n.type!=="actor").forEach(r=>edgesOf(r.n.id).filter(e=>["uses","demonstrates"].includes(e.relationship)).forEach(e=>{const id=other(e,r.n.id);tech[id]=(tech[id]||0)+1}));
  const tm=Math.max(1,...Object.values(tech));
  const dated=rows.filter(r=>r.n.type!=="actor").map(r=>({...r,date:nodeDate(r.n)})).sort((a,b)=>b.date.localeCompare(a.date));
  box.innerHTML=`<div class="strip" style="grid-template-columns:repeat(4,1fr)">${stat(nf(by("actor").length),t("stat.actors"))}${stat(nf(by("campaign").length),t("stat.campaigns"))}${stat(nf(by("incident").length),t("stat.incidents"))}${stat(nf(Object.keys(tech).length),t("stat.techniques"))}</div>
    <div class="dash two"><div class="dp"><h3>${esc(t("latam.countries"))}</h3><div class="bars sm">${Object.entries(ctry).sort((a,b)=>b[1]-a[1]).map(([c,n])=>`<div class="bar"><span>${esc(c==="–"?t("latam.bytext"):c)}</span><i style="width:${(100*n/cm).toFixed(1)}%"></i><b>${n}</b></div>`).join("")}</div></div>
    <div class="dp"><h3>${esc(t("latam.techniques"))}</h3><div class="bars sm">${Object.entries(tech).sort((a,b)=>b[1]-a[1]).slice(0,10).map(([id,n])=>`<div class="bar" data-id="${esc(id)}"><span>${esc(id.slice(5))} · ${esc(nodeById(id)?.label||id)}</span><i style="width:${(100*n/tm).toFixed(1)}%"></i><b>${n}</b></div>`).join("")}</div></div></div>
    <h3 class="sect">${esc(t("latam.actors"))}</h3><div class="rcards">${by("actor").map(r=>`<button type="button" class="rcard" data-id="${esc(r.n.id)}"><span class="eyebrow">${esc((r.regions.join(" · "))||t("latam.bytext"))}</span><b>${esc(r.n.label)}</b><span class="id">${esc(String(r.n.data.nexus||"").split(" (")[0])} · ${esc((r.n.data.ai_role||[]).join(", "))}</span>${conf(r.n.data.confidence)}</button>`).join("")}</div>
    <h3 class="sect">${esc(t("latam.records"))}</h3><div class="tl">${dated.map(({n,date,regions,byText})=>`<div class="d">${esc(date||t("common.undated"))}</div><div class="e" data-id="${esc(n.id)}"><div class="kind">${esc(typeLabel(n.type))} · ${esc(regions.join(", ")||(byText?t("latam.bytext"):""))}</div><h3>${esc(n.label)}</h3><p>${esc(n.data.summary||"")}</p><div style="margin-top:6px">${conf(n.data.confidence)}</div>${linksRow(n.id,3)}</div>`).join("")}</div>
    <p class="note" style="margin-top:18px">${esc(t("latam.rule"))}</p>`;
}

/* ---------- defense matrix: threat model x harness x guardrail x hardening, one row per technique */
const HARNESS_CLASSES=new Set(["assessment-tool","benchmark","prompt-corpus","research-technique","lab-exercise"]);
function matrixRows(){
  const cov=new Map((state.cov?.techniques||[]).map(r=>[r.id,r])),eco=new Map(state.eco.map(e=>[e.id,e]));
  const vault=SP.vault?.summary?.per_technique||{};
  return state.graph.nodes.filter(n=>n.type==="technique").map(n=>{
    const r=cov.get(n.id)||{},ctl=edgesOf(n.id,"mitigated-by").map(e=>nodeById(other(e,n.id))).filter(Boolean);
    const tools=(r.tools||[]).map(id=>eco.get(id)).filter(Boolean);
    return{n,r,tests:r.tests||[],harness:tools.filter(e=>HARNESS_CLASSES.has(e.evidence_class)),payloads:vault[n.id]||0,
      guard:ctl.filter(c=>c.data.layer==="guardrail"),guardTools:tools.filter(e=>e.evidence_class==="defence-tool"),
      hard:ctl.filter(c=>c.data.layer==="hardening"),mon:ctl.filter(c=>c.data.layer==="monitoring"),dets:r.detections||[]};
  });
}
function renderMatrix(){
  const box=$("#matrixBody");if(!box)return;
  const rows=matrixRows(),show=$("#matrixShow")?.value||"";
  const full=r=>(r.tests.length||r.harness.length||r.payloads)&&(r.guard.length||r.guardTools.length)&&r.hard.length;
  const gaps={harness:r=>!r.tests.length&&!r.harness.length&&!r.payloads,guard:r=>!r.guard.length&&!r.guardTools.length,hard:r=>!r.hard.length};
  const sel=$("#matrixShow");
  if(sel&&!sel.options.length){sel.innerHTML=[["",t("mx.show.all")],["gaps",t("mx.show.gaps")],["harness",t("mx.show.harness")],["guard",t("mx.show.guard")],["hard",t("mx.show.hard")]].map(([v,l])=>`<option value="${v}">${esc(l)}</option>`).join("");sel.onchange=()=>{renderMatrix();afterRender()}}
  const shown=rows.filter(r=>!show||(show==="gaps"?!full(r):gaps[show](r)));
  const list=(xs,f)=>xs.length?xs.map(f).join(""):`<span class="gap">${esc(t("mx.none"))}</span>`;
  const ctlChip=c=>`<a href="#" class="tchip ctl" data-id="${esc(c.id)}">${esc(c.label)}</a>`;
  const ecoChip=e=>`<a class="out tchip ctl" href="${esc(e.url)}" rel="noopener">${esc(e.name)}</a>`;
  const cats=[...new Set(shown.map(r=>r.n.data.category))];
  box.innerHTML=`<div class="strip" style="grid-template-columns:repeat(4,1fr)">${stat(nf(rows.filter(full).length)+"/"+nf(rows.length),t("mx.full"))}${stat(nf(rows.filter(gaps.harness).length),t("mx.gap.harness"))}${stat(nf(rows.filter(gaps.guard).length),t("mx.gap.guard"))}${stat(nf(rows.filter(gaps.hard).length),t("mx.gap.hard"))}</div>`+
  cats.map(c=>`<h3 class="sect">${esc(tOr("cat."+c,c.replace(/-/g," ")))}</h3><div class="table-wrap" tabindex="0"><table class="tbl dmx"><thead><tr><th>${esc(t("mx.col.tm"))}</th><th>${esc(t("mx.col.harness"))}</th><th>${esc(t("mx.col.guard"))}</th><th>${esc(t("mx.col.hard"))}</th></tr></thead><tbody>${shown.filter(r=>r.n.data.category===c).map(r=>`<tr>
    <td><a href="#" data-id="${esc(r.n.id)}"><b>${esc(r.n.label)}</b></a><br><span class="id">${esc(r.n.id)} · ${esc(matLabel(r.n.data.maturity))}</span><br><span class="id">${esc(t("mx.evidence",{n:(r.r.evidence||[]).length,a:(r.r.actors||[]).length}))}</span>${(r.r.evidence||[]).length?` <button type="button" class="rmore" data-explode="${esc(r.n.id)}">${esc(t("rl.reports"))}</button>`:""}${r.dets.length?`<br><span class="id">${esc(t("mx.dets",{n:r.dets.length}))}</span>`:""}${r.mon.map(ctlChip).join("")}</td>
    <td>${r.tests.length?`<span class="id">${esc(t("mx.tests",{n:r.tests.length}))}: ${esc(r.tests.join(", "))}</span><br>`:""}${r.payloads?`<span class="id">${esc(t("mx.payloads",{n:nf(r.payloads)}))}</span><br>`:""}${r.harness.length?r.harness.slice(0,6).map(ecoChip).join(""):(r.tests.length||r.payloads?"":`<span class="gap">${esc(t("mx.none"))}</span>`)}${r.harness.length>6?`<span class="id"> +${r.harness.length-6}</span>`:""}</td>
    <td>${list([...r.guard.map(ctlChip),...r.guardTools.slice(0,4).map(ecoChip)],x=>x)}</td>
    <td>${list(r.hard,ctlChip)}</td></tr>`).join("")}</tbody></table></div>`).join("")+
  (SP.vault?`<p class="note" style="margin-top:14px">${esc(t("mx.vault",{n:nf(SP.vault.summary.payloads),date:SP.vault.meta.read}))} <a class="out" href="${esc(SP.vault.meta.source)}" rel="noopener">Payload Vault</a></p>`:"");
}

/* ---------- report links: every place that names a record can open the report behind it */
function reportLinks(id,{deep=false}={}){
  const n=nodeById(id);if(!n)return[];
  const out=new Map(),add=(url,label,grade,publisher,date)=>{if(url&&/^https:\/\//.test(url)&&!out.has(url))out.set(url,{url,label:label||url,grade:grade||"",publisher:publisher||"",date:date||""})};
  const fromNode=x=>{
    if(x.type==="source")add(x.data.url,x.label,x.data.grade,x.data.publisher,x.data.published);
    (x.data.source_ids||[]).forEach(s=>{const sn=nodeById(s);if(sn)add(sn.data.url,sn.label,sn.data.grade,sn.data.publisher,sn.data.published)});
    (Array.isArray(x.data.sources)?x.data.sources:[]).forEach(s=>s&&add(s.url,s.title,s.grade,s.publisher));
  };
  fromNode(n);
  if(deep||["actor","technique","tool"].includes(n.type))
    edgesOf(id).forEach(e=>{const o=nodeById(other(e,id));if(o&&["campaign","incident","vulnerability","actor","source"].includes(o.type))fromNode(o)});
  return[...out.values()].sort((a,b)=>(a.grade||"Z").localeCompare(b.grade||"Z")||String(b.date).localeCompare(String(a.date)));
}
const linkChip=l=>`<a class="rlink" href="${esc(l.url)}" target="_blank" rel="noopener" title="${esc(l.publisher)}${l.date?" · "+esc(l.date):""}"><b>${esc(l.grade||"·")}</b>${esc(l.label.length>70?l.label.slice(0,69)+"…":l.label)}<span aria-hidden="true">↗</span></a>`;
function linksRow(id,max=4){
  const ls=reportLinks(id);if(!ls.length)return"";
  return`<div class="rlinks">${ls.slice(0,max).map(linkChip).join("")}${ls.length>max?`<button type="button" class="rmore" data-explode="${esc(id)}">${esc(t("rl.more",{n:ls.length-max}))}</button>`:""}</div>`;
}
/* the exploded list: all reports behind a set of records, grouped by publisher, copyable */
function explodeReports(ids,title){
  const box=$("#reportsPanel");if(!box)return;
  const all=new Map();ids.forEach(id=>reportLinks(id,{deep:true}).forEach(l=>{if(!all.has(l.url))all.set(l.url,{...l,via:new Set()});all.get(l.url).via.add(id)}));
  const ls=[...all.values()],q=norm($("#rlFilter")?.value||"");
  const shown=ls.filter(l=>!q||norm(l.label+" "+l.publisher).includes(q));
  const pubs={};shown.forEach(l=>(pubs[l.publisher||"–"]=pubs[l.publisher||"–"]||[]).push(l));
  box.hidden=false;
  box.innerHTML=`<div class="rp-head"><div><span class="eyebrow">${esc(t("rl.eyebrow"))}</span><h3>${esc(title)}</h3><p class="note">${esc(t("rl.count",{n:nf(ls.length),p:nf(Object.keys(pubs).length)}))}</p></div><div class="rp-tools"><input id="rlFilter" type="search" placeholder="${esc(t("rl.filter"))}" value="${esc($("#rlFilter")?.value||"")}"><button type="button" class="export" data-copy-links>${esc(t("rl.copy"))}</button><button type="button" class="export" data-close-links>${esc(t("rep.close"))}</button></div></div>
    <div class="rp-body">${Object.entries(pubs).sort((a,b)=>b[1].length-a[1].length).map(([p,xs])=>`<div class="rp-pub"><h4>${esc(p)} · ${xs.length}</h4>${xs.map(l=>`<div class="rp-row">${linkChip(l)}<span class="id">${esc([...l.via].slice(0,3).map(v=>nodeById(v)?.label||v).join(" · "))}${l.via.size>3?" +"+(l.via.size-3):""}</span></div>`).join("")}</div>`).join("")||`<p class="empty">${esc(t("common.nothing"))}</p>`}</div>`;
  const f=$("#rlFilter");f.oninput=()=>{const pos=f.selectionStart;explodeReports(ids,title);const g=$("#rlFilter");g.focus();g.setSelectionRange(pos,pos)};
  box.querySelector("[data-close-links]").onclick=()=>{box.hidden=true;patchHash({reports:null})};
  box.querySelector("[data-copy-links]").onclick=e=>{const md=shown.map(l=>`- [${l.label}](${l.url}) — ${l.publisher}${l.grade?" (grade "+l.grade+")":""}`).join("\n");
    navigator.clipboard?.writeText(md).then(()=>{e.target.textContent=t("rl.copied")},()=>{})};
}
document.addEventListener("click",e=>{const b=e.target.closest("[data-explode]");if(!b)return;e.preventDefault();e.stopPropagation();
  const id=b.dataset.explode,ids=id==="@focus"?[...egoIds(G.focus)]:[id],n=nodeById(id==="@focus"?G.focus:id);
  if(!$("#graph").classList.contains("active"))showTab("graph",true);
  explodeReports(ids,t("rl.title",{name:n?.label||id}));patchHash({reports:id});
  requestAnimationFrame(()=>$("#reportsPanel").scrollIntoView({behavior:"smooth",block:"start"}))},true);
