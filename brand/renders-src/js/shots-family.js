// Family shot, panel cutout and the two motion pieces.
import * as THREE from 'three';
import { createStudio, capture } from './studio.js';
import { buildFloor, buildContactShadow } from './floor.js';
import { areaLight } from './lights.js';
import { buildSensor } from './sensor.js';
import { buildPanel, HXP } from './panel.js';
import { placeCamera, sensorStudio } from './shots-sensor.js';
import { wallStudio } from './shots-panel.js';

const ease = (t) => t * t * (3 - 2 * t);
const clamp01 = (t) => Math.min(1, Math.max(0, t));

export const familyShots = {
  family: () => {
    const st = createStudio({ width: 2400, height: 1600 });
    const { scene } = st;
    const P = buildPanel();
    P.group.position.set(-40, HXP.h / 2 + 0.08, -45); P.group.rotation.y = 0.32; scene.add(P.group);
    const S = buildSensor();
    S.group.position.set(80, 24.08, 15); S.group.rotation.y = -0.38; scene.add(S.group);
    const floor = buildFloor({ poolCenter: [10, -10], poolRadius: 320, strength: 0.09, fadeRadius: 400 });
    scene.add(floor);
    const shadow = buildContactShadow({ width: 500, height: 500, camHeight: 45, darkness: 1.5, opacity: 0.9, blur: 1.6 });
    scene.add(shadow.group);
    const T = new THREE.Vector3(10, 40, 0);
    areaLight(scene, { az: -50, el: 42, dist: 900, w: 500, h: 340, intensity: 8, target: T });
    areaLight(scene, { az: 140, el: 15, dist: 800, w: 50, h: 600, intensity: 10, target: T });
    areaLight(scene, { az: -150, el: 20, dist: 800, w: 40, h: 500, intensity: 5, target: T });
    placeCamera(st.camera, { az: 14, el: 11, dist: 780, target: new THREE.Vector3(14, 44, 0), fov: 20 });
    return () => { shadow.update(st.renderer, scene, [floor]); return capture(st); };
  },

  'hxp-cutout': () => {
    const { st } = wallStudio({ width: 2000, height: 1400, alpha: true, bloom: { strength: 0 } });
    placeCamera(st.camera, { az: 32, el: 8, dist: 420, target: new THREE.Vector3(4, -2, 0), fov: 20 });
    return () => st.render({ grain: 2 });
  },

  // 6 s seamless loop: yaw oscillates ±15° (30° sweep) on a cosine, so frame N == frame 0.
  'hx01-turntable': () => {
    const { st, S, T } = sensorStudio({ width: 1920, height: 1080, yaw: -0.5, ss: 1.25, env: { rim: 3.5, fill: 1.0 }, lights: { rim: 7 } });
    placeCamera(st.camera, { az: 18, el: 11, dist: 300, target: T.clone().add(new THREE.Vector3(0, 1, 0)), fov: 20 });
    const base = -0.42;
    return { still: () => st.render(), frame: (i, n) => {
      S.group.rotation.y = base + Math.sin(i / n * Math.PI * 2) * THREE.MathUtils.degToRad(15);
      return st.render({ grain: 2.5, type: 'image/png' });
    } };
  },

  // 5 s: screen fades up from black, a light sweep crosses the frame, then the amber ring lights.
  'hxp-reveal': () => {
    const W = wallStudio({ width: 1920, height: 1080, ss: 1.25, panel: { screenOn: 0, ringOn: 0 }, spill: { intensity: 2.2e6, x: 40, y: 520, z: 160, tx: 20, ty: 60 } });
    const { st } = W;
    placeCamera(st.camera, { az: 30, el: 6, dist: 600, target: new THREE.Vector3(8, -4, 0), fov: 20 });
    // rebuild panel per frame state cheaply: swap materials' intensities
    const scene = st.scene;
    scene.remove(W.P.group);
    const on = buildPanel({ screenOn: 1, ringOn: 1 });
    scene.add(on.group);
    const ringParts = on.group.children.filter((o) => o.material && (o.material.type === 'ShaderMaterial' || (o.material.toneMapped === false && o.geometry.type === 'RingGeometry')));
    const ringLight = on.group.children.find((o) => o.isPointLight);
    const base = ringParts.map((o) => (o.material.uniforms ? o.material.uniforms.c.value.clone() : o.material.color.clone()));
    const ringLightI = ringLight.intensity;
    // sweep: a moving vertical area light from left to right
    const sweep = new THREE.RectAreaLight(0xffffff, 0, 140, 900); scene.add(sweep);
    return { still: () => st.render(), frame: (i, n) => {
      const t = i / (n - 1) * 5;
      const screen = ease(clamp01((t - 0.6) / 1.4));
      on.screenMat.color.setScalar(1.25 * screen);
      const ring = ease(clamp01((t - 3.0) / 0.8));
      ringParts.forEach((o, k) => { const c = base[k].clone().multiplyScalar(ring); if (o.material.uniforms) o.material.uniforms.c.value.copy(c); else o.material.color.copy(c); });
      ringLight.intensity = ringLightI * ring;
      const s = clamp01((t - 1.2) / 2.4);
      sweep.intensity = 3.2 * Math.pow(Math.sin(s * Math.PI), 1.5);
      sweep.position.set(-500 + 1000 * ease(s), 120, 420); sweep.lookAt(0, 0, 0);
      return st.render({ grain: 2.5 });
    } };
  },
};
