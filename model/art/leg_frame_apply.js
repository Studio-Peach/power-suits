(() => {
  /* Machine legs inside the iron (2026-11-10, see leg_frame_art.py). PLAN = its plan3.json. Removes knee_r/l and their
     frame_knee_* groups, builds upper_leg_* (frame_thigh_*, leg bone) and lower_leg_* (frame_shin_*, shin bone).
     Strip comments before risky_eval. */
  if (Project.name !== 'power_suit') return 'wrong project';
  if (Cube.all.some(c => c.name === 'upper_leg_r')) return 'abort, already built';
  const plan = PLAN, tex = Texture.all[0], G = n => Group.all.find(g => g.name === n);
  const probe = document.createElement('canvas'); probe.width = tex.width; probe.height = tex.height;
  const pctx = probe.getContext('2d'); pctx.drawImage(tex.canvas || tex.img, 0, 0);
  plan.clear.forEach(([x, y]) => pctx.clearRect(x, y, 1, 1));
  for (const [k, [u, v, w, h]] of Object.entries(plan.rects)) {
    const d = pctx.getImageData(u, v, w, h).data;
    for (let i = 3; i < d.length; i += 4) if (d[i] !== 0) return 'abort, not transparent: ' + k; }
  const knees = Cube.all.filter(c => /^knee_[rl]$/.test(c.name));
  Undo.initEdit({outliner: true, elements: knees});
  knees.forEach(c => c.remove());
  Undo.finishEdit('Remove the knee blocks', {outliner: true, elements: []});
  const kg = Group.all.filter(g => /^frame_knee_[rl]$/.test(g.name) && !g.children.length);
  Undo.initEdit({outliner: true, groups: kg});
  kg.forEach(g => g.remove(false));
  Undo.finishEdit('Remove empty frame_knee groups');
  tex.edit(canvas => { const ctx = canvas.getContext('2d');
    plan.clear.forEach(([x, y]) => ctx.clearRect(x, y, 1, 1));
    for (const [k, [u, v, w, h]] of Object.entries(plan.rects)) {
      const hex = plan.hex[k], img = ctx.createImageData(w, h);
      for (let i = 0; i < w * h * 4; i++) img.data[i] = parseInt(hex.substr(i * 2, 2), 16);
      ctx.putImageData(img, u, v); }
    return canvas; }, {edit_name: 'Machine legs paint'});
  const faces = (p, mirror) => { const out = {};
    for (const f of ['north', 'south', 'east', 'west', 'up', 'down']) {
      const [u, v, w, h] = plan.rects[p + '_' + f];
      const key = mirror && f === 'east' ? 'west' : mirror && f === 'west' ? 'east' : f;
      out[key] = {uv: mirror ? [u + w, v, u, v + h] : [u, v, u + w, v + h], texture: tex.uuid}; }
    return out; };
  const made = [];
  Undo.initEdit({outliner: true, elements: []});
  const group = (name, bone) => new Group({name, origin: G(bone).origin.slice()}).addTo(G(bone)).init();
  const cube = (grp, name, from, to, p, mirror, inflate) => { const c = new Cube({name, from, to, origin: grp.origin.slice(),
    box_uv: false, inflate: inflate || 0, faces: faces(p, mirror)}).addTo(grp).init(); made.push(c); return c; };
  const M = (f, t) => [[-t[0], f[1], f[2]], [-f[0], t[1], t[2]]];
  for (const [s, side, mirror] of [['r', 'right', false], ['l', 'left', true]]) {
    const X = (f, t) => mirror ? M(f, t) : [f, t];
    cube(group('frame_thigh_' + s, side + '_leg'), 'upper_leg_' + s, ...X([2, 12.625, -3], [9, 25.625, 3]), 'ul', mirror);
    cube(group('frame_shin_' + s, side + '_shin'), 'lower_leg_' + s, ...X([2.5, -0.375, -2.5], [8.5, 14.625, 2.5]), 'll', mirror, -0.05);
  }
  made.forEach(c => c.visibility = true);
  Undo.finishEdit('Machine legs inside the iron', {outliner: true, elements: made});
  Canvas.updateAll();
  return 'ok, removed ' + knees.length + ' knees, ' + kg.length + ' groups; made ' + made.length;
})()
