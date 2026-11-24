// HX-P Paneeli: 168 x 104 x 12 mm, corner radius 16 mm. Origin = centre, front = +z (back at z = -6).
import * as THREE from 'three';
import { roundedSlab, latheZ, stadiumShape } from './geom.js';
import { materials, AMBER, ADD } from './materials.js';
import { uiTexture } from './ui.js';
import { turnedMaps } from './textures.js';

export const HXP = {
  w: 168, h: 104, d: 12, r: 16, front: 6,
  screen: { x: -15, y: 0, w: 126, h: 79 },     // ~5.9" visible, 6" panel class
  knob: { x: 64, y: 0, d: 28, h: 10 },
};

function knurlBand(r, z0, z1, ridges = 120, depth = 0.32, sub = 6) {
  const pos = [], idx = [], uv = [];
  const n = ridges * sub;
  const rows = [z0, z0 + 0.25, z1 - 0.25, z1];
  rows.forEach((z, k) => {
    const edge = (k === 0 || k === 3) ? 0.55 : 1; // ridges fade out at the chamfers
    for (let i = 0; i <= n; i++) {
      const a = i / n * Math.PI * 2, ph = (i % sub) / sub;
      const tri = 1 - Math.abs(ph * 2 - 1);           // 0 at valley, 1 at crest
      const rr = r - depth + depth * Math.pow(tri, 0.7) * edge - (1 - edge) * 0.1;
      pos.push(Math.cos(a) * rr, Math.sin(a) * rr, z); uv.push(i / n * 40, z);
    }
  });
  for (let k = 0; k < rows.length - 1; k++) for (let i = 0; i < n; i++) {
    const a = k * (n + 1) + i, b = a + n + 1;
    idx.push(a, a + 1, b + 1, a, b + 1, b);
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2));
  g.setIndex(idx); g.computeVertexNormals();
  return g;
}

export function ringGlowMaterial(radius, width, intensity) {
  return new THREE.ShaderMaterial({
    uniforms: { c: { value: AMBER.clone().multiplyScalar(intensity) }, R: { value: radius }, W: { value: width } },
    vertexShader: 'varying vec2 p; void main(){ p = position.xy; gl_Position = projectionMatrix*modelViewMatrix*vec4(position,1.); }',
    fragmentShader: 'uniform vec3 c; uniform float R, W; varying vec2 p; void main(){ float d = abs(length(p)-R); float a = exp(-d*d/(W*W)); gl_FragColor = vec4(c*a, 1.); }',
    transparent: true, depthWrite: false, toneMapped: false, ...ADD,
  });
}

export function buildPanel({ screenOn = 1, ringOn = 1, uiBrightness = 1 } = {}) {
  const M = materials();
  const group = new THREE.Group(); group.name = 'HX-P';
  const anchors = {};
  const frame = new THREE.Mesh(roundedSlab(HXP.w, HXP.h, HXP.r, -6, 4.8, 1.8, { bevelSegments: 12, curveSegments: 48 }), M.aluminium);
  frame.castShadow = true; group.add(frame);
  const glass = new THREE.Mesh(roundedSlab(HXP.w - 3, HXP.h - 3, HXP.r - 1.5, 3.5, HXP.front, 0.6, { bevelSegments: 6, curveSegments: 48 }), M.glossGlass);
  group.add(glass);

  // display: emissive UI under the cover glass + reflection-only coating on top
  const S = HXP.screen;
  const screenMat = new THREE.MeshBasicMaterial({ map: uiTexture({ brightness: uiBrightness }), toneMapped: false });
  screenMat.color.setScalar(1.25 * screenOn);
  const screen = new THREE.Mesh(new THREE.PlaneGeometry(S.w, S.h), screenMat);
  screen.position.set(S.x, S.y, HXP.front + 0.004); group.add(screen);
  const coat = new THREE.Mesh(new THREE.PlaneGeometry(S.w, S.h), M.coating);
  coat.position.set(S.x, S.y, HXP.front + 0.01); group.add(coat);

  // knob (titanium), lathe body + knurled band + pointer groove
  const K = HXP.knob, R = K.d / 2, z0 = HXP.front, z1 = HXP.front + K.h;
  const knob = new THREE.Group(); knob.position.set(K.x, K.y, 0);
  const prof = [[12.3, z0 + 0.05], [12.3, z0 + 0.6], [13.0, z0 + 1.0], [13.75, z0 + 1.5], [13.62, z0 + 1.6], [13.62, z1 - 2.0],
    [13.75, z1 - 1.9], [14.0, z1 - 1.5], [13.95, z1 - 0.55], [13.55, z1 - 0.08], [13.2, z1]];
  const body = new THREE.Mesh(latheZ(prof, 192), M.titanium); body.castShadow = true; knob.add(body);
  const tm = turnedMaps();
  const capMat = new THREE.MeshPhysicalMaterial({ color: '#a4a9ae', metalness: 1, roughness: 0.3, roughnessMap: tm.roughness,
    anisotropy: 0.85, anisotropyMap: tm.anisotropy });
  const cap = new THREE.Mesh(new THREE.CircleGeometry(13.2, 128), capMat); cap.position.z = z1; knob.add(cap);
  const knurlMat = M.titanium.clone(); knurlMat.color.set('#868b90'); knurlMat.roughness = 0.34;
  const band = new THREE.Mesh(knurlBand(R, z0 + 1.6, z1 - 2.0), knurlMat); knob.add(band);
  const groove = new THREE.Mesh(new THREE.ShapeGeometry(stadiumShape(10.5, 2.6), 16), new THREE.MeshPhysicalMaterial({ color: '#08090a', roughness: 0.5, metalness: 0.3 }));
  groove.rotation.z = Math.PI / 2; groove.position.set(0, 5.6, z1 + 0.02); knob.add(groove);
  const grooveRim = new THREE.Mesh(new THREE.ShapeGeometry(stadiumShape(11.2, 3.3), 16), new THREE.MeshPhysicalMaterial({ color: '#c3c8cc', metalness: 1, roughness: 0.12 }));
  grooveRim.rotation.z = Math.PI / 2; grooveRim.position.set(0, 5.6, z1 + 0.01); knob.add(grooveRim);
  group.add(knob);
  anchors.knob = new THREE.Vector3(K.x, K.y, z1);

  // amber light ring around the knob base
  if (ringOn > 0) {
    const ring = new THREE.Mesh(new THREE.RingGeometry(14.55, 15.25, 192), M.led.clone());
    ring.material.color = AMBER.clone().multiplyScalar(5 * ringOn);
    ring.position.set(K.x, K.y, z0 + 0.03); group.add(ring);
    const glow = new THREE.Mesh(new THREE.PlaneGeometry(50, 50), ringGlowMaterial(14.9, 1.4, 0.6 * ringOn));
    glow.position.set(K.x, K.y, z0 + 0.05); group.add(glow);
    // knob underside catches the ring: a light hidden under the knob (no specular dot on the glass)
    const pl = new THREE.PointLight(AMBER, 40 * ringOn, 40, 2); pl.position.set(K.x, K.y, z0 + 0.8); group.add(pl);
  } else {
    const ring = new THREE.Mesh(new THREE.RingGeometry(14.55, 15.25, 192), M.darkMetal);
    ring.position.set(K.x, K.y, z0 + 0.03); group.add(ring);
  }
  return { group, anchors, screenMat };
}
