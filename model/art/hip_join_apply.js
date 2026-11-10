(() => {
  /* Legs straight into the belt (2026-11-10, see hip_join_art.py). PLAN = its plan2.json. Removes hip_axle,
     hip_axle_top and the then empty frame_hips group, grows thigh_r/l to y 25.625 with new 13-row sides.
     Strip comments before risky_eval. */
  if (Project.name !== 'power_suit') return 'wrong project';
  const plan = PLAN, tex = Texture.all[0];
  const thighs = ['thigh_r', 'thigh_l'].map(n => Cube.all.find(c => c.name === n));
  if (thighs.some(c => !c) || thighs[0].to[1] !== 23.625) return 'abort, thighs not as expected';
  const probe = document.createElement('canvas'); probe.width = tex.width; probe.height = tex.height;
  const pctx = probe.getContext('2d'); pctx.drawImage(tex.canvas || tex.img, 0, 0);
  plan.clear.forEach(([x, y]) => pctx.clearRect(x, y, 1, 1));
  for (const [k, [u, v, w, h]] of Object.entries(plan.rects)) {
    const d = pctx.getImageData(u, v, w, h).data;
    for (let i = 3; i < d.length; i += 4) if (d[i] !== 0) return 'abort, not transparent: ' + k; }
  const axle = Cube.all.filter(c => /^hip_axle(_top)?$/.test(c.name));
  Undo.initEdit({outliner: true, elements: axle});
  axle.forEach(c => c.remove());
  Undo.finishEdit('Remove the hip axle', {outliner: true, elements: []});
  const fh = Group.all.filter(g => g.name === 'frame_hips' && !g.children.length);
  Undo.initEdit({outliner: true, groups: fh});
  fh.forEach(g => g.remove(false));
  Undo.finishEdit('Remove empty frame_hips');
  tex.edit(canvas => { const ctx = canvas.getContext('2d');
    plan.clear.forEach(([x, y]) => ctx.clearRect(x, y, 1, 1));
    for (const [k, [u, v, w, h]] of Object.entries(plan.rects)) {
      const hex = plan.hex[k], img = ctx.createImageData(w, h);
      for (let i = 0; i < w * h * 4; i++) img.data[i] = parseInt(hex.substr(i * 2, 2), 16);
      ctx.putImageData(img, u, v); }
    return canvas; }, {edit_name: 'Thigh sides 13 rows'});
  Undo.initEdit({elements: thighs});
  thighs.forEach(c => { const mirror = c.name === 'thigh_l'; c.to[1] = 25.625;
    for (const f of ['north', 'south', 'east', 'west']) {
      const src = mirror && f === 'east' ? 'west' : mirror && f === 'west' ? 'east' : f;
      const [u, v, w, h] = plan.rects['thigh_' + src];
      c.faces[f].uv = mirror ? [u + w, v, u, v + h] : [u, v, u + w, v + h]; } });
  Undo.finishEdit('Thighs up to the belt');
  Canvas.updateAll();
  return 'ok, removed ' + axle.length + ' axle cubes, ' + fh.length + ' group';
})()
