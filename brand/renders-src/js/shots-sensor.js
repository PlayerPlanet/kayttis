// HX-01 shots.
import * as THREE from 'three';
import { createStudio, capture } from './studio.js';
import { buildFloor, buildContactShadow } from './floor.js';
import { areaLight, dir } from './lights.js';
import { buildSensor, explode, EXPLODE, HX01, glassZ } from './sensor.js';
import { projector, style, leader, dimension, worldAnchor, dot } from './overlay.js';

export function placeCamera(cam, { az, el, dist, target, fov }) {
  if (fov) cam.fov = fov;
  cam.position.copy(dir(az, el).multiplyScalar(dist).add(target)); cam.lookAt(target); cam.updateProjectionMatrix();
}

// Standard studio around a sensor standing on its bottom edge.
export function sensorStudio(opts) {
  const st = createStudio(opts);
  const { scene } = st;
  const S = buildSensor({ ledOn: opts.ledOn ?? true });
  S.group.position.y = opts.lift ?? 24.08; S.group.rotation.y = opts.yaw ?? -0.42;
  scene.add(S.group);
  let floor = null, shadow = null;
  if (!opts.alpha) {
    floor = buildFloor({ poolCenter: [0, -30], poolRadius: 170, strength: 0.14, ...(opts.floor || {}) });
    scene.add(floor);
    shadow = buildContactShadow({ width: 140, height: 140, camHeight: 30, darkness: 1.6, opacity: 0.9, blur: 2.2 });
    scene.add(shadow.group);
  }
  const T = new THREE.Vector3(0, opts.lift ?? 24, 0);
  const k = opts.lights || {};
  areaLight(scene, { az: -50, el: 42, dist: 500, w: 260, h: 180, intensity: k.key ?? 10, target: T });
  areaLight(scene, { az: 140, el: 15, dist: 450, w: 30, h: 340, intensity: k.rim ?? 14, target: T });
  areaLight(scene, { az: -150, el: 20, dist: 450, w: 24, h: 300, intensity: k.rim2 ?? 6, target: T });
  st.render = (cfg = {}) => {
    if (shadow) shadow.update(st.renderer, scene, [floor]);
    return capture(st, cfg);
  };
  return { st, S, T, floor, shadow };
}

export const sensorShots = {
  'hx01-hero': () => {
    const { st, T } = sensorStudio({ width: 2400, height: 1600, yaw: -0.5 });
    placeCamera(st.camera, { az: 22, el: 12, dist: 285, target: T.clone().add(new THREE.Vector3(0, 1, 0)), fov: 20 });
    return () => st.render();
  },
  'hx01-front': () => frontShot(false),
  'hx01-front-callouts': () => frontShot(true),
  'hx01-exploded': () => {
    const { st, S, T } = sensorStudio({ width: 2400, height: 1600, yaw: 0, lift: 44, lights: { key: 16 }, floor: { strength: 0.08, poolCenter: [0, 0] } });
    explode(S.parts, 1);
    placeCamera(st.camera, { az: 58, el: 16, dist: 470, target: T.clone().add(new THREE.Vector3(0, -2, 0)), fov: 20 });
    const s = 1, A = S.anchors, E = EXPLODE;
    const z = (v, k) => v.clone().add(new THREE.Vector3(0, 0, E[k]));
    const items = [
      [z(new THREE.Vector3(-6, 14, glassZ(-6, 14)), 'glass'), 'ETULASI'],
      [z(A.lens, 'lens').add(new THREE.Vector3(0, 4.5 - 0, 0)).setX(0), 'KAMERA'],
      [z(new THREE.Vector3(-4, 18.5, 1.6), 'board'), 'ESP32-MODUULI'],
      [z(new THREE.Vector3(0, 15.5, -1.7), 'battery'), 'AKKU'],
      [z(new THREE.Vector3(0, 9.8, -4.4), 'magnet'), 'MAGNEETTI'],
    ];
    return () => st.render({ overlay: (g, w, h) => {
      const P = projector(st.camera, w, h); style(g, s);
      const pts = items.map(([v, l]) => [P(worldAnchor(S.group, v)), l]);
      pts.forEach(([p, l], i) => {
        const top = 300 + (i % 2) * 70;
        dot(g, p, s); g.beginPath(); g.moveTo(p[0], p[1] - 9); g.lineTo(p[0], top); g.lineTo(p[0] + 24, top); g.stroke();
        g.textAlign = 'left'; g.fillText(l, p[0] + 34, top);
      });
    } });
  },
  'hx01-macro-led': () => {
    const { st, S } = sensorStudio({ width: 2400, height: 1600, yaw: -0.35, env: { key: 3.5, top: 0.2 }, lights: { key: 4 } });
    const led = worldAnchor(S.group, S.anchors.led);
    const t = led.clone().add(new THREE.Vector3(-4, -3, 0));
    placeCamera(st.camera, { az: 8, el: 24, dist: 105, target: t, fov: 18 });
    return () => st.render();
  },
  'hx01-cutout': () => {
    const { st, T } = sensorStudio({ width: 1600, height: 1600, yaw: -0.5, alpha: true, bloom: { strength: 0 } });
    placeCamera(st.camera, { az: 22, el: 13, dist: 235, target: T, fov: 20 });
    return () => st.render({ grain: 2 });
  },
};

function frontShot(callouts) {
  const { st, S, T } = sensorStudio({ width: 2400, height: 1600, yaw: 0, env: { strip: 0 }, floor: { strength: 0.1 } });
  placeCamera(st.camera, { az: 0, el: 0, dist: 330, target: T, fov: 20 });
  if (!callouts) return () => st.render();
  return () => st.render({ overlay: (g, w, h) => {
    const s = 1, P = projector(st.camera, w, h), A = S.anchors, W = (v) => P(worldAnchor(S.group, v));
    style(g, s);
    const tl = W(new THREE.Vector3(-24, 24, 8.5)), tr = W(new THREE.Vector3(24, 24, 8.5));
    const y = tl[1] - 70;
    dimension(g, [tl[0], y], [tr[0], y], '48 MM', s, [[tl[0], tl[1] - 14], [tr[0], tr[1] - 14]]);
    const lens = W(new THREE.Vector3(-HX01.lens.d / 2, HX01.lens.y, glassZ(0, -4) + 0.6));
    leader(g, lens, [lens[0] - 120, lens[1]], lens[0] - 330, 'KAMERA Ø 9 MM', s, { side: 'left' });
    const led = W(A.led);
    leader(g, led, [led[0] + 110, led[1] - 110], led[0] + 330, 'MERKKIVALO', s, { side: 'right', sub: 'Ø 3 MM' });
    const bot = W(new THREE.Vector3(9.2, -24, 7.2));
    leader(g, bot, [bot[0] + 90, bot[1] + 90], bot[0] + 320, 'HX-01', s, { side: 'right', sub: 'KAIVERRUS, ALAREUNA' });
  } });
}
