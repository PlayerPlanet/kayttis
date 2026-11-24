// Studio floor: blurred faint reflection (Reflector) + baked light pool, and a soft contact shadow.
import * as THREE from 'three';
import { Reflector } from 'three/addons/objects/Reflector.js';
import { HorizontalBlurShader } from 'three/addons/shaders/HorizontalBlurShader.js';
import { VerticalBlurShader } from 'three/addons/shaders/VerticalBlurShader.js';

const FloorShader = {
  uniforms: {
    color: { value: null }, tDiffuse: { value: null }, textureMatrix: { value: null },
    base: { value: new THREE.Color(0.0035, 0.004, 0.0048) }, pool: { value: new THREE.Color(0.02, 0.021, 0.023) },
    poolCenter: { value: new THREE.Vector2(0, 0) }, poolRadius: { value: 250 },
    strength: { value: 0.16 }, blur: { value: 0.004 }, fadeRadius: { value: 220 },
  },
  vertexShader: /* glsl */`
    uniform mat4 textureMatrix; varying vec4 vUv; varying vec3 vW;
    void main(){ vUv = textureMatrix * vec4(position,1.0); vW = (modelMatrix*vec4(position,1.0)).xyz; gl_Position = projectionMatrix*modelViewMatrix*vec4(position,1.0); }`,
  fragmentShader: /* glsl */`
    uniform sampler2D tDiffuse; uniform vec3 base, pool; uniform vec2 poolCenter; uniform float poolRadius, strength, blur, fadeRadius;
    varying vec4 vUv; varying vec3 vW;
    void main(){
      vec2 uv = vUv.xy / vUv.w;
      vec3 r = vec3(0.0); float wsum = 0.0;
      float rot = fract(sin(dot(gl_FragCoord.xy, vec2(12.9898,78.233)))*43758.5453)*6.2831;
      for (int i=0;i<32;i++){ float fi = float(i)+0.5; float rr = sqrt(fi/32.0)*2.2; float a = fi*2.39996+rot;
        vec2 o = vec2(cos(a),sin(a))*rr; float w = exp(-rr*rr/2.0); r += min(texture2D(tDiffuse, uv + o*blur).rgb, vec3(0.6))*w; wsum += w; }
      r /= wsum;
      float d = length(vW.xz - poolCenter);
      float p = exp(-pow(d/poolRadius, 2.0));
      float f = exp(-pow(length(vW.xz)/fadeRadius, 2.0));
      gl_FragColor = vec4(base + pool*p + r*strength*f, 1.0);
    }`,
};

export function buildFloor({ size = 4000, ...u } = {}) {
  const geo = new THREE.PlaneGeometry(size, size);
  const floor = new Reflector(geo, { shader: FloorShader, textureWidth: 2048, textureHeight: 2048, clipBias: 0.0, multisample: 4 });
  floor.rotation.x = -Math.PI / 2;
  for (const k in u) {
    const un = floor.material.uniforms[k];
    if (un.value && un.value.set && typeof u[k] !== 'number') { if (Array.isArray(u[k])) un.value.set(...u[k]); else un.value.copy(u[k]); } else un.value = u[k];
  }
  return floor;
}

// Contact shadow (after three.js webgl_shadow_contact example). Call update(renderer, scene) before render.
export function buildContactShadow({ width = 200, height = 200, camHeight = 40, darkness = 1.2, opacity = 0.85, blur = 2.5, res = 1024 } = {}) {
  const group = new THREE.Group();
  const rt = new THREE.WebGLRenderTarget(res, res); rt.texture.generateMipmaps = false;
  const rtBlur = new THREE.WebGLRenderTarget(res, res); rtBlur.texture.generateMipmaps = false;
  const plane = new THREE.Mesh(new THREE.PlaneGeometry(width, height).rotateX(Math.PI / 2),
    new THREE.MeshBasicMaterial({ map: rt.texture, opacity, transparent: true, depthWrite: false, color: 0x000000 }));
  plane.material.onBeforeCompile = (sh) => { sh.fragmentShader = sh.fragmentShader.replace('#include <map_fragment>', 'diffuseColor.a *= texture2D(map, vMapUv).a;'); };
  plane.material.map = rt.texture; plane.renderOrder = 1; plane.scale.y = -1; plane.position.y = 0.02;
  group.add(plane);
  const blurPlane = new THREE.Mesh(new THREE.PlaneGeometry(width, height).rotateX(Math.PI / 2)); blurPlane.visible = false; group.add(blurPlane);
  const cam = new THREE.OrthographicCamera(-width / 2, width / 2, height / 2, -height / 2, 0, camHeight);
  cam.rotation.x = Math.PI / 2; group.add(cam);
  const depthMat = new THREE.MeshDepthMaterial();
  depthMat.userData.darkness = { value: darkness };
  depthMat.onBeforeCompile = (sh) => {
    sh.uniforms.darkness = depthMat.userData.darkness;
    sh.fragmentShader = 'uniform float darkness;\n' + sh.fragmentShader.replace('gl_FragColor = vec4( vec3( 1.0 - fragCoordZ ), opacity );', 'gl_FragColor = vec4( vec3( 0.0 ), ( 1.0 - fragCoordZ ) * darkness );');
  };
  depthMat.depthTest = false; depthMat.depthWrite = false;
  const hb = new THREE.ShaderMaterial(HorizontalBlurShader); hb.depthTest = false;
  const vb = new THREE.ShaderMaterial(VerticalBlurShader); vb.depthTest = false;
  function blurOnce(renderer, amount) {
    blurPlane.visible = true;
    blurPlane.material = hb; hb.uniforms.tDiffuse.value = rt.texture; hb.uniforms.h.value = amount / 256;
    renderer.setRenderTarget(rtBlur); renderer.render(blurPlane, cam);
    blurPlane.material = vb; vb.uniforms.tDiffuse.value = rtBlur.texture; vb.uniforms.v.value = amount / 256;
    renderer.setRenderTarget(rt); renderer.render(blurPlane, cam);
    blurPlane.visible = false;
  }
  function update(renderer, scene, hide = []) {
    const bg = scene.background, prevOverride = scene.overrideMaterial, prevClear = renderer.getClearAlpha();
    const hidden = hide.filter((o) => o.visible); hidden.forEach((o) => (o.visible = false));
    plane.visible = false; scene.background = null; scene.overrideMaterial = depthMat; renderer.setClearAlpha(0);
    renderer.setRenderTarget(rt); renderer.clear(); renderer.render(scene, cam);
    scene.overrideMaterial = prevOverride;
    blurOnce(renderer, blur); blurOnce(renderer, blur * 0.4);
    renderer.setRenderTarget(null); renderer.setClearAlpha(prevClear);
    scene.background = bg; plane.visible = true; hidden.forEach((o) => (o.visible = true));
  }
  return { group, update };
}
