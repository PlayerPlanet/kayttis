// Dark studio environment for reflections: black sphere + emissive softboxes, baked with PMREM.
import * as THREE from 'three';

function card(w, h, intensity, pos, look, round = false) {
  const geo = round ? new THREE.CircleGeometry(w / 2, 48) : new THREE.PlaneGeometry(w, h);
  const m = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: new THREE.Color(1, 1, 1).multiplyScalar(intensity), side: THREE.DoubleSide }));
  m.position.copy(pos); m.lookAt(look); return m;
}

// Softbox gradient so reflections have falloff instead of hard rectangles.
function softbox(w, h, intensity, pos, look) {
  const c = document.createElement('canvas'); c.width = 64; c.height = 256;
  const g = c.getContext('2d'); const grd = g.createLinearGradient(0, 0, 0, 256);
  grd.addColorStop(0, '#fff'); grd.addColorStop(0.55, '#9a9a9a'); grd.addColorStop(1, '#202020');
  g.fillStyle = grd; g.fillRect(0, 0, 64, 256);
  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace;
  const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ map: tex, color: new THREE.Color(1, 1, 1).multiplyScalar(intensity), side: THREE.DoubleSide }));
  m.position.copy(pos); m.lookAt(look); return m;
}

// layout: key = big soft box upper-left-front, rim = thin strip(s) behind, fill = weak card right.
export function buildEnvironment(renderer, opts = {}) {
  const o = { key: 9, rim: 9, fill: 1.6, top: 0.6, keyAz: -50, rimAz: 140, rimAz2: -150, rim2: 4, floorBounce: 0.02, ...opts };
  const s = new THREE.Scene();
  const sky = new THREE.Mesh(new THREE.SphereGeometry(50, 64, 32), new THREE.ShaderMaterial({
    side: THREE.BackSide, uniforms: { b: { value: o.floorBounce } },
    vertexShader: 'varying vec3 vP; void main(){ vP = position; gl_Position = projectionMatrix*modelViewMatrix*vec4(position,1.); }',
    fragmentShader: 'uniform float b; varying vec3 vP; void main(){ float y = normalize(vP).y; vec3 c = mix(vec3(b*0.6), vec3(0.012,0.013,0.015), smoothstep(-0.2,0.6,y)); gl_FragColor = vec4(c,1.); }',
  }));
  s.add(sky);
  const at = (az, el, d) => new THREE.Vector3(Math.sin(az * Math.PI / 180) * Math.cos(el * Math.PI / 180) * d, Math.sin(el * Math.PI / 180) * d, Math.cos(az * Math.PI / 180) * Math.cos(el * Math.PI / 180) * d);
  const O = new THREE.Vector3();
  s.add(softbox(o.keyW ?? 34, o.keyH ?? 24, o.key, at(o.keyAz, o.keyEl ?? 34, 30), O));
  s.add(card(3, 34, o.rim, at(o.rimAz, 15, 30), O));
  if (o.rim2) s.add(card(2.2, 30, o.rim2, at(o.rimAz2, 20, 30), O));
  s.add(softbox(18, 30, o.fill, at(o.fillAz ?? 105, 2, 30), O));
  s.add(softbox(12, 30, o.side ?? 3, at(o.sideAz ?? -88, 6, 30), O));
  s.add(card(30, 30, o.top, at(0, 88, 30), O));
  // thin horizontal strip low in front: gives the bottom bevels a line of light
  s.add(card(40, 1.2, o.strip ?? 1.5, at(10, -4, 30), O));
  const pm = new THREE.PMREMGenerator(renderer);
  const rt = pm.fromScene(s, 0.02);
  pm.dispose();
  return rt.texture;
}
