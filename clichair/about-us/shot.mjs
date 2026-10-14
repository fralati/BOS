// Screenshots of the local preview (desktop 1280 and mobile 390) plus a few numeric checks.
// Usage: node shot.mjs [lang ...]   (default: en it de fr)
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
let pw; try { pw = require('playwright'); } catch { pw = require('/opt/node-tools/node_modules/playwright'); }
const { chromium } = pw;
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const langs = process.argv.slice(2).length ? process.argv.slice(2) : ['en', 'it', 'de', 'fr'];
fs.mkdirSync(path.join(here, 'shots'), { recursive: true });

const browser = await chromium.launch();
let failed = false;
for (const lang of langs) {
  const url = 'file://' + path.join(here, 'preview', `about-us.${lang}.html`);
  for (const [name, vp] of [['desktop', { width: 1280, height: 900 }], ['wide', { width: 1920, height: 1000 }], ['mobile', { width: 390, height: 844 }]]) {
    const ctx = await browser.newContext({ viewport: vp, deviceScaleFactor: 1 });
    const page = await ctx.newPage();
    const errors = [];
    page.on('pageerror', e => errors.push(String(e)));
    page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
    await page.goto(url);
    await page.waitForTimeout(200);
    const m = await page.evaluate(() => {
      const de = document.documentElement;
      const sections = [...document.querySelectorAll('.cca > section')].map(s => ({ id: s.id || 'hero', h: Math.round(s.getBoundingClientRect().height) }));
      const h1 = document.querySelector('.cca-h1');
      const facts = document.querySelector('.cca-facts');
      const pillars = [...document.querySelectorAll('.cca-pillar')].map(p => Math.round(p.getBoundingClientRect().height));
      return {
        scrollWidth: de.scrollWidth, clientWidth: de.clientWidth, pageHeight: de.scrollHeight,
        h1Size: getComputedStyle(h1).fontSize, h1Font: getComputedStyle(h1).fontFamily.split(',')[0],
        factsCols: getComputedStyle(facts).gridTemplateColumns.split(' ').length,
        pillars, sections,
        links: document.querySelectorAll('.cca a').length,
      };
    });
    const hscroll = m.scrollWidth > m.clientWidth;
    if (hscroll || errors.length) failed = true;
    console.log(`${lang} ${name}: width ${m.clientWidth}/${m.scrollWidth} ${hscroll ? 'HORIZONTAL SCROLL!' : 'ok'}; height ${m.pageHeight}px; h1 ${m.h1Size} ${m.h1Font}; facts cols ${m.factsCols}; pillars ${m.pillars.join('/')}; links ${m.links}; errors ${errors.length}`);
    if (errors.length) console.log('  ', errors);
    await page.screenshot({ path: path.join(here, 'shots', `${lang}-${name}.png`), fullPage: true });
    await ctx.close();
  }
}
await browser.close();
process.exit(failed ? 1 : 0);
