// Hairline callouts drawn over the final 2D image (Geist Mono, uppercase, +0.08em).
import * as THREE from 'three';

export const INK = 'rgba(201,206,211,0.92)', LINE = 'rgba(201,206,211,0.55)';

export function projector(camera, width, height) {
  return (v) => { const p = v.clone().project(camera); return [(p.x * 0.5 + 0.5) * width, (-p.y * 0.5 + 0.5) * height]; };
}

export function style(g, s) {
  g.strokeStyle = LINE; g.fillStyle = INK; g.lineWidth = 1.5 * s; g.lineCap = 'butt';
  g.font = `500 ${24 * s}px "Geist Mono"`; g.letterSpacing = `${0.08 * 24 * s}px`; g.textBaseline = 'middle';
}

export function dot(g, [x, y], s) {
  g.save(); g.fillStyle = INK; g.beginPath(); g.arc(x, y, 3.5 * s, 0, Math.PI * 2); g.fill();
  g.strokeStyle = LINE; g.beginPath(); g.arc(x, y, 9 * s, 0, Math.PI * 2); g.stroke(); g.restore();
}

// Leader: anchor -> elbow -> horizontal run -> label.
export function leader(g, a, elbow, endX, label, s, { side = 'right', sub = null } = {}) {
  dot(g, a, s);
  g.beginPath(); g.moveTo(a[0], a[1]); g.lineTo(elbow[0], elbow[1]); g.lineTo(endX, elbow[1]); g.stroke();
  const pad = 16 * s;
  g.textAlign = side === 'right' ? 'left' : 'right';
  const tx = side === 'right' ? endX + pad : endX - pad;
  g.fillText(label, tx, elbow[1]);
  if (sub) { g.save(); g.fillStyle = 'rgba(139,149,157,0.9)'; g.font = `400 ${18 * s}px "Geist Mono"`; g.fillText(sub, tx, elbow[1] + 30 * s); g.restore(); }
}

// Dimension line between two screen points with ticks and a centred label above.
export function dimension(g, p0, p1, label, s, ext = null) {
  if (ext) { g.beginPath(); g.moveTo(ext[0][0], ext[0][1]); g.lineTo(p0[0], p0[1] - 10 * s); g.moveTo(ext[1][0], ext[1][1]); g.lineTo(p1[0], p1[1] - 10 * s); g.stroke(); }
  g.beginPath(); g.moveTo(p0[0], p0[1]); g.lineTo(p1[0], p1[1]); g.stroke();
  for (const p of [p0, p1]) { g.beginPath(); g.moveTo(p[0], p[1] - 10 * s); g.lineTo(p[0], p[1] + 10 * s); g.stroke(); }
  g.textAlign = 'center'; g.fillText(label, (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2 - 26 * s);
}

export function worldAnchor(obj, local) { obj.updateWorldMatrix(true, false); return local.clone().applyMatrix4(obj.matrixWorld); }
export { THREE };
