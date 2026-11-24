// Render the HX-P screen UI as a transparent PNG at 2x: node render-overlay.mjs <out.png>
import puppeteer from "puppeteer-core";
import { pathToFileURL } from "node:url";
import path from "node:path";
const out = process.argv[2];
const browser = await puppeteer.launch({ executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe", headless: "new" });
const page = await browser.newPage();
await page.setViewport({ width: 625, height: 430, deviceScaleFactor: 2 });
await page.goto(pathToFileURL(path.join(import.meta.dirname, "overlay.html")).href, { waitUntil: "load" });
await page.evaluate(() => document.fonts.ready);
await page.screenshot({ path: out, omitBackground: true, clip: { x: 0, y: 0, width: 625, height: 430 } });
await browser.close();
