/* Coverage tab: sortable, filterable, with drill-down to the linked records.
   Data comes from coverage.json, built by scripts/coverage_model.py. Loaded before app.js; uses its globals at call time. */
const COV={sort:"id",dir:"asc",show:"",view:"matrix",open:new Set()};
const COV_SHOW=["","observed","spec","noctl","nobench","single","stale","noev"];
const COV_COLS=[["name","th.technique","asc"],["maturity","th.maturity","asc"],["evidence","th.evidence","desc"],["tests","th.tests","desc"],["detections","th.detections","desc"],["controls","th.controls","desc"],["tools","th.tools","desc"],["benchmarks","th.bench","desc"],["priority","th.priority","desc"]];
const COV_MAX_PRIORITY=16, COV_LIST_LIMIT=8;
const covHasRule=r=>r.detections.some(d=>d.implementation==="rule-file");
const COV_TEST={
  "":()=>true,
  observed:r=>r.maturity==="observed-in-the-wild",
  spec:r=>r.detections.length>0&&!covHasRule(r),
  noctl:r=>!r.controls.length,
  nobench:r=>!r.benchmarks.length,
  single:r=>r.publishers.length===1,
  stale:r=>r.stale,
  noev:r=>!r.evidence.length
};
const covCount=(r,k)=>Array.isArray(r[k])?r[k].length:r[k];

function covRows(){
  const vis=new Set(visibleNodes().map(n=>n.id));
  const k=COV.sort,dir=COV.dir==="desc"?-1:1;
  const val=r=>k==="name"?r.name:k==="maturity"?MATURITY_ORDER.indexOf(r.maturity):k==="id"?r.id:covCount(r,k);
  return state.cov.techniques.filter(r=>vis.has(r.id)&&COV_TEST[COV.show](r)).sort((a,b)=>{
    const x=val(a),y=val(b),c=typeof x==="string"?x.localeCompare(y,I18N.locale):x-y;
    return c*dir||a.id.localeCompare(b.id);
  });
}

function buildCoverageControls(){
  const show=$("#covShow"),view=$("#covView");if(!show||!view)return;
  show.innerHTML=COV_SHOW.map(v=>`<option value="${v}">${esc(t("cov.show."+(v||"all")))}</option>`).join("");
  show.value=COV.show;view.value=COV.view;
  if(!show.dataset.bound){
    show.dataset.bound=view.dataset.bound="1";
    show.addEventListener("change",e=>{COV.show=e.target.value;patchHash({show:COV.show||null});renderCoverage()});
    view.addEventListener("change",e=>{COV.view=e.target.value;patchHash({view:COV.view==="matrix"?null:COV.view});renderCoverage()});
    $("#coverageTable").addEventListener("click",covClick);
  }
}
function applyCoverageHash(p){
  const sort=p.get("sort"),dir=p.get("dir"),show=p.get("show"),view=p.get("view");
  if(sort&&(sort==="id"||COV_COLS.some(c=>c[0]===sort)))COV.sort=sort;
  if(dir==="asc"||dir==="desc")COV.dir=dir;
  COV.show=COV_SHOW.includes(show)?show:"";
  COV.view=view==="actors"?"actors":"matrix";
  if(state.cov){buildCoverageControls();renderCoverage()}
}
function covClick(e){
  const sortBtn=e.target.closest(".sortbtn");
  if(sortBtn){
    const key=sortBtn.dataset.sort,col=COV_COLS.find(c=>c[0]===key);
    COV.dir=COV.sort===key?(COV.dir==="asc"?"desc":"asc"):col[2];COV.sort=key;
    patchHash({sort:key,dir:COV.dir});renderCoverage();
    $(`.sortbtn[data-sort="${key}"]`)?.focus();return;
  }
  const exp=e.target.closest(".exp");
  if(exp){
    const id=exp.dataset.t;COV.open.has(id)?COV.open.delete(id):COV.open.add(id);
    renderCoverage();$(`.exp[data-t="${id}"]`)?.focus();
  }
}

