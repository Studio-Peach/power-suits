(() => {
  const P = PLAN;
  const tex = Texture.all[0];
  const fore = ['forearm_r', 'forearm_l'].map(n => Cube.all.find(c => c.name === n));
  if (Cube.all.some(c => /^forearm_inner_/.test(c.name))) return 'abort: inner exists';
  const OLD = OLDFACES;
  const put = (ctx, u, v, w, h, hex) => { const img = ctx.createImageData(w, h);
    for (let i = 0; i < w * h * 4; i++) img.data[i] = parseInt(hex.substr(i * 2, 2), 16); ctx.putImageData(img, u, v); };
  const empty = (ctx, u, v, w, h) => { const d = ctx.getImageData(u, v, w, h).data; for (let i = 3; i < d.length; i += 4) if (d[i]) return false; return true; };
  let bad = '';
  tex.edit(canvas => {
    const ctx = canvas.getContext('2d');
    ctx.clearRect(...P.clear);
    const paint = [[...P.side, 6, 8, P.side_hex], [...P.end, 6, 5, P.end_hex]];
    for (const k of Object.keys(P.restore)) { const [u, v, w, h] = k.split(',').map(Number); if (!empty(ctx, u, v, w, h)) bad += ' restore ' + k; }
    for (const [u, v, w, h] of paint) if (!empty(ctx, u, v, w, h)) bad += ' paint ' + u + ',' + v;
    if (bad) return canvas;
    for (const [k, hex] of Object.entries(P.restore)) { const [u, v, w, h] = k.split(',').map(Number); put(ctx, u, v, w, h, hex); }
    for (const [u, v, w, h, hex] of paint) put(ctx, u, v, w, h, hex);
    return canvas;
  }, {edit_name: 'Gauntlet faces back, inner forearm paint'});
  if (bad) return 'abort (undo the texture edit, it only cleared 79,0):' + bad;
  Undo.initEdit({elements: fore});
  fore.forEach(c => { c.to[1] = 27.625; for (const f of ['north', 'south', 'east', 'west']) c.faces[f].uv = OLD[c.name][f].slice(); });
  Undo.finishEdit('Gauntlet back to 8x7x8');
  const R = (u, v, w, h, m) => m ? [u + w, v, u, v + h] : [u, v, u + w, v + h];
  const made = [];
  Undo.initEdit({outliner: true, elements: []});
  for (const s of ['r', 'l']) {
    const right = s === 'r', m = !right, g = Group.all.find(x => x.name === (right ? 'right_forearm' : 'left_forearm'));
    const ns = R(...P.side, 6, 8, m), ew = R(...P.side, 5, 8, m), en = R(...P.end, 6, 5, m);
    const faces = {north: {uv: ns}, south: {uv: ns}, east: {uv: ew}, west: {uv: ew}, up: {uv: en}, down: {uv: en}};
    for (const f of Object.values(faces)) f.texture = tex.uuid;
    made.push(new Cube({name: 'forearm_inner_' + s, from: [right ? 8.5 : -14.5, 22.625, -4], to: [right ? 14.5 : -8.5, 30.625, 1],
      origin: g.origin.slice(), box_uv: false, faces}).addTo(g).init());
  }
  Undo.finishEdit('Inner forearm blocks', {outliner: true, elements: made});
  Canvas.updateAll();
  return JSON.stringify(Cube.all.filter(c => /^(upper_arm_|forearm_)/.test(c.name)).map(c => [c.name, c.parent.name, c.from, c.to, c.faces.north.uv]));
})()
