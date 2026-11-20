/* On-demand report: the records picked in the graph, their context, how to detect and defend, and every source.
   Built in the browser from graph.json and reports.json; nothing leaves the page. */
const TYPE_ORDER=["actor","campaign","incident","vulnerability","tool","technique","test-case","detection","control","framework","model","source"];
const CONF_RANK={confirmed:0,high:1,medium:2,low:3,unverified:4};
const REPO_BLOB="https://github.com/Ridd1kulusC0d3r/LLmInjection/blob/main/";
const KEV="SRC-CISA-KEV-CATALOG";
const R={graph:null,idx:null,byId:new Map(),adj:new Map(),reportsText:{}};
const $=s=>document.querySelector(s);
function esc(v){return String(v??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]))}
const typeLabel=x=>tOr("type."+x,x),confLabel=x=>tOr("conf."+x,x),relLabel=x=>tOr("rel."+x,x);
const node=id=>R.byId.get(id);
const params=()=>new URLSearchParams(location.hash.slice(1));

async function boot(){
  await setLang(detectLang(),{persist:false});
  const [g,idx]=await Promise.all([fetch("graph.json").then(r=>r.json()),fetch("reports.json").then(r=>r.ok?r.json():null).catch(()=>null)]);
  R.graph=g;R.idx=idx;
  g.nodes.forEach(n=>R.byId.set(n.id,n));
  g.edges.forEach(e=>{[[e.source,e.target],[e.target,e.source]].forEach(([a,b])=>{(R.adj.get(a)||R.adj.set(a,[]).get(a)).push({e,o:b})})});
  /* authored reports: fetched once so the page can say which of them mention the records in scope */
  await Promise.all((idx?.reports||[]).filter(r=>r.kind!=="platform"&&r.kind!=="template").map(r=>fetch(r.path).then(x=>x.ok?x.text():"").then(t=>{R.reportsText[r.path]=t}).catch(()=>{})));
  $("#lang").innerHTML=LANGS.map(l=>`<option value="${l.code}"${l.code===I18N.lang?" selected":""}>${esc(l.name)}</option>`).join("");
  $("#lang").onchange=async e=>{await setLang(e.target.value);setParam("lang",e.target.value);render()};
  window.addEventListener("hashchange",render);
  render();
}
function setParam(k,v){const p=params();v==null?p.delete(k):p.set(k,v);history.replaceState(null,"","#"+p.toString())}

/* scope: the picked records, plus (depth 1) the same neighbourhood the graph's focus view uses */
function scopeOf(ids,depth){
  const keep=new Set(ids),ctx=new Set();
  if(depth>0)ids.forEach(id=>{
    const hop=x=>(R.adj.get(x)||[]).map(a=>a.o).filter(y=>node(y)&&node(y).type!=="source");
    const first=hop(id);first.forEach(x=>ctx.add(x));
    first.filter(x=>["campaign","incident","vulnerability","actor"].includes(node(x)?.type)).forEach(x=>hop(x).forEach(y=>ctx.add(y)));
  });
  keep.forEach(x=>ctx.delete(x));
  return{sel:[...keep],ctx:[...ctx]};
}
const byType=(ids,type)=>ids.map(node).filter(n=>n&&n.type===type);
const sortConf=(a,b)=>(CONF_RANK[a.data.confidence]??9)-(CONF_RANK[b.data.confidence]??9)||a.label.localeCompare(b.label);
const isKev=n=>(n.data.source_ids||[]).includes(KEV);

