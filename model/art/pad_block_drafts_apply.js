(() => {
  const plan = PLAN;
  const tex = Texture.all[0];
  const bad = [];
  const cv = tex.canvas || tex.img;
  const probe = document.createElement('canvas'); probe.width = tex.width; probe.height = tex.height;
  const pctx = probe.getContext('2d'); pctx.drawImage(tex.img, 0, 0);
  for (const [k, [u, v, w, h]] of Object.entries(plan.rects)) {
    const d = pctx.getImageData(u, v, w, h).data;
    for (let i = 3; i < d.length; i += 4) if (d[i] !== 0) { bad.push(k); break; }
  }
  if (bad.length) return 'abort, not transparent: ' + bad.join(',');
  if (Group.all.some(g => /^proto_pad_/.test(g.name))) return 'abort, drafts exist';
  tex.edit(canvas => {
    const ctx = canvas.getContext('2d');
    for (const [k, [u, v, w, h]] of Object.entries(plan.rects)) {
      const hex = plan.hex[k], img = ctx.createImageData(w, h);
      for (let i = 0; i < w * h * 4; i++) img.data[i] = parseInt(hex.substr(i * 2, 2), 16);
      ctx.putImageData(img, u, v);
    }
    return canvas;
  }, {edit_name: 'Pad block draft paint'});
  const R = plan.rects, uv = (r, m) => m ? [r[0] + r[2], r[1], r[0], r[1] + r[3]] : [r[0], r[1], r[0] + r[2], r[1] + r[3]];
  const made = [];
  Undo.initEdit({outliner: true, elements: []});
  for (const [d, H] of [['A', 9], ['B', 11], ['C', 14]]) for (const s of ['r', 'l']) {
    const right = s === 'r', pad = Group.all.find(g => g.name === (right ? 'right_pad' : 'left_pad'));
    const g = new Group({name: `proto_pad_${d}_${s}`, origin: pad.origin.slice()}).addTo(pad).init();
    g.visibility = false;
    const x0 = right ? 7.5 : -16.5, x1 = right ? 16.5 : -7.5, m = !right;
    const faces = {north: {uv: uv(R[d + '_ns'], m)}, south: {uv: uv(R[d + '_ns'], m)}, east: {uv: uv(R[d + '_ew'], m)},
      west: {uv: uv(R[d + '_ew'], m)}, up: {uv: uv(R.up, m)}, down: {uv: uv(R.down, m)}};
    for (const f of Object.values(faces)) f.texture = tex.uuid;
    const c = new Cube({name: `pbk${d}_${s}`, from: [x0, 42.625 - H, -5], to: [x1, 42.625, 5], origin: pad.origin.slice(),
      box_uv: false, faces}).addTo(g).init();
    c.visibility = false;
    made.push(c);
  }
  Undo.finishEdit('Pad block drafts', {outliner: true, elements: made});
  Canvas.updateAll();
  return 'ok ' + made.map(c => c.name).join(',');
})()
