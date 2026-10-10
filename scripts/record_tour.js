// Records the frames for assets/explorer-tour.gif: node scripts/record_tour.js <base-url> <out-dir>
// Needs Playwright (npm i playwright) and a built site:
//   python scripts/build_site.py --out _site && python -m http.server 8000 --directory _site
// Then: python scripts/make_tour_gif.py <out-dir> assets/explorer-tour.gif
// Set CHROMIUM_PATH to use an already installed Chromium instead of Playwright's own.
const { chromium } = require("playwright");
const fs = require("fs");

const [base = "http://localhost:8000/", out = "tour-frames"] = process.argv.slice(2);
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
  const tab = async (name) => { await page.click(`.tab[data-tab="${name}"]`); await scrollTo(0); await pause(150); };

  await page.goto(`${base}#tab=overview&lang=en`);
  await page.waitForSelector(".tab");
  await pause(700);
  await snap(2200);                                   // overview
  await scrollTo(380); await snap(900);
  await scrollTo(900); await snap(1800);              // dashboard, lower half
  await tab("landscape"); await snap(1500);
  await tab("graph"); await snap(1700);
  await tab("coverage"); await scrollTo(250); await snap(1400);
  await page.click('.sortbtn[data-sort="priority"]'); await pause(300); await snap(1600);   // sorted by priority
  await page.click('.exp[data-t="LLMI-T013"]'); await pause(300);                                         // drill-down on a technique that has a rule file
  await page.evaluate(() => document.querySelector("#cd-LLMI-T013").scrollIntoView({ block: "center" })); await pause(300); await snap(2600);
  await page.selectOption("#covView", "actors"); await pause(300); await scrollTo(250); await snap(2000); // actors x techniques
  await tab("ecosystem"); await snap(1500);
  await page.goto(`${base}#tab=overview&lang=pt`);
  await page.reload();
  await page.waitForSelector(".tab");
  await pause(700);
  await snap(2000);                                   // Portuguese interface
  fs.writeFileSync(`${out}/steps.json`, JSON.stringify(steps));
  await browser.close();
})();
