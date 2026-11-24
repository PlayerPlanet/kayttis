// Direct lights aligned with the environment softboxes so reflections and shading agree.
import * as THREE from 'three';

export const dir = (az, el) => new THREE.Vector3(
  Math.sin(az * Math.PI / 180) * Math.cos(el * Math.PI / 180), Math.sin(el * Math.PI / 180),
  Math.cos(az * Math.PI / 180) * Math.cos(el * Math.PI / 180));

export function areaLight(scene, { az, el, dist = 600, w = 300, h = 200, intensity = 4, target = new THREE.Vector3(), color = 0xffffff }) {
  const l = new THREE.RectAreaLight(color, intensity, w, h);
  l.position.copy(dir(az, el).multiplyScalar(dist).add(target)); l.lookAt(target);
  scene.add(l); return l;
}

// Soft shadow-casting spot (used for the wall spill and as key shadow in panel shots).
export function spot(scene, { pos, target, intensity = 1e6, angle = 0.5, penumbra = 1, shadow = true, radius = 8, mapSize = 2048, color = 0xffffff, decay = 2 }) {
  const s = new THREE.SpotLight(color, intensity, 0, angle, penumbra, decay);
  s.position.copy(pos); s.target.position.copy(target);
  if (shadow) {
    s.castShadow = true; s.shadow.mapSize.set(mapSize, mapSize); s.shadow.radius = radius;
    s.shadow.bias = -0.0002; s.shadow.normalBias = 0.3; s.shadow.camera.near = 50; s.shadow.camera.far = 5000;
  }
  scene.add(s, s.target); return s;
}
