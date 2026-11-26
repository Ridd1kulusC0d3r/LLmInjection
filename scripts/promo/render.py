"""Render the LLMInjection video tour frame by frame (Playwright + ffmpeg).

usage: python render.py en|pt  -> out/llminjection-promo-<lang>.mp4 and out/timeline-<lang>.json
The site must be served at BASE (python -m http.server 8765 -d _site).
Numbers on the title cards and captions are read from the live Explorer at render time.
The timeline file lists when each beat starts, so a voice-over can be placed on it.
"""

import json
import math
import shutil
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

LANG = sys.argv[1] if len(sys.argv) > 1 else "en"
FPS = 30
VW, VH, DSF = 1440, 810, 4 / 3  # -> 1920x1080
BASE = "http://localhost:8765/"
HERE = Path(__file__).parent
FR = HERE / f"frames-{LANG}"
OUT = HERE / "out"
shutil.rmtree(FR, ignore_errors=True)
FR.mkdir(parents=True)
OUT.mkdir(exist_ok=True)

T = json.loads((HERE / "copy.json").read_text())[LANG]
NUM = "{:,}".format if LANG == "en" else (lambda v: f"{v:,}".replace(",", "."))

n = 0
marks = {}
ticks = []  # per-frame callbacks (caption and cursor easing)


def snap(pg):
    global n
    for f in ticks:
        f()
    pg.screenshot(path=str(FR / f"{n:05d}.jpg"), type="jpeg", quality=93)
    n += 1


def mark(name):
    marks[name] = round(n / FPS, 2)


def ease(x):
    x = max(0, min(1, x))
    return 4 * x * x * x if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def run(pg, sec, fn=None):
    k = max(1, round(sec * FPS))
    for i in range(k):
        if fn:
            fn(i / (k - 1) if k > 1 else 1)
        snap(pg)


OVERLAY = """
(()=>{
 const st=document.createElement('style');st.textContent=`
 #vcap{position:fixed;left:32px;bottom:30px;max-width:740px;background:#15140f;color:#f6f5f1;padding:16px 24px 18px;z-index:9999;
  border-radius:16px;box-shadow:0 14px 40px rgba(0,0,0,.22);opacity:0}
 #vcap .k{font:600 12px "DejaVu Sans Mono",monospace;letter-spacing:.2em;text-transform:uppercase;color:#f0885a;margin-bottom:6px}
 #vcap .t{font:700 25px/1.25 "Inter Display",Inter,sans-serif;letter-spacing:-.01em}
 #vcur{position:fixed;left:0;top:0;width:26px;height:26px;z-index:10000;pointer-events:none;opacity:0;transform-origin:3px 3px}
 #vfade{position:fixed;inset:0;background:#f6f5f1;z-index:10001;pointer-events:none;opacity:1}
 #vring{position:fixed;width:44px;height:44px;margin:-22px 0 0 -22px;border:3px solid #b43c0e;border-radius:50%;z-index:9998;pointer-events:none;opacity:0}
 #vbadge{position:fixed;right:28px;top:22px;z-index:9999;font:700 11px "DejaVu Sans Mono",monospace;letter-spacing:.18em;background:#b43c0e;color:#fff;padding:7px 13px;border-radius:999px;opacity:0}
 html{scroll-behavior:auto!important}.tabs{position:static!important}`;
 document.head.appendChild(st);
 const d=document.createElement('div');d.id='vcap';d.innerHTML='<div class="k"></div><div class="t"></div>';document.body.appendChild(d);
 const c=document.createElement('div');c.id='vcur';c.innerHTML='<svg viewBox="0 0 26 26" width="26" height="26"><path d="M3 2 L3 21 L8 16.5 L11.5 24 L15 22.4 L11.6 15 L18.5 15 Z" fill="#15140f" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/></svg>';document.body.appendChild(c);
 const r=document.createElement('div');r.id='vring';document.body.appendChild(r);
 const f=document.createElement('div');f.id='vfade';document.body.appendChild(f);
 const b=document.createElement('div');b.id='vbadge';b.textContent='LIVE · ridd1kulusc0d3r.github.io/LLmInjection';document.body.appendChild(b);
 window.__cap=(k,t,a)=>{const e=document.getElementById('vcap');if(k!==null){e.querySelector('.k').textContent=k;e.querySelector('.t').textContent=t}e.style.opacity=a;e.style.transform=`translateY(${(1-a)*14}px)`};
 window.__cur=(x,y,a,s)=>{const e=document.getElementById('vcur');e.style.opacity=a;e.style.transform=`translate(${x-3}px,${y-3}px) scale(${s||1})`};
 window.__ring=(x,y,p)=>{const e=document.getElementById('vring');e.style.left=x+'px';e.style.top=y+'px';e.style.opacity=p>0&&p<1?(1-p):0;e.style.transform=`scale(${.4+p*1.1})`};
 window.__fade=a=>document.getElementById('vfade').style.opacity=a;
 window.__badge=a=>document.getElementById('vbadge').style.opacity=a;
})();
"""


