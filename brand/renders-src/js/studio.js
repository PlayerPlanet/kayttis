// Renderer + post chain + capture (supersample, downscale, grain) shared by all shots.
import * as THREE from 'three';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { BokehPass } from 'three/addons/postprocessing/BokehPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';
import { RectAreaLightUniformsLib } from 'three/addons/lights/RectAreaLightUniformsLib.js';
import { buildEnvironment } from './environment.js';

export function createStudio({ width, height, ss = 1.5, alpha = false, exposure = 1.0, env = {}, bloom = {}, bokeh = null, samples = 4 }) {
  RectAreaLightUniformsLib.init();
  const W = Math.round(width * ss), H = Math.round(height * ss);
  const renderer = new THREE.WebGLRenderer({ antialias: false, alpha, preserveDrawingBuffer: true, powerPreference: 'high-performance' });
  renderer.setPixelRatio(1); renderer.setSize(W, H, false);
  renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = exposure;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.setClearColor(0x000000, alpha ? 0 : 1);
  document.body.appendChild(renderer.domElement);

  const scene = new THREE.Scene();
  scene.environment = buildEnvironment(renderer, env);
  if (!alpha) scene.background = new THREE.Color(0.0032, 0.0037, 0.0045);
  const camera = new THREE.PerspectiveCamera(20, width / height, 5, 20000);

  const rt = new THREE.WebGLRenderTarget(W, H, { type: THREE.HalfFloatType, samples });
  const composer = new EffectComposer(renderer, rt);
  composer.setPixelRatio(1); composer.setSize(W, H);
  composer.addPass(new RenderPass(scene, camera, null, new THREE.Color(0, 0, 0), alpha ? 0 : 1));
  const b = { strength: 0.35, radius: 0.55, threshold: 1.6, ...bloom };
  const bloomPass = new UnrealBloomPass(new THREE.Vector2(W, H), b.strength, b.radius, b.threshold);
  if (b.strength > 0) composer.addPass(bloomPass);
  let bokehPass = null;
  if (bokeh) { bokehPass = new BokehPass(scene, camera, { focus: 300, aperture: 0.0002, maxblur: 0.01, ...bokeh }); composer.addPass(bokehPass); }
  composer.addPass(new OutputPass());

  return { renderer, scene, camera, composer, bloomPass, bokehPass, W, H, width, height, alpha };
}

// Render, then downscale into a 2D canvas, add grain/dither, optional overlay callback.
export function capture(studio, { grain = 4.0, overlay = null, type = 'image/png' } = {}) {
  const { composer, renderer, width, height } = studio;
  composer.render();
  const c = document.createElement('canvas'); c.width = width; c.height = height;
  const g = c.getContext('2d', { willReadFrequently: true });
  g.imageSmoothingEnabled = true; g.imageSmoothingQuality = 'high';
  g.drawImage(renderer.domElement, 0, 0, width, height);
  if (grain > 0) {
    const img = g.getImageData(0, 0, width, height), d = img.data;
    let s = 1234567;
    for (let i = 0; i < d.length; i += 4) {
      if (d[i + 3] === 0) continue;
      s ^= s << 13; s ^= s >>> 17; s ^= s << 5;
      const n1 = ((s >>> 0) / 4294967296);
      s ^= s << 13; s ^= s >>> 17; s ^= s << 5;
      const n = (n1 + (s >>> 0) / 4294967296 - 1) * grain; // triangular dither
      d[i] += n; d[i + 1] += n; d[i + 2] += n;
    }
    g.putImageData(img, 0, 0);
  }
  if (overlay) overlay(g, width, height);
  return c.toDataURL(type);
}
