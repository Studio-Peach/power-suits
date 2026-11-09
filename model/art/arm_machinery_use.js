(() => {
  const D = DRAFT, T = window.__armtex;
  const cubes = ['upper_arm_r', 'upper_arm_l', 'forearm_inner_r', 'forearm_inner_l'].map(n => Cube.all.find(c => c.name === n));
  Undo.initEdit({elements: cubes});
  for (const c of cubes) {
    if (D === 'now') { for (const f in c.faces) c.faces[f].uv = T.orig[c.name][f].slice(); continue; }
    const p = c.name.startsWith('upper') ? 'ua_' : 'fi_', left = c.name.endsWith('_l'), rs = T.P.rects[D];
    const R = k => { const [u, v, w, h] = rs[p + k]; return left ? [u + w, v, u, v + h] : [u, v, u + w, v + h]; };
    const map = {north: 'front', south: 'back', east: left ? 'in' : 'out', west: left ? 'out' : 'in', up: 'end', down: 'end'};
    for (const [f, k] of Object.entries(map)) c.faces[f].uv = R(k);
  }
  Undo.finishEdit('Arm machinery draft ' + D);
  Canvas.updateAll();
  return 'using ' + D;
})()
