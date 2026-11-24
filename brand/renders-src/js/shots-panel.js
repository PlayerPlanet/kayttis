// HX-P shots (+ family and cutouts live in shots-family.js).
import * as THREE from 'three';
import { createStudio, capture } from './studio.js';
import { areaLight, spot } from './lights.js';
import { buildPanel, HXP } from './panel.js';
import { placeCamera } from './shots-sensor.js';

// Panel mounted on a dark wall (wall plane z = -6), soft spill from above.
export function wallStudio(opts) {
  const st = createStudio(opts);
  const { scene, renderer } = st;
  renderer.shadowMap.type = THREE.PCFShadowMap;
  const P = buildPanel(opts.panel || {});
  scene.add(P.group);
  if (!opts.alpha) {
    const wall = new THREE.Mesh(new THREE.PlaneGeometry(6000, 4000), new THREE.MeshStandardMaterial({ color: '#1c1f23', roughness: 0.93, metalness: 0 }));
    wall.position.z = -6.05; wall.receiveShadow = true; scene.add(wall);
    const sp = opts.spill || {};
    spot(scene, { pos: new THREE.Vector3(sp.x ?? -60, sp.y ?? 620, sp.z ?? 230), target: new THREE.Vector3(sp.tx ?? 0, sp.ty ?? 10, -6),
      intensity: sp.intensity ?? 1.1e6, angle: 0.42, penumbra: 1, radius: 10, mapSize: 2048 });
  }
  const T = new THREE.Vector3(0, 0, 0);
  const k = opts.lights || {};
  areaLight(scene, { az: -45, el: 38, dist: 800, w: 400, h: 260, intensity: k.key ?? 5, target: T });
  areaLight(scene, { az: 120, el: 15, dist: 700, w: 40, h: 500, intensity: k.rim ?? 5, target: T });
  st.render = (cfg = {}) => capture(st, cfg);
  return { st, P, T };
}

export const panelShots = {
  'hxp-hero': () => {
    const { st } = wallStudio({ width: 2400, height: 1600, spill: { intensity: 2.2e6, x: 40, y: 520, z: 160, tx: 20, ty: 60 } });
    placeCamera(st.camera, { az: 34, el: 7, dist: 640, target: new THREE.Vector3(6, -4, 0), fov: 20 });
    return () => st.render();
  },
  'hxp-front': () => {
    const { st } = wallStudio({ width: 2400, height: 1600, env: { strip: 0 }, spill: { intensity: 0.8e6 } });
    placeCamera(st.camera, { az: 0, el: 0, dist: 560, target: new THREE.Vector3(0, 0, 0), fov: 20 });
    return () => st.render();
  },
  'hxp-knob-macro': () => {
    const { st } = wallStudio({ width: 2400, height: 1600, lights: { key: 3 } });
    const t = new THREE.Vector3(HXP.knob.x, HXP.knob.y, 10);
    placeCamera(st.camera, { az: 38, el: 20, dist: 150, target: t, fov: 18 });
    return () => st.render();
  },
};
