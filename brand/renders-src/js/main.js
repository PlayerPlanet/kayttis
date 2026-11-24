// Entry: index.html?shot=<name>. Exposes window.renderShot() / window.renderFrame(i, n).
import * as THREE from 'three';
import { sensorShots } from './shots-sensor.js';
import { panelShots } from './shots-panel.js';
import { familyShots } from './shots-family.js';

const shot = new URLSearchParams(location.search).get('shot');

async function main() {
  await Promise.all([document.fonts.load('500 20px "Geist"'), document.fonts.load('600 20px "Geist"'),
    document.fonts.load('400 20px "Geist Mono"'), document.fonts.load('500 20px "Geist Mono"')]);
  if (shot === 'probe') {
    const gl = new THREE.WebGLRenderer().getContext(); const ext = gl.getExtension('WEBGL_debug_renderer_info');
    window.__info = JSON.stringify({ renderer: gl.getParameter(ext.UNMASKED_RENDERER_WEBGL), samples: gl.getParameter(gl.MAX_SAMPLES) });
    window.__ready = true; return;
  }
  const all = { ...sensorShots, ...panelShots, ...familyShots };
  if (!all[shot]) throw new Error('unknown shot ' + shot);
  const r = await all[shot]();
  if (typeof r === 'function') window.renderShot = r;
  else { window.renderShot = r.still; window.renderFrame = r.frame; }
  window.__ready = true;
}
main().catch((e) => { window.__error = String(e.stack || e); });