function model(){
  const p=params(),ids=(p.get("ids")||"").split(",").map(s=>s.trim()).filter(id=>R.byId.has(id)),depth=p.get("depth")==="0"?0:1;
  const {sel,ctx}=scopeOf(ids,depth),scope=[...sel,...ctx],inScope=new Set(scope);
  const techs=scope.filter(id=>node(id).type==="technique");
  const rel=(id,r,t)=>(R.adj.get(id)||[]).filter(a=>a.e.relationship===r&&node(a.o)?.type===t).map(a=>a.o);
  const dets=new Map(),ctrls=new Map();
  scope.forEach(id=>{const n=node(id);if(n.type==="detection")dets.set(id,new Set());if(n.type==="control")ctrls.set(id,new Set())});
  techs.forEach(tid=>{rel(tid,"detects","detection").forEach(d=>(dets.get(d)||dets.set(d,new Set()).get(d)).add(tid));rel(tid,"mitigated-by","control").forEach(c=>(ctrls.get(c)||ctrls.set(c,new Set()).get(c)).add(tid))});
  scope.filter(id=>["vulnerability","tool"].includes(node(id).type)).forEach(v=>{rel(v,"mitigated-by","control").forEach(c=>(ctrls.get(c)||ctrls.set(c,new Set()).get(c)).add(v));rel(v,"detects","detection").forEach(d=>(dets.get(d)||dets.set(d,new Set()).get(d)).add(v))});
  /* links among picked records, then records that touch two or more of them */
  const among=R.graph.edges.filter(e=>sel.includes(e.source)&&sel.includes(e.target));
  const shared=sel.length>1?[...new Set(sel.flatMap(id=>(R.adj.get(id)||[]).map(a=>a.o)))].filter(o=>!sel.includes(o)&&node(o)?.type!=="source"&&sel.filter(s=>(R.adj.get(s)||[]).some(a=>a.o===o)).length>1):[];
  /* evidence */
  const src=new Map(),addSrc=(s,via)=>{const n=node(s);if(!n||n.type!=="source"||!/^https:\/\//.test(n.data.url||""))return;(src.get(s)||src.set(s,{n,via:new Set()}).get(s)).via.add(via)};
  scope.forEach(id=>{const n=node(id);(n.data.source_ids||[]).forEach(s=>addSrc(s,id));(R.adj.get(id)||[]).filter(a=>a.e.relationship==="sourced-by").forEach(a=>addSrc(a.o,id));
    (Array.isArray(n.data.sources)?n.data.sources:[]).forEach(s=>{if(s&&/^https:\/\//.test(s.url||"")){const k="url:"+s.url;(src.get(k)||src.set(k,{n:{id:k,label:s.title||s.url,data:{url:s.url,grade:s.grade||"",publisher:s.publisher||""}},via:new Set()}).get(k)).via.add(id)}})});
  const sources=[...src.values()].sort((a,b)=>String(a.n.data.grade||"Z").localeCompare(String(b.n.data.grade||"Z"))||b.via.size-a.via.size);
  const reports=(R.idx?.reports||[]).filter(r=>R.reportsText[r.path]).map(r=>({r,hits:sel.filter(id=>R.reportsText[r.path].includes(id)||R.reportsText[r.path].includes(node(id).label))})).filter(x=>x.hits.length);
  return{ids,depth,sel,ctx,scope,inScope,techs,dets,ctrls,among,shared,sources,reports};
}

function facts(n){
  const d=n.data,f=[];
  if(d.identifiers)f.push([t("srp.f.ids"),d.identifiers.join(", ")]);
  if(d.severity)f.push([t("srp.f.severity"),d.severity]);
  if(d.affected?.length)f.push([t("srp.f.affected"),d.affected.join("; ")]);
  if(n.type==="vulnerability")f.push([t("srp.f.patched"),d.patched?.length?d.patched.join(", "):t("srp.f.nofix")]);
  if(d.first_seen||d.last_seen)f.push([t("srp.f.seen"),[d.first_seen,d.last_seen].filter(Boolean).join(" → ")]);
  if(d.date)f.push([t("srp.f.date"),d.date]);
  if(d.nexus)f.push([t("srp.f.nexus"),d.nexus]);
  if(d.aliases?.length)f.push([t("srp.f.aliases"),d.aliases.join(", ")]);
  if(d.maturity)f.push([t("srp.f.maturity"),tOr("mat."+d.maturity,d.maturity)]);
  if(d.layer)f.push([t("srp.f.layer"),d.layer]);
  if(d.telemetry?.length)f.push([t("srp.f.telemetry"),d.telemetry.join("; ")]);
  if(isKev(n))f.push(["CISA KEV",t("srp.f.kev")]);
  return f;
}
const text=n=>n.data.summary||n.data.hypothesis||n.data.description||n.data.goal||"";
const ruleFiles=id=>R.idx?.rule_files?.[id]||[];
const extRules=id=>R.idx?.external_rules?.[id]?.urls||[];

function bluf(m){
  const c=t=>m.scope.filter(id=>node(id).type===t).length;
  const vulns=byType(m.scope,"vulnerability"),kev=vulns.filter(isKev).length,withRules=[...m.dets.keys()].filter(d=>ruleFiles(d).length||extRules(d).length).length;
  const gradeA=m.sources.filter(s=>s.n.data.grade==="A").length;
  return t("srp.bluf",{n:m.scope.length,sel:m.sel.length,actors:c("actor"),campaigns:c("campaign")+c("incident"),techs:m.techs.length,vulns:vulns.length,kev,dets:m.dets.size,rules:withRules,ctrls:m.ctrls.size,src:m.sources.length,a:gradeA});
}

function render(){
  const m=model(),gen=new Date().toISOString().slice(0,10),asof=(R.graph.meta?.generated_at||"").slice(0,10);
  document.querySelectorAll("[data-depth]").forEach(b=>b.setAttribute("aria-pressed",String(+b.dataset.depth===m.depth)));
  $("#back").href="./#tab=graph"+(m.ids.length===1?"&focus="+encodeURIComponent(m.ids[0]):"")+"&lang="+I18N.lang;
  if(!m.ids.length){$("#doc").innerHTML=`<p class="empty">${esc(t("srp.empty"))}</p>`;return}
  const title=m.sel.length<=3?m.sel.map(id=>node(id).label).join(" · "):`${m.sel.slice(0,2).map(id=>node(id).label).join(" · ")} +${m.sel.length-2}`;
  const code="LLMI-SEL-"+[...m.ids.join("|")].reduce((h,ch)=>(h*31+ch.charCodeAt(0))>>>0,7).toString(36).toUpperCase().slice(0,6);
  document.title=`${title} · ${t("srp.kind")}`;R.file=code;
  const chip=id=>{const n=node(id);return`<a class="rchip" href="./#node=${encodeURIComponent(id)}&lang=${I18N.lang}" title="${esc(n.id)}"><span>${esc(typeLabel(n.type))}</span>${esc(n.label)}</a>`};
  const conf=c=>c?`<span class="rconf c-${esc(c)}">${esc(confLabel(c))}</span>`:"";
  const card=n=>`<article class="rcard"><header><span class="eyebrow">${esc(typeLabel(n.type))}</span><span class="id">${esc(n.id)}</span>${conf(n.data.confidence)}</header><h3>${esc(n.label)}</h3>${text(n)?`<p>${esc(text(n))}</p>`:""}${facts(n).length?`<dl>${facts(n).map(([k,v])=>`<dt>${esc(k)}</dt><dd>${esc(v)}</dd>`).join("")}</dl>`:""}<a class="more" href="./#node=${encodeURIComponent(n.id)}&lang=${I18N.lang}">${esc(t("srp.open"))} →</a></article>`;
  const table=(head,rows)=>rows.length?`<div class="rtable"><table><thead><tr>${head.map(h=>`<th>${esc(h)}</th>`).join("")}</tr></thead><tbody>${rows.map(r=>`<tr>${r.map(c=>`<td>${c}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`:`<p class="empty">${esc(t("srp.none"))}</p>`;
  const sec=(n,key,body,note)=>`<section class="rsec"><h2><span>${n}</span>${esc(t(key))}</h2>${note?`<p class="note">${esc(note)}</p>`:""}${body}</section>`;
  let k=0;const S=[];
  S.push(sec(++k,"srp.s.selected",`<div class="rcards">${m.sel.map(node).map(card).join("")}</div>`));
  if(m.sel.length>1)S.push(sec(++k,"srp.s.connect",
    table([t("srp.h.from"),t("srp.h.rel"),t("srp.h.to"),t("srp.h.conf")],m.among.map(e=>[chip(e.source),esc(relLabel(e.relationship)),chip(e.target),conf(e.confidence)]))+
    (m.shared.length?`<h4>${esc(t("srp.shared",{n:m.shared.length}))}</h4><div class="rchips">${m.shared.map(chip).join("")}</div>`:""),t("srp.connect.note")));
  if(m.depth>0){
    const groups=TYPE_ORDER.filter(x=>!["detection","control","source"].includes(x)).map(x=>[x,byType(m.ctx,x).sort(sortConf)]).filter(([,v])=>v.length);
    S.push(sec(++k,"srp.s.context",groups.map(([x,v])=>`<h4>${esc(typeLabel(x))} · ${v.length}</h4>`+(x==="vulnerability"
      ?table([t("srp.h.record"),t("srp.f.ids"),t("srp.f.severity"),t("srp.f.patched"),"KEV"],v.map(n=>[chip(n.id),esc((n.data.identifiers||[]).join(", ")),esc(n.data.severity||""),esc((n.data.patched||[]).join(", ")||t("srp.f.nofix")),isKev(n)?"<b class=kev>KEV</b>":""]))
      :table([t("srp.h.record"),t("srp.h.conf"),t("srp.h.summary")],v.map(n=>[chip(n.id),conf(n.data.confidence)||esc(tOr("mat."+n.data.maturity,n.data.maturity||"")),esc(text(n).slice(0,220)+(text(n).length>220?"…":""))])))).join(""),t("srp.context.note")));
  }
  const dets=[...m.dets.entries()].map(([d,via])=>[node(d),via]).sort((a,b)=>(ruleFiles(b[0].id).length+extRules(b[0].id).length)-(ruleFiles(a[0].id).length+extRules(a[0].id).length)||a[0].id.localeCompare(b[0].id));
  S.push(sec(++k,"srp.s.detect",table([t("srp.h.detection"),t("srp.f.severity"),t("srp.h.hypothesis"),t("srp.h.covers"),t("srp.h.rules")],dets.map(([n,via])=>[chip(n.id),esc(n.data.severity||""),esc(n.data.hypothesis||""),[...via].map(chip).join(" "),
    [...ruleFiles(n.id).map(p=>`<a class="out" href="${REPO_BLOB}${esc(p)}" rel="noopener">${esc(p.split("/")[1])}</a>`),...extRules(n.id).slice(0,3).map(u=>`<a class="out" href="${esc(u)}" rel="noopener">artex-detections</a>`)].join(" ")||`<span class="id">${esc(t("srp.spec"))}</span>`])),t("srp.detect.note")));
  const ctrls=[...m.ctrls.entries()].map(([c,via])=>[node(c),via]).sort((a,b)=>String(a[0].data.layer).localeCompare(String(b[0].data.layer)));
  S.push(sec(++k,"srp.s.defend",table([t("srp.h.control"),t("srp.f.layer"),t("srp.h.summary"),t("srp.h.covers")],ctrls.map(([n,via])=>[chip(n.id),esc(n.data.layer||""),esc(n.data.description||""),[...via].map(chip).join(" ")]))));
  if(m.reports.length)S.push(sec(++k,"srp.s.reports",`<ul class="rlist">${m.reports.map(x=>`<li><a href="./#tab=reports&report=${encodeURIComponent(x.r.path)}&lang=${I18N.lang}">${esc(x.r.title)}</a> <span class="id">${esc(x.r.kind)} · ${esc(x.r.date)}</span> <span class="rchips">${x.hits.map(chip).join("")}</span></li>`).join("")}</ul>`));
  S.push(sec(++k,"srp.s.sources",table([t("srp.h.source"),t("srp.h.publisher"),t("srp.h.grade"),t("srp.h.supports")],m.sources.map(s=>[`<a class="out" href="${esc(s.n.data.url)}" rel="noopener">${esc(s.n.label)}</a>`,esc(s.n.data.publisher||""),s.n.data.grade?`<b class="grade g-${esc(s.n.data.grade)}">${esc(s.n.data.grade)}</b>`:"",[...s.via].slice(0,4).map(chip).join(" ")+(s.via.size>4?` <span class="id">+${s.via.size-4}</span>`:"")])),t("srp.sources.note")));
  $("#doc").innerHTML=`<header class="rmast"><div class="rmast-bar"><span>LLMINJECTION / ${esc(t("srp.kind").toUpperCase())}</span><span class="tlp">TLP:CLEAR</span></div>
    <h1 contenteditable="true" spellcheck="false" title="${esc(t("srp.edit"))}">${esc(title)}</h1>
    <p class="rhead"><span>${esc(code)}</span><span>${esc(t("srp.generated",{d:gen}))}</span><span>${esc(t("srp.asof",{d:asof}))}</span><span>${esc(t("srp.scope",{n:m.scope.length}))}</span></p></header>
    <div class="rbluf"><b>BLUF</b> ${esc(bluf(m))}</div>
    <p class="rprov">${esc(t("srp.prov"))}</p>${S.join("")}`;
  R.md=()=>markdown(m,title,code,gen,asof,dets,ctrls);
}

function markdown(m,title,code,gen,asof,dets,ctrls){
  const L=[];title=$("#doc h1")?.textContent||title;const lbl=id=>`${node(id).label} (\`${id}\`)`,cell=s=>String(s??"").replace(/\|/g,"\\|").replace(/\n/g," ");
  const tbl=(h,rows)=>rows.length?[`| ${h.join(" | ")} |`,`|${h.map(()=>"---").join("|")}|`,...rows.map(r=>`| ${r.map(cell).join(" | ")} |`),""]:[`_${t("srp.none")}_`,""];
  L.push(`# ${title}`,"",`${code} · TLP:CLEAR · ${t("srp.generated",{d:gen})} · ${t("srp.asof",{d:asof})}`,"",`> **BLUF** ${bluf(m)}`,"",`_${t("srp.prov")}_`,"");
  L.push(`## ${t("srp.s.selected")}`,"");
  m.sel.map(node).forEach(n=>{L.push(`### ${n.label}`,"",`${typeLabel(n.type)} · \`${n.id}\`${n.data.confidence?" · "+confLabel(n.data.confidence):""}`,"");if(text(n))L.push(text(n),"");facts(n).forEach(([a,b])=>L.push(`- **${a}:** ${b}`));L.push("")});
  if(m.sel.length>1){L.push(`## ${t("srp.s.connect")}`,"",...tbl([t("srp.h.from"),t("srp.h.rel"),t("srp.h.to"),t("srp.h.conf")],m.among.map(e=>[lbl(e.source),relLabel(e.relationship),lbl(e.target),confLabel(e.confidence||"")])));if(m.shared.length)L.push(`${t("srp.shared",{n:m.shared.length})}: ${m.shared.map(lbl).join(", ")}`,"")}
  if(m.depth>0){L.push(`## ${t("srp.s.context")}`,"");TYPE_ORDER.filter(x=>!["detection","control","source"].includes(x)).forEach(x=>{const v=byType(m.ctx,x).sort(sortConf);if(v.length){L.push(`### ${typeLabel(x)} · ${v.length}`,"");v.forEach(n=>L.push(`- ${lbl(n.id)}${n.data.confidence?" — "+confLabel(n.data.confidence):""}${isKev(n)?" — CISA KEV":""}`));L.push("")}})}
  L.push(`## ${t("srp.s.detect")}`,"",...tbl([t("srp.h.detection"),t("srp.f.severity"),t("srp.h.hypothesis"),t("srp.h.rules")],dets.map(([n])=>[lbl(n.id),n.data.severity||"",n.data.hypothesis||"",[...ruleFiles(n.id).map(p=>`[${p.split("/")[1]}](${REPO_BLOB}${p})`),...extRules(n.id).slice(0,3).map(u=>`[artex-detections](${u})`)].join(" ")||t("srp.spec")])));
  L.push(`## ${t("srp.s.defend")}`,"",...tbl([t("srp.h.control"),t("srp.f.layer"),t("srp.h.summary")],ctrls.map(([n])=>[lbl(n.id),n.data.layer||"",n.data.description||""])));
  if(m.reports.length){L.push(`## ${t("srp.s.reports")}`,"");m.reports.forEach(x=>L.push(`- [${x.r.title}](${x.r.github}) — ${x.r.kind}, ${x.r.date}`));L.push("")}
  L.push(`## ${t("srp.s.sources")}`,"");m.sources.forEach(s=>L.push(`- [${s.n.label}](${s.n.data.url}) — ${s.n.data.publisher||""}${s.n.data.grade?` (${t("srp.h.grade")} ${s.n.data.grade})`:""}`));
  L.push("","---",`${t("srp.permalink")}: ${location.href}`);
  return L.join("\n")+"\n";
}

document.addEventListener("click",e=>{
  const d=e.target.closest("[data-depth]");if(d){setParam("depth",d.dataset.depth);render();return}
  const a=e.target.closest("[data-act]");if(!a)return;
  const act=a.dataset.act;
  if(act==="print")window.print();
  if(act==="md"){const md=R.md?.();if(!md)return;const u=URL.createObjectURL(new Blob([md],{type:"text/markdown"}));const x=document.createElement("a");x.href=u;x.download=`${R.file||"report"}-${(($("#doc h1")?.textContent)||"").replace(/[^\p{L}\p{N}]+/gu,"-").replace(/^-|-$/g,"").slice(0,60)}.md`;x.click();setTimeout(()=>URL.revokeObjectURL(u),1000)}
  if(act==="copy")navigator.clipboard?.writeText(location.href).then(()=>{a.textContent=t("rl.copied")},()=>{});
});
boot().catch(e=>{$("#doc").innerHTML=`<p role="alert" class="empty">${esc(e.message)}</p>`});
