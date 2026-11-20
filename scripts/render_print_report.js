// Render the print edition: cover + body + back cover into one PDF, with a two-pass table of contents.
//   node scripts/render_print_report.js dist/print out.pdf [--dossier reports/dossiers/artex.md]
// Needs Playwright with Chromium, pdftotext and pdfunite (poppler-utils).
const {chromium} = require('playwright');
const {execFileSync} = require('child_process');
const fs = require('fs'), path = require('path');

const dir = path.resolve(process.argv[2] || 'dist/print');
const out = path.resolve(process.argv[3] || path.join(dir, 'report.pdf'));
const extra = process.argv.slice(4);  // e.g. --dossier reports/dossiers/artex.md
const root = path.resolve(__dirname, '..');
const footer = `<div style="font:7px 'JetBrains Mono',monospace;width:100%;padding:0 16mm;display:flex;justify-content:space-between;color:#77736a">
<span>LLMInjection · Ameaças a sistemas de IA · 2026</span><span>TLP:CLEAR · <span class="pageNumber"></span></span></div>`;

async function pdf(page, file, dest, opts) {
  await page.goto('file://' + file, {waitUntil: 'load'});
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({path: dest, format: 'A4', printBackground: true, ...opts});
}

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  const bodyOpts = {margin: {top: '16mm', bottom: '18mm', left: '16mm', right: '16mm'}, displayHeaderFooter: true,
    headerTemplate: '<span></span>', footerTemplate: footer};
  // pass 1: find the page of each section marker
  await pdf(p, path.join(dir, 'body.html'), path.join(dir, 'body.pdf'), bodyOpts);
  const keys = JSON.parse(fs.readFileSync(path.join(dir, 'toc-keys.json'), 'utf8'));
  const n = parseInt(execFileSync('pdfinfo', [path.join(dir, 'body.pdf')]).toString().match(/Pages:\s+(\d+)/)[1], 10);
  const toc = {};
  for (let i = 1; i <= n; i++) {
    const t = execFileSync('pdftotext', ['-f', String(i), '-l', String(i), path.join(dir, 'body.pdf'), '-']).toString();
    for (const k of keys) if (!toc[k] && t.includes(`@@${k}@@`)) toc[k] = i;
  }
  fs.writeFileSync(path.join(dir, 'toc.json'), JSON.stringify(toc));
  // pass 2: rebuild the body with page numbers, then render everything
  execFileSync('python3', [path.join(root, 'scripts', 'build_print_report.py'), '--out', dir, '--toc', path.join(dir, 'toc.json'), ...extra]);
  await pdf(p, path.join(dir, 'body.html'), path.join(dir, 'body.pdf'), bodyOpts);
  await pdf(p, path.join(dir, 'cover.html'), path.join(dir, 'cover.pdf'), {margin: {top: 0, bottom: 0, left: 0, right: 0}});
  await pdf(p, path.join(dir, 'back.html'), path.join(dir, 'back.pdf'), {margin: {top: 0, bottom: 0, left: 0, right: 0}});
  await b.close();
  execFileSync('pdfunite', [path.join(dir, 'cover.pdf'), path.join(dir, 'body.pdf'), path.join(dir, 'back.pdf'), out]);
  console.log(out, JSON.stringify(toc));
})();
