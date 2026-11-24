// HX-P screen UI drawn to a canvas (dark theme, brand/tokens.css values, Geist + Geist Mono).
import * as THREE from 'three';

const T = { bg: '#0a0c0e', surface: '#111418', surface2: '#181c21', ink: '#e8ecef', muted: '#8b959d',
  line: '#1f252b', amber: '#ff9a2e', amberInk: '#ffb46a', glow: 'rgba(255,154,46,0.18)' };

export const ROWS = [
  { name: 'Keittiön hana', on: true },
  { name: 'Liesi', on: true },
  { name: 'Olohuoneen valot', on: false },
  { name: 'Kahvinkeitin', on: false },
];

function rr(g, x, y, w, h, r) { g.beginPath(); g.roundRect(x, y, w, h, r); }

export function drawUI(W = 2048, H = 1284, { brightness = 1 } = {}) {
  const c = document.createElement('canvas'); c.width = W; c.height = H;
  const g = c.getContext('2d');
  const u = W / 1000; // layout unit
  g.fillStyle = T.bg; g.fillRect(0, 0, W, H);
  const pad = 56 * u;
  // header
  g.fillStyle = T.amber; g.shadowColor = T.amber; g.shadowBlur = 18 * u;
  g.beginPath(); g.arc(pad + 11 * u, 74 * u, 11 * u, 0, Math.PI * 2); g.fill(); g.shadowBlur = 0;
  g.fillStyle = T.ink; g.font = `600 ${52 * u}px "Geist"`; g.letterSpacing = `${-0.035 * 52 * u}px`; g.textBaseline = 'middle';
  g.fillText('2 PÄÄLLÄ', pad + 38 * u, 76 * u);
  g.font = `500 ${26 * u}px "Geist Mono"`; g.letterSpacing = `${0.08 * 26 * u}px`; g.fillStyle = T.muted; g.textAlign = 'right';
  g.fillText('13:56', W - pad, 76 * u); g.textAlign = 'left';
  g.font = `400 ${17 * u}px "Geist Mono"`; g.letterSpacing = `${0.08 * 17 * u}px`;
  g.fillText('ETEINEN · KAIKKI LAITTEET', pad, 128 * u);
  // rows
  const top = 160 * u, rowH = (H - top - 34 * u) / ROWS.length;
  ROWS.forEach((r, i) => {
    const y = top + i * rowH;
    g.fillStyle = T.line; g.fillRect(pad, y, W - 2 * pad, Math.max(2, 1.6 * u));
    const cy = y + rowH / 2;
    g.fillStyle = r.on ? T.ink : T.muted; g.font = `500 ${34 * u}px "Geist"`; g.letterSpacing = `${-0.02 * 34 * u}px`;
    g.fillText(r.name, pad, cy - 16 * u);
    g.fillStyle = T.muted; g.font = `400 ${18 * u}px "Geist Mono"`; g.letterSpacing = `${0.04 * 18 * u}px`;
    g.fillText('tarkistettu 12 s sitten', pad, cy + 26 * u);
    // chip
    const label = r.on ? 'PÄÄLLÄ' : 'POIS';
    g.font = `500 ${20 * u}px "Geist Mono"`; g.letterSpacing = `${0.08 * 20 * u}px`;
    const tw = g.measureText(label).width, cw = tw + 56 * u, ch = 46 * u, cx = W - pad - cw;
    rr(g, cx, cy - ch / 2, cw, ch, ch / 2);
    if (r.on) {
      g.fillStyle = T.glow; g.fill(); g.strokeStyle = 'rgba(255,154,46,0.6)'; g.lineWidth = 2 * u; g.stroke();
      g.fillStyle = T.amber; g.beginPath(); g.arc(cx + 22 * u, cy, 5 * u, 0, Math.PI * 2); g.fill();
      g.fillStyle = T.amberInk; g.fillText(label, cx + 36 * u, cy + 1 * u);
    } else {
      g.strokeStyle = '#2a3138'; g.lineWidth = 2 * u; g.stroke();
      g.fillStyle = T.muted; g.fillText(label, cx + 28 * u, cy + 1 * u);
    }
  });
  if (brightness < 1) { g.fillStyle = `rgba(0,0,0,${1 - brightness})`; g.fillRect(0, 0, W, H); }
  return c;
}

export function uiTexture(opts) {
  const t = new THREE.CanvasTexture(drawUI(2048, 1284, opts));
  t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 16; t.generateMipmaps = true; t.minFilter = THREE.LinearMipmapLinearFilter;
  return t;
}
