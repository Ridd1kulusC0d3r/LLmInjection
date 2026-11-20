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
  cats.map(c=>`<h3 class="sect">${esc(tOr("cat."+c,c.replace(/-/g," ")))}</h3><div class="table-wrap" tabindex="0"><table class="tbl"><thead><tr><th>${esc(t("th.technique"))}</th><th>${esc(t("ttp.maturity"))}</th><th class="num">${esc(t("ttp.actors"))}</th><th class="num">${esc(t("ttp.evidence"))}</th><th>OWASP</th><th>MITRE ATLAS</th><th>${esc(t("ttp.playbook"))}</th></tr></thead><tbody>${techs.filter(n=>n.data.category===c).map(n=>{const r=cov.get(n.id)||{};return`<tr data-id="${esc(n.id)}"><td><span class="id">${esc(n.id)}</span><br><b>${esc(n.label)}</b></td><td>${esc(matLabel(n.data.maturity))}</td><td class="num">${(r.actors||[]).length}</td><td class="num">${(r.evidence||[]).length}</td><td class="id">${esc(ext(n,"OWASP").join(", ")||"–")}</td><td class="id">${esc(ext(n,"MITRE ATLAS").join(", ")||"–")}</td><td><a class="out" href="${REPO_BLOB}docs/playbooks/${esc(n.id)}.md" rel="noopener">${esc(t("ttp.open"))}</a></td></tr>`}).join("")}</tbody></table></div>`).join("");
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
  box.innerHTML=`<p class="note" style="margin:0 0 14px">${esc(t("hunt.count",{n:nf(shown.length)}))}</p><div class="hunts">${shown.map((r,i)=>`<div class="hunt" data-id="${esc(r.n.id)}"><div class="hunt-h"><span class="rank">${i+1}</span><span class="id">${esc(r.n.id)} · ${esc(r.n.data.severity||"")}</span><span class="trend${r.best===3?" rising":""}">${esc(r.best===3?t("hunt.wild"):r.best===2?t("hunt.vuln"):t("hunt.research"))}</span></div><h3>${esc(r.n.data.hypothesis||r.n.label)}</h3><p class="note">${esc(r.n.label)}</p><div class="tele">${(r.n.data.telemetry||[]).map(x=>`<span>${esc(x)}</span>`).join("")}</div><div class="hunt-f">${r.techs.map(chipLink).join(" ")}<span class="id">${esc(t("hunt.evidence",{n:r.evidence}))}</span></div></div>`).join("")}</div>`;
}

/* ---------- detection engineering: every detection, its rule files and its tests */
function renderDetection(){
  const box=$("#detBody");if(!box)return;
  const rules=SP.reports?.rule_files||{},rows=state.graph.nodes.filter(n=>n.type==="detection");
  const withRule=rows.filter(n=>rules[n.id]).length;
  box.innerHTML=`<div class="strip" style="grid-template-columns:repeat(3,1fr)">${stat(nf(rows.length),t("det.total"))}${stat(nf(withRule),t("det.rules"))}${stat(nf(rows.filter(n=>(n.data.test_ids||[]).length).length),t("det.tested"))}</div>
    <div class="table-wrap" tabindex="0"><table class="tbl"><thead><tr><th>${esc(t("det.rule"))}</th><th>${esc(t("det.cat"))}</th><th>${esc(t("det.state"))}</th><th>${esc(t("det.files"))}</th><th>${esc(t("det.techs"))}</th><th>${esc(t("det.tests"))}</th></tr></thead><tbody>${rows.sort((a,b)=>(rules[b.id]?1:0)-(rules[a.id]?1:0)||a.id.localeCompare(b.id)).map(n=>`<tr data-id="${esc(n.id)}"><td><span class="id">${esc(n.id)}</span><br><b>${esc(n.label)}</b></td><td>${esc(n.data.category||"")} · ${esc(n.data.severity||"")}</td><td><span class="trend${rules[n.id]?" rising":""}">${esc(rules[n.id]?t("det.state.rule"):t("det.state.spec"))}</span></td><td>${(rules[n.id]||[]).map(p=>`<a class="out" href="${REPO_BLOB}${esc(p)}" rel="noopener">${esc(p.split("/")[1])}</a>`).join(" ")||"–"}</td><td>${edgesOf(n.id,"detects").map(e=>chipLink(other(e,n.id))).join(" ")}</td><td class="id">${esc((n.data.test_ids||[]).join(", ")||"–")}</td></tr>`).join("")}</tbody></table></div>`;
}

/* ---------- threat modelling: attack surface → techniques → controls → frameworks */
function renderThreatModel(){
  const box=$("#tmBody");if(!box)return;
  const techs=state.graph.nodes.filter(n=>n.type==="technique"),cats=[...new Set(techs.map(n=>n.data.category))];
  const ctl=id=>edgesOf(id,"mitigated-by").map(e=>other(e,id)).filter(x=>x.startsWith("CTRL-"));
  const fw=state.graph.nodes.filter(n=>n.type==="framework");
  box.innerHTML=`<div class="tm">${cats.map(c=>{const ts=techs.filter(n=>n.data.category===c);return`<div class="dp"><h3>${esc(tOr("cat."+c,c.replace(/-/g," ")))}</h3><ul class="plain">${ts.map(n=>{const cs=ctl(n.id);return`<li><a href="#" data-id="${esc(n.id)}">${esc(n.label)}</a> <span class="id">${esc(matLabel(n.data.maturity))}</span><div class="tm-ctl">${cs.length?cs.map(id=>`<a href="#" class="tchip ctl" data-id="${esc(id)}">${esc(nodeById(id)?.label||id)}</a>`).join(""):`<span class="gap">${esc(t("tm.noctl"))}</span>`}</div></li>`}).join("")}</ul></div>`}).join("")}</div>
    <h3 class="sect">${esc(t("tm.frameworks"))}</h3><div class="table-wrap" tabindex="0"><table class="tbl"><thead><tr><th>${esc(t("tm.fw"))}</th><th>${esc(t("tm.scope"))}</th><th>${esc(t("tm.use"))}</th></tr></thead><tbody>${fw.map(n=>`<tr><td>${n.data.url?`<a class="out" href="${esc(n.data.url)}" rel="noopener"><b>${esc(n.label)}</b></a>`:`<b>${esc(n.label)}</b>`}</td><td>${esc(n.data.scope||"")}</td><td>${esc(n.data.use||"")}</td></tr>`).join("")}</tbody></table></div>`;
}
function renderSpaces(){renderReports();renderTrends();renderTTPs();renderHunting();renderDetection();renderThreatModel()}
