(() => {
  const plan = PLAN, drafts = DRAFTS;
  const tex = Texture.all[0], torso = Group.all.find(g => g.name === 'torso_armor');
  if (Cube.all.some(c => c.name === 'torso_core')) return 'abort, already built';
  const dg = Group.all.filter(g => /^proto_(chest|collar)_/.test(g.name));
  if (dg.length) {
    const dc = dg.flatMap(g => g.children);
    Undo.initEdit({outliner: true, elements: dc});
    dc.forEach(c => c.remove()); dg.forEach(g => g.remove());
    Undo.finishEdit('Remove chest/collar block drafts', {outliner: true, elements: []});
    tex.edit(canvas => { const ctx = canvas.getContext('2d');
      for (const [u, v, w, h] of Object.values(drafts)) ctx.clearRect(u, v, w, h); return canvas; }, {edit_name: 'Clear draft texels'});
  }
  const probe = document.createElement('canvas'); probe.width = tex.width; probe.height = tex.height;
  const pctx = probe.getContext('2d'); pctx.drawImage(tex.canvas || tex.img, 0, 0);
  const bad = [];
  for (const [k, [u, v, w, h]] of Object.entries(plan.rects)) {
    const d = pctx.getImageData(u, v, w, h).data;
    for (let i = 3; i < d.length; i += 4) if (d[i] !== 0) { bad.push(k); break; }
  }
  if (bad.length) return 'abort, not transparent: ' + bad.join(',');
  tex.edit(canvas => { const ctx = canvas.getContext('2d');
    for (const [k, [u, v, w, h]] of Object.entries(plan.rects)) {
      const hex = plan.hex[k], img = ctx.createImageData(w, h);
      for (let i = 0; i < w * h * 4; i++) img.data[i] = parseInt(hex.substr(i * 2, 2), 16);
      ctx.putImageData(img, u, v);
    }
    return canvas; }, {edit_name: 'Torso core + breastplate paint'});
  const faces = p => Object.fromEntries(['north', 'south', 'east', 'west', 'up', 'down'].map(f => {
    const [u, v, w, h] = plan.rects[p + '_' + f]; return [f, {uv: [u, v, u + w, v + h], texture: tex.uuid}]; }));
  const chestParts = Group.all.find(g => g.name === 'chest_parts'), abd = Cube.all.find(c => c.name === 'abd_core');
  Undo.initEdit({outliner: true, elements: []});
  const frame = new Group({name: 'frame_parts', origin: torso.origin.slice()}).addTo(torso).init();
  const core = new Cube({name: 'torso_core', from: [-6.5, 31.625, -1], to: [6.5, 38.625, 6], origin: torso.origin.slice(),
    box_uv: false, faces: faces('core')}).addTo(frame).init();
  abd.addTo(frame);
  const bp = new Cube({name: 'bp_plate', from: [-7.5, 31.625, -7], to: [7.5, 38.625, -1], origin: torso.origin.slice(),
    box_uv: false, faces: faces('bp')}).addTo(chestParts).init();
  [core, bp].forEach(c => c.visibility = true);
  Undo.finishEdit('Torso core + iron breastplate', {outliner: true, elements: [core, bp]});
  const old = Cube.all.filter(c => /^(chest|bp_main|bp_lower)$/.test(c.name));
  Undo.initEdit({outliner: true, elements: old});
  old.forEach(c => c.remove());
  Undo.finishEdit('Remove old chest pieces', {outliner: true, elements: []});
  Canvas.updateAll();
  return 'ok, removed ' + old.length + ' old, ' + dg.length + ' draft groups';
})()
