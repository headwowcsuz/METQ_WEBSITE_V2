// Render: HTML/SVG -> PNG / JPG / PDF (Chromium, Playwright)
const { chromium } = require('playwright');
const jobs = require(process.argv[2]);
const only = process.argv[3] ? new RegExp(process.argv[3]) : null;
(async () => {
  const b = await chromium.launch();
  const ctxs = {};
  for (const j of jobs) {
    if (only && !only.test(j.out)) continue;
    const key = `${j.vw || 800}x${j.vh || 600}@${j.dsf || 1}`;
    if (!ctxs[key]) ctxs[key] = await b.newContext({ viewport: { width: j.vw || 800, height: j.vh || 600 }, deviceScaleFactor: j.dsf || 1 });
    const p = await ctxs[key].newPage();
    await p.goto('file://' + j.html, { waitUntil: 'load' });
    if (j.kind === 'pdf') {
      const o = { path: j.out, printBackground: true, preferCSSPageSize: true };
      if (j.format) o.format = j.format; else { o.width = j.width; o.height = j.height; }
      await p.pdf(o);
    } else if (j.kind === 'png') {
      await p.screenshot({ path: j.out, omitBackground: !!j.transparent, clip: { x: 0, y: 0, width: j.vw, height: j.vh } });
    } else {
      await p.screenshot({ path: j.out, type: 'jpeg', quality: 90, clip: { x: 0, y: 0, width: j.vw, height: j.vh } });
    }
    await p.close();
    process.stdout.write('.');
  }
  await b.close(); console.log(' tayyor');
})();