const covHeat=n=>`<span class="heat h${Math.min(n,4)}">${n}</span>`;
const covLabel=id=>state.graph.nodes.find(n=>n.id===id)?.label||id;
function covList(ids,render){
  if(!ids.length)return`<p class="note">${esc(t("cov.detail.none"))}</p>`;
  const more=ids.length-COV_LIST_LIMIT;
  return`<ul>${ids.slice(0,COV_LIST_LIMIT).map(render).join("")}</ul>`+(more>0?`<p class="note">${esc(t("cov.detail.more",{n:nf(more)}))}</p>`:"");
}
function covDetail(r){
  const eco=id=>state.eco.find(e=>e.id===id);
  const ext=id=>{const e=eco(id);return e?`<li><a href="${esc(e.url)}" target="_blank" rel="noopener noreferrer">${esc(e.owner)}/${esc(e.name)}</a></li>`:""};
  const det=d=>`<li>${link(d.id,d.name)} <span class="impl ${d.implementation==="rule-file"?"rule":"spec"}">${esc(t(d.implementation==="rule-file"?"cov.rule":"cov.spec"))}</span>${d.platforms.length?` <span class="note">${esc(d.platforms.join(", "))}</span>`:""}</li>`;
  const node=id=>`<li>${link(id,covLabel(id))}</li>`;
  const block=(key,body)=>`<div><h4>${esc(t("cov.detail."+key))}</h4>${body}</div>`;
  const facts=[
    r.newest_evidence?t("cov.fresh",{date:r.newest_evidence}):t("cov.nofresh"),
    r.stale?t("cov.stale",{n:nf(state.cov.stale_days)}):"",
    r.publishers.length?t("cov.pubs",{n:nf(r.publishers.length),list:r.publishers.join(", ")}):"",
    r.best_grade?t("cov.bestgrade",{g:r.best_grade}):""
  ].filter(Boolean).join(" · ");
  return`<div class="cd-grid">${block("evidence",covList(r.evidence,node))}${block("tests",covList(r.tests,node))}${block("detections",covList(r.detections,det))}${block("controls",covList(r.controls,node))}${block("bench",covList(r.benchmarks,ext))}${block("tools",covList(r.tools.filter(id=>!r.benchmarks.includes(id)),ext))}${block("actors",covList(r.actors,node))}</div><p class="note cd-facts">${esc(facts)}</p><p><a href="#" data-id="${esc(r.id)}">${esc(t("cov.detail.open"))}</a></p>`;
}
function covMatrixTable(rows){
  const th=COV_COLS.map(([k,label])=>{
    const on=COV.sort===k,aria=on?(COV.dir==="asc"?"ascending":"descending"):"none";
    return`<th scope="col" aria-sort="${aria}"><button type="button" class="sortbtn" data-sort="${k}" title="${esc(t("cov.sortby",{col:t(label)}))}">${esc(t(label))}<span class="arrow" aria-hidden="true">${on?(COV.dir==="asc"?"▲":"▼"):""}</span></button></th>`;
  }).join("");
  const body=rows.map(r=>{
    const open=COV.open.has(r.id),rule=covHasRule(r);
    const nd=r.detections.length;
    return`<tr class="covrow${open?" open":""}"><td><button type="button" class="exp" data-t="${esc(r.id)}" aria-expanded="${open}" aria-controls="cd-${esc(r.id)}"><span class="chev" aria-hidden="true"></span><b>${esc(r.name)}</b></button><br><span class="id">${esc(r.id)}</span></td>`+
      `<td><span class="mat ${esc(r.maturity)}">${esc(matLabel(r.maturity))}</span></td>`+
      `<td>${covHeat(r.evidence.length)}${r.stale?`<span class="stale" title="${esc(t("cov.stale",{n:nf(state.cov.stale_days)}))}">!</span>`:""}</td>`+
      `<td>${covHeat(r.tests.length)}</td>`+
      `<td>${covHeat(nd)}${rule?`<span class="impl rule" title="${esc(t("cov.rule"))}">${esc(t("cov.rule.short"))}</span>`:""}</td>`+
      `<td>${covHeat(r.controls.length)}</td><td>${covHeat(r.tools.length)}</td><td>${covHeat(r.benchmarks.length)}</td>`+
      `<td><span class="pbar" role="img" aria-label="${r.priority}/${COV_MAX_PRIORITY}"><i style="width:${(100*r.priority/COV_MAX_PRIORITY).toFixed(0)}%"></i></span><span class="pnum">${r.priority}</span></td></tr>`+
      (open?`<tr class="covdetail" id="cd-${esc(r.id)}"><td colspan="${COV_COLS.length}">${covDetail(r)}</td></tr>`:"");
  }).join("");
  return`<thead><tr>${th}</tr></thead><tbody>${body||`<tr><td colspan="${COV_COLS.length}" class="empty">${esc(t("cov.empty"))}</td></tr>`}</tbody>`;
}
function covActorsTable(){
  const m=state.cov.matrix,techs=[...new Set(m.map(x=>x.technique))].sort(),actors=state.cov.actors;
  const name=Object.fromEntries(state.cov.techniques.map(r=>[r.id,r.name]));
  if(!m.length)return`<tbody><tr><td class="empty">${esc(t("cov.empty"))}</td></tr></tbody>`;
  const head=`<thead><tr><th scope="col">${esc(t("cov.actor"))}</th>${techs.map(id=>`<th scope="col" class="mxh" title="${esc(name[id])}"><span class="id">${esc(id.slice(-4))}</span></th>`).join("")}</tr></thead>`;
  const rows=actors.map(a=>`<tr><th scope="row"><b>${esc(a.name)}</b></th>${techs.map(id=>{
    const hit=m.find(x=>x.actor===a.id&&x.technique===id);
    return hit?`<td><button type="button" class="mx" data-id="${esc(hit.via[0])}" aria-label="${esc(a.name)} · ${esc(name[id])} · ${esc(covLabel(hit.via[0]))}" title="${esc(covLabel(hit.via[0]))}"></button></td>`:`<td><span class="mx0" aria-hidden="true"></span></td>`;
  }).join("")}</tr>`).join("");
  const legend=`<caption class="mxcap"><div>${techs.map(id=>`<span><span class="id">${esc(id.slice(-4))}</span> ${esc(name[id])}</span>`).join("")}</div></caption>`;
  return legend+head+`<tbody>${rows}</tbody>`;
}
function renderCoverage(){
  const tbl=$("#coverageTable");
  if(!state.cov){tbl.innerHTML=`<tbody><tr><td class="empty">${esc(t("cov.unavailable"))}</td></tr></tbody>`;return}
  const s=state.cov.summary,actors=COV.view==="actors";
  $("#covShowWrap").hidden=actors;
  $("#covNote").textContent=actors?t("cov.actors.note"):t("cov.note",{rules:nf(s.detections_with_rule_file),total:nf(s.detections_total),asof:state.cov.as_of});
  $("#covFormula").hidden=actors;
  tbl.className="tbl cov"+(actors?" actors":"");
  tbl.innerHTML=actors?covActorsTable():covMatrixTable(covRows());
  afterRender();
}
function coverageCsv(){
  const headers=["id","technique","maturity","evidence","publishers","best_grade","newest_evidence","stale","tests","detections","detections_with_rule_file","controls","tools","benchmarks","actors","priority"];
  return[headers,covRows().map(r=>[r.id,r.name,r.maturity,r.evidence.length,r.publishers,r.best_grade,r.newest_evidence,r.stale,r.tests.length,r.detections.length,r.detections.filter(d=>d.implementation==="rule-file").length,r.controls.length,r.tools.length,r.benchmarks.length,r.actors,r.priority])];
}