class Site:
    """A live Explorer page with caption, cursor and fade overlays that ease on every frame."""

    def __init__(s, pg):
        s.pg = pg
        s.cx, s.cy = VW * 0.62, VH * 0.55
        s.want, s.shown, s.alpha = None, None, 0.0  # caption: wanted text, shown text, opacity
        s.cur_want, s.cur_a, s.cur_scale = 0.0, 0.0, 1.0
        ticks.clear()
        ticks.append(s.tick)

    def js(s, code, arg=None):
        return s.pg.evaluate(code, arg)

    def tick(s):
        if s.shown != s.want:
            s.alpha -= 1 / (0.28 * FPS)
            if s.alpha <= 0:
                s.alpha, s.shown = 0.0, s.want
                if s.shown:
                    s.js("([k,t])=>__cap(k,t,0)", list(s.shown))
        elif s.shown:
            s.alpha = min(1.0, s.alpha + 1 / (0.35 * FPS))
        s.js("a=>__cap(null,null,a)", max(0.0, s.alpha) if s.shown else 0.0)
        step = 1 / (0.3 * FPS)
        s.cur_a = min(s.cur_want, s.cur_a + step) if s.cur_a < s.cur_want else max(s.cur_want, s.cur_a - step)
        s.js("([x,y,a,k])=>__cur(x,y,a,k)", [s.cx, s.cy, s.cur_a, s.cur_scale])

    def cap(s, i):
        s.want = tuple(i) if i else None

    def open(s, tab):
        s.pg.goto(f"{BASE}?lang={LANG}#tab={tab}")
        s.pg.wait_for_timeout(1800)
        s.js(OVERLAY)
        s.js("window.scrollTo(0,0)")
        s.pg.mouse.move(2, 2)
        s.pg.wait_for_timeout(300)

    def scroll_to(s, sec, y1, el=None):
        get = "e=>e?document.querySelector(e).scrollTop:scrollY"
        put = "([e,y])=>e?document.querySelector(e).scrollTop=y:scrollTo(0,y)"
        y0 = s.js(get, el)
        run(s.pg, sec, lambda p: s.js(put, [el, y0 + (y1 - y0) * ease(p)]))

    def move_to(s, sec, x1, y1):
        x0, y0 = s.cx, s.cy
        s.cur_want = 1.0

        def f(p):
            e = ease(p)
            s.cx = x0 + (x1 - x0) * e
            s.cy = y0 + (y1 - y0) * e - math.sin(math.pi * p) * 18
            s.pg.mouse.move(s.cx, s.cy)

        run(s.pg, sec, f)

    def move_el(s, sec, sel, dx=None):
        r = s.js("s=>{const r=document.querySelector(s).getBoundingClientRect();return [r.x,r.y,r.width,r.height]}", sel)
        s.move_to(sec, r[0] + (dx if dx is not None else min(40, r[2] / 2)), r[1] + r[3] / 2)

    def click_fx(s, sec=0.45, action=None):
        def f(p):
            if action and p > 0.15 and not f.done:
                action()
                f.done = True
            s.js("([x,y,p])=>__ring(x,y,p)", [s.cx, s.cy, p])
            s.cur_scale = 1 - 0.18 * math.sin(math.pi * min(1, p * 2))

        f.done = False
        run(s.pg, sec, f)
        s.cur_scale = 1.0
        s.js("__ring(0,0,0)")

    def hide_cursor(s):
        s.cur_want = 0.0
        s.pg.mouse.move(2, 2)

    def fade(s, sec, a0, a1):
        run(s.pg, sec, lambda p: s.js("a=>__fade(a)", a0 + (a1 - a0) * p))


