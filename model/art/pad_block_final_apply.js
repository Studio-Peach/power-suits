(() => {
  const clear = CLEAR;
  const tex = Texture.all[0];
  const B = ['r', 'l'].map(s => Cube.all.find(c => c.name === 'pbkB_' + s));
  if (B.some(c => !c)) return 'abort: pbkB missing';
  const gone = Cube.all.filter(c => /^pad_/.test(c.name) || /^pbk[AC]_/.test(c.name));
  Undo.initEdit({elements: gone, outliner: true});
  gone.forEach(c => c.remove());
  Undo.finishEdit('Remove old pads and pad drafts A, C');
  Undo.initEdit({elements: B, outliner: true});
  B.forEach((c, i) => {
    const right = i === 0, pad = Group.all.find(g => g.name === (right ? 'right_pad' : 'left_pad'));
    c.addTo(pad); c.name = right ? 'pad_r' : 'pad_l'; c.visibility = true;
  });
  Undo.finishEdit('Pad B becomes the pad');
  const protos = Group.all.filter(g => /^proto_pad_/.test(g.name));
  if (protos.some(g => g.children.length)) return 'stop: proto groups not empty';
  Undo.initEdit({outliner: true, groups: protos});
  protos.forEach(g => g.remove(false));
  Undo.finishEdit('Remove empty pad draft groups');
  tex.edit(canvas => {
    const ctx = canvas.getContext('2d');
    clear.forEach(([x, y]) => ctx.clearRect(x, y, 1, 1));
    return canvas;
  }, {edit_name: 'Clear old pad texels'});
  Canvas.updateAll();
  return JSON.stringify({pads: Cube.all.filter(c => /^pad_/.test(c.name)).map(c => [c.name, c.parent.name, c.from, c.to]),
    protos: Group.all.filter(g => /^proto_/.test(g.name)).length, cubes: Cube.all.length});
})()
