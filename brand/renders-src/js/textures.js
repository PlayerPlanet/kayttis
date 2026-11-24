// Procedural textures: brushed-metal maps, radial glow, engraved text.
import * as THREE from 'three';

// Deterministic PRNG so every render of a shot is identical.
export function rng(seed = 1) {
  let s = seed >>> 0;
  return () => { s = (s + 0x6D2B79F5) >>> 0; let t = s; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
}

// Brushed aluminium: long streaks along +u. Returns { roughness, normal } textures.
export function brushedMaps(size = 1024, seed = 7) {
  const r = rng(seed);
  const h = new Float32Array(size * size);
  // each row = sum of long 1D streak noise; neighbouring rows are independent -> hairline brushing
  for (let y = 0; y < size; y++) {
    const base = (r() - 0.5) * 0.6;
    const a1 = r() * 6.28, a2 = r() * 6.28, f1 = 1 + Math.floor(r() * 3), f2 = 3 + Math.floor(r() * 6);
    for (let x = 0; x < size; x++) {
      const u = x / size * Math.PI * 2;
      h[y * size + x] = base + 0.25 * Math.sin(u * f1 + a1) + 0.12 * Math.sin(u * f2 + a2) + (r() - 0.5) * 0.08;
    }
  }
  // occasional deeper scratches
  for (let k = 0; k < size / 6; k++) {
    const y = Math.floor(r() * size), x0 = Math.floor(r() * size), len = Math.floor(size * (0.1 + r() * 0.5));
    for (let i = 0; i < len; i++) h[y * size + ((x0 + i) % size)] += 0.5;
  }
  const rough = new Uint8Array(size * size * 4), nrm = new Uint8Array(size * size * 4);
  for (let y = 0; y < size; y++) {
    for (let x = 0; x < size; x++) {
      const i = y * size + x, v = h[i];
      const g = Math.max(0, Math.min(255, 170 + v * 60));
      rough[i * 4] = rough[i * 4 + 1] = rough[i * 4 + 2] = g; rough[i * 4 + 3] = 255;
      const dy = h[((y + 1) % size) * size + x] - h[((y - 1 + size) % size) * size + x];
      const n = new THREE.Vector3(0, -dy * 0.5, 1).normalize();
      nrm[i * 4] = 128; nrm[i * 4 + 1] = (n.y * 0.5 + 0.5) * 255; nrm[i * 4 + 2] = (n.z * 0.5 + 0.5) * 255; nrm[i * 4 + 3] = 255;
    }
  }
  const mk = (data, srgb) => {
    const t = new THREE.DataTexture(data, size, size, THREE.RGBAFormat);
    t.wrapS = t.wrapT = THREE.RepeatWrapping; t.generateMipmaps = true;
    t.minFilter = THREE.LinearMipmapLinearFilter; t.magFilter = THREE.LinearFilter; t.anisotropy = 16;
    if (srgb) t.colorSpace = THREE.SRGBColorSpace;
    t.needsUpdate = true; return t;
  };
  return { roughness: mk(rough), normal: mk(nrm) };
}

// Soft radial falloff (white, alpha in luminance) for glows and fake light spill.
export function radialTexture(size = 256, power = 2.2) {
  const c = document.createElement('canvas'); c.width = c.height = size;
  const g = c.getContext('2d'), img = g.createImageData(size, size);
  for (let y = 0; y < size; y++) for (let x = 0; x < size; x++) {
    const d = Math.hypot(x - size / 2 + 0.5, y - size / 2 + 0.5) / (size / 2);
    const v = Math.pow(Math.max(0, 1 - d), power) * 255;
    const i = (y * size + x) * 4; img.data[i] = img.data[i + 1] = img.data[i + 2] = v; img.data[i + 3] = 255;
  }
  g.putImageData(img, 0, 0);
  const t = new THREE.CanvasTexture(c); return t;
}

// White text on transparent, used as an alpha map for laser-etched markings.
export function textTexture(text, { px = 128, font = '500 100px "Geist Mono"', spacing = 0.12 } = {}) {
  const c = document.createElement('canvas'); const g = c.getContext('2d');
  g.font = font; g.letterSpacing = `${spacing}em`;
  const w = Math.ceil(g.measureText(text).width + px * 0.4);
  c.width = w; c.height = px;
  g.font = font; g.letterSpacing = `${spacing}em`;
  g.fillStyle = '#fff'; g.textBaseline = 'middle'; g.textAlign = 'center';
  g.fillText(text, w / 2, px / 2 + px * 0.04);
  const t = new THREE.CanvasTexture(c); t.anisotropy = 16;
  return { texture: t, aspect: w / px };
}

// Turned (concentric) finish for a disc with planar UVs: anisotropy direction map (rg = dir, b = strength)
// plus a roughness map with fine lathe rings.
export function turnedMaps(size = 1024, rings = 140, seed = 5) {
  const r = rng(seed);
  const ringNoise = new Float32Array(rings * 4); for (let i = 0; i < ringNoise.length; i++) ringNoise[i] = r();
  const an = new Uint8Array(size * size * 4), ro = new Uint8Array(size * size * 4);
  for (let y = 0; y < size; y++) for (let x = 0; x < size; x++) {
    const dx = (x + 0.5) / size * 2 - 1, dy = (y + 0.5) / size * 2 - 1, d = Math.hypot(dx, dy) + 1e-6;
    const i = (y * size + x) * 4;
    an[i] = (-dy / d * 0.5 + 0.5) * 255; an[i + 1] = (dx / d * 0.5 + 0.5) * 255; an[i + 2] = 255; an[i + 3] = 255;
    const k = Math.min(ringNoise.length - 1, Math.floor(d * ringNoise.length));
    const v = 150 + (ringNoise[k] - 0.5) * 50 + Math.sin(d * rings * Math.PI * 2) * 8;
    ro[i] = ro[i + 1] = ro[i + 2] = v; ro[i + 3] = 255;
  }
  const mk = (data) => { const t = new THREE.DataTexture(data, size, size, THREE.RGBAFormat); t.generateMipmaps = true;
    t.minFilter = THREE.LinearMipmapLinearFilter; t.magFilter = THREE.LinearFilter; t.anisotropy = 8; t.needsUpdate = true; return t; };
  return { anisotropy: mk(an), roughness: mk(ro) };
}
