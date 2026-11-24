// Dev helper: screenshot the demo app with real Basic auth at a given viewport.
//   node shot-app.mjs <url> <out.png> <width> <height> [user] [pass]
import puppeteer from "puppeteer-core";

const [url, out, w = "390", h = "900", user = "demo", pass = "demo"] = process.argv.slice(2);
const browser = await puppeteer.launch({
  executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe",
  headless: "new",
});
const page = await browser.newPage();
await page.authenticate({ username: user, password: pass });
await page.setViewport({ width: Number(w), height: Number(h), deviceScaleFactor: 1 });
await page.goto(url, { waitUntil: "networkidle2" });
await new Promise((r) => setTimeout(r, 4000));
const info = await page.evaluate(() => ({
  scrollWidth: document.documentElement.scrollWidth,
  live: document.querySelector("#live-text")?.textContent,
  summary: document.querySelector("#summary")?.textContent,
}));
console.log(JSON.stringify(info));
await page.screenshot({ path: out, fullPage: false });
await browser.close();
