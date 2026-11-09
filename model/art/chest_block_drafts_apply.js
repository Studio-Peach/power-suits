(() => {
  const plan = PLAN;
  const tex = Texture.all[0];
  const probe = document.createElement('canvas'); probe.width = tex.width; probe.height = tex.height;
  const pctx = probe.getContext('2d'); pctx.drawImage(tex.img, 0, 0);
  const bad = [];
  for (const [k, [u, v, w, h]] of Object.entries(plan.rects)) {
    const d = pctx.getImageData(u, v, w, h).data;
    for (let i = 3; i < d.length; i += 4) if (d[i] !== 0) { bad.push(k); break; }
  }
  if (bad.length) return 'abort, not transparent: ' + bad.join(',');
  if (Group.all.some(g => /^proto_(chest|collar)_/.test(g.name))) return 'abort, drafts exist';
  tex.edit(canvas => {
    const ctx = canvas.getContext('2d');
    for (const [k, [u, v, w, h]] of Object.entries(plan.rects)) {
      const hex = plan.hex[k], img = ctx.createImageData(w, h);
      for (let i = 0; i < w * h * 4; i++) img.data[i] = parseInt(hex.substr(i * 2, 2), 16);
      ctx.putImageData(img, u, v);
    }
    return canvas;
  }, {edit_name: 'Chest block draft paint'});
  const R = plan.rects, torso = Group.all.find(g => g.name === 'torso_armor');
  const DRAFTS = [
    ['proto_chest_A', 'cbA_chest', 'A', [-7.5, 31.625, -7], [7.5, 38.625, 6]],
    ['proto_chest_B', 'cbB_plate', 'B', [-6.5, 31.625, -7], [6.5, 38.625, -5]],
    ['proto_chest_C', 'cbC_step', 'C', [-5.5, 31.625, -6], [5.5, 34.625, -5]],
    ['proto_collar_1', 'cg1_gorget', 'G', [-6.5, 38.625, -6], [6.5, 41.625, 6]]];
  const made = [];
  Undo.initEdit({outliner: true, elements: []});
  for (const [gname, cname, k, from, to] of DRAFTS) {
    const g = new Group({name: gname, origin: torso.origin.slice()}).addTo(torso).init();
    g.visibility = false;
    const faces = {};
    for (const f of ['north', 'south', 'east', 'west', 'up', 'down']) {
      const [u, v, w, h] = R[k + '_' + f];
      faces[f] = {uv: [u, v, u + w, v + h], texture: tex.uuid};
    }
    const c = new Cube({name: cname, from, to, origin: torso.origin.slice(), box_uv: false, faces}).addTo(g).init();
    c.visibility = false;
    made.push(c);
  }
  Undo.finishEdit('Chest + collar block drafts', {outliner: true, elements: made});
  Canvas.updateAll();
  return 'ok ' + made.map(c => c.name).join(',');
})()
