// HX-01 Anturi: 48 x 48 x 17 mm, corner radius 12 mm. Origin = body centre, front = +z, up = +y.
import * as THREE from 'three';
import { roundedSlab, roundedRectPath, domeGeometry, rrRadius, latheZ, stadiumShape } from './geom.js';
import { materials, glowMaterial, AMBER } from './materials.js';
import { radialTexture, textTexture, rng } from './textures.js';

export const HX01 = {
  size: 48, depth: 17, radius: 12,
  back: -8.5, lip: 7.2,                       // metal shell z-range
  glass: { hw: 19.3, r: 7.3, edge: 6.0, rise: 2.5 },
  lens: { x: 0, y: -4, d: 9 },
  led: { x: 15, y: 15, d: 3 },
};
const G = HX01.glass;
// separable superellipse pillow: smooth everywhere (no diagonal creases)
export const domeZ = (t, x, y) => {
  const f = (v) => 1 - Math.pow(Math.min(1, Math.abs(v) / (G.hw + 0.4)), 2.6);
  return G.edge + G.rise * Math.max(0, f(x) * f(y));
};
export function glassZ(x, y) {
  return domeZ(0, x, y);
}
function glassNormal(x, y) {
  const e = 0.05, dzdx = (glassZ(x + e, y) - glassZ(x - e, y)) / (2 * e), dzdy = (glassZ(x, y + e) - glassZ(x, y - e)) / (2 * e);
  return new THREE.Vector3(-dzdx, -dzdy, 1).normalize();
}
function onGlass(obj, x, y, lift = 0) {
  const n = glassNormal(x, y);
  obj.position.set(x, y, glassZ(x, y)).addScaledVector(n, lift);
  obj.quaternion.setFromUnitVectors(new THREE.Vector3(0, 0, 1), n);
  return obj;
}

