// Shared physical materials. Units are millimetres; texture repeats are per mm.
import * as THREE from 'three';
import { brushedMaps } from './textures.js';

export const AMBER = new THREE.Color('#ff9a2e');

let cache;
export function materials() {
  if (cache) return cache;
  const brushed = brushedMaps(1024, 11);
  const rep = (t, s) => { const c = t.clone(); c.repeat.set(s, s * 3); c.needsUpdate = true; return c; };

  // Anodised graphite aluminium, bead-blast + brush. Anisotropy stretches highlights along u.
  const aluminium = new THREE.MeshPhysicalMaterial({
    color: new THREE.Color('#5d646b'), metalness: 0.92, roughness: 0.42,
    roughnessMap: rep(brushed.roughness, 1 / 60), normalMap: rep(brushed.normal, 1 / 60),
    normalScale: new THREE.Vector2(0.25, 0.25), anisotropy: 0.55, anisotropyRotation: 0,
    clearcoat: 0.25, clearcoatRoughness: 0.35, envMapIntensity: 1.0,
  });

  // Frosted black glass: soft broad sheen, no mirror.
  const frosted = new THREE.MeshPhysicalMaterial({
    color: new THREE.Color('#07080a'), metalness: 0, roughness: 0.3, ior: 1.5,
    specularIntensity: 1, clearcoat: 0.35, clearcoatRoughness: 0.22, envMapIntensity: 1.2,
  });

  // Gloss black glass (panel cover, lens): sharp reflections.
  const glossGlass = new THREE.MeshPhysicalMaterial({
    color: new THREE.Color('#050607'), metalness: 0, roughness: 0.06, ior: 1.52,
    clearcoat: 1, clearcoatRoughness: 0.03, envMapIntensity: 1.1,
  });

  // Reflection-only coating layered additively over emissive content (screen, lens interior).
  const coating = new THREE.MeshPhysicalMaterial({
    color: 0x000000, metalness: 0, roughness: 0.05, clearcoat: 1, clearcoatRoughness: 0.03,
    envMapIntensity: 1.1, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false,
  });

  // Titanium: lighter, warmer-neutral grey, finer finish.
  const titanium = new THREE.MeshPhysicalMaterial({
    color: new THREE.Color('#a4a9ae'), metalness: 1, roughness: 0.3,
    roughnessMap: rep(brushed.roughness, 1 / 30), anisotropy: 0.45,
    envMapIntensity: 1.0,
  });

  const black = new THREE.MeshPhysicalMaterial({ color: '#08090a', roughness: 0.6, metalness: 0 });
  const darkMetal = new THREE.MeshPhysicalMaterial({ color: '#2a2e33', roughness: 0.4, metalness: 0.9 });
  const pcb = new THREE.MeshPhysicalMaterial({ color: '#1c1f23', roughness: 0.45, clearcoat: 0.6, clearcoatRoughness: 0.3 });
  const shield = new THREE.MeshPhysicalMaterial({ color: '#9aa0a6', metalness: 1, roughness: 0.32, roughnessMap: rep(brushed.roughness, 1 / 25) });
  const pouch = new THREE.MeshPhysicalMaterial({ color: '#6f757b', metalness: 0.85, roughness: 0.38, clearcoat: 0.4 });
  const nickel = new THREE.MeshPhysicalMaterial({ color: '#a7acb1', metalness: 1, roughness: 0.18 });

  const led = new THREE.MeshBasicMaterial({ color: AMBER.clone().multiplyScalar(9), toneMapped: false });
  cache = { aluminium, frosted, glossGlass, coating, titanium, black, darkMetal, pcb, shield, pouch, nickel, led };
  return cache;
}

// Additive glow sprite material (amber), linear HDR so bloom can pick it up.
// Pure additive light that leaves destination alpha untouched (so cutouts stay clean).
export const ADD = { blending: THREE.CustomBlending, blendEquation: THREE.AddEquation, blendSrc: THREE.OneFactor, blendDst: THREE.OneFactor,
  blendSrcAlpha: THREE.ZeroFactor, blendDstAlpha: THREE.OneFactor };
export function glowMaterial(tex, intensity = 1.5, color = AMBER) {
  return new THREE.MeshBasicMaterial({
    map: tex, color: color.clone().multiplyScalar(intensity), transparent: true, depthWrite: false, toneMapped: false, ...ADD,
  });
}
