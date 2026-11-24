// Geometry helpers (mm).
import * as THREE from 'three';

// Explicit point list (no duplicate vertices: those make ExtrudeGeometry bevels kink).
export function roundedRectPoints(w, h, r, seg = 24) {
  const pts = [], cs = [[w / 2 - r, h / 2 - r, 0], [-w / 2 + r, h / 2 - r, 90], [-w / 2 + r, -h / 2 + r, 180], [w / 2 - r, -h / 2 + r, 270]];
  for (const [cx, cy, a0] of cs) for (let i = 0; i <= seg; i++) {
    const a = (a0 + 90 * i / seg) * Math.PI / 180; pts.push(new THREE.Vector2(cx + Math.cos(a) * r, cy + Math.sin(a) * r));
  }
  return pts.filter((p, i) => i === 0 || p.distanceTo(pts[i - 1]) > 1e-4);
}
export function roundedRectShape(w, h, r, seg = 64) { return new THREE.Shape(roundedRectPoints(w, h, r, seg)); }
export function roundedRectPath(w, h, r, seg = 64) { return new THREE.Path(roundedRectPoints(w, h, r, seg).reverse()); }

// Distance from origin to a rounded-rect boundary along direction angle a.
export function rrRadius(a, hw, hh, r) {
  const dx = Math.cos(a), dy = Math.sin(a);
  // ray march (cheap, exact enough for mesh generation)
  let lo = 0, hi = Math.hypot(hw, hh) + 1;
  for (let i = 0; i < 40; i++) {
    const m = (lo + hi) / 2, x = Math.abs(dx * m), y = Math.abs(dy * m);
    const qx = Math.max(x - (hw - r), 0), qy = Math.max(y - (hh - r), 0);
    const inside = x <= hw && y <= hh && Math.hypot(qx, qy) <= r;
    if (inside) lo = m; else hi = m;
  }
  return lo;
}

// Solid rounded slab with bevelled edges, centred, from z0 to z1.
export function roundedSlab(w, h, r, z0, z1, bevel, opts = {}) {
  const b = Math.min(bevel, (z1 - z0) / 2 - 0.01);
  const shape = roundedRectShape(w - 2 * b, h - 2 * b, Math.max(0.1, r - b));
  if (opts.hole) shape.holes.push(opts.hole);
  const g = new THREE.ExtrudeGeometry(shape, {
    depth: z1 - z0 - 2 * b, bevelEnabled: b > 0, bevelThickness: b, bevelSize: b,
    bevelSegments: opts.bevelSegments ?? 10, curveSegments: opts.curveSegments ?? 40,
  });
  g.translate(0, 0, z0 + b);
  return g;
}

// Convex "pillow" surface over a rounded rect: rings from centre to boundary.
// zFn(t, x, y) gives height; t = normalised radius in [0,1].
export function domeGeometry(hw, hh, r, zFn, { seg = 256, rings = 48, skirt = 0 } = {}) {
  const pos = [], uv = [], idx = [];
  const bound = [];
  for (let i = 0; i < seg; i++) bound.push(rrRadius(i / seg * Math.PI * 2, hw, hh, r));
  pos.push(0, 0, zFn(0, 0, 0)); uv.push(0.5, 0.5);
  for (let k = 1; k <= rings; k++) {
    const t = Math.pow(k / rings, 0.8);
    for (let i = 0; i < seg; i++) {
      const a = i / seg * Math.PI * 2, R = bound[i] * t;
      const x = Math.cos(a) * R, y = Math.sin(a) * R;
      pos.push(x, y, zFn(t, x, y)); uv.push(x / (2 * hw) + 0.5, y / (2 * hh) + 0.5);
    }
  }
  let total = rings;
  if (skirt > 0) {
    for (const [f, dz] of [[0.995, 0.12], [0.985, skirt]]) {
      for (let i = 0; i < seg; i++) {
        const a = i / seg * Math.PI * 2, R = bound[i] * f;
        pos.push(Math.cos(a) * R, Math.sin(a) * R, zFn(1, Math.cos(a) * R, Math.sin(a) * R) - dz); uv.push(0, 0);
      }
      total++;
    }
  }
  for (let i = 0; i < seg; i++) idx.push(0, 1 + i, 1 + (i + 1) % seg);
  for (let k = 1; k < total; k++) {
    const a0 = 1 + (k - 1) * seg, a1 = 1 + k * seg;
    for (let i = 0; i < seg; i++) {
      const j = (i + 1) % seg;
      idx.push(a0 + i, a1 + i, a1 + j, a0 + i, a1 + j, a0 + j);
    }
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
  g.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2));
  g.setIndex(idx); g.computeVertexNormals();
  return g;
}

// Lathe around z axis (LatheGeometry spins around y; rotate so the axis is +z).
export function latheZ(points, segments = 128) {
  const g = new THREE.LatheGeometry(points.map(([r, z]) => new THREE.Vector2(r, z)), segments);
  g.rotateX(Math.PI / 2);
  return g;
}

// Stadium (rounded slot) shape.
export function stadiumShape(len, wid) {
  const r = wid / 2, s = new THREE.Shape();
  s.moveTo(-len / 2 + r, -r); s.lineTo(len / 2 - r, -r); s.absarc(len / 2 - r, 0, r, -Math.PI / 2, Math.PI / 2);
  s.lineTo(-len / 2 + r, r); s.absarc(-len / 2 + r, 0, r, Math.PI / 2, Math.PI * 1.5);
  return s;
}