def cards(pg, scene, sec, opt=None):
    ticks.clear()
    pg.goto((HERE / "cards.html").as_uri())
    pg.evaluate("c=>setup(c)", T["cards"])
    run(pg, sec, lambda p: pg.evaluate("([s,t,o])=>scene(s,t,o)", [scene, p * sec, opt or {}]))


with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": VW, "height": VH}, device_scale_factor=DSF, locale="pt-BR" if LANG == "pt" else "en-US")
    pg = ctx.new_page()

    # ---------- live numbers ----------
    pg.goto(f"{BASE}?lang={LANG}#tab=graph")
    pg.wait_for_timeout(2000)
    stats = pg.evaluate(
        "(()=>{const c={};state.graph.nodes.forEach(n=>c[n.type]=(c[n.type]||0)+1);"
        "return {...c,nodes:state.graph.nodes.length,edges:state.graph.edges.length,types:Object.keys(c).length}})()"
    )
    T["cards"]["stats"] = [[stats.get(k, 0), lab] for k, lab in T["cards"]["stat_keys"]]
    fmt = {k: NUM(v) for k, v in stats.items()}
    G = [[k, t.format(**fmt)] for k, t in T["graph"]]
    V = [[k, t.format(**fmt)] for k, t in T["cov"]]

    # ---------- 1. intro cards ----------
    mark("intro")
    cards(pg, "intro", 8.0)
    mark("stats")
    cards(pg, "stats", 4.6)
    mark("ch1")
    cards(pg, "chapter", 2.3, T["ch1"])

    # ---------- 2. intelligence graph ----------
    s = Site(pg)
    s.open("graph")
    s.js("()=>{const st=document.createElement('style');st.textContent='#graphSvg{height:640px!important}';document.head.appendChild(st);graphStart()}")
    pg.wait_for_timeout(300)
    gw = s.js("document.querySelector('.gwrap').getBoundingClientRect().top+scrollY-24")
    mark("graph")
    s.js("__badge(1)")
    s.fade(0.4, 1, 0)
    s.cap(G[0])
    s.scroll_to(2.0, gw)
    run(pg, 0.6)
    # pan across every column and back
    v0 = s.js("({...G.view})")
    full = s.js("({...G.full})")
    x_end = full["x"] + full["w"] - v0["w"] + 10
    run(pg, 4.4, lambda p: s.js("v=>setView(v,false)", {**v0, "x": v0["x"] + (x_end - v0["x"]) * ease(p)}))
    run(pg, 1.4, lambda p: s.js("v=>setView(v,false)", {**v0, "x": x_end + (v0["x"] - x_end) * ease(p)}))
    # select a campaign: the chain lights up and the selection card lists the reports behind it
    nid = s.js(
        "(()=>{const d={};state.graph.edges.forEach(e=>{d[e.source]=(d[e.source]||0)+1;d[e.target]=(d[e.target]||0)+1});"
        "return [...document.querySelectorAll('#graphSvg .node')].filter(n=>n.dataset.col==1&&+n.dataset.row<10)"
        ".sort((a,b)=>(d[b.dataset.nid]||0)-(d[a.dataset.nid]||0))[0].dataset.nid})()"
    )
    sel = f'#graphSvg .node[data-nid="{nid}"] text'
    mark("g_select")
    s.cap(G[1])
    s.move_el(1.2, sel, 30)
    s.click_fx(0.45, lambda: pg.mouse.click(s.cx, s.cy))
    s.hide_cursor()
    run(pg, 2.6)
    # focus on it
    s.scroll_to(0.9, 2000, "#graphSel")
    mark("g_focus")
    s.cap(G[2])
    s.move_el(0.9, "#graphSel [data-focus]")
    s.click_fx(0.45, lambda: s.js("document.querySelector('#graphSel [data-focus]').click()"))
    pg.wait_for_timeout(500)
    s.js(
        "()=>{const f=G.full,ar=graphAR(),w=(f.w+80)/0.7;setView({x:f.x-40,y:f.y-40,w,h:w/ar},false);"
        "document.querySelector('#graphSel').scrollTop=0}"
    )
    s.js(f"scrollTo(0,{gw})")
    s.hide_cursor()
    run(pg, 2.4)
    # open the full record
    s.scroll_to(0.8, 2000, "#graphSel")
    mark("g_open")
    s.cap(G[3])
    s.move_el(0.8, "#graphSel [data-open]")
    s.click_fx(0.45, lambda: s.js("document.querySelector('#graphSel [data-open]').click()"))
    s.hide_cursor()
    run(pg, 1.0)
    s.scroll_to(3.6, 520, ".drawer.open")
    run(pg, 0.6)
    s.cap(None)
    s.fade(0.45, 0, 1)

    # ---------- 3. coverage ----------
    mark("ch2")
    cards(pg, "chapter", 2.3, T["ch2"])
    s = Site(pg)
    s.open("coverage")
    s.js(
        "()=>{let w=document.querySelector('#coverageTable');"
        "while(w&&!['auto','scroll'].includes(getComputedStyle(w).overflowY))w=w.parentElement;"
        "(w||document.querySelector('#coverageTable')).id='covScroll'}"
    )
    cy = s.js("document.querySelector('#coverage').getBoundingClientRect().top+scrollY-28")
    mark("coverage")
    s.js("__badge(1)")
    s.fade(0.4, 1, 0)
    s.cap(V[0])
    s.scroll_to(2.0, cy)
    run(pg, 1.0)
    mark("c_heat")
    s.cap(V[1])
    deep = s.js("(()=>{const e=document.querySelector('#covScroll');return e.scrollHeight-e.clientHeight})()")
    s.scroll_to(4.6, deep, "#covScroll")
    s.scroll_to(1.2, 0, "#covScroll")
    mark("c_drill")
    s.cap(V[2])
    s.js("document.querySelectorAll('#coverageTable .exp')[1].id='vExp2'")
    s.move_el(1.0, "#vExp2")
    s.click_fx(0.45, lambda: s.js("document.querySelector('#vExp2').click()"))
    s.hide_cursor()
    s.scroll_to(2.6, 330, "#covScroll")
    run(pg, 0.6)
    s.scroll_to(0.9, 0, "#covScroll")
    mark("c_gaps")
    s.cap(V[3])
    s.move_el(0.9, "#covShow", None)
    s.click_fx(0.45, lambda: pg.select_option("#covShow", "noctl"))
    run(pg, 2.4)
    s.click_fx(0.45, lambda: pg.select_option("#covShow", "nobench"))
    run(pg, 1.8)
    mark("c_actors")
    s.cap(V[4])
    s.move_el(0.8, "#covView", None)
    s.click_fx(0.45, lambda: (pg.select_option("#covShow", ""), pg.select_option("#covView", "actors")))
    s.hide_cursor()
    s.scroll_to(3.0, cy + 330)
    run(pg, 0.5)
    s.cap(None)
    s.fade(0.45, 0, 1)

    # ---------- 4. outro ----------
    mark("outro")
    cards(pg, "outro", 5.2)
    mark("end")
    b.close()

print("frames", n, "=", round(n / FPS, 1), "s")
(OUT / f"timeline-{LANG}.json").write_text(json.dumps({"marks": marks, "stats": stats}, indent=1))
mp4 = OUT / f"llminjection-promo-{LANG}.mp4"
subprocess.run(
    ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(FR / "%05d.jpg"),
     "-vf", "scale=1920:1080:flags=lanczos,format=yuv420p", "-c:v", "libx264", "-preset", "slow", "-crf", "20",
     "-movflags", "+faststart", str(mp4)],
    check=True,
)
subprocess.run(
    ["ffmpeg", "-y", "-loglevel", "error", "-ss", str(marks["g_select"] + 2.6), "-i", str(mp4), "-frames:v", "1", "-q:v", "3",
     str(OUT / f"poster-{LANG}.jpg")],
    check=True,
)
print(mp4, mp4.stat().st_size // 1024, "KB", marks)
