// Records the frames for the README GIFs: node scripts/record_tour.js <base-url> <out-dir> [tour|graph|filters]
// Needs Playwright (npm i playwright) and a built site:
//   python scripts/build_site.py --out _site && python -m http.server 8000 --directory _site
// Then: python scripts/make_tour_gif.py <out-dir> assets/explorer-<name>.gif
// Set CHROMIUM_PATH to use an already installed Chromium instead of Playwright's own.
const { chromium } = require("playwright");
const fs = require("fs");

const [base = "http://localhost:8000/", out = "tour-frames", name = "tour"] = process.argv.slice(2);
fs.mkdirSync(out, { recursive: true });

(async () => {
  const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined, args: ["--no-sandbox", "--disable-gpu"] });
  const page = await browser.newPage({ viewport: { width: 1200, height: 760 } });
  const steps = []; // [file, hold in ms], read by make_tour_gif.py
  let n = 0;
  const pause = (ms) => page.waitForTimeout(ms);
  const snap = async (hold) => {
    const file = `f${String(++n).padStart(2, "0")}.png`;
    await page.screenshot({ path: `${out}/${file}` });
    steps.push([file, hold]);
  };
  const scrollTo = async (y) => { await page.evaluate((v) => window.scrollTo(0, v), y); await pause(250); };
  const into = async (sel) => { await page.evaluate((s) => document.querySelector(s).scrollIntoView({ block: "start" }), sel); await page.evaluate(() => window.scrollBy(0, -90)); await pause(300); };
  const tab = async (t) => { await page.click(`.tab[data-tab="${t}"]`); await scrollTo(0); await pause(200); };
  const open = async (hash) => { await page.goto(`${base}#${hash}`); await page.waitForSelector(".tab"); await pause(800); };

  if (name === "tour") {
    await open("tab=overview&lang=en");
    await snap(2200);                                                     // hero and stat cards
    await into(".dash.three"); await snap(1900);                         // dashboard panels
    await into("#actors"); await snap(1700);                             // actors using AI
    await tab("landscape"); await snap(1400);
    await tab("graph"); await into(".gwrap"); await snap(1500);          // graph, readable first view
    await page.click('.node[data-nid="ACTOR-JADEPUFFER"]'); await pause(450); await snap(2200);   // pinned selection
    await tab("coverage"); await scrollTo(250);
    await page.click('.sortbtn[data-sort="priority"]'); await pause(300); await snap(1500);
    await page.click('.exp[data-t="LLMI-T013"]'); await pause(300);
    await page.evaluate(() => document.querySelector("#cd-LLMI-T013").scrollIntoView({ block: "center" })); await pause(300); await snap(2300);
    await page.selectOption("#covView", "actors"); await pause(300); await scrollTo(250); await snap(1800);
    await tab("timeline"); await snap(1400);
    await tab("ecosystem"); await snap(1300);
    await page.evaluate(() => { document.documentElement.dataset.theme = "dark"; }); await tab("overview"); await snap(1700);   // dark theme
    await page.evaluate(() => { document.documentElement.dataset.theme = "light"; });
    await open("tab=overview&lang=pt"); await page.reload(); await page.waitForSelector(".tab"); await pause(700);
    await snap(1800);                                                     // Portuguese interface
  } else if (name === "graph") {
    await open("tab=graph&lang=en"); await into(".gwrap"); await snap(1500);
    const node = page.locator('.node[data-nid="ACTOR-GTG-1002"]');
    await node.hover(); await pause(300); await snap(1100);              // hover traces
    await node.click(); await pause(450); await snap(1800);              // click pins the selection
    await page.click("#graphSel [data-go]"); await pause(500); await snap(1600);   // jump along a link
    const box = await page.locator("#graphSvg").boundingBox();
    for (const [dx, dy] of [[0, 0], [-120, -60], [-240, -120]]) {      // drag to pan
      await page.mouse.move(box.x + 600 + dx, box.y + 300 + dy);
      if (dx === 0) await page.mouse.down();
      await pause(60); await snap(450);
    }
    await page.mouse.up();
    await page.click('#graphTools [data-zoom="in"]'); await pause(400); await snap(900);
    await page.click('#graphTools [data-zoom="in"]'); await pause(400); await snap(1100);   // zoom in
    await page.click('#graphTypes [data-gtype="test-case"]'); await pause(300);
    await page.click('#graphTypes [data-gtype="detection"]'); await pause(400); await snap(1400);   // hide columns
    await page.click('#graphTools [data-zoom="all"]'); await pause(500); await snap(1800);    // whole graph
  } else if (name === "filters") {
    await open("tab=overview&lang=en"); await into(".dash.three"); await snap(1500);
    await page.hover('#dashConf [data-filter="confidence:high"]'); await pause(250); await snap(900);
    await page.click('#dashConf [data-filter="confidence:high"]'); await pause(500); await snap(1800);   // filter by a segment
    await into("#actors"); await snap(1500);                             // lists follow the filter
    await page.click('#filterChips [data-unset="confidence"]'); await pause(400);
    await into("#dashMaturity"); await snap(1200);
    await page.click('#dashMaturity [data-filter="maturity:observed-in-the-wild"]'); await pause(500); await scrollTo(250); await snap(1900);   // maturity bar opens coverage
    await tab("overview"); await into("#dashGrades");
    await page.click('#dashGrades [data-filter="grade:A"]'); await pause(500); await snap(1800);   // grade bar opens sources
  }
  fs.writeFileSync(`${out}/steps.json`, JSON.stringify(steps));
  await browser.close();
})();