// Returns { group, parts, anchors } ; parts are separately movable for the exploded view.
export function buildSensor({ ledOn = true, ledLight = true } = {}) {
  const M = materials();
  const group = new THREE.Group(); group.name = 'HX-01';
  const parts = {};
  const anchors = {};

  // --- rear shell (tray) + back plate + magnet ---
  const shell = new THREE.Group(); parts.shell = shell;
  const tube = new THREE.Mesh(roundedSlab(48, 48, 12, HX01.back, HX01.lip, 1.4, { hole: roundedRectPath(41.2, 41.2, 8.6), bevelSegments: 24 }), M.aluminium);
  const plate = new THREE.Mesh(roundedSlab(42.5, 42.5, 9.2, HX01.back + 0.25, -6.4, 0.4), M.darkMetal);
  shell.add(tube, plate);
  // USB-C port on the bottom face (y = -24), centred
  const zc = (HX01.back + HX01.lip) / 2 - 0.4;
  const port = new THREE.Mesh(new THREE.ShapeGeometry(stadiumShape(8.9, 3.2), 24), M.black);
  port.rotation.x = Math.PI / 2; port.position.set(0, -24.02, zc); shell.add(port);
  const portRim = new THREE.Mesh(new THREE.ShapeGeometry(stadiumShape(9.5, 3.8), 24), M.darkMetal);
  portRim.rotation.x = Math.PI / 2; portRim.position.set(0, -24.01, zc); shell.add(portRim);
  const tongue = new THREE.Mesh(new THREE.PlaneGeometry(6.6, 0.7), M.darkMetal);
  tongue.rotation.x = Math.PI / 2; tongue.position.set(0, -24.03, zc); shell.add(tongue);
  // laser-etched HX-01 on the bottom face, right of the port
  const { texture, aspect } = textTexture('HX-01');
  const etch = new THREE.Mesh(new THREE.PlaneGeometry(1.5 * aspect, 1.5), new THREE.MeshPhysicalMaterial({
    color: '#9aa1a8', roughness: 0.7, metalness: 0.6, alphaMap: texture, transparent: true, depthWrite: false }));
  etch.rotation.x = Math.PI / 2; etch.position.set(9.2, -24.03, zc); shell.add(etch);
  anchors.engraving = new THREE.Vector3(9.2, -24, zc);
  anchors.usb = new THREE.Vector3(0, -24, zc);

  const magnet = new THREE.Mesh(latheZ([[0, 0], [9.6, 0], [10, 0.4], [10, 1.6], [9.6, 2], [0, 2]], 96), M.nickel);
  magnet.position.z = -6.4; parts.magnet = magnet;

  // --- front glass (frosted black, slightly convex) with light pipe ---
  const glass = new THREE.Group(); parts.glass = glass;
  const dome = new THREE.Mesh(domeGeometry(G.hw, G.hw, G.r, domeZ, { skirt: 2.5 }), M.frosted);
  glass.add(dome);
  const L = HX01.led;
  const glowTex = radialTexture(256, 2.0), coreTex = radialTexture(128, 1.1);
  const ledCore = onGlass(new THREE.Mesh(new THREE.CircleGeometry(L.d / 2, 48), ledOn ? glowMaterial(coreTex, 14) : M.black), L.x, L.y, 0.02);
  glass.add(ledCore);
  if (ledOn) {
    const halo = onGlass(new THREE.Mesh(new THREE.PlaneGeometry(14, 14), glowMaterial(glowTex, 0.55)), L.x, L.y, 0.04);
    glass.add(halo);
    if (ledLight) {
      const pl = new THREE.PointLight(AMBER, 60, 30, 2);
      onGlass(pl, L.x, L.y, 1.2); glass.add(pl);
    }
  } else {
    const ring = onGlass(new THREE.Mesh(new THREE.RingGeometry(1.2, 1.5, 48), M.darkMetal), L.x, L.y, 0.02); glass.add(ring);
  }
  anchors.led = new THREE.Vector3(L.x, L.y, glassZ(L.x, L.y));
  anchors.glass = new THREE.Vector3(-12, 10, glassZ(-12, 10));

  // --- lens: titanium ring, aperture, black glass element ---
  const lens = new THREE.Group(); parts.lens = lens;
  const lr = HX01.lens.d / 2;
  lens.add(new THREE.Mesh(latheZ([[lr - 0.95, -0.2], [lr - 0.95, 0.5], [lr - 0.8, 0.68], [lr - 0.15, 0.68], [lr, 0.5], [lr, -0.6]], 128), M.titanium));
  lens.add(new THREE.Mesh(new THREE.CircleGeometry(lr - 0.95, 64), M.black));
  const ap = new THREE.Mesh(latheZ([[lr - 0.95, 0.05], [2.9, 0.15], [2.6, 0.25], [2.1, 0.32], [1.9, 0.3]], 96), M.darkMetal);
  lens.add(ap);
  const elem = new THREE.Mesh(new THREE.SphereGeometry(5, 64, 16, 0, Math.PI * 2, 0, Math.asin(2.05 / 5)), M.glossGlass);
  elem.rotation.x = Math.PI / 2; elem.position.z = 0.32 - 5 * Math.cos(Math.asin(2.05 / 5)); lens.add(elem);
  const cover = new THREE.Mesh(new THREE.CircleGeometry(lr - 0.95, 64), M.coating);
  cover.position.z = 0.62; lens.add(cover);
  onGlass(lens, HX01.lens.x, HX01.lens.y, -0.12);
  anchors.lens = new THREE.Vector3(HX01.lens.x + lr, HX01.lens.y, glassZ(0, -4));

  // --- internals: ESP32-CAM class board (27 x 40.5), camera module, battery ---
  const board = new THREE.Group(); parts.board = board;
  const pcb = new THREE.Mesh(roundedSlab(27, 40.5, 1.2, -1.0, 0, 0.15, { bevelSegments: 2, curveSegments: 6 }), M.pcb);
  board.add(pcb);
  const can = new THREE.Mesh(roundedSlab(16, 12.5, 0.6, 0, 2.4, 0.2, { bevelSegments: 2, curveSegments: 6 }), M.shield);
  can.position.y = 11; board.add(can);
  const ant = new THREE.Mesh(new THREE.BoxGeometry(16, 4.5, 0.6), M.black); ant.position.set(0, 18.4, 0.3); board.add(ant);
  // camera module on a short ribbon
  const cam = new THREE.Group();
  cam.add(new THREE.Mesh(roundedSlab(8.5, 8.5, 0.6, 0, 1.6, 0.2, { bevelSegments: 2, curveSegments: 6 }), M.black));
  cam.add(new THREE.Mesh(latheZ([[0, 5.4], [2.6, 5.4], [3.0, 5.0], [3.0, 1.6]], 64), M.darkMetal));
  cam.add(new THREE.Mesh(new THREE.CircleGeometry(1.4, 48), M.glossGlass).translateZ(5.42));
  cam.position.set(HX01.lens.x, HX01.lens.y, 0.4); board.add(cam);
  const ribbon = new THREE.Mesh(new THREE.BoxGeometry(6.5, 7, 0.15), new THREE.MeshPhysicalMaterial({ color: '#1a1714', roughness: 0.35, clearcoat: 0.8 }));
  ribbon.position.set(0, -11.5, 0.45); board.add(ribbon);
  const conn = new THREE.Mesh(new THREE.BoxGeometry(9, 2.6, 1.2), M.black); conn.position.set(0, -15.6, 0.6); board.add(conn);
  const r = rng(3);
  for (let i = 0; i < 26; i++) {
    const w = 0.6 + r() * 2.2, h = 0.4 + r() * 1.6, x = (r() - 0.5) * 22, y = -19 + r() * 22;
    if (Math.abs(x) < 6 && y > -17 && y < 1) continue;
    const c = new THREE.Mesh(new THREE.BoxGeometry(w, h, 0.35 + r() * 0.6), r() > 0.5 ? M.shield : M.black);
    c.position.set(x, y, 0.3); board.add(c);
  }
  board.position.z = -0.4;
  anchors.board = new THREE.Vector3(-8, 10, 2.0);
  anchors.camera = new THREE.Vector3(0, -4, 5.8);

  const battery = new THREE.Group(); parts.battery = battery;
  battery.add(new THREE.Mesh(roundedSlab(36, 32, 3, -6.0, -1.7, 1.2, { bevelSegments: 6, curveSegments: 16 }), M.pouch));
  const tab = new THREE.Mesh(new THREE.BoxGeometry(8, 3, 0.4), M.nickel); tab.position.set(0, 17, -3.8); battery.add(tab);
  anchors.battery = new THREE.Vector3(14, -8, -1.7);
  anchors.magnet = new THREE.Vector3(7, -7, -4.4);

  group.add(shell, magnet, battery, board, lens, glass);
  return { group, parts, anchors };
}

// Exploded offsets along +z (front) / -z (back), in mm.
export const EXPLODE = { glass: 78, lens: 56, board: 30, battery: 6, magnet: -14, shell: -34 };
export function explode(parts, e) {
  for (const k in EXPLODE) {
    const p = parts[k];
    if (!p.userData.base) p.userData.base = p.position.clone();
    p.position.copy(p.userData.base); p.position.z += EXPLODE[k] * e;
  }
}
