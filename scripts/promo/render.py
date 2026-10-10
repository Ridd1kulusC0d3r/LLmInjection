"""Render the LLMInjection marketing video frame by frame (Playwright + ffmpeg).

usage: python render.py en|pt  -> out/llminjection-promo-<lang>.mp4
The site must be served at BASE (python -m http.server 8765 -d _site).
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

n = 0


def snap(pg):
    global n
    pg.screenshot(path=str(FR / f"{n:05d}.jpg"), type="jpeg", quality=93)
    n += 1


def ease(x):
    x = max(0, min(1, x))
    return 4 * x * x * x if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def run(pg, sec, fn=None):
    k = max(1, round(sec * FPS))
    for i in range(k):
        if fn:
            fn(i / (k - 1) if k > 1 else 1, i / FPS)
        snap(pg)


OVERLAY = """
(()=>{
 const st=document.createElement('style');st.textContent=`
 #vcap{position:fixed;left:36px;bottom:34px;max-width:760px;background:#17150f;color:#f3f0e8;padding:18px 26px 20px;z-index:9999;
  border-left:6px solid #b43c0e;box-shadow:0 10px 30px rgba(0,0,0,.18);opacity:0;transition:none}
 #vcap .k{font:600 12px "DejaVu Sans Mono",monospace;letter-spacing:.22em;text-transform:uppercase;color:#e9b394;margin-bottom:6px}
 #vcap .t{font:700 27px/1.25 "Liberation Serif",Georgia,serif}
 #vcur{position:fixed;left:0;top:0;width:26px;height:26px;z-index:10000;pointer-events:none;opacity:0;transform-origin:3px 3px}
 #vfade{position:fixed;inset:0;background:#f3f0e8;z-index:10001;pointer-events:none;opacity:1}
 #vring{position:fixed;width:44px;height:44px;margin:-22px 0 0 -22px;border:3px solid #b43c0e;border-radius:50%;z-index:9998;pointer-events:none;opacity:0}
 #vbadge{position:fixed;right:30px;top:24px;z-index:9999;font:700 12px "DejaVu Sans Mono",monospace;letter-spacing:.2em;background:#b43c0e;color:#fff;padding:7px 12px;opacity:0}
 html{scroll-behavior:auto!important}`;
 document.head.appendChild(st);
 const d=document.createElement('div');d.id='vcap';d.innerHTML='<div class="k"></div><div class="t"></div>';document.body.appendChild(d);
 const c=document.createElement('div');c.id='vcur';c.innerHTML='<svg viewBox="0 0 26 26" width="26" height="26"><path d="M3 2 L3 21 L8 16.5 L11.5 24 L15 22.4 L11.6 15 L18.5 15 Z" fill="#17150f" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/></svg>';document.body.appendChild(c);
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
    """Helpers for a live Explorer page with caption, cursor and fade overlays."""

    def __init__(s, pg):
        s.pg = pg
        s.cx, s.cy = VW * 0.62, VH * 0.55
        s.cap_txt = None

    def js(s, code, arg=None):
        return s.pg.evaluate(code, arg)

    def open(s, tab, extra_css=""):
        s.pg.goto(f"{BASE}?lang={LANG}#tab={tab}")
        s.pg.wait_for_timeout(1800)
        s.js(OVERLAY)
        if extra_css:
            s.js("c=>{const st=document.createElement('style');st.textContent=c;document.head.appendChild(st)}", extra_css)
        s.js("window.scrollTo(0,0)")
        s.pg.mouse.move(2, 2)
        s.pg.wait_for_timeout(300)

    def cap(s, k, t, a):
        s.js("([k,t,a])=>__cap(k,t,a)", [k, t, a])

    def cur(s, a=1, sc=1):
        s.js("([x,y,a,s])=>__cur(x,y,a,s)", [s.cx, s.cy, a, sc])

    def scroll_to(s, sec, y1, during=None):
        y0 = s.js("scrollY")

        def f(p, t):
            s.js("y=>window.scrollTo(0,y)", y0 + (y1 - y0) * ease(p))
            if during:
                during(p, t)

        run(s.pg, sec, f)

    def move(s, sec, x1, y1, real=True, during=None):
        x0, y0 = s.cx, s.cy

        def f(p, t):
            e = ease(p)
            s.cx = x0 + (x1 - x0) * e
            s.cy = y0 + (y1 - y0) * e - math.sin(math.pi * p) * 18
            if real:
                s.pg.mouse.move(s.cx, s.cy)
            s.cur()
            if during:
                during(p, t)

        run(s.pg, sec, f)

    def click_fx(s, sec=0.45, during=None):
        def f(p, t):
            s.js("([x,y,p])=>__ring(x,y,p)", [s.cx, s.cy, p])
            s.cur(1, 1 - 0.18 * math.sin(math.pi * min(1, p * 2)))
            if during:
                during(p, t)

        run(s.pg, sec, f)
        s.js("__ring(0,0,0)")

    def fade(s, sec, a0, a1, during=None):
        def f(p, t):
            s.js("a=>__fade(a)", a0 + (a1 - a0) * p)
            if during:
                during(p, t)

        run(s.pg, sec, f)


def capfx(site, k, t, t_in, t_out, total):
    """returns a during() that fades a caption in at t_in and out at t_out (seconds within a block)."""

    def f(p, tt):
        sec = p * total
        a = min(1, max(0, (sec - t_in) / 0.4)) * (1 - min(1, max(0, (sec - t_out) / 0.4)))
        site.cap(k, t, a)

    return f


def rect(pg, sel):
    return pg.evaluate(
        "s=>{const e=document.querySelector(s);if(!e)return null;const r=e.getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height}}", sel
    )


with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": VW, "height": VH}, device_scale_factor=DSF, locale="pt-BR" if LANG == "pt" else "en-US")
    pg = ctx.new_page()

    # ---------- 1. intro cards ----------
    pg.goto((HERE / "cards.html").as_uri())
    pg.evaluate("c=>setup(c)", T["cards"])
    run(pg, 8.0, lambda p, t: pg.evaluate("t=>scene('intro',t)", t))
    run(pg, 4.6, lambda p, t: pg.evaluate("t=>scene('stats',t)", t))
    run(pg, 2.3, lambda p, t: pg.evaluate("([t,o])=>scene('chapter',t,o)", [t, T["ch1"]]))

    # ---------- 2. graph ----------
    s = Site(pg)
    s.open("graph", "#graphSvg{width:1900px!important;min-width:1900px!important}.gwrap{scrollbar-width:none}")
    gy = s.js("document.querySelector('#graph').getBoundingClientRect().top+scrollY-70")
    G = T["graph"]
    s.fade(0.4, 1, 0, lambda p, t: s.js("a=>__badge(a)", p))
    s.scroll_to(2.2, gy, capfx(s, G[0][0], G[0][1], 0.6, 99, 2.2))
    # cursor to first actor
    a = rect(pg, "#graphSvg .node[data-col='1'][data-row='6'] text")
    s.cur(0)
    s.move(1.3, a["x"] + 30, a["y"] + a["h"] / 2, during=lambda p, t: s.cap(None, None, 1))
    run(pg, 1.2, lambda p, t: s.cur())
    # lock trace with focus, then pan right across all columns
    actor = s.js("document.querySelector(\"#graphSvg .node[data-col='1'][data-row='6']\").dataset.nid")
    pg.mouse.move(2, 2)
    s.js("""()=>{const svg=document.querySelector('#graphSvg');svg.onmouseover=svg.onmouseout=null;
      window.__trace=id=>{const near=new Set([id]);svg.querySelectorAll('.edge').forEach(l=>{const hit=!!id&&(l.dataset.a===id||l.dataset.b===id);l.classList.toggle('on',hit);if(hit){near.add(l.dataset.a);near.add(l.dataset.b)}});
      svg.querySelectorAll('.node').forEach(g=>{g.classList.toggle('dim',!!id&&!near.has(g.dataset.nid));g.classList.toggle('on',g.dataset.nid===id)});}}""")
    s.js("id=>__trace(id)", actor)
    maxl = s.js("(()=>{const g=document.querySelector('.gwrap');return g.scrollWidth-g.clientWidth})()")
    cf0 = capfx(s, G[0][0], G[0][1], -1, 0.0, 6.5)
    cf1 = capfx(s, G[1][0], G[1][1], 0.5, 99, 6.5)

    def pan(p, t):
        s.js("x=>document.querySelector('.gwrap').scrollLeft=x", maxl * ease(p))
        r = rect(pg, f'#graphSvg .node[data-nid="{actor}"] text')
        s.cx = r["x"] + 30
        s.cur(max(0, 1 - p * 4))
        (cf0 if p * 6.5 < 0.4 else cf1)(p, t)

    run(pg, 6.5, pan)
    run(pg, 1.0, lambda p, t: s.cap(G[1][0], G[1][1], 1))
    # back to the technique column and open a technique
    s.js("__trace(null)")
    tech_col = s.js(
        "(()=>{const t=[...document.querySelectorAll('#graphSvg text.gcol')].findIndex(x=>/LLMI|T[eé]cnica|Technique/i.test(x.textContent));return t})()"
    )
    tech_col = tech_col if tech_col >= 0 else 4
    target = s.js(
        f"(()=>{{const g=document.querySelector('.gwrap');const n=document.querySelector(\"#graphSvg .node[data-col='{tech_col}'][data-row='1'] text\");const r=n.getBoundingClientRect(),gr=g.getBoundingClientRect();return Math.max(0,Math.min(g.scrollWidth-g.clientWidth,g.scrollLeft+r.x-gr.x-gr.width*0.4))}})()"
    )
    l0 = maxl
    run(pg, 1.6, lambda p, t: (s.js("x=>document.querySelector('.gwrap').scrollLeft=x", l0 + (target - l0) * ease(p)), s.cap(G[1][0], G[1][1], 1 - p)))
    tn = rect(pg, f"#graphSvg .node[data-col='{tech_col}'][data-row='1'] text")
    s.cx, s.cy = tn["x"] + 160, tn["y"] + 120
    s.move(1.2, tn["x"] + 40, tn["y"] + tn["h"] / 2, during=lambda p, t: s.cur(min(1, p * 3)))
    tid = s.js(f"document.querySelector(\"#graphSvg .node[data-col='{tech_col}'][data-row='1']\").dataset.nid")
    s.js("id=>__trace(id)", tid)
    run(pg, 1.5, lambda p, t: s.cap(G[2][0], G[2][1], min(1, p * 2.5)))
    pg.mouse.click(s.cx, s.cy)
    s.click_fx(0.5, lambda p, t: s.cap(G[2][0], G[2][1], 1))
    pg.mouse.move(2, 2)
    run(pg, 1.2, lambda p, t: (s.cur(1 - p), s.cap(G[2][0], G[2][1], 1)))

    def drawer_scroll(p, t):
        s.js("y=>{const d=document.querySelector('#drawer .body, #drawer .content, #drawer');if(d)d.scrollTop=y}", 380 * ease(p))
        s.cap(G[2][0], G[2][1], 1)

    run(pg, 3.4, drawer_scroll)
    s.fade(0.45, 0, 1, lambda p, t: s.cap(G[2][0], G[2][1], 1 - p))

    # ---------- 3. coverage ----------
    pg.goto((HERE / "cards.html").as_uri())
    pg.evaluate("c=>setup(c)", T["cards"])
    run(pg, 2.3, lambda p, t: pg.evaluate("([t,o])=>scene('chapter',t,o)", [t, T["ch2"]]))
    s = Site(pg)
    s.open("coverage")
    V = T["cov"]
    cy = s.js("document.querySelector('#coverage').getBoundingClientRect().top+scrollY-60")
    s.fade(0.4, 1, 0, lambda p, t: s.js("a=>__badge(a)", p))
    s.scroll_to(2.0, cy, capfx(s, V[0][0], V[0][1], 0.5, 99, 2.0))
    run(pg, 1.2, lambda p, t: s.cap(V[0][0], V[0][1], 1))
    tbl = s.js("document.querySelector('#coverageTable').getBoundingClientRect().top+scrollY-90")
    s.scroll_to(
        4.2,
        tbl + 900,
        capfx(s, V[1][0], V[1][1], 0.3, 99, 4.2)
        if False
        else (
            lambda p, t: s.cap(
                V[0][0] if p < 0.12 else V[1][0], V[0][1] if p < 0.12 else V[1][1], abs(1 - min(1, p / 0.12) * 2) if p < 0.12 else min(1, (p - 0.12) / 0.08)
            )
        ),
    )
    run(pg, 0.8, lambda p, t: s.cap(V[1][0], V[1][1], 1))
    # expand second technique
    s.scroll_to(1.6, tbl, lambda p, t: s.cap(V[1][0], V[1][1], 1 - p))
    ex = rect(pg, "#coverageTable .exp:nth-of-type(1)")
    exps = s.js("[...document.querySelectorAll('#coverageTable .exp')].length")
    ex = s.js(
        "(()=>{const e=document.querySelectorAll('#coverageTable .exp')[1];const r=e.getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height}})()"
    )
    s.cx, s.cy = ex["x"] + 300, ex["y"] + 160
    s.cur(0)
    s.move(1.1, ex["x"] + 40, ex["y"] + ex["h"] / 2, during=lambda p, t: (s.cur(min(1, p * 3)), s.cap(V[2][0], V[2][1], p)))
    pg.mouse.click(s.cx, s.cy)
    s.click_fx(0.5, lambda p, t: s.cap(V[2][0], V[2][1], 1))
    pg.mouse.move(2, 2)
    y0 = s.js("scrollY")
    s.scroll_to(3.0, y0 + 300, lambda p, t: (s.cur(max(0, 1 - p * 3)), s.cap(V[2][0], V[2][1], 1)))
    run(pg, 1.0, lambda p, t: s.cap(V[2][0], V[2][1], 1))
    # filter the gaps
    s.scroll_to(1.3, cy + 40, lambda p, t: s.cap(V[2][0], V[2][1], 1 - p))
    sel = rect(pg, "#covShow")
    s.cx, s.cy = sel["x"] + 380, sel["y"] + 140
    s.move(1.0, sel["x"] + sel["w"] - 30, sel["y"] + sel["h"] / 2, during=lambda p, t: (s.cur(min(1, p * 3)), s.cap(V[3][0], V[3][1], p)))
    s.click_fx(0.45, lambda p, t: s.cap(V[3][0], V[3][1], 1))
    pg.select_option("#covShow", "noctl")
    run(pg, 2.6, lambda p, t: s.cap(V[3][0], V[3][1], 1))
    pg.select_option("#covShow", "nobench")
    run(pg, 2.0, lambda p, t: s.cap(V[3][0], V[3][1], 1))
    # actors view
    vw = rect(pg, "#covView")
    s.move(
        0.9,
        vw["x"] + vw["w"] - 30,
        vw["y"] + vw["h"] / 2,
        during=lambda p, t: s.cap(V[3][0] if p < 0.5 else V[4][0], V[3][1] if p < 0.5 else V[4][1], abs(1 - 2 * p) if p < 1 else 1),
    )
    s.click_fx(0.45, lambda p, t: s.cap(V[4][0], V[4][1], 1))
    pg.select_option("#covShow", "")
    pg.select_option("#covView", "actors")
    pg.mouse.move(2, 2)
    y0 = s.js("scrollY")
    s.scroll_to(3.2, y0 + 360, lambda p, t: (s.cur(max(0, 1 - p * 3)), s.cap(V[4][0], V[4][1], 1)))
    s.fade(0.45, 0, 1, lambda p, t: s.cap(V[4][0], V[4][1], 1 - p))

    # ---------- 4. outro ----------
    pg.goto((HERE / "cards.html").as_uri())
    pg.evaluate("c=>setup(c)", T["cards"])
    run(pg, 5.0, lambda p, t: pg.evaluate("t=>scene('outro',t)", t))
    b.close()

print("frames", n, "=", round(n / FPS, 1), "s")
mp4 = OUT / f"llminjection-promo-{LANG}.mp4"
subprocess.run(
    [
        "ffmpeg",
        "-y",
        "-loglevel",
        "error",
        "-framerate",
        str(FPS),
        "-i",
        str(FR / "%05d.jpg"),
        "-vf",
        "scale=1920:1080:flags=lanczos,format=yuv420p",
        "-c:v",
        "libx264",
        "-preset",
        "slow",
        "-crf",
        "20",
        "-movflags",
        "+faststart",
        str(mp4),
    ],
    check=True,
)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "26", "-i", str(mp4), "-frames:v", "1", "-q:v", "3", str(OUT / f"poster-{LANG}.jpg")], check=True)
print(mp4, mp4.stat().st_size // 1024, "KB")
