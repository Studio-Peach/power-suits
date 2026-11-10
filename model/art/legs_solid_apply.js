(() => {
  /* Solid legs (2026-11-09, draft G made final; see legs_solid_art.py). PLAN = its plan.json. Removes the old leg
     pieces, the leg drafts and the empty hood bones (no animation keys them), clears and paints the texels, builds
     thigh_/shin_/knee_ per side and the hip plates, and groups the hips' machine (hip_axle*) and the abdomen.
     Strip comments before risky_eval. */
  if (Project.name !== 'power_suit') return 'wrong project';
  if (Cube.all.some(c => c.name === 'thigh_r')) return 'abort, already built';
  const plan = PLAN, tex = Texture.all[0], G = n => Group.all.find(g => g.name === n);
  const OLD = /^(thigh_|cap_[cfb]_|shin_|knee_joint|boot_|hood_|lg[ABG]_)/;
  const hoods = ['right_hood', 'left_hood'].map(G);
  for (const a of Animation.all) for (const h of hoods) {
    const an = a.animators[h.uuid]; if (an && (an.keyframes || []).length) return 'abort, ' + h.name + ' keyed in ' + a.name; }
  const probe = document.createElement('canvas'); probe.width = tex.width; probe.height = tex.height;
  const pctx = probe.getContext('2d'); pctx.drawImage(tex.canvas || tex.img, 0, 0);
  plan.clear.forEach(([x, y]) => pctx.clearRect(x, y, 1, 1));
  for (const [k, [u, v, w, h]] of Object.entries(plan.rects)) {
    const d = pctx.getImageData(u, v, w, h).data;
    for (let i = 3; i < d.length; i += 4) if (d[i] !== 0) return 'abort, not transparent: ' + k; }
  const old = Cube.all.filter(c => OLD.test(c.name));
  Undo.initEdit({outliner: true, elements: old});
  old.forEach(c => c.remove());
  Undo.finishEdit('Remove old legs and leg drafts', {outliner: true, elements: []});
  const empty = Group.all.filter(g => /^proto_legs/.test(g.name) || /^(right|left)_hood$/.test(g.name));
  if (empty.some(g => g.children.length)) return 'stop: groups to remove not empty';
  Undo.initEdit({outliner: true, groups: empty});
  empty.forEach(g => g.remove(false));
  Undo.finishEdit('Remove empty leg draft groups and hood bones');
  tex.edit(canvas => { const ctx = canvas.getContext('2d');
    plan.clear.forEach(([x, y]) => ctx.clearRect(x, y, 1, 1));
    for (const [k, [u, v, w, h]] of Object.entries(plan.rects)) {
      const hex = plan.hex[k], img = ctx.createImageData(w, h);
      for (let i = 0; i < w * h * 4; i++) img.data[i] = parseInt(hex.substr(i * 2, 2), 16);
      ctx.putImageData(img, u, v); }
    return canvas; }, {edit_name: 'Solid legs paint'});
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
    cube(group('iron_thigh_' + s, side + '_leg'), 'thigh_' + s, ...X([1, 12.625, -4], [10, 23.625, 4]), 'thigh', mirror, 0.1);
    cube(group('iron_shin_' + s, side + '_shin'), 'shin_' + s, ...X([1, -0.375, -4], [10, 11.625, 4]), 'shin', mirror);
    cube(group('frame_knee_' + s, side + '_shin'), 'knee_' + s, ...X([2, 10.625, -3], [9, 14.625, 3]), 'knee', mirror);
  }
  /* 0.1 under the abdomen's top: at 28.625 they shared its plane and flickered (zfight.mjs) */
  const ironHips = group('iron_hips', 'hips');
  cube(ironHips, 'hip_plate_r', [0.25, 25.525, -5.5], [7.25, 28.525, 5.5], 'hip', false);
  cube(ironHips, 'hip_plate_l', [-7.25, 25.525, -5.5], [-0.25, 28.525, 5.5], 'hip', true);
  const frameHips = group('frame_hips', 'hips');
  ['hip_axle', 'hip_axle_top'].forEach(n => Cube.all.find(c => c.name === n).addTo(frameHips));
  Cube.all.find(c => c.name === 'belt_buckle').addTo(ironHips);
  Cube.all.find(c => c.name === 'abdomen').addTo(group('frame_abdomen', 'body'));
  made.forEach(c => c.visibility = true);
  Undo.finishEdit('Solid legs', {outliner: true, elements: made});
  Canvas.updateAll();
  return 'ok, removed ' + old.length + ' cubes, ' + empty.length + ' groups; made ' + made.length;
})()
