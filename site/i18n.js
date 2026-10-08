/* Minimal i18n runtime: JSON dictionaries in i18n/<code>.json, English as the fallback. */
const LANGS=[
  {code:"en",name:"English",htmlLang:"en",locale:"en"},
  {code:"pt",name:"Português",htmlLang:"pt-BR",locale:"pt-BR"},
  {code:"es",name:"Español",htmlLang:"es",locale:"es"},
  {code:"zh",name:"中文(简体)",htmlLang:"zh-Hans",locale:"zh-CN"},
  {code:"ru",name:"Русский",htmlLang:"ru",locale:"ru"}
];
const I18N={lang:"en",locale:"en",dict:{},fallback:{}};

const t=(key,vars)=>{
  let s=I18N.dict[key]??I18N.fallback[key]??key;
  if(vars)s=s.replace(/\{(\w+)\}/g,(_,k)=>vars[k]??"");
  return s;
};
/* label lookup with a graceful fallback for values the dictionary does not cover */
const tOr=(key,fallback)=>I18N.dict[key]??I18N.fallback[key]??fallback;
const nf=(n,opts)=>new Intl.NumberFormat(I18N.locale,opts).format(n);
/* accent- and case-insensitive text for search; keeps Cyrillic and CJK intact */
const norm=s=>String(s??"").normalize("NFD").replace(/[̀-ͯ]/g,"").toLowerCase();

async function loadDict(code){
  const r=await fetch(`i18n/${code}.json`);
  if(!r.ok)throw new Error(`i18n/${code}.json ${r.status}`);
  return r.json();
}
function detectLang(){
  const p=new URLSearchParams(location.hash.slice(1)).get("lang")||new URLSearchParams(location.search).get("lang");
  const known=c=>LANGS.some(l=>l.code===c)?c:null;
  if(known(p))return p;
  try{const s=localStorage.getItem("llmi-lang");if(known(s))return s}catch(_){}
  for(const tag of navigator.languages||[navigator.language||"en"]){
    const base=String(tag).toLowerCase().split("-")[0];
    if(known(base))return base;
  }
  return "en";
}
function applyStatic(){
  document.querySelectorAll("[data-i18n]").forEach(el=>{el.textContent=t(el.dataset.i18n)});
  document.querySelectorAll("[data-i18n-attr]").forEach(el=>{
    el.dataset.i18nAttr.split(";").forEach(pair=>{const [attr,key]=pair.split(":");if(attr&&key)el.setAttribute(attr.trim(),t(key.trim()))});
  });
  document.title=t("meta.title");
  const m=document.querySelector('meta[name="description"]');if(m)m.content=t("meta.description");
}
async function setLang(code,{persist=true}={}){
  const meta=LANGS.find(l=>l.code===code)||LANGS[0];
  if(!Object.keys(I18N.fallback).length)I18N.fallback=await loadDict("en");
  I18N.dict=meta.code==="en"?I18N.fallback:await loadDict(meta.code);
  I18N.lang=meta.code;I18N.locale=meta.locale;
  document.documentElement.lang=meta.htmlLang;
  applyStatic();
  if(persist){try{localStorage.setItem("llmi-lang",meta.code)}catch(_){}}
  return meta;
}
