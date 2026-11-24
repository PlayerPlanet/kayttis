// Drives headless Chrome: loads index.html?shot=<name>, saves the canvas to ../renders/.
// Usage: node render.mjs [shot ...] | node render.mjs --probe | node render.mjs --video <name>
import puppeteer from 'puppeteer-core';
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { startServer } from './server.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const out = path.resolve(here, '..', 'renders');
const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';

const STILLS = ['hx01-hero', 'hx01-front', 'hx01-front-callouts', 'hx01-exploded', 'hx01-macro-led',
  'hxp-hero', 'hxp-front', 'hxp-knob-macro', 'family', 'hx01-cutout', 'hxp-cutout'];
const VIDEOS = { 'hx01-turntable': { frames: 180 }, 'hxp-reveal': { frames: 150 } };

const args = process.argv.slice(2);
const server = await startServer();
const port = server.address().port;
const browser = await puppeteer.launch({
  executablePath: CHROME, headless: true,
  args: ['--use-angle=d3d11', '--enable-gpu', '--ignore-gpu-blocklist', '--enable-unsafe-swiftshader',
    '--disable-gpu-sandbox', '--force-color-profile=srgb'],
  protocolTimeout: 600000,
});

async function openPage(shot) {
  const page = await browser.newPage();
  page.on('console', (m) => { const t = m.text(); if (!t.includes('THREE.WebGLProgram')) console.log('  [page]', t.slice(0, 300)); });
  page.on('pageerror', (e) => console.log('  [pageerror]', e.message));
  await page.goto(`http://127.0.0.1:${port}/renders-src/index.html?shot=${shot}`);
  await page.waitForFunction('window.__ready === true || window.__error', { timeout: 120000 });
  const err = await page.evaluate('window.__error');
  if (err) throw new Error(err);
  return page;
}

function save(file, dataUrl) {
  fs.writeFileSync(file, Buffer.from(dataUrl.split(',')[1], 'base64'));
}

try {
  if (args[0] === '--probe') {
    const page = await openPage('probe');
    console.log(await page.evaluate('window.__info'));
  } else if (args[0] === '--video') {
    for (const name of args.slice(1)) {
      const { frames } = VIDEOS[name];
      const dir = path.join(here, 'frames', name);
      fs.rmSync(dir, { recursive: true, force: true });
      fs.mkdirSync(dir, { recursive: true });
      const page = await openPage(name);
      const t0 = Date.now();
      for (let i = 0; i < frames; i++) {
        save(path.join(dir, `f${String(i).padStart(4, '0')}.png`), await page.evaluate(`window.renderFrame(${i}, ${frames})`));
        if (i % 30 === 0) console.log(`  ${name} frame ${i}/${frames} ${((Date.now() - t0) / 1000).toFixed(0)}s`);
      }
      await page.close();
      const mp4 = path.join(out, `${name}.mp4`);
      execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', '30', '-i', path.join(dir, 'f%04d.png'),
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'slow', '-movflags', '+faststart', mp4]);
      console.log('wrote', mp4);
    }
  } else {
    const shots = args.length ? args : STILLS;
    for (const shot of shots) {
      const t0 = Date.now();
      const page = await openPage(shot);
      const dataUrl = await page.evaluate('window.renderShot()');
      save(path.join(out, `${shot}.png`), dataUrl);
      await page.close();
      console.log(`wrote ${shot}.png ${((Date.now() - t0) / 1000).toFixed(1)}s`);
    }
  }
} finally {
  await browser.close();
  server.close();
}
