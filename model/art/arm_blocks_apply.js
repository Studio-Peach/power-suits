(() => {
  const P = PLAN;
  const tex = Texture.all[0];
  const gone = Cube.all.filter(c => /^(upper_core_|elbow_joint|elbow_arc_)/.test(c.name));
  const fore = ['forearm_r', 'forearm_l'].map(n => Cube.all.find(c => c.name === n));
  if (gone.length !== 12 || fore.some(c => !c)) return 'abort: expected 12 old cubes, got ' + gone.length;
  if (Cube.all.some(c => /^upper_arm_/.test(c.name))) return 'abort: upper_arm exists';
  const rects = [[...P.up_side, 7, 15, P.up_side_hex], [...P.up_end, 7, 7, P.up_end_hex], [...P.fside, 8, 10, P.fside_hex]];
  let bad = '';
  tex.edit(canvas => {
    const ctx = canvas.getContext('2d');
    P.clear.forEach(([x, y]) => ctx.clearRect(x, y, 1, 1));
    for (const [u, v, w, h] of rects) { const d = ctx.getImageData(u, v, w, h).data;
      for (let i = 3; i < d.length; i += 4) if (d[i]) { bad = 'rect ' + u + ',' + v + ' not empty'; return canvas; } }
    for (const [u, v, w, h, hex] of rects) { const img = ctx.createImageData(w, h);
      for (let i = 0; i < w * h * 4; i++) img.data[i] = parseInt(hex.substr(i * 2, 2), 16);
      ctx.putImageData(img, u, v); }
    return canvas;
  }, {edit_name: 'Two-block arms paint'});
  if (bad) return 'abort after clear (undo the texture edit): ' + bad;
  Undo.initEdit({elements: gone, outliner: true});
  gone.forEach(c => c.remove());
  Undo.finishEdit('Remove upper cores and elbow joints');
  const R = (u, v, w, h, m) => m ? [u + w, v, u, v + h] : [u, v, u + w, v + h];
  const made = [];
  Undo.initEdit({outliner: true, elements: []});
  for (const s of ['r', 'l']) {
    const right = s === 'r', m = !right, arm = Group.all.find(g => g.name === (right ? 'right_arm' : 'left_arm'));
    const sd = R(...P.up_side, 7, 15, m), en = R(...P.up_end, 7, 7, m);
    const faces = {north: {uv: sd}, south: {uv: sd}, east: {uv: sd}, west: {uv: sd}, up: {uv: en}, down: {uv: en}};
    for (const f of Object.values(faces)) f.texture = tex.uuid;
    const c = new Cube({name: 'upper_arm_' + s, from: [right ? 8 : -15, 26.625, -5], to: [right ? 15 : -8, 41.625, 2],
      origin: arm.origin.slice(), box_uv: false, faces}).addTo(arm).init();
    made.push(c);
  }
  Undo.finishEdit('Upper arm blocks', {outliner: true, elements: made});
  Undo.initEdit({elements: fore});
  fore.forEach((c, i) => {
    c.to[1] = 30.625;
    const r = R(...P.fside, 8, 10, i === 1);
    for (const f of ['north', 'south', 'east', 'west']) c.faces[f].uv = r.slice();
  });
  Undo.finishEdit('Forearms grow 3 px over the elbow');
  Canvas.updateAll();
  return JSON.stringify(Cube.all.filter(c => /^(upper_arm_|forearm_)/.test(c.name)).map(c => [c.name, c.parent.name, c.from, c.to, c.visibility]));
})()
