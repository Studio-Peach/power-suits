(() => {
  const P = PLAN;
  const tex = Texture.all[0];
  const cubes = ['upper_arm_r', 'upper_arm_l', 'forearm_inner_r', 'forearm_inner_l'].map(n => Cube.all.find(c => c.name === n));
  if (cubes.some(c => !c)) return 'abort: cubes missing';
  if (window.__armtex) return 'abort: already applied';
  let bad = '';
  tex.edit(canvas => {
    const ctx = canvas.getContext('2d');
    for (const [d, rs] of Object.entries(P.rects)) for (const [k, [u, v, w, h]] of Object.entries(rs)) {
      const a = ctx.getImageData(u, v, w, h).data; for (let i = 3; i < a.length; i += 4) if (a[i]) { bad += ' ' + d + k; break; } }
    if (bad) return canvas;
    for (const [d, rs] of Object.entries(P.rects)) for (const [k, [u, v, w, h]] of Object.entries(rs)) {
      const hex = P.hex[d + ':' + k], img = ctx.createImageData(w, h);
      for (let i = 0; i < w * h * 4; i++) img.data[i] = parseInt(hex.substr(i * 2, 2), 16);
      ctx.putImageData(img, u, v); }
    return canvas;
  }, {edit_name: 'Arm machinery drafts paint'});
  if (bad) return 'abort, not empty:' + bad;
  window.__armtex = {P, orig: Object.fromEntries(cubes.map(c => [c.name, Object.fromEntries(Object.entries(c.faces).map(([f, x]) => [f, x.uv.slice()]))]))};
  return 'painted';
})()
